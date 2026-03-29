---
layout: default
title: "HashDB Schema"
categories:
  - "Development"

redirect_from:
  - "/index.php/HashDB_Schema"
  - "/wiki/HashDB_Schema"

last_modified: 2014-02-12
---

[The Sleuth Kit](/The-Sleuth-Kit/) comes with hash database functionality.  Historically, that meant that you could point it at a database file (such as NSRL or Encase hashset) and it would allow you to query it.  Starting with version 4.2 of the tool, it now includes a SQLite hashdatabase that allows you to create hashsets.  It is used in Autopsy 3.1.

# Schema
Make this more pretty:

```
CREATE TABLE db_properties (name TEXT NOT NULL, value TEXT)
CREATE TABLE hashes (id INTEGER PRIMARY KEY AUTOINCREMENT, md5 BINARY(16) UNIQUE, sha1 BINARY(20), sha2_256 BINARY(32))
CREATE TABLE file_names (name TEXT NOT NULL, hash_id INTEGER NOT NULL, PRIMARY KEY(name, hash_id))
CREATE TABLE comments (comment TEXT NOT NULL, hash_id INTEGER NOT NULL, PRIMARY KEY(comment, hash_id))
CREATE INDEX md5_index ON hashes(md5)
```

# Notes
We store the hashes in binary format.  To query for hashes (for testing) from the command line, use something like this:

```
select id,quote(md5) from hashes WHERE md5=X'B162EEB68B6BAC40E97C5A856E17D705';
```
