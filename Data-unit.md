---
layout: default
title: "Data unit"
categories:
  - "Concepts"

redirect_from:
  - "/index.php/Data_unit"
  - "/index.php/Data_units"
  - "/wiki/Data_unit"
  - "/wiki/Data_units"

last_modified: 2013-02-05
---

Data unit is the generic term used in [TSK](/The-Sleuth-Kit/) to refer to a grouping of consecutive sectors.  Sectors are typically 512-bytes and file systems group them together to form larger storage units.  For example, they may group 8 consecutive 512-byte sectors together to form units that are 4096-bytes each.  The file system assigns an address to each of these data units.  Typically, the file system does not provide an address to each sector. It only allocates and refers to the data units.  

The following are the terms that are used by each of the file systems to refer to a data unit.
* ExtX: [fragment](/Fragment/) 
* FAT: [sector](/Sector/) (note that FAT groups sectors into [cluster](/Cluster/)s, but not all sectors are allocated to a cluster and therefore cluster addresses do not cover the entire file system.  TSK uses sector addresses with FAT so that all parts of the file system can be referenced. See [FAT Implementation Notes](/FAT-Implementation-Notes/)). 
* FFS: [fragment](/Fragment/) (note that FFS also groups multiple fragments into blocks, but each fragment has an address)
* HFS: [block](/Block/)
* NTFS: [cluster](/Cluster/)
* YAFFS2: [chunk](/Chunk/) (note that YAFFS2 groups multiple chunks into blocks but each chunk has an address)
