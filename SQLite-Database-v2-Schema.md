---
layout: default
title: "SQLite Database v2 Schema"
categories:
  - "Development"

redirect_from:
  - "/index.php/SQLite_Database_v2_Schema"
  - "/wiki/SQLite_Database_v2_Schema"

last_modified: 2014-02-20
---

This page outlines version 2 of the [TSK](/The-Sleuth-Kit/) SQLite schema.  This database is made by using the [tsk_loaddb](/tsk_loaddb/) command line tool or the equivalent library-level methods.  Version 2 of the schema was released with version 4.0 of TSK and is used by [Autopsy 3](/Autopsy/).  We have a [SQLite Database v3 Schema](/SQLite-Database-v3-Schema/) that will be released as part of Autopsy 3.1 and TSK 4.1. 

Some general notes on this schema:
* This database can store information about multiple images (v1 was only for a single image). 
* Every type of data is assigned a unique ID, called the Object ID (v1 had unique file IDs and unique file system IDs, but not database-wide unique IDs). 
* Data in a disk image has a hierarchy.  Images are the root, with volume or file systems below it, followed by volumes and files.  
* The tsk_objects table is used to keep track of what object IDs have been used and to map the parent and child relationship. 
* This schema has been designed to store more than what TSK initially imports.  It has been designed to support carved files and a folder full of local files, etc.
* This schema supports the [blackboard](/Blackboard/) so that modules in Autopsy (and eventually the [TSK Framework](/TSK-Framework/)) can communicate and save results.
* The [TSK Framework](/TSK-Framework/) is not yet using this schema.  It is using v1.5, which added tables to the v1 schema.  v2 was created based on the lessons learned from the framework, but we have not yet ported the framework to it.  The details of the v1.5 schema can be found in the [Framework Users's and Developer's Guide](http://sleuthkit.org/sleuthkit/docs/framework-docs/index.html).
* Virtual files are made of unallocated space with the naming format of:
  * Unalloc_[PARENT-OBJECT-ID]_[BYTE-START]_[BYTE-END]

# General Information Tables
## tsk_db_info
Metadata about the database.
* *schema_ver* - Version of the database schema used to create database (must be 2 in this case)
* *tsk_ver* - Version of TSK used to create database

# Object Tables
## tsk_objects
Every object (image, volume system, file, etc.) has an entry in this table.  This table allows you to find the parent of a given object. 
* *obj_id* - Unique id 
* *par_obj_id* - The object id of the parent object (null for root objects). The parent of a volume system is an image, the parent of a directory is a directory or filesystem, the parent of a filesystem is a volume or an image, etc.
* *type* - Object type (as [TSK_DB_OBJECT_TYPE_ENUM](http://www.sleuthkit.org/sleuthkit/docs/api-docs/tsk__db__sqlite_8h.html) enum).

# Image Tables
## tsk_image_info
Contains information about each set of images that is stored in the database. 
* *obj_id* - Id of image in tsk_objects
* *type* - Type of disk image format (as TSK_IMG_TYPE_ENUM)
* *ssize* - Sector size of device in bytes
* *tzone* - Timezone where image is from (the same format that TSK tools want as input)

## tsk_image_names
Stores path(s) to file(s) on disk that make up an image set.
* *obj_id* - Id of image in tsk_objects
* *name* - Path to location of image file on disk
* *sequence* - Position in sequence of image parts

# Volume System Tables
## tsk_vs_info
Contains one row for every volume system found in the images.
* *obj_id* - Id of volume system in tsk_objects
* *vs_type* - Type of volume system / media management (as [TSK_VS_TYPE_ENUM](http://sleuthkit.org/sleuthkit/docs/api-docs/tsk__vs_8h.html#a0659bf1a83a42f2f5795f807e73ce0ff))
* *img_offset* - Byte offset where VS starts in disk image
* *block_size* - Size of blocks in bytes

## tsk_vs_parts
Contains one row for every volume / partition in the images. 
* *obj_id* - Id of volume in tsk_objects
* *addr* - Address of this partition
* *start* - Sector offset of start of partition
* *length* - Number of sectors in partition
* *desc* - Description of partition (volume system type-specific)
* *flags* - Flags for partition (as [TSK_VS_PART_FLAG_ENUM](http://sleuthkit.org/sleuthkit/docs/api-docs/tsk__vs_8h.html#a4b2397da0861c68e1c6f5101ce3dd8dc))

# File System Tables
## tsk_fs_info
Contains one for for every file system in the images. 
* *obj_id* - Id of filesystem in tsk_objects
* *img_offset* - Byte offset that filesystem starts at
* *fs_type* - Type of file system (as [TSK_FS_TYPE_ENUM](http://sleuthkit.org/sleuthkit/docs/api-docs/group__fslib.html#ga345301b5ebdaef825e93987fb5c777fd))
* *block_size* - Size of each block (in bytes)
* *block_count* - Number of blocks in filesystem
* *root_inum* - Metadata address of root directory
* *first_inum* - First valid metadata address
* *last_inum* - Last valid metadata address

## tsk_files
Contains one for for every file found in the images.  Has the basic metadata for the file. 
* *obj_id* - Id of file in tsk_objects
* *fs_obj_id* - Id of filesystem in tsk_objects (NULL if file is not located in a file system -- carved in unpartitioned space, etc.)
* *type* - Type of file: filesystem, carved, etc. (as [TSK_DB_FILES_TYPE_ENUM](http://sleuthkit.org/sleuthkit/docs/api-docs/tsk__db__sqlite_8h.html#a1111f5877e6a9cc56c14905807f29d01) enum)
* *attr_type* - Type of attribute (as TSK_FS_ATTR_TYPE_ENUM)
* *attr_id* - Id of attribute
* *name* - Name of attribute. Will be NULL if attribute doesn't have a name.
* *meta_addr* - Address of the metadata structure that the name points to.
* *has_layout* - True if file has an entry in tsk_file_layout
* *has_path* - True if file has an entry in tsk_files_path
* *dir_type* - File type information: directory, file, etc. (as TSK_FS_NAME_TYPE_ENUM)
* *meta_type* - File type (as TSK_FS_META_TYPE_ENUM)
* *dir_flags* -  Flags that describe allocation status etc. (as TSK_FS_NAME_FLAG_ENUM)
* *meta_flags* - Flags for this file for its allocation status etc. (as TSK_FS_META_FLAG_ENUM)
* *size* - File size in bytes
* *ctime* - Last file / metadata status change time (stored in number of seconds since Jan 1, 1970 UTC)
* *crtime* - Created time
* *atime* - Last file content accessed time
* *mtime* - Last file content modification time
* *mode* - Unix-style permissions (as TSK_FS_META_MODE_ENUM)
* *uid* - Owner id
* *gid* - Group id
* *md5* - MD5 hash of file contents
* *known* - Known status of file (as [TSK_DB_FILES_KNOWN_ENUM](http://www.sleuthkit.org/sleuthkit/docs/api-docs/tsk__db__sqlite_8h.html))
* *parent_path* - full path of parent folder. 

## tsk_file_layout
Stores the layout of a file within the image.  A file will have one or more rows in this table depending on how fragmented it was. All file types use this table (file system, carved, unallocated blocks, etc.).
* *obj_id* - Id of file in tsk_objects
* *sequence* - Position of this run in the file (0-based and the obj_id and sequence pair will be unique in the table)
* *byte_start* - Byte offset of fragment relative to the start of the image file
* *byte_len* - Length of fragment in bytes

## tsk_files_path
If a "locally-stored" file has been imported into the database for analysis, then this table stores its path.  Used for derived files and other files that are not directly in the image file.
* *obj_id* - Id of file in tsk_objects
* *path* - Path to where the file is locally stored in a file system.

## tsk_files_derived_method
Derived files are those that result from analyzing another file.  For example, files that are extracted from a ZIP file will be considered derived.  This table keeps track of the derivation techniques that were used to make the derived files. 
* *derived_id* - Unique id for this derivation method. 
* *tool_name* - Name of derivation method/tool
* *tool_version* - Version of tool used in derivation method
* *other* - Other details

## tsk_files_derived
Each derived file has a row that captures the information needed to re-derive it
* *obj_id* - Id of file in tsk_objects
* *derived_id* - Id of derivation method in tsk_files_derived_method
* *rederive* - Details needed to re-derive file (will be specific to the derivation method)

# Blackboard Tables
The [blackboard](/Blackboard/) is used to store results from analysis modules. 

## blackboard_artifacts
Stores artifacts associated with objects.
* *artifact_id* - Id of the artifact (assigned by the database)
* *obj_id* - Id of the associated object
* *artifact_type_id* - Id for the type of artifact (can be looked up in the blackboard_artifact_types table)

## blackboard_attributes
Stores name value pairs associated with an artifact. Only one of the value columns should be populated
* *artifact_id* - Id of the associated artifact.
* *source* - Source string, should be module name that created the entry.
* *context* - Additional context string
* *attribute_type_id* - Id for the type of attribute (can be looked up in the blackboard_attribute_types)
* *value_type* - The type of value (0 for string, 1 for int, 2 for long, 3 for double, 4 for byte array)
* *value_byte* - A blob of binary data (should be empty unless the value type is byte)
* *value_text* - A string of text (should be empty unless the value type is string)
* *value_int32* - An integer (should be 0 unless the value type is int)
* *value_int64* - A long integer (should be 0 unless the value type is long)
* *value_double* - A double (should be 0.0 unless the value type is double)

## blackboard_artifact_types
Types of artifacts
* *artifact_type_id* - Id for the type (this is used by the blackboard_artifacts table)
* *type_name* - A string identifier for the type (unique)
* *display_name* - A display name for the type (not unique, should be human readable)

Types of attribute
## blackboard_attribute_types
* *attribute_type_id* - Id for the type (this is used by the blackboard_attributes table)
* *type_name* - A string identifier for the type (unique)
* ''display_name - A display name for the type (not unique, should be human readable)

# Indexes
## parObjId
Index to speed up the process of finding parent objects.

* artifactID ON blackboard_artifacts(artifact_id)
* artifact_objID ON blackboard_artifacts(obj_id)
* attrsArtifactID ON blackboard_attributes(artifact_id)
* layout_objID ON tsk_file_layout(obj_id)
