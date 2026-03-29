---
layout: default
title: "Mactime output"
categories:
  - "Tools"

redirect_from:
  - "/index.php/Mac-robber_output"
  - "/index.php/Mactime_output"
  - "/wiki/Mac-robber_output"
  - "/wiki/Mactime_output"

last_modified: 2016-10-08
---

Back to [Help Documents](/Help-Documents/)

## mactime
[mactime](/Mactime/) is a [TSK](/The-Sleuth-Kit/) Perl script that reads [file metadata](/file-metadata/) stored in the [body file](/Body-file/) format and sorts the data to create a [timeline](/Timeline/) of file activity.   The resulting timeline is plain text with several columns. This page describes what each column means.  This program was originally created to analyze Unix file systems and therefore some of the columns have little meaning when analyzing a Windows file system. 

### Example Output

```
Columns:
      Date/Time              Size    Activity         Unix      User     Group     inode     File Name
                            (Bytes)    Type        Permissions   Id        Id     
Example:
[...]
Thu Aug 21 2003 01:20:38      512       m.c.       -/-rwxrwxrwx     0        0        4        /file1.dat
                              900       m.c.       -/-rwxrwxrwx     0        0        8        /file3.dat
Thu Aug 21 2003 01:21:36      512       m.c.       -/-rwxrwxrwx     0        0        12       /_ILE5.DAT (deleted)
Thu Aug 21 2003 01:22:56      512       .a..       -/-rwxrwxrwx     0        0        4        /file1.dat
[...]
```

### Date/Time
The first column is the date and time of the activity.  If the following line is for activity during the same second as the previous line, then the time is not duplicated.  We can see this in the above example.  Both 'file1.dat' and 'file3.dat' had activity at the same time. 

### File Size
The second column is the size of the file (in bytes).

### Activity Type
The third column describes the activity type for the given time.  This column can be the source of confusion. It contains the letters 'm', 'a', 'c', 'b', and '.'.  Each represents a time associated with the file (and '.' is used when a given time is not being used for that entry).  Confusion can exist because different file systems have different file times.  Use the following table to determine what time is being shown:

#### MAC Meaning by File System
<table class="wiki-table table table-bordered table-sm">
  <thead>
  <tr>
    <th>File System</th>
    <th>m</th>
    <th>a</th>
    <th>c</th>
    <th>b</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Ext4</td>
    <td>Modified</td>
    <td>Accessed</td>
    <td>Changed</td>
    <td>Created</td>
  </tr>
  <tr>
  </tr>
  <tr>
    <td>Ext2/3</td>
    <td>Modified</td>
    <td>Accessed</td>
    <td>Changed</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>FAT</td>
    <td>Written</td>
    <td>Accessed</td>
    <td>N/A</td>
    <td>Created</td>
  </tr>
  <tr>
    <td>NTFS</td>
    <td>File Modified</td>
    <td>Accessed</td>
    <td>MFT Modified</td>
    <td>Created</td>
  </tr>
  <tr>
    <td>UFS</td>
    <td>Modified</td>
    <td>Accessed</td>
    <td>Changed</td>
    <td>N/A</td>
  </tr>
  </tbody>
</table>

*Note:* Some file systems have additional times that will not be displayed.  For example, [Ext2/3](/ExtX/) has a 'deleted' time that is not displayed. NTFS also has another set of times that are stored in the $FILE_NAME [attribute](/attribute/) that are not displayed in the time line.  The $FILE_NAME times can be viewed using the [istat](/Istat/) tool.

### Unix Permissions
The fourth column is the permissions of the file (in Unix format).  In this example, we have a FAT file system and therefore all permissions are displayed (because FAT does not have a notion of permissions outside of "read only"). 

### User & Group IDs
The fifth and sixth columns contain the User and Group Ids.  These will be non-zero only on Ext2/3 or UFS file systems.

### inode
The seventh column is the "inode" or [metadata address](/Metadata-Address/) of the file. 

### File Name
The eighth column is the file name.  If the file name is not allocated, then it will have "(deleted)" after the name.  This can be seen in the previous example. If the name is not allocated, but the metadata for the file is allocated, then it will have "(realloc)" in the name.  This shows that the metadata associated with this file name may not be valid any more because it could correspond to a different file.
