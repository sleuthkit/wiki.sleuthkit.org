---
layout: default
title: "Carving"
categories:
  - "Concepts"

redirect_from:
  - "/index.php/Carving"
  - "/wiki/Carving"

last_modified: 2013-03-09
---

## Carving
Carving, also known as Data Carving, is the process of extracting data from a disc image. The data is typically in unallocated space, slack space, or even hidden inside other files. The word “Carving” is used because data is carved out of the image. Many commercial forensic suites offer an automatic carving feature that carves out different file types, such as images (JPG, GIF, PNG, etc.), and MS Office files. Manual carving is also possible, which Sleuthkit supports. To manually carve in TSK with Autopsy go to the “Data Unit” section and specify the sector you want to start at, and indicate how many sectors you want to carve out. Data Carving is a great way to find data that would not otherwise be found, or shown in the file hierarchy.
