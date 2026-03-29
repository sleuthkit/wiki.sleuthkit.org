---
layout: default
title: "Mmls"
categories:
  - "Tools"

redirect_from:
  - "/index.php/Mmls"
  - "/wiki/Mmls"

last_modified: 2010-03-18
---

Back to [Help Documents](/Help-Documents/)

mmls displays the contents of a volume system (media management).  In general, this is used to list the partition table contents so that you can determine where each partition starts. The output identifies the type of partition and its length, which makes it easy to use 'dd' to extract the partitions.  The output is sorted based on the starting sector so it is easy to identify gaps in the layout.
* [Automatically Updated man Page](http://www.sleuthkit.org/sleuthkit/man/mmls.html)

## Output Example
### DOS Partition
Output of running 'mmls' on a DOS partition

```
% mmls -t dos disk.dd
DOS Partition Table
Units are in 512-byte sectors

     Slot    Start        End          Length       Description
00:  Meta    0000000000   0000000000   0000000001   Primary Table (#0)
01:  -----   0000000000   0000000062   0000000063   Unallocated
02:  00:00   0000000063   0002056319   0002056257   Win95 FAT32 (0x0B)
03:  00:01   0002056320   0008209214   0006152895   OpenBSD (0xA6)
04:  00:02   0008209215   0019999727   0011790513   FreeBSD (0xA5)
```

The first column lists the Sleuth Kit assigned partition id.  

The <b>Slot</b> column lists where this partition is described in the volume system table. The contents of this column are volume system specific, but here are some general entries:
* ##: A two digit number is used with volume systems that have only one table and the number corresponds to the entry in the single table. 
* ##:##: This format is used with volume systems that have multiple tables (like DOS partitions). The first two numbers correspond to the table ID and the second set of numbers correspond to the entry in that table. 00:01 is entry 1 in table 0. 
* Meta: This is used to describe an entry that is created by TSK to show where metadata structures are located. Meta entries can be suppressed with flag options. These entries are not in any volume system table, but maybe helpful to the user.
* -----: This is used to identify an entry that is created by TSK for unallocated space. 

The <b>Start</b>, <b>End</b>, and <b>Length</b> columns describe the starting, ending and length of the volume (in sectors). The final column is a text description of the volume.  Sometimes this is directly from the volume table and other times it is created by TSK. 

### BSD Disk Label
Output of running 'mmls' on an OpenBSD disk label, which is inside of a DOS partition (as shown in the DOS partition example).  

```
% mmls -t bsd -o 2056321 disk.dd
BSD Disk Label
Units are in 512-byte sectors

     Slot    Start        End          Length       Description
00:  02      0000000000   0019999727   0019999728   Unused (0x00)
01:  08      0000000063   0002056319   0002056257   MSDOS (0x08)
02:  00      0002056320   0002260943   0000204624   4.2BSD (0x07)
03:  01      0002260944   0002875823   0000614880   Swap (0x01)
04:  03      0002875824   0003080447   0000204624   4.2BSD (0x07)
05:  04      0003080448   0003233663   0000153216   4.2BSD (0x07)
06:  07      0003233664   0004257791   0001024128   4.2BSD (0x07)
07:  06      0004257792   0008209214   0003951423   4.2BSD (0x07)
08:  09      0008209215   0019984859   0011775645   Unknown (0x0A)
```

### Mac Partitions
Output from running 'mmls' on a Mac system:

```
# mmls -t mac mac-disk.dd
MAC Partition Map
Units are in 512-byte sectors

     Slot    Start        End          Length       Description
00:  -----   0000000000   0000000000   0000000001   Unallocated
01:  Meta    0000000001   0000000010   0000000010   Table
02:  00      0000000001   0000000063   0000000063   Apple_partition_map
03:  01      0000000064   0000000117   0000000054   Apple_Driver43
04:  02      0000000118   0000000191   0000000074   Apple_Driver43
05:  03      0000000192   0000000245   0000000054   Apple_Driver_ATA
06:  04      0000000246   0000000319   0000000074   Apple_Driver_ATA
07:  05      0000000320   0000000519   0000000200   Apple_FWDriver
08:  06      0000000520   0000001031   0000000512   Apple_Driver_IOKit
09:  07      0000001032   0000001543   0000000512   Apple_Patches
10:  08      0000001544   0039070059   0039068516   Apple_HFS
11:  09      0039070060   0039070079   0000000020   Apple_Free
```

### Sun VTOC
Output of running 'mmls' on a Sun sparc disk:

```
# mmls -t sun solaris.disk.dd 
Sun VTOC
Units are in 512-byte sectors

     Slot    Start        End          Length       Description
00:  01      0000000000   0001048949   0001048950   swap (0x03)
01:  02      0000000000   0010257029   0010257030   backup (0x05)
02:  07      0001050840   0001460024   0000409185   /home/ (0x08)
03:  05      0001460025   0001971269   0000511245   /var/ (0x07)
04:  00      0001971270   0004113584   0002142315   / (0x02)
05:  06      0004113585   0010257029   0006143445   /usr/ (0x04)
```
