---
layout: default
title: "Block"
categories:
  - "Concepts"

redirect_from:
  - "/index.php/Block"
  - "/wiki/Block"

last_modified: 2014-04-28
---

The term block is used in a couple of different contexts with TSK. 

# Data Unit
Block is the term used in the [HFS](/HFS/) file systems to refer to a grouping of consecutive [sectors](/Sectors/). Sectors are typically 512-bytes each and it is more efficient for a file system to allocate and use multiple sectors at a time. Each file system uses a different term for the resulting group. [TSK](/The-Sleuth-Kit/) uses the term [data unit](/Data-unit/) to refer to the grouping. 

Block is also used in the [ExtX](/ExtX/) and [UFS](/UFS/) file systems to refer to a grouping of [fragments](/Fragments/). These file systems group sectors into fragments and fragments into blocks.  However, blocks are not given unique addresses.  Their address is the address of the first fragment in the block. 

# Data Unit Layer Command Line Tools
The command line tools in TSK are organized into layers. The data unit layer tools start with 'blk', which is short for block. See the [TSK Tool Overview](/TSK-Tool-Overview/) for more details on the tool layers.
