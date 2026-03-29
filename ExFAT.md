---
layout: default
title: "ExFAT"
categories:
  - "File Systems"

redirect_from:
  - "/index.php/ExFAT"
  - "/wiki/ExFAT"

last_modified: 2014-01-02
---

ExFAT (Extended File Allocation Table) is a newer (2006) file system designed by Microsoft to be used on removable media. It is one of the file systems supported by [TSK](/The-Sleuth-Kit/). ExFAT shares many properties with the [FAT](/FAT/) file system, but also has significant differences, the largest probably being that file data is no longer stored exclusively by FAT chains. See the [exFAT Implementation Notes](/ExFAT-Implementation-Notes/) for details on how exFAT support was added to TSK.

Docs used during development:
* http://www.sans.org/reading-room/whitepapers/forensics/reverse-engineering-microsoft-exfat-file-system-33274
