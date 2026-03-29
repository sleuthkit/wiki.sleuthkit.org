---
layout: default
title: "Fls"
categories:
  - "Tools"

redirect_from:
  - "/index.php/Fls"
  - "/wiki/Fls"

last_modified: 2014-01-13
---

Back to [Help Documents](/Help-Documents/)

fls lists the files and directory names in a file system.  It will process the contents of a given directory and can display information on deleted files. 

* [Automatically Updated man Page](http://www.sleuthkit.org/sleuthkit/man/fls.html)

## Output Data
The default output (i.e. if -l or -m are not given) has one line for each file in the directory.  An NTFS example is:

`
r/r 1304-128-1: IO.SYS
`

### File Type
The <tt>r/r</tt> value shows the file type.  The first 'r' is the type as saved in the file's [file name  structure](/file-name-structure/) and the second 'r' is the type as saved in the file's [metadata structure](/metadata-structure/). For [allocated files](/Allocated-files/), these should always be equal.  For [deleted files](/Deleted-files/), they could be different if one of the structures was reallocated to a different file type. The types are listed here:
* -: Unknown type
* r: Regular file
* d: Directory 
* c: Character device
* b: Block device
* l: Symbolic link
* p: Named FIFO
* s: Shadow 
* h: Socket
* w: Whiteout
* v: TSK Virtual file / directory (not a real directory, created by TSK for convenience).
Most entries will be 'r' and 'd'.  The others are Unix-focused. 

### Metadata Address
The <tt>1304-128-1</tt> part of the entry shows the [Metadata Address](/Metadata-Address/) associated with this name.  Because this is an NTFS example, the <tt>-128-1</tt> part exists, which identifies the $Data attribute that this name points to.  Other file systems may have a single number in this field. 

### File Name
Finally, the <tt>IO.SYS</tt> part of the entry is the name of the file for this entry.

If you use the '-r' option to recursively go into directories, a '+' is added to the front of each entry to show how deep the file is.  '++' means that the entry is two directories deep.

### Deleted File Names
If the file name in unallocated space of the directory, there will be a '*' between the file type and the metadata address.  

`
r/r * 1304-128-1: IO.SYS
`

In general, this means that the file is deleted.  But, some file systems keep the directory contents sorted and will move file names around.  This can result in unallocated copies of the file name, even when the file is still allocated.  As of version 3.0.0, TSK suppresses duplicate file names and will suppress a deleted version of a name if an equivalent allocated version exists (equivalent is defined as the same name and pointing to the same metadata address).  

Sometimes, you will see the text '(realloc)' after the metadata address.  

`
r/r * 1304-128-1(realloc): IO.SYS
`

This occurs when the file name is in an unallocated state and the metadata structure is in an allocated state. This can only occur on file systems that separate the file name from the metadata (such as NTFS, Ext2/3, UFS, etc.). Seeing '(realloc)' with versions of TSK 3.0.0 and greater (because of the duplicate name suppression) is generally an indication that the metadata structure has been reallocated to a new file and therefore not likely to be the metadta or file content that originally corresponded to this file name.  

### -l format
The '-l' argument causes the "long" format with more details.  It is tab-delimited with the following fields:
* file type as reported in file name and metadata structure (see above)
* [Metadata Address](/Metadata-Address/)
* name
* mtime (last modified time)
* atime (last accessed time)
* ctime (last changed time)
* crtime (created time)
* size (in bytes)
* uid (User ID)
* gid (Group ID)

Note that the 2.X versions of TSK do not print the created time.

### -m format
The '-m' argument causes the data to be in the [body file](/Body-file/) format. It is used to make [timelines](/Timelines/). An example:

 # fls -r -m / image.dd > body.txt
