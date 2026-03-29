---
layout: default
title: "TSK Schema Versioning"
categories:
  - "Development"

redirect_from:
  - "/index.php/TSK_Schema_Versioning"
  - "/wiki/TSK_Schema_Versioning"

last_modified: 2019-07-19
---

Autopsy uses the database schema that TSK creates (which is also created by tsk_loaddb). 

Each database has a schema version to help applications determine which tables should exist. 

Prior to Autopsy 2.9 (Schema 7.0), the version was a single number.  It is now a two part number that aligns with [Semantic Versioning ](https://semver.org/) so that backward incompatible changes are easier to detect.  There is no patch in the number (i.e. the 3rd number in semantic versions). 

    MAJOR.MINOR

The Major number is incremented when backward incompatible changes are made.  Examples include:
* Removing a table or column (expected data is missing)
* Adding a uniqueness constraint (can no longer add data)
* New enum value in an existing column (unexpected results - may cause some clients to throw errors because it doesn't know what to do with it). 

The Minor number is incremented when backward compatible changes are made.  Examples include:
* New table is added.
* New column is added.
* An index is added.

Example Schemas:
* [Database v7.2 Schema](/Database-v72-Schema/)
