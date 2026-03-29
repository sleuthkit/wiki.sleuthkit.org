---
layout: default
title: "Sector"
categories:
  - "Concepts"

redirect_from:
  - "/index.php/Sector"
  - "/index.php/Sectors"
  - "/wiki/Sector"
  - "/wiki/Sectors"

last_modified: 2010-10-27
---

A sector is the smallest addressable unit on a hard drive or other non-volatile storage media.  On a typical hard drive, a sector is 512-bytes in size. CD-ROMs use 4096-byte sectors and there are newer hard drives that are coming out with 4096-byte sectors.

Each sector is given an address, starting at 0.  This is called its LBA address.  Other addressing schemes exist that use the geometry of the drive, but those are rarely used anymore.

For efficiency, file systems typically group consecutive sectors into [data units](/Data-units/) (common names include [cluster](/Cluster/) or [block](/Block/)).  The data units are also given addresses.
