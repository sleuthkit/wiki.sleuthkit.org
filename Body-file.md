---
layout: default
title: "Body file"
categories:
  - "Concepts"

redirect_from:
  - "/index.php/Body_file"
  - "/wiki/Body_file"

last_modified: 2009-04-27
---

The body file is an intermediate file when creating a [timeline](/Timeline/) of file activity.  It is a pipe ("|") delimited text file that contains one line for each file (or other even type, such as a log or registry key). The [fls](/fls/), [ils](/ils/), and [mac-robber](/mac-robber/) tools all output this data format.   The [mactime](/mactime/) tool reads this file and sorts the contents (therefore the format is sometimes referred to as the "mactime format"). 

The body file format in TSK 3.0+ is different from the format used in TSK 1.X and 2.X. 

The 3.X output has the following fields:

```
MD5|name|inode|mode_as_string|UID|GID|size|atime|mtime|ctime|crtime
```

The times are reported in UNIX time format. Lines that start with '#' are ignored and treated as comments.  In mactime, many of theses fields are optional.  Its only requirement is that at least one of the time values is non-zero. The non-time values are simply printed as is. Other tools that read this file format may have different requirements. 

The 2.X output has the following fields:

```
MD5 | path/name | device | inode | mode_as_value | mode_as_string | num_of_links
 | UID | GID | rdev | size | atime | mtime | ctime | block_size | num_of_blocks
```

For example:

```
0|/wusagedl.exe|0|6|33279|-/-rwxrwxrwx|1|0|0|0|3827200|1220846400|1216831874|1216831874|512|0
```
