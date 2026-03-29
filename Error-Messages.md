---
layout: default
title: "Error Messages"
categories:
  - "Tools"

redirect_from:
  - "/index.php/Error_Messages"
  - "/wiki/Error_Messages"

last_modified: 2015-03-07
---

This page contains some error messages that could be encountered when running [TSK](/The-Sleuth-Kit/) and [Autopsy](/Autopsy/). 

<hr>

```
Error extracting file from image (ntfs_uncompress_compunit: Phrase token offset is too large:  1 (max: 0))
```

This message occurs when trying to process a compressed [NTFS](/NTFS/) file that is corrupt.  This can occur when a file has been deleted and the clusters have been reallocated to another file. 

<hr>

```
# blkls -f ntfs -i raw -a /dev/sde1 > /tmp/allocatedspace.dump
Error in metadata structure (dinode_lookup: More Update Sequence Entries than MFT size)
```

This message can occur when trying to view allocated data on an NTFS filesystem damaged by unplugging a USB drive while it was writing.  This file system is not recognized/fixable by chkdsk either, and needs some reconstruction before chkdsk will work.

<hr>
