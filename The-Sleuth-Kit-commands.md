---
layout: default
title: "The Sleuth Kit commands"
categories:
  - "Tools"

redirect_from:
  - "/index.php/The_Sleuth_Kit_commands"
  - "/wiki/The_Sleuth_Kit_commands"

last_modified: 2014-02-14
---

## The TSK 4 command list
*<strong>blkcalc</strong> - Converts between unallocated disk unit numbers and regular disk unit numbers.
*<strong>blkcat</strong> - Display the contents of file system data unit in a disk image.
*<strong>blkls</strong> - List or output file system data units.
*<strong>blkstat</strong> - Display details of a file system data unit (i.e. block or sector).
*<strong>fcat</strong> - Output the contents of a file based on its name.
*<strong>ffind</strong> - Finds the name of the file or directory using a given inode.
*<strong>fiwalk</strong> - print the filesystem statistics and exit.
*<strong>fls</strong> - List file and directory names in a disk image.
*<strong>fsstat</strong> - Display general details of a file system.
*<strong>hfind</strong> - Lookup a hash value in a hash database.
*<strong>icat</strong> - Output the contents of a file based on its inode number.
*<strong>ifind</strong> - Find the meta-data structure that has allocated a given disk unit or file name.
*<strong>ils</strong> - List inode information.
*<strong>img_cat</strong> - Output contents of an image file.
*<strong>img_stat</strong> - Display details of an image file.
*<strong>istat</strong> - Display details of a meta-data structure (i.e. inode).
*<strong>jcat</strong> - Show the contents of a block in the file system journal.
*<strong>jls</strong> - List the contents of a file system journal.
*<strong>jpeg_extract</strong> - jpeg extractor.
*<strong>mactime</strong> - Create an ASCII time line of file activity.
*<strong>mmcat</strong> - Output the contents of a partition to stdout.
*<strong>mmls</strong> - Display the partition layout of a volume system (partition tables).
*<strong>mmstat</strong> - Display details about the volume system (partition tables).
*<strong>sigfind</strong> - Find a binary signature in a file.
*<strong>sorter</strong> - Sort files in an image into categories based on file type.
*<strong>srch_strings</strong> - Display printable strings in files.
*<strong>tsk_comparedir</strong> - compare the contents of a directory with the contents of an image or local device.
*<strong>tsk_gettimes</strong> - Collect MAC times from a disk image into a body file.
*<strong>tsk_loaddb</strong> - populate a SQLite database with metadata from a disk image.
*<strong>tsk_recover</strong> - Export files from an image into a local directory.
  
  

## The TSK 3 command list (historical)
*<strong>blkcalc</strong>          - Converts between unallocated disk unit numbers and regular disk unit numbers.
*<strong>blkcat</strong>           - Display the contents of file system data unit in a disk image.
*<strong>blkls</strong>            - List or output file system data units.
*<strong>blkstat</strong>          - Display details of a file system data unit (i.e. block or sector).
*<strong>ffind</strong>            - Finds the name of the file or directory using a given inode.
*<strong>fls</strong>              - List file and directory names in a disk image.
*<strong>fsstat</strong>           - Display general details of a file system.
*<strong>hfind</strong>            - Lookup a hash value in a hash database.
*<strong>icat-sleuthkit</strong>   - Output the contents of a file based on its inode number.
*<strong>ifind</strong>            - Find the meta-data structure that has allocated a given disk unit or file name.
*<strong>ils-sleuthkit</strong>    - List inode information.
*<strong>img_cat</strong>          - Output contents of an image file.
*<strong>img_stat</strong>         - Display details of an image file.
*<strong>istat</strong>            - Display details of a meta-data structure (i.e. inode).
*<strong>jcat</strong>             - Show the contents of a block in the file system journal.
*<strong>jls</strong>              - List the contents of a file system journal.
*<strong>mactime-sleuthkit</strong> - Create an ASCII time line of file activity.
*<strong>mmcat</strong>            - Output the contents of a partition to stdout.
*<strong>mmls</strong>             - Display the partition layout of a volume system (partition tables).
*<strong>mmstat</strong>           - Display details about the volume system (partition tables).
*<strong>sigfind</strong>          - Find a binary signature in a file.
*<strong>sorter</strong>           - Sort files in an image into categories based on file type.
*<strong>srch_strings</strong>     - Display printable strings in files.

## Get a refreshed list
The list put in this page was created by a shell Bash command to show the basic function of the each TSK command.

The command used (in Debian) was:

 eriberto@canopus~$ dpkg -L sleuthkit | grep /usr/bin/ | cut -d"/" -f4 | sort | xargs whatis -l | sed 's/^/*<strong>/; s/ (1)/<\/strong>/; s/$/./' | tr -s . | tr -s " "

You should use the above command to refresh the list.
  
  

## Short-cut
This page can be accessed through the following short url: http://bit.ly/tsk-commands.
