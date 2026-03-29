---
layout: default
title: "YAFFS2 Implementation Notes"
categories:
  - "File Systems"

redirect_from:
  - "/index.php/YAFFS2_Implementation_Notes"
  - "/wiki/YAFFS2_Implementation_Notes"

last_modified: 2013-06-17
---

See [YAFFS2](/YAFFS2/) for general information about the YAFFS2 file system.

# General File System Reconstruction
## Page/spare size
### Overview
As outlined in the [YAFFS2](/YAFFS2/) page, the file system relies on the 'spare area' of each flash memory page to store information about what file system chunk that is stored in that page.  The YAFFS2 spec does not specify though the exact format of how that data is stored because devices can choose how to use the spare area for other things, such as check sums.  Further, there is nothing in the file system that stores how the spare area is organized, so tools must guess.

There are two things that tools must guess: 
- Page size and spare area size
- Layout of spare area

TSK assumes that all pages are 2048-bytes and spare area is 64-bytes. It knows about several spare area layouts, but does not know all of them.  We need to add the ability to pass in the layout details if you have reverse engineered them.

### Determining the layout of the spare area
This section contains some of the layouts that TSK detects.  As with all docs, the code will likely evolve to more formats than are documented here. 

In practice we've seen this format the most:
* 4 byte sequence number
* 4 byte object ID (with the object type in the high four bits if the header flag is set in the next entry)
* 4 byte chunk ID **OR** high bit set (header flag) and the parent ID in the rest
* 4 byte number of bytes

At present we've seen these 16 bytes start at offset 0, offset 2, or offset 30. TSK attempts to determine where the fields are by reading in a reasonable number of initialized spare areas and then doing some tests on each possible offset:
* Sequence numbers should be the same for all chunks in a block
* Sequence number shouldn't be null or 0xffffffff
* Object ID can't be zero
* If we have other options, we'd prefer the sequence number not to start with 0xff

These tests could certainly be improved upon.

## Constructing the current version of each object
1. Read in the sequence number, object ID, and chunk ID from the spare area of each chunk and record the offset of the chunk
1. Make a list of chunks for each object ID and sort it by sequence number and then offset, resulting in a chronological list of chunks for each object
1. The current header and data chunks can then be found by reading backwards through the list
The inode for the current version of an object is its object ID.

## Constructing the file hierarchy
1. The root directory always has object ID 1
1. To find the children of a directory, search over all objects to find those with the appropriate parent ID

# Finding Deleted/Older Versions of Objects
## Object versions
As described in the previous section, for each object we create a chronologically ordered list of chunks with that object ID. The current version of an object is created by starting at the end of the list and reading backwards, but we can start at any point in the list and read backwards to create an older version of the object. Object IDs tend to get reused frequently, so in addition to multiple versions of the same file we also expect to see old files that have been deleted.

### Creating versions
The question is, where do we start these versions? Starting at every chunk in the list would produce way too many files. Even only starting at header chunks seems like it would create more versions than could reasonably be worked with. For now, we base versions around changes in the sequence number and create them as follows:
* A version has a number, a pointer to its most recent header, and a pointer its the most recent chunk
* Go through the sorted list of chunks adding each to the current version (i.e., updating the most recent header and chunk pointers) until the sequence number changes
  * Note that if we find an unlinked/deleted header we don't record it in the header chunk pointer unless we have no previous header. These headers give us no information and can cause us to entirely miss files created and deleted in one block, as in the following example:

```
Obj id   Seq num  Offset   Type Parent   Name
000005f9 00001b3c 07229a00 file 00000004 deleted       
000005f9 00001b3d 07240d40 file 0000032e im.db-journal
000005f9 00001b3d 07245780 file 0000032e im.db-journal
000005f9 00001b3d 07246800 file 0000032e im.db-journal
000005f9 00001b3d 0724b240 file 00000003 unlinked     
000005f9 00001b3d 0724ba80 file 00000004 deleted
```

* Save that version and create a new one, incrementing the version number. This new version will start with the older header pointer as its most recent header. A few exceptions:
  * If we're looking at a directory (which will only have a header chunk) and its name hasn't changed, don't start a new version. Multiple copies of the same directory name don't give us much information
  * If we never found a header for the previous version, don't start a new version. We can't do anything with a version with no header

### Inodes and filenames
Inodes for older versions are created using the object ID and version number. A version number of zero always returns the current version of the object. To avoid name conflicts, non-current versions have their version number and object ID appended to the file name.

```
r/r 764:        pvcodec.txt
r/r * 2360060:  pvcodec.txt#764,9
r/r * 2097916:  pvcodec.txt#764,8
r/r * 1835772:  pvcodec.txt#764,7
```

## Determining allocated/unallocated status of versions and chunks
We consider a version of an object to be unallocated if it is not the most recent version or if the most recent header block is a deleted block. We consider a chunk to be allocated if it is part of an allocated version of an object. Since each chunk contains the object ID it belongs to, linking chunks with objects to determine their allocated status is fairly simple.

# Possible Future Work
* Improve the spare area format detection
* Add parameters to allow a user to set the spare area format and page/spare size
* Consider possible improvements to how versions are created, maybe allowing different algorithms based on parameters
