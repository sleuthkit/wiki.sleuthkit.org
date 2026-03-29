---
layout: default
title: "SQLite Database v6 Schema"
categories:
  - "Development"

redirect_from:
  - "/index.php/SQLite_Database_v6_Schema"
  - "/wiki/SQLite_Database_v6_Schema"

last_modified: 2017-04-22
---

This page outlines version 6 of the [TSK](/The-Sleuth-Kit/) SQLite schema.  It is used in Autopsy 4.3.0 and beyond.  There is also a page for the [SQLite Database v3 Schema](/SQLite-Database-v3-Schema/). 

The database is made by using the [tsk_loaddb](/tsk_loaddb/) command line tool or the equivalent library-level methods.  It is also used by [Autopsy](/Autopsy/).

Some general notes on this schema:
* Every type of data is assigned a unique ID, called the Object ID
* Data sources are grouped by devices (to allow a computer or phone to have multiple drives in it)
* Data in a disk image has a hierarchy.  Images are the root, with volume or file systems below it, followed by volumes and files.  
* The tsk_objects table is used to keep track of what object IDs have been used and to map the parent and child relationship. 
* This schema has been designed to store more than what TSK initially imports.  It has been designed to support carved files and a folder full of local files, etc.
* This schema supports the [blackboard](/Blackboard/) so that modules in Autopsy can communicate and save results.
* Virtual files are made of unallocated space with the naming format of:
  * Unalloc_[PARENT-OBJECT-ID]_[BYTE-START]_[BYTE-END]

NOTE: This maybe a bit out of date. The code is the best reference.  See the initialize() method in [db_sqlite.cpp](https://github.com/sleuthkit/sleuthkit/blob/develop/tsk/auto/db_sqlite.cpp).

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

# Data Source/Device Tables
## data_source_info
Contains information about a data source, which could be an image.  This is where we group data sources into devices (based on device ID)
**obj_id* - Id of image/data source in tsk_objects
* *device_id* - Unique ID (GUID) for the device that contains the data source. 
* *time_zone* - Timezone that the data source was originally located in. 

## tsk_image_info
Contains information about each set of images that is stored in the database. 
* *obj_id* - Id of image in tsk_objects
* *type* - Type of disk image format (as TSK_IMG_TYPE_ENUM)
* *ssize* - Sector size of device in bytes
* *tzone* - Timezone where image is from (the same format that TSK tools want as input)
* *size* - Size of the original image (in bytes) 
* *md5* - Hash of the image.  Currently, this is populated only if the input image is E01. 
* *display_name* - display name of the image. 

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
* *display_name* - Display name of file system (could be volume label) (New in V3)

## tsk_files
Contains one for for every file found in the images.  Has the basic metadata for the file. 
* *obj_id* - Id of file in tsk_objects
* *fs_obj_id* - Id of filesystem in tsk_objects (NULL if file is not located in a file system -- carved in unpartitioned space, etc.)
* *type* - Type of file: filesystem, carved, etc. (as [TSK_DB_FILES_TYPE_ENUM](http://sleuthkit.org/sleuthkit/docs/api-docs/tsk__db__sqlite_8h.html#a1111f5877e6a9cc56c14905807f29d01) enum)
* *attr_type* - Type of attribute (as [TSK_FS_ATTR_TYPE_ENUM](http://www.sleuthkit.org/sleuthkit/docs/jni-docs/enumorg_1_1sleuthkit_1_1datamodel_1_1_tsk_data_1_1_t_s_k___f_s___a_t_t_r___t_y_p_e___e_n_u_m.html))
* *attr_id* - Id of attribute
* *name* - Name of attribute. Will be NULL if attribute doesn't have a name.  Must not have any slashes in it. 
* *meta_addr* - Address of the metadata structure that the name points to.
* *meta_seq* - Sequence of the metadata address - New in V3
* *has_layout* - True if file has an entry in tsk_file_layout
* *has_path* - True if file has an entry in tsk_files_path
* *dir_type* - File type information: directory, file, etc. (as [TSK_FS_NAME_TYPE_ENUM](http://www.sleuthkit.org/sleuthkit/docs/jni-docs/enumorg_1_1sleuthkit_1_1datamodel_1_1_tsk_data_1_1_t_s_k___f_s___n_a_m_e___t_y_p_e___e_n_u_m.html))
* *meta_type* - File type (as [TSK_FS_META_TYPE_ENUM](http://www.sleuthkit.org/sleuthkit/docs/jni-docs/enumorg_1_1sleuthkit_1_1datamodel_1_1_tsk_data_1_1_t_s_k___f_s___m_e_t_a___t_y_p_e___e_n_u_m.html))
* *dir_flags* -  Flags that describe allocation status etc. (as [TSK_FS_NAME_FLAG_ENUM](http://www.sleuthkit.org/sleuthkit/docs/jni-docs/enumorg_1_1sleuthkit_1_1datamodel_1_1_tsk_data_1_1_t_s_k___f_s___n_a_m_e___f_l_a_g___e_n_u_m.html))
* *meta_flags* - Flags for this file for its allocation status etc. (as [TSK_FS_META_FLAG_ENUM](http://www.sleuthkit.org/sleuthkit/docs/jni-docs/enumorg_1_1sleuthkit_1_1datamodel_1_1_tsk_data_1_1_t_s_k___f_s___m_e_t_a___f_l_a_g___e_n_u_m.html))
* *size* - File size in bytes
* *ctime* - Last file / metadata status change time (stored in number of seconds since Jan 1, 1970 UTC)
* *crtime* - Created time
* *atime* - Last file content accessed time
* *mtime* - Last file content modification time
* *mode* - Unix-style permissions (as [TSK_FS_META_MODE_ENUM](http://www.sleuthkit.org/sleuthkit/docs/jni-docs/enumorg_1_1sleuthkit_1_1datamodel_1_1_tsk_data_1_1_t_s_k___f_s___m_e_t_a___m_o_d_e___e_n_u_m.html))
* *uid* - Owner id
* *gid* - Group id
* *md5* - MD5 hash of file contents
* *known* - Known status of file (as [TSK_DB_FILES_KNOWN_ENUM](http://www.sleuthkit.org/sleuthkit/docs/api-docs/tsk__db__sqlite_8h.html))
* *parent_path* - full path of parent folder. Must begin and end with a '/' (Note that a single '/' is valid).
* *mime_type* - MIME type of the file content, if it has been detected. 

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
* *encoding_type* - Method used to store the file on the disk. 

## file_encoding_types
Methods that can be used to store files on local disks to prevent them from being quarantined by antivirus
* *encoding_type* - ID of method used to store data.  See [EncodingType](http://www.sleuthkit.org/sleuthkit/docs/jni-docs/4.3/enumorg_1_1sleuthkit_1_1datamodel_1_1_tsk_data_1_1_encoding_type.html) enum. 
* *name* -  Display name of technique. 

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

# Tags
## tag_names table
Defines what tag names the user has created and can therefore be applied.
* tag_name_id - Unique ID for each tag name
* display_name - Display name of tag
* description  - Description  (can be empty string)
* color - Color choice for tag (can be empty string)

## content_tags table
One row for each file tagged.  
* tag_id - unique ID
* obj_id - object id of Content that has been tagged
* tag_name_id - Tag name that was used
* comment  - optional comment 
* begin_byte_offset - optional byte offset into file that was tagged
* end_byte_offset - optional byte ending offset into file that was tagged

## blackboard_artifact_tags table
One row for each artifact that is tagged.
* tag_id - unique ID
* artifact_id - Artifact ID of artifact that was tagged
* tag_name_id - Tag name that was used
* comment - optional comment

# Ingest Module Status
These tables keep track in Autopsy which modules were run on the data sources.

## ingest_module_types table
Defines the types of ingest modules supported. 
* type_id INTEGER PRIMARY KEY
* type_name TEXT NOT NULL)",

## ingest_modules
Defines which modules were installed.  One row for each module. 
* ingest_module_id INTEGER PRIMARY KEY
* display_name TEXT NOT NULL
* unique_name TEXT UNIQUE NOT NULL
* type_id INTEGER NOT NULL
* version TEXT NOT NULL,

## ingest_job_status_types table
* type_id INTEGER PRIMARY KEY
* type_name TEXT NOT NULL

## ingest_jobs
One row is created each time ingest is started, which is a set of modules in a pipeline. 
* ingest_job_id INTEGER PRIMARY KEY
* obj_id INTEGER NOT NULL
* host_name TEXT NOT NULL
* start_date_time INTEGER NOT NULL
* end_date_time INTEGER NOT NULL
* status_id INTEGER NOT NULL
* settings_dir TEXT

## ingest_job_modules
Defines the order of the modules in a given pipeline (i.e. ingest_job)
* ingest_job_id INTEGER
* ingest_module_id INTEGER
* pipeline_position INTEGER,

# Indexes
## parObjId
Index to speed up the process of finding parent objects.

* artifactID ON blackboard_artifacts(artifact_id)
* artifact_objID ON blackboard_artifacts(obj_id)
* attrsArtifactID ON blackboard_attributes(artifact_id)
* layout_objID ON tsk_file_layout(obj_id)
