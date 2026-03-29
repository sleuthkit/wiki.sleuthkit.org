---
layout: default
title: "ISO9660 Implementation Notes"
categories:
  - "File Systems"

redirect_from:
  - "/index.php/ISO9660_Implementation_Notes"
  - "/wiki/ISO9660_Implementation_Notes"

last_modified: 2013-02-04
---

# Introduction
The [ISO9660](/ISO9660/) file system is used on many platforms and has many variations and extensions.  At the most basic level of ISO9660 there are several differences than traditional file systems due to the type of media available.

This document describes how it was implemented.  It assumes that you know the basics of the [ISO9660](/ISO9660/) format. 

# General Notes
Due to many reports of mastering software errata, there are some
issues that The Sleuth Kit handles that the specifications for ISO9660
say will never happen.  The specs say that there is only one unique
primary volume descriptor per volume.  The Sleuth Kit handles the 
possibility of finding more and alerts the user to this.

When TSK loads the file system, it chooses a secondary volume descriptor, runs through its path table, and processes each directory listed in it.  Each file found during this process is saved in memory and assigned a metadata address.  

After the secondary volume descriptor is loaded, the other volume descriptors are processed in the same manor.  Now though, we check for an entry that duplicates an entry that was added by the previous process.  We skip entries for files that duplicate the starting block and size of an existing entry. If the file is unique, it is added to the internal list and given an address.  However, these files will be treated specially because they cannot be reached from the directory tree of the initially processed volume descriptor. They will be marked as being "unallocated" (because they can't be reached from the root directory) and will end up as orphan files in the $OrphanFiles directory.  

The file name code in TSK processes each directory, but needs to figure out the metadata address.  Therefore, it searches the previously loaded data. It needs to match the loaded files with the current file.  It does this based on the byte offset of the directory entry. 

# What TSK Cannot Currently Do
There are a few things that The Sleuth Kit is not yet able to do
with ISO9660:

* Multisessions CDs are not handled.
* High Sierra is not handled.
* Files that are stored with an interleave gap
