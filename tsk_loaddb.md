---
layout: default
title: "tsk_loaddb"
categories:
  - "Tools"

redirect_from:
  - "/Tsk-loaddb/"
  - "/index.php/Tsk_loaddb"
  - "/index.php/tsk_loaddb"
  - "/wiki/Tsk_loaddb"
  - "/wiki/tsk_loaddb"

last_modified: 2017-11-21
---

Back to [Help Documents](/Help-Documents/)

tsk_loaddb will save the image, volume, and file metadata to a SQLite database.  The database can be used by other programs so that they can access information about the image without using all of the TSK methods. 

There are multiple versions of the schema.  
* Version 1 was released with TSK 3.2. Its schema was never officially documented, but you can figure it out by looking at the CREATE statements in [tsk3/auto/auto_db.cpp](https://github.com/sleuthkit/sleuthkit/blob/sleuthkit-3.2/tsk3/auto/auto_db.cpp). 
* [SQLite Database v2 Schema](/SQLite-Database-v2-Schema/)
* [SQLite Database v3 Schema](/SQLite-Database-v3-Schema/)
* [SQLite Database v6 Schema](/SQLite-Database-v6-Schema/)
* [Database v7.2 Schema](/Database-v72-Schema/)

[Automatically Updated man Page](http://www.sleuthkit.org/sleuthkit/man/tsk_loaddb.html)
