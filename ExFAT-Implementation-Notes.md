---
layout: default
title: "ExFAT Implementation Notes"
categories:
  - "File Systems"

redirect_from:
  - "/index.php/ExFAT_Implementation_Notes"
  - "/wiki/ExFAT_Implementation_Notes"

last_modified: 2014-06-03
---

# Introduction
This document contains information on the implementation of the [exFAT](/ExFAT/) file system in [The Sleuth Kit](/The-Sleuth-Kit/) (TSK). Like [FAT](/FAT/), exFAT has significant differences with the UNIX file system TSK was originally designed to support, and this document will identify how they were handled. A basic understanding of exFAT is assumed.

# Disk Unit Addressing
Like [FAT](/FAT/), exFAT saves file content in clusters, which are groupings of consecutive sectors (512-bytes each). It has the same problems as FAT in using these clusters as the addressable units, so like FAT the solution is to use sectors as the addressable unit instead. See [FAT_Implementation_Notes#Disk_Unit_Addressing](/FAT_Implementation_NotesDisk_Unit_Addressing/) for more information.

exFAT should support AF (Advance Format) so it is eventually possible to encounter an exFAT partition with 4K sectors and running in 4kn mode. Keep in mind that unlike legacy FAT and NTFS which have a 64K cluster size limit, exFAT can have clusters (allocation units) up to 32MiB.

# Metadata Addressing
Again, exFAT shares the same problems discussed in [FAT_Implementation_Notes#Metadata_Addressing](/FAT_Implementation_NotesMetadata_Addressing/), and the same solution is used. Note that normal exFAT files have at least three directory entry structures (more the longer the filename is), so the metadata addresses will increase by three or more for files in the same directory.

# Tool-specific Notes
## mmls and Partition Codes
ExFAT shares the same partition code as NTFS, so the string displayed by [mmls](/Mmls/) for type 0x07 is now "NTFS / exFAT (0x07)". See http://www.win.tue.nl/~aeb/partitions/partition_types-1.html

## fsstat and FAT Chains
Like FAT, exFAT does have FAT chains. However, they are only used to keep track of clusters for fragmented files. Printing a list of FAT Chains in fsstat could give the incorrect impression that those were the only allocated sectors, so it was decided that this part of the output should be hidden for exFAT.

Thought for design consideration:
The FAT indices are not used for contiguous files, and is so flagged by the FAT invalid flag. That means if the FAT Invalid flag is not set, then the FAT chain should be used.
Another consideration or issue to note is that unlike legacy FAT (FAT12/16/32) when a file is deleted, the FAT indices are not wiped out (in legacy FAT they had to be zeroed to indicate the cluster was free, but the Allocation Bitmap does that now). What this means is that if: 1) A file is fragmented, 2) That file is deleted, and 3) none of its clusters are reused - then a fragmented file where its clusters are all over the place and in any order can be collected and reconstructed because the FAT chain is intact after the delete. A lot of ifs, but a potential feature that is not possible in legacy FAT.

# Time Information
ExFAT stores the local time in its timestamp fields, so the notes in [FAT_Implementation_Notes#Notes_on_Timezones](/FAT_Implementation_NotesNotes_on_Timezones/) also apply here. However, exFAT does add some additional issues.

## Last Accessed Time
In testing, it does not appear that the last accessed time is ever updated from a file being accessed. It does change when a file is modified.

## Timezones
Timezone information for the three timestamp fields are also stored along with the DOS-format timestamps. However, these three fields are not found in the original specification, and the timezone fields are empty in some older versions of Windows, such as Vista SP1. Other implementations of exFAT may also leave the TZ fields empty, for example the Panasonic Lumix camera is leaving the TZ fields as zero on the SDXC cards (which are exFAT format). At present, TSK does not store this time zone information.

## Mac OS Differences
Through analysis, it was found that exFAT images created on Mac OS store time information differently than the Windows versions.

This is the File Directory Entry from a file created with Windows 7 (UTC-5:00), at 11:27 AM local time on 2013-12-31:

<tt>000230E0 85 02 8B B6 20 00 00 00 **6E 5B 9F 43** 73 5B 9F 43  

000230F0 73 5B 9F 43 18 00 **EC** EC EC 00 00 00 00 00 00 00</tt>

*Create time: 0x5B6E => 11:27:28
*Create time: 0x439F => 2013-12-31
*Create timezone: 0xEC = UTC-5:00 (see chart near end of http://www.sans.org/reading-room/whitepapers/forensics/reverse-engineering-microsoft-exfat-file-system-33274)

All that data is correct. Now here is the File Directory Entry from a file created on a Mac (UTC-8:00), at 10:11 local time on 2013-12-31:

<tt>000231E0 85 03 D4 40 30 00 00 00 **5D 11 21 44** 5D 11 21 44  

000231F0 5D 11 21 44 A9 AD **A0** A0 A0 00 00 00 00 00 00 00</tt>

*Create time: 0x115D => 2:10:58
*Create date: 0x4421 => 2014-01-01
*Create timezone: 0xA0 = UTC+8:00

Files created on a system set for UTC-5:00 end up with a timezone for UTC+5:00 (and have 10 hours added to the stored time/date). For these files, the overall time is correct (if strange), but what should be the local time is not. At present, since TSK does not process the timezone field, this means that timestamps from Mac images will be off by double the original time zone value.
