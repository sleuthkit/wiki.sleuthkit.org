---
layout: default
title: "Orphan Files"
categories:
  - "Concepts"

redirect_from:
  - "/index.php/Orphan_Files"
  - "/wiki/Orphan_Files"

last_modified: 2008-11-05
---

# What They Are
Orphan files are deleted files that still have file metadata in the file system, but that cannot be accessed from the root directory. In most file systems, the file metadata (such as times and which blocks are allocated to a file) are stored in a different location than the file name. The name points to the metadata location.  

It is possible for the name of a deleted file to be erased or reused, but the file metadata still exists.  We call these Orphan Files because they have no parent (or at least the root directory is not its ultimate parent). 

Starting in [TSK](/The-Sleuth-Kit/) version 3, orphan files are listed in the $OrphanFiles directory in the root directory.  Note that this directory does not actually exist in the disk image, it is just a virtual way for TSK to provide you with access to the metadata that exists. 

# How They Are Determined
TSK determines the orphan files by first walking the directory tree and enumerating all of the [metadata addresses](/Metadata-addresses/) that the file names point to. Then, it goes through all of the metadata structures and identifies which of the unallocated structures do not have a name pointing to them.  These are the orphan files.
