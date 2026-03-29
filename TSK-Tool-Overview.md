---
layout: default
title: "TSK Tool Overview"
categories:
  - "Tools"

redirect_from:
  - "/index.php/TSK_Tool_Overview"
  - "/wiki/TSK_Tool_Overview"

last_modified: 2014-01-13
---

This page provides an overview of the command line tools in TSK.  The TSK tools are organized into layers and this page is organized based on those layers.  In general, the following tools take a disk or file system image as input.  

# File System Tools
## Fully Automated Tools
These tools integrate the volume and file system functionality.  Instead of analyzing only a single file system, these tools take a disk image as input and identify the volumes and process the contents. 
* [tsk_comparedir](/tsk_comparedir/): Compares a local directory hierarchy with the contents of raw device (or disk image). This can be used to detect rootkits. 
* [tsk_gettimes](/tsk_gettimes/): Extracts all of the temporal data from the image to make a [timeline](/Timeline/).  Equivalent to running [fls](/Fls/) with the '-m' option. 
* [tsk_loaddb](/tsk_loaddb/): Loads the metadata from an image into a SQLite database.  This allows other tools to be easily written in a variety of languages and give them access to the image contents. 
* [tsk_recover](/tsk_recover/): Extracts the unallocated (or allocated) files from a disk image to a local directory.

## File System Layer Tools
These file system tools process general file system data, such as the layout, allocation structures, and boot blocks
* [fsstat](/Fsstat/): Shows file system details and statistics including layout, sizes, and labels.

## File Name Layer Tools
These file system tools process the file name structures, which are typically located in the parent directory.
* [ffind](/Ffind/):  Finds allocated and unallocated file names that point to a given meta data structure.
* [fls](/Fls/): Lists allocated and deleted file names in a directory.

## Meta Data Layer Tools
These file system tools process the meta data structures, which store the details about a file.  Examples of this structure include directory entries in FAT, MFT entries in NTFS, and inodes in ExtX and UFS.
* [icat](/Icat/): Extracts the data units of a file, which is specified by its meta data address (instead of the file name).
* [ifind](/Ifind/): Finds the meta data structure that has a given file name pointing to it or the meta data structure that points to a given data unit.  
* [ils](/Ils/): Lists the meta data structures and their contents in a pipe delimited format.  
* [istat](/Istat/): Displays the statistics and details about a given meta data structure in an easy to read format.

## Data Unit Layer Tools
These file system tools process the [data unit](/Data-unit/)s where file content is stored.  Examples of this layer include clusters in FAT and NTFS and blocks and fragments in ExtX and UFS.  
* [blkcat](/Blkcat/): Extracts the contents of a given data unit.
* [blkls](/Blkls/): Lists the details about data units and can extract the unallocated  space of the file system.  
* [blkstat](/Blkstat/): Displays the statistics about a given data unit in an easy to read format.
* [blkcalc](/Blkcalc/): Calculates where data in the unallocated space image (from [blkls](/Blkls/)) exists in the original image.  This is used when evidence is found in unallocated space.

## File System Journal Tools
These file system tools process the journal that some file systems have.  The journal records the metadata (and sometimes content) updates that are made.  This could help recover recently deleted data.  Examples of file systems with journals include Ext3 and NTFS.
* [jcat](/Jcat/): Display the contents of a specific journal block.
* [jls](/Jls/): List the entries in the file system journal.

# Volume System Tools
These tools take a disk (or other media) image as input and analyze its partition structures.  Examples include DOS partitions, BSD disk labels, and the Sun Volume Table of Contents (VTOC).  These
can be used find hidden data between partitions and to identify the file system offset for The Sleuth Kit tools.  The media management tools support DOS partitions, BSD disk labels, Sun VTOC, and Mac
partitions.  
* [mmls](/Mmls/):  Displays the layout of a disk, including the unallocated spaces.
* [mmstat](/Mmstat/): Display details about a volume system (typically only the type).
* [mmcat](/Mmcat/): Extracts the contents of a specific volume to STDOUT.

# Image File Tools
This layer contains tools for the image file format.  For example, if the  image format is a split image or a compressed image.  
* [img_stat](/img_stat/): tool will show the details of the image format
* [img_cat](/img_cat/): This tool will show the raw contents of an image file.

# Disk Tools
These tools can be used to detect and remove a Host Protected Area (HPA) in an ATA disk.  A HPA could be used to hide data so that it would not be copied during an acquisition.  These tools are currently Linux-only.  
* [disk_sreset](/disk_sreset/): This tool will temporarily remove a HPA if one exists.  After the disk is reset, the HPA will return.
* [disk_stat](/disk_stat/): This tool will show if an HPA exists.  

# Other Tools
* [hfind](/Hfind/):  Uses a binary sort algorithm to lookup hashes in the NIST NSRL, Hashkeeper, and custom hash databases created by md5sum.
* [mactime](/Mactime/): Takes input from the [fls](/Fls/) and [ils](/Ils/) tools to  create a [timeline](/Timeline/) of file activity.  
* [sorter](/Sorter/): Sorts files based on their file type and performs extension checking and hash database lookups.   
* [sigfind](/Sigfind/): Searches for a binary value at a given offset.  Useful for recovering lost data structures.
