---
layout: default
title: "YAFFS2"
categories:
  - "File Systems"

redirect_from:
  - "/index.php/YAFFS2"
  - "/wiki/YAFFS2"

last_modified: 2013-10-29
---

# YAFFS2 Overview
This page provides a quick overview of the YAFFS2 file system. For a more complete description, see 
[How Yaffs Works](http://www.dubeiko.com/development/FileSystems/YAFFS/HowYaffsWorks.pdf).

Details on how TSK implements YAFFS2 can be found in [YAFFS2 Implementation Notes](/YAFFS2-Implementation-Notes/). The description below should be enough to understand the basic implementation.

## YAFFS2 Terms
* **Chunk** : Data unit consisting of a page and spare area (you can think of a chunk as a cluster in NTFS/FAT -- with some extra spare area that is not storing content)
* **Block** : Group of chunks ( a block is the unit of erasure)
* **Object** : A YAFFS2 file/directory/etc
* **Object ID** : Unique identifier for each object (you can think of this as the meta data address, but we use a different meta data address to better deal with different versions of an object)
* **Chunk ID** : Position of this chunk in the file (0 = header, 1 = first chunk with content, 2 = second chunk with content, etc.)  
* **Sequence Number** : Increments with each block written and stored in each chunk of a block (used to order blocks chronologically)

## YAFFS2 Objects
A YAFFS2 Object (file, directory, etc.) consists of a header chunk, storing all metadata for the object, and zero or more data chunks. The spare area of each chunk will contain an object ID, sequence number, chunk ID, and file size, and possibly the type of object and the object ID of its parent (the type and parent object ID will also be in the data portion of the header chunk).

A YAFFS2 file system consists entirely of these objects - there is no master record of files or directory structure. The parent object ID field in each object is the only source for reconstructing the file hierarchy.

## Basic YAFFS2 Operation
YAFFS2 is a log-structured file system that writes only once to each chunk. It does not use deletion markers; instead it stores enough information to reconstruct the chronological order of each chunk and from there use the most recent. The primary tool to do this is a sequence number stored in each chunk. This sequence number is incremented with each new block written, so that ordering blocks by sequence number will result in a chronological list regardless of where the blocks are in memory. Chunks are written sequentially within each block, so chunks early in a block are older than chunks that occur later.

For those not familiar with the workings of flash memory, an entire block is erased at a time. Once a chunk is written to, it cannot be changed without resetting the entire block that it belongs to. When the block is reset, it gets a new sequence number. 

As an example, if we create a file temp.txt with 2 chunks worth of data, and then the first chunk of data is changed, we could see the following:
<table class="wiki-table table table-bordered table-sm">
  <tbody>
  <tr>
    <td>Sequence number</td>
    <td>Offset</td>
    <td>Object ID</td>
    <td>Chunk ID</td>
    <td>Notes</td>
  </tr>
  <tr>
    <td>1000</td>
    <td>0x29400</td>
    <td>500</td>
    <td>0</td>
    <td>Object header containing file name "temp.txt" and other metadata</td>
  </tr>
  <tr>
    <td>1000</td>
    <td>0x29c40</td>
    <td>500</td>
    <td>1</td>
    <td>First chunk of "temp.txt"</td>
  </tr>
  <tr>
    <td>1000</td>
    <td>0x2a480</td>
    <td>500</td>
    <td>2</td>
    <td>Second chunk of "temp.txt"</td>
  </tr>
  <tr>
    <td>1000</td>
    <td>0x2acc0</td>
    <td>500</td>
    <td>1</td>
    <td>First chunk of "temp.txt"</td>
  </tr>
  </tbody>
</table>

The first version of chunk 1 is still there, but since we have a newer one it will now be ignored. 

If after that we delete the file, it will get two new header blocks with the file named changed to "unlinked" or "deleted", the size set to zero, and the parent ID set to the unlinked or deleted folders.
<table class="wiki-table table table-bordered table-sm">
  <tbody>
  <tr>
    <td>Sequence number</td>
    <td>Offset</td>
    <td>Object ID</td>
    <td>Chunk ID</td>
    <td>Notes</td>
  </tr>
  <tr>
    <td>1000</td>
    <td>0x29400</td>
    <td>500</td>
    <td>0</td>
    <td>Object header containing file name "temp.txt" and other metadata</td>
  </tr>
  <tr>
    <td>1000</td>
    <td>0x29c40</td>
    <td>500</td>
    <td>1</td>
    <td>First chunk of "temp.txt"</td>
  </tr>
  <tr>
    <td>1000</td>
    <td>0x2a480</td>
    <td>500</td>
    <td>2</td>
    <td>Second chunk of "temp.txt"</td>
  </tr>
  <tr>
    <td>1000</td>
    <td>0x2acc0</td>
    <td>500</td>
    <td>1</td>
    <td>First chunk of "temp.txt"</td>
  </tr>
  <tr>
    <td>1006</td>
    <td>0x02940</td>
    <td>500</td>
    <td>0</td>
    <td>Unlinked header</td>
  </tr>
  <tr>
    <td>1006</td>
    <td>0x03180</td>
    <td>500</td>
    <td>0</td>
    <td>Deleted header</td>
  </tr>
  </tbody>
</table>

Again, all the old data is still present (though at some point it may be garbage collected) but it will be ignored since we have a new header. Also note how the deleted header has a lower offset than the older data but a higher sequence number.

# YAFFS2 TSK Configuration File
The YAFFS2 code in TSK uses the most common settings for page and spare size, and number of chunks per block, and attempts to detect the spare area offsets, but if this fails the user can create a configuration file. This configuration file should have the same name as the image (or the first segment of the image) followed by "-yaffs2.config" (MAY CHANGE).

## Configuration File Format
The configuration file supports the following parameters:
* Flash layout-related (any combination of these can be present; missing values will go to defaults)
  * flash_page_size (default 2048)
  * flash_spare_size (default 64)
  * flash_chunks_per_block (default 64)
* Spare layout-related (need either all three or none - auto-detection routine will run if none are specified)
  * spare_seq_num_offset
  * spare_obj_id_offset
  * spare_chunk_id_offset

See the YAFFS2 summary above or look in the references for more information on each field. Note that there is a fourth spare area field, nBytes, but it is not currently needed to load a YAFFS2 image so we omit it from the configuration file.

## Sample Configuration File

```
# YAFFS2 config file

spare_seq_num_offset = 12
spare_obj_id_offset = 16
spare_chunk_id_offset = 20

flash_page_size = 4096
flash_spare_size = 128
```

In this case, flash_chunks_per_block will go to the default value.

## Tips for Creating the Configuration File
Running with the verbose flag (-v) set and specifying the YAFFS2 file system (-f yaffs2) displays information that may help in figuring out the correct spare area offsets.

First, the spare areas being tested are displayed. 

```
yaffs_initialize_spare_format: Testing potential offsets for the sequence number in the spare area
81180000730500008b14000000080000bfa885970002201c23d5ffffffffffffffff000000000000000000000000000000000000000000000000000000000000
81180000310200004a00000000080000994333f0ea2a7d1af439ffffffffffffffff60e3d379ac3f1c9903f5e787ceb57affc5940b3008136f39c03afe49aa94
81180000310200004b00000000080000976bf0194a9b19e13c60ffffffffffffffff8d7b96028d2c59c55e83ecf0aefbd204216f36aae521e00d057a5bf508b8
81180000310200004c0000000008000000c3d3b6e2410dedc2a1ffffffffffffffff852a62efe74305cbaedfb9691771a49366660cbfb46e358a69a3f307fffd
81180000310200004d0000000008000006022912b7a750c31318ffffffffffffffffb1e041f10a6d47c6130695e929e75fdd0cd1d552ed93a573121a9279bc75
81180000310200004e00000000080000932b3a03743a9c01e228ffffffffffffffff8cd806b2dca1ed0e86a0b46538ae5348bc66a4dc599f5ca1f83babcf001c
81180000310200004f00000000080000d7d7a23cdb5510108fccfffffffffffffffff670218f472fdd661c7891e438d3a55daf5d0cbda416325a388edd564c36
81180000310200005000000000080000f04526b40c419919e041ffffffffffffffff8283543170dc1fe937f64ef906c33af1108cba2019779cb9aeddcd07ac9a
81180000310200005200000000080000aa39f8bde8e626e2bb70fffffffffffffffff1d9bbd6fd6bb5664d2c6858efac023346bb59c611049807402f35b3b37f
81180000310200005300000000080000957cfaa6060aabea8236ffffffffffffffff20d5027839e3dbe5144114b0f976458b0e3b2b0eec2c17f8e3a2898139d8
001000000a01000018000000000800001e88e153dbdd1a44f460ffffffffffffffffa5da0966954c8360ee9b67754b433d203d3067232c0f03e7b9c7a913ba2d
001000000a01000019000000000800004aef0ab29d0d314ce893ffffffffffffffff2ea6c326ceb00664b16956562a4d4df0ff014fd9facd3015417809602b16
001000000a0100001a00000000080000ba07de1edafd6e3d7dddffffffffffffffffaa2831a599b484a0eb0d246e6682fc4dc240f96850bfb2cb5628f6a3a7b7
...
```

These spare areas are pulled out from various blocks in the file, currently 10 spare areas per block. The spare areas generally do have structure to them like the example above; if there doesn't appear to be any then it's possible the page/spare size could be wrong. The auto-detection assumes that the sequence number, object id, and chunk id fields will be contiguous, though this is not guaranteed to be true. Generally, this is what we expect in each field:
* Sequence number: 4 bytes. Should not be 0x00000000 or 0xffffffff, should be the same for every spare in the block
* Object ID: 4 bytes. Should not be 0x00000000, frequently repeats when writing multiple chunks of one file at a time
* Chunk ID: 4 bytes. Frequently see values increment as a multi-chunk section of a file is written

The verbose output will print out the results for each starting offset. Most of the testing is done on the sequence number, with just a check that the object ID is not zero and that all the bytes are not the same (almost certainly a false hit). 

```
yaffs_initialize_spare_format: Found potential spare offsets:  0 (sequence number), 4 (object id), 8 (chunk id), 12 (n bytes)
yaffs_initialize_spare_format:  Previous offsets appear good - will use as final offsets
yaffs_initialize_spare_format: Elimimating offset 1 - did not match previous chunk sequence number
yaffs_initialize_spare_format: Elimimating offset 2 - did not match previous chunk sequence number
...
yaffs_initialize_spare_format: Elimimating offset 8 - did not match previous chunk sequence number
yaffs_initialize_spare_format: Elimimating offset 9 - invalid sequence number 0
yaffs_initialize_spare_format: Found potential spare offsets:  10 (sequence number), 14 (object id), 18 (chunk id), 22 (n bytes)
yaffs_initialize_spare_format:  Previous offsets appear good but staying with earlier valid ones
yaffs_initialize_spare_format: Found potential spare offsets:  11 (sequence number), 15 (object id), 19 (chunk id), 23 (n bytes)
yaffs_initialize_spare_format:  Previous offsets appear good but staying with earlier valid ones
...
```

If there are other possibilities listed, putting those in the config file could be a good place to start. Otherwise use the listing of spare areas to try to figure out what the offsets should be.

# Reference Docs
* [How Yaffs Works](http://www.dubeiko.com/development/FileSystems/YAFFS/HowYaffsWorks.pdf)
* [Yaffs 2 Specification](http://www.yaffs.net/yaffs-2-specification)
