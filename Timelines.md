---
layout: default
title: "Timelines"
categories:
  - "Concepts"

redirect_from:
  - "/index.php/Timeline"
  - "/index.php/Timelines"
  - "/wiki/Timeline"
  - "/wiki/Timelines"

last_modified: 2008-10-26
---

Creating a timeline of system activity will give an investigator clues regarding where to probe further.  The timelines in [The Sleuth Kit](/The-Sleuth-Kit/) allow one to quickly get a high-level look at system activity, such as when files were compiled and when archives were opened. TSK allows you to generate timelines of activity from a variety of sources. [Autopsy](/Autopsy/) allows you to also create timelines using the TSK tools. 

# Background
Many files and directories have times associated with them.  The quantity and description of which depend on the file system type. For example, FFS and Ext2/3 file systems have a Modified, Accessed, and Changed time.  Ext2/3 also has a deleted time. FAT stores the Written, Accessed, and Created time, although by spec the Created and Access times are optional and the Access time is only accurate to the day.  NTFS has created, modified, changed, and accessed times. 

Other logs and sources of data may also have temporal data. For example, event logs, system logs, the Windows registry, and document metadata. Having those in a single time line, along with the file system data, can help to reconstruct events. You can create or find tools to save temporal data to the [body file](/Body-file/) format. 

# Timeline Creation
At a high level, generation is a two step process.  In the first step, temporal data is gathered from various data sources (such as file systems, registries, logs, etc.) and saved to the [body file](/Body-file/) format.  This step is done using the 'fls' tool in TSK or other tools, which are listed below. The second step is to sort and merge all of the temporal data into a single timeline.  This step is done using the 'mactime' script in TSK. 

## Data Gathering
The primary method for collecting temporal data from file systems is to run [fls](/Fls/) with the '-m' flag. With version 1.X and 2.X of TSK, you also had to run the [ils](/Ils/) command to get all unallocated files, but that is no longer required. 

The 'fls' command requires the '-m' argument with the '-r' flag to gather all files.  This step walks through the directory hierarchy and outputs a line for each file in the file system.  This command needs to be run for each partition in a disk image. 

As an example, consider a Windows system with only one partition (that starts at offset sector 63):

```
# fls -m "C:/" -o 63 -r images/disk.dd > body.txt
```

An example of an OpenBSD system with two partitions could be:

```
# fls -o 63 -f openbsd -m / -r images/disk.dd > body.txt
# fls -o 3233664 -f openbsd -m /var/ -r images/disk.dd >> body.txt
```

The time skew of the system can also be taken into consideration during this step. Using the '-s' argument to 'fls', the body file can have the adjusted times so that the system is consistent with other servers.

NOTE: This replaces the actions of 'grave-robber -m' in TCT.  The [mac-robber](/Mac-robber/) tool (on the www.sleuthkit.org web site) can also be used to gather allocated file data on a mounted file system. 'mac-robber' is useful for file systems where tools do not exist (such as AIX jfs).
 
Any data with times can be converted to the format needed by mactime. I have created scripts to convert log files to the format before so that all data was in a single timeline. 

Other scripts that are written to convert data to the mactime format include:
* Add here...

## Timeline Creation
When all of the temporal data has been merged into a single [body file](/Body-file/), the data can be sorted based on the times.  The [mactime](/Mactime/) program does that. 

The [Zeitline](http://projects.cerias.purdue.edu/forensics/timeline.php) tool also imports the same data format and has a more graphical display. 

# Other
See also [Ex-Tip](http://www.sans.org/reading_room/whitepapers/forensics/32767.php): An Extensible Timeline Analysis Framework in Perl (Michael Cloppert)
