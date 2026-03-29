---
layout: default
title: "Fragment"
categories:
  - "Concepts"

redirect_from:
  - "/index.php/Fragment"
  - "/index.php/Fragments"
  - "/wiki/Fragment"
  - "/wiki/Fragments"

last_modified: 2010-01-05
---

Fragment is the term used in the [ExtX](/ExtX/) and [UFS](/UFS/) file systems to refer to a grouping of consecutive [sectors](/Sectors/). Sectors are typically 512-bytes each and it is more efficient for a file system to allocate and use multiple sectors at a time.  Each file system uses a different term for the resulting group.  [TSK](/The-Sleuth-Kit/) uses the term [data unit](/Data-unit/) to refer to the grouping.

These file systems will also group consecutive fragments into [block](/Block/)s, but block addresses are equal to the fragment addresses. 

Note that while ExtX file systems support fragments and blocks, they typically are equal sizes (meaning that 1 block is equal to 1 fragment).
