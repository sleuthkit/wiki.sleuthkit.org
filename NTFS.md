---
layout: default
title: "NTFS"
categories:
  - "File Systems"

redirect_from:
  - "/index.php/NTFS"
  - "/wiki/NTFS"

last_modified: 2015-03-07
---

# NTFS Overview
This provides a quick introduction to the NTFS file system.  The
terms used are different then with other file systems.  For a full
overview of the file system, refer to the book "File System Forensic Analysis", 
a preview and purchase details of which are available here:

       http://www.digital-evidence.org/fsfa/

The "Inside Windows 2000" book by Solomon and Russinovich also provides a high-level overview and details of the file system structures can be found at the Linux NTFS Source Forge project:

        http://linux-ntfs.sourceforge.net/ntfs/index.html , which redirects to
          http://www.linux-ntfs.org/ , which redirects to 
            http://www.tuxera.com/ , where you can find
              http://www.tuxera.com/community/open-source-ntfs-3g/

For another deep look at the structure of NTFS, see the free book "NTFS Forensics: A Programmers View of Raw Filesystem Data Extraction" by Jason Medeiros, Grayscale Research 2008.

   http://grayscale-research.org/new/pdfs/NTFS%20forensics.pdf

* Details on how TSK implemented NTFS can be found in the [NTFS Implementation Notes](/NTFS-Implementation-Notes/).  
* Details on file recovery can be found in [NTFS File Recovery](/NTFS-File-Recovery/).
* Details on filesystem recovery can be found in [NTFS Filesystem Recovery](/NTFS-Filesystem-Recovery/).

## MFT
The Master File Table (MFT) contains entries that describe all
system files, user files, and directories.   The MFT even contains
an entry (#0) that describes the MFT itself, which is how we
determine its current size.  Other system files in the MFT include
the Root Directory (#5), the cluster allocation map, Security
Descriptors, and the journal.

## MFT Entries
Each MFT entry is given a number (similar to inode numbers in UNIX).
The user files and directories start at MFT #25.  The MFT entry
contains a list of attributes.  Example attributes include "Standard
Information" which stores data such as MAC times, "File Name" which
stores the file or directories name(s), $DATA which stores the
actual file content, or "Index Alloc" and "Index Root" which contain
directory contents stored in a B-Tree.

Each type of attribute is given a numerical value and more than
one instance of a type can exist for a file.  The "id" value for
each attribute allows one to specify an instance.  A given file
can have more than one "$Data" attribute, which is a method that
can be used to hide data from an investigator.  To get a mapping
of attribute type values to name, use the 'fsstat' command.  It
displays the contents of the $AttrDef system file.

Each attribute has a header and a value and an attribute is either
resident or non-resident.  A resident attribute has both the header
and the content value stored in the MFT entry.  This only works
for attributes with a small value (the file name for example).
For larger attributes, the header is stored in the MFT entry and
the content value is stored in Clusters in the data area.  A Cluster
in NTFS is the same as FAT, it is a consecutive group of sectors.
If a file has too many different attributes, an "Attribute List"
is used that stores the other attribute headers in additional MFT
entries.

## Files
Files in NTFS typically have the following attributes:

* $STANDARD_INFORMATION (#16): Contains MAC times, security ID, Owners ID, permissions in DOS format, and quota data.
*  $FILE_NAME (#48): Contains the file name in UNICODE, as well as additional MAC times, and the MFT entry of the parent directory.
* $OBJECT_ID (#64): Identifiers regarding the files original Object ID, its birth Volume ID, and Domain ID.
* $DATA (#128): The raw content data of the file.

When a file is deleted, the IN_USE flag is cleared from the MFT entry,
but the attribute contents still exist. 

## Directories
Directories in NTFS are indexed to make finding a specific entry
in them faster.  By default, they are stored in a B-Tree sorted in
alphabetical order.  There are two attributes that describe the
B-Tree contents.  Directories in NTFS typically have the following
attributes:

  * $STANDARD_INFORMATION (#16): See above
  * $FILE_NAME (#48): See above
  * $OBJECT_ID (#64): See above
  * $INDEX_ROOT (#144): The root of the B-Tree.  The $INDEX_ROOT value is one more more "Index Entry" structures that each describe a file or directory.  The "Index Entry" structure contains a copy of the "$FILE_NAME" attribute for the file or sub-directory.
  * $INDEX_ALLOCATION (#160): The sub-nodes of the B-Tree.  For small directories, this attribute will not exist and all information will be saved in the $INDEX_ROOT structure.  The content of this attribute is one or more "Index Buffers".  Each "Index Buffer" contains one or more "Index Entry" structures, which are the same ones found in the $INDEX_ROOT.
  * $BITMAP (#176): This describes which structures in the B-Tree are being used.

When files are deleted from a directory, the tree node is removed
and the tree is resorted.  Therefore, the "Index Entry" for the
deleted file maybe written over when the tree is resorted.  This
is different than what is usually seen with UNIX and FAT file
systems, which always have the original name and structure until
a new file is created.  Also, when the tree is resorted, a file
that is on the bottom of the tree can be moved up and a deleted
file name will exist for the original location (even though it was
never deleted by a user).

# Reference Docs
* [Linux NTFS Documentation](http://sourceforge.net/projects/linux-ntfs/files/NTFS%20Documentation/0.5/)  
* [Forensics Wiki Entry](http://www.forensicswiki.org/wiki/NTFS)
* [Wikipedia Entry](http://en.wikipedia.org/wiki/NTFS)
