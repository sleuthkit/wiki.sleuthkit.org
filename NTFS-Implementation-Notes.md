---
layout: default
title: "NTFS Implementation Notes"
categories:
  - "File Systems"

redirect_from:
  - "/index.php/NTFS_Implementation_Notes"
  - "/wiki/NTFS_Implementation_Notes"

last_modified: 2009-02-08
---

NOTE: This was copied from skins_ntfs.txt. It will need some updating and wiki'ing help.

# Introduction
The [NTFS](/NTFS/) file system is used in all critical Microsoft Windows
systems.  It is an advanced file system that is significantly different
from the UNIX file systems that the original [TCT](/TCT/) was designed for.
This document gives a quick overview of NTFS and how it was
implemented.  The biggest difference is the use of Alternate Data
Streams (ADS) when specifying a meta data structure.

[The Sleuth Kit](/The-Sleuth-Kit/) allows one to investigate an NTFS image in the same
ways as any UNIX image, including:

* Creation of ASCII [timeline](/Timeline/) of file activity
* Cluster analysis and mapping between clusters and MFT entries
* MFT analysis and mapping between MFT entries and file names
* File and directory level analysis including deleted files

# Metadata Addresses
The Sleuth Kit allows one to view all aspects of the NTFS structure.
It does this using a special [Metadata Address](/Metadata-Address/) format. 
With UNIX you only need
to reference the inode number because there is only one piece of
content for the file.  With NTFS, one can either specify just the
MFT number and the default data attribute is used or the type can
be specified by adding it to the end of the MFT entry, 36-128 for
example.  If more than one attribute of the same type exists, then
the id can be used after the type, 36-128-5 for example.

All Sleuth Kit tools can take MFT values in any of the above formats
and output from the tools will also be in one of the above formats.
For example, the [istat](/Istat/) tool will list all attributes a file has.
To get the details of MFT entry 49, use:

```
# istat -f ntfs ntfs.dd 49
    MFT Entry: 49
    Sequence: 2
    Allocated
    UID: 0
    DOS Mode: File
    Size: 15
    Links: 1
    Name: multiple.txt

    $STANDARD_INFORMATION Times:
    File Modified:  Mon Nov  5 19:58:27 2001
    MFT Modified:   Mon Nov  5 19:58:27 2001
    Accessed:       Mon Nov  5 19:58:27 2001

    $FILE_NAME Times:
    Created:        Mon Nov  5 19:57:29 2001
    File Modified:  Mon Nov  5 19:57:29 2001
    MFT Modified:   Mon Nov  5 19:57:29 2001
    Accessed:       Mon Nov  5 19:57:29 2001

    Attributes: 
    Type: $STANDARD_INFORMATION (16-0)   Name: N/A   Resident   size: 72
    Type: $FILE_NAME (48-2)   Name: N/A   Resident   size: 90
    Type: $OBJECT_ID (64-3)   Name: N/A   Resident   size: 16
    Type: $DATA (128-1)   Name: $Data   Resident   size: 15
    Type: $DATA (128-5)   Name: overhere   Resident   size: 26
```

We see that it has 5 attributes, all of them are resident (notice
the small sizes).  Two of the attributes are $DATA attributes (128-1
and 128-5).  The full name of 128-1 is 'multiple.txt' and the full
name of 128-5 is 'multiple.txt:overhere'.

The following command would display the default data attribute
(128-1):

```
# icat -f ntfs ntfs.dd 49
```

The following is the same:

```
# icat -f ntfs ntfs.dd 49-128-1
```

The following displays the other data stream: 

```
# icat -f ntfs ntfs.dd 49-128-5
```

As an additional example, the raw format of the $FILE_NAME attribute
can be viewed using:

```
# icat -f ntfs ntfs.dd 49-48-2
```

The output of the above command would be a combination of UNICODE
characters and other binary data (I would recommend just using the
output of the istat command for this type of data).
    

The output of the [fls](/Fls/) command is similar:

```
# fls -f ntfs ntfs.dd
    <...>
    r/r 48-128-1:   test-1.txt
    r/r 49-128-1:   multiple.txt
    r/r 49-128-5:   multiple.txt:NEW
    r/r 50-128-1:   test-2.txt
    <...>
```

This allows you to easily identify all data streams.  

Note that Autopsy can automate this process for you and allows you
to view all attributes.

   http://www.sleuthkit.org/autopsy

# What TSK Cannot Currently Do
There are a few things that The Sleuth Kit is not yet able to do
with NTFS:

* The Security Descriptors are not yet analyzed.  Therefore, the exact ACLs of the object can not be displayed.
* Directories that are indexed by a descriptor other than the file name, are not supported.
* Encrypted files are not supported
