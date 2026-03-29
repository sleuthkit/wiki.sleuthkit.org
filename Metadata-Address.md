---
layout: default
title: "Metadata Address"
categories:
  - "Concepts"

redirect_from:
  - "/index.php/Metadata_Address"
  - "/index.php/Metadata_address"
  - "/index.php/Metadata_addresses"
  - "/wiki/Metadata_Address"
  - "/wiki/Metadata_address"
  - "/wiki/Metadata_addresses"

last_modified: 2014-01-14
---

# Overview
Metadata Address is a term that is used in [TSK](/The-Sleuth-Kit/) as a generic term for the addresses of file system-specific [data structures](/data-structures/) that store [file metadata](/file-metadata/).  Each file system has a different name for the structure(s) that store the metadata, including:
* [FAT](/FAT/)/[exFAT](/ExFAT/): Directory entry
* [NTFS](/NTFS/): MFT Entry
* [UFS](/UFS/): Inode
* [ExtX](/ExtX/): Inode
* [HFS](/HFS/): Catalog record
* [YAFFS2](/YAFFS2/): Header chunk

The metadata address can be used in TSK to specify the files to analyze.

# Format
In general, each metadata structure is given a single numerical address. Some file systems, such as FAT, do not assign the structures an address, but TSK makes them up (see [FAT Implementation Notes](/FAT-Implementation-Notes/)). 

Some file systems, such as NTFS and HFS, allow a file to have multiple notions of content. NTFS files can have multiple $Data attributes and each is basically an independent file.  To allow the user to access each attribute, special metadata addresses are used.  These addresses take the form of <tt>ADDR-TYPE</tt> or <tt>ADDR-TYPE-ID</tt>.  <tt>ADDR</tt> is the metadata address, <tt>TYPE</tt> is the attribute type, and <tt>ID</tt> is the attribute id. 

The <tt>TYPE</tt> number specifies the type of data being stored in the attribute (such as file content, directory contents, or file metadata).  These numbers are file system-specific. The <tt>ID</tt> number allows you to differentiate between different instances of the same attribute type. Each attribute in a file will have a unique <tt>ID</tt> value.  Note that some NTFS files will have attributes that span multiple MFT entries.  In that case, NTFS does not guarantee that each attribute ID will be unique because NTFS guarantees only that an ID will be unique to a single MFT entry.  TSK overrides those ID values though and assigns new ones so that each attribute is unique. 

As an example, here is the output of the [fls](/Fls/) command on an NTFS image:

```
# fls -f ntfs ntfs.dd
    <...>
    r/r 48-128-1:   test-1.txt
    r/r 49-128-1:   multiple.txt
    r/r 49-128-5:   multiple.txt:NEW
    r/r 50-128-1:   test-2.txt
    <...>
```

There are three files (with addresses 48, 49, and 50). The type value of 128 in an NTFS file system is for the $Data attribute. The file at address 49 has two $Data attributes (one is the default and the other is named ":NEW").  You can see that each of them has a unique ID value (1 and 5). Refer to the [NTFS Implementation Notes](/NTFS-Implementation-Notes/) for more examples. 

In general, if you want TSK to choose the default data attribute (or if the file system does not support the notion of attributes), give TSK only the metadata address.  If you want to specify an attribute and you know there is only one of them, use <tt>ADDR-TYPE</tt>.  If there are multiple attributes of the same type, then also specify an <tt>ID</tt>.  Typically, the [istat](/Istat/) output will show which attributes are defined for a file.
