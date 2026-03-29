---
layout: default
title: "Cluster"
categories:
  - "Concepts"

redirect_from:
  - "/index.php/Cluster"
  - "/wiki/Cluster"

last_modified: 2010-01-05
---

Cluster is the term used in the [FAT](/FAT/) and [NTFS](/NTFS/) file systems to refer to a grouping of consecutive [sectors](/Sectors/). Sectors are typically 512-bytes each and it is more efficient for a file system to allocate and use multiple sectors at a time.  Each file system uses a different term for the resulting group.  [TSK](/The-Sleuth-Kit/) uses the term [data unit](/Data-unit/) to refer to the grouping.

See the [FAT Implementation Notes](/FAT-Implementation-Notes/) for a description of why TSK uses sector and not cluster addresses when dealing with FAT file systems.
