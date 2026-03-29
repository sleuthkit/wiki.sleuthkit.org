---
layout: default
title: "FAT"
categories:
  - "File Systems"

redirect_from:
  - "/index.php/FAT"
  - "/wiki/FAT"

last_modified: 2010-01-05
---

FAT is a file system that is used on some older Windows systems and on media cards in phones, cameras, and USB sticks. It is one of the file systems that is supported by [TSK](/The-Sleuth-Kit/). While TSK has been designed to abstract many file system components into general layers (data, metadata, name, etc.), FAT has been the most difficult to abstract because it uses a very simple design. See the [FAT Implementation Notes](/FAT-Implementation-Notes/) page for details on how it was merged into the layered model. 

More details on FAT can be found at:
* [File System Forensic Analysis Book](http://www.digital-evidence.org/fsfa)
* [Forensics Wiki Entry](http://www.forensicswiki.org/wiki/FAT)
* [Wikipedia Entry](http://en.wikipedia.org/wiki/File_Allocation_Table)

Docs used during development:
* [FAT32 File System Specification](http://www.microsoft.com/whdc/system/platform/firmware/fatgen.mspx) 1.03 (MS)
