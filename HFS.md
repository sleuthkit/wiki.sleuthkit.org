---
layout: default
title: "HFS"
categories:
  - "File Systems"

redirect_from:
  - "/index.php/HFS"
  - "/wiki/HFS"

last_modified: 2019-12-29
---

HFS is a generic term used by [TSK](/The-Sleuth-Kit/) to refer to the HFS, HFS+, and HFSX file systems.  They are commonly found on Apple systems and are supported by TSK (as of 3.1.0).  As of TSK 4.0.0, HFS+ extended attributes, resource forks, hard links, symbolic links, and compressed files are also supported.  HFS file systems (not HFS+ or HFSX) are not supported by TSK.

## Background
HFS+ is the native file system for all versions Mac OS X and was introduced in 1998 to replace HFS.  On Macs, HFS+ is often referred to as "Mac OS Extended."  HFS (without the +) is rarely seen any more, except as a compatibility wrapper around early HFS+ file systems (from before OS X 10.4).

HFSX is a version of HFS+ that *optionally* supports case-sensitive path names.  It is commonly used on iOS devices (iPhones, etc.).

For more information, refer to:
* [Apple Developer's Technical Note 1150](http://developer.apple.com/legacy/mac/library/#technotes/tn/tn1150.html) which describes the HFS+ format
* [Forensics Wiki Entry](http://www.forensicswiki.org/wiki/HFS)
* [Wikipedia HFS Entry](http://en.wikipedia.org/wiki/Hierarchical_File_System)
* [Wikipedia HFS+ Entry](http://en.wikipedia.org/wiki/HFS%2B)

For reference, the source code to Apple's own implementation of HFS+ for Mac OS X is available at [opensource.apple.com](http://opensource.apple.com/) under [xnu/bsd/hfs/](http://opensource.apple.com/source/xnu/xnu-1699.26.8/bsd/hfs/) (this link is for OS X 10.7.4).

## HFS in TSK
The SleuthKit supports HFS+ and HFSX.  It also supports HFS, but only as a wrapper around an HFS+ file system.

### Resource Forks
Files in HFS+ can have two sets of data, called *forks*: a data fork and a resource fork.  The data fork of most files contains what is conventionally considered to be the file's content.  With the exception of [compressed files](/HFS-File-Compression/), resource forks are not often used in modern versions of Mac OS X.  As of TSK 4.0.0, a file's resource fork is visible in its [istat](/istat/) output and can be retrieved via [icat](/icat/).  In TSK, a file's resource fork is made available as a file attribute called RSRC, number 4353-1, that can be passed to [icat](/icat/) for examination.  (The data fork is attribute 4352-0, DATA, and is normally the default one used by [icat](/icat/).)

[istat](/istat/) also parses the resource fork's contents (if present) and prints a list of the individual resource entries.  For each resource, it shows the resource *type* (four ASCII characters), the numeric ID, the offset (in bytes) within the file's resource fork, the size (in bytes), and the name of the resource (which is optional).

To access an individual resource within the resource fork, use [icat](/icat/) on *inum-4353-1* and examine the data at the offset and size given by [istat](/istat/).

### HFS+ Attributes
HFS+ supports arbitrary named attributes, called *extended attributes*, on files and directories.  Access Control Lists (ACLs) are the most common use for attributes in HFS+.  Extended attributes are also used to mark compressed files.

As of TSK 4.0.0, [istat](/istat/) shows all of a file's extended attributes.  Each extended attribute is loaded as a TSK attribute, with type ExATTR (numerically, 4354-*) and the name of the extended attribute as its TSK attribute name.  There is one exception: an attribute that marks a file as compressed, as explained in the next section, will have type CMPF (numerically, 4355).

### HFS+ File Compression
In Mac OS X 10.6, Apple introduced *file compression* (AppleFSCompression, internally) in HFS+.  Compression is most often used for files installed as part of Mac OS X; user files are typically not compressed (but certainly can be!).  Reading and writing compressed files is transparent as far as Apple's file system APIs.

Compressed files have an empty data fork.  This means that forensic tools not aware of HFS+ file compression (including TSK before 4.0.0) will not see **any** data associated with a compressed file!

All compressed files have an extended attribute named <tt>com.apple.decmpfs</tt> which contains a compression header of 16 bytes.  The actual data for compressed files is stored in one of three ways, depending on the size and compressibility of the file:

1. The data is stored in the resource fork and compressed with zlib.  (The resource fork will contain exactly one resource, of type <tt>cmpf</tt>.  Apple's HFS+ implementation prevents compressed HFS+ files from having other resource fork data.)  This compression strategy is used for large files.
1. The data is stored in the <tt>com.apple.decmpfs</tt> extended attribute, compressed with zlib, immediately after the compression header.  This compression strategy is used for mid-sized files (those that compress down to ~3800 bytes or less).
1. The data is stored, uncompressed, in the <tt>com.apple.decmpfs</tt> extended attribute immediately after the compression header.  This compression strategy is used for very small (or empty) files, effectively storing their data directly in the Attributes tree rather than reserving separate blocks on disk for it.

(The on-disk format allows for other compression strategies to be defined and used, but Mac OS X as of 10.7.4 only uses these three. Since Mac OS X 10.9 LZVN is occasionally used on system files by default but SleuthKit does not support them yet. LZFSE is also introduced in 10.9. See [afsctool.h](https://github.com/RJVB/afsctool/blob/a716a6a4341fdd5116c70114449c5377bca0c8c5/src/afsctool.h#L52-L57).)

As of TSK 4.0.0, [istat](/istat/) will show these details about compressed HFS+ files.  In addition, [icat](/icat/) will automatically decompress the file data by default.

In cases 2 and 3 (above), TSK will load the uncompressed data of the file into resident DATA attribute 4352-0.  In case 1, TSK will make the compressed data in the resource fork available as non-resident RSRC attribute 4353-1.  The *uncompressed* data will be available as a virtual DATA attribute, 4352-0 (appearing as non-resident).

Thus, for any compressed file, [icat](/icat/) of the default DATA attribute (4352-0) will show the uncompressed content of the file.  To read the raw, compressed data, point [icat](/icat/) at the resource fork attribute (4353-1) or at the <tt>com.apple.decmpfs</tt> attribute as appropriate.

The exact same mechanism is also used by APFS, which SleuthKit supports.

### HFS+ Hard Links
In HFS+, all hard linked files are really pointers to "actual" files in a special directory:

>  <tt>/^^^^HFS+ Private Data</tt>

Those four leading carets represent null characters (ASCII 0).  We call this the metadata directory.  The files all have names like

>  <tt>iNode<i>&lt;nnnn></i></tt>

where *&lt;nnnn>* is a link number.  In practice, the link number is equal to the inode number (or CNID).  However, this is not required in the specification, and TSK does not assume that this is so.

In TSK (in the standard build) those null characters, and all other nulls appearing in file names, are mapped to the caret character.  Thus, in printed form, you will see carets, and you may enter carets when specifying such a path name.

The HFS+ hard link is a file in the file system Catalog which is marked as a "regular" file, but has some special characteristics that indicate that it is a hard link.  One of its metadata fields is a "link number" which can be used to assemble the path name to the actual file which we refer to as the target of the link.  The HFS+ file system is supposed to transparently direct all references to the hard link to the target file instead.  Such target files are, themselves, never hard links.

HFS+ file systems can also contain hard links to directories, although such links cannot be created by users of Apple software in any ordinary way (they are primarily used for Time Machine backups).  They are implemented very similarly to file hard links, except that the targets are differently named, and occur in a different metadata directory.  The metadata directory is:

>  <tt>/HFS+ Private Directory Data^</tt>

where that last caret is a carriage return character (ASCII 0x0D).  In TSK, the [fls](/fls/) and [istat](/istat/) programs display this character as a caret, but in all other parts of TSK, the character is left as-is.  Each hard linked directory has a name like:

>  <tt>dir_<i>&lt;nnn></i></tt>

where *&lt;nnn>* is the link number.  As with hard linked files, the link number and the inode number (or CNID) are the same in practice, although this is not required by the specification, and TSK does not assume this.

With ordinary use of TSK on an HFS+ file system, you will never have "in hand" the inode number (or CNID) of a hard link.  All of the utility programs and libraries that return inode numbers will only return the inode numbers of the link targets.  Thus, if you do an [istat](/istat/), [icat](/icat/), or [fls](/fls/) of such an inode number, you will see the results for the hard link target.  So, the file name will be iNode<nnn> or dir_<nnn> for the appropriate link number.   The [istat](/istat/) program will tell you that this is a hard link to a file or directory.   If you run [fls](/fls/) on a directory that contains a hard link (file, or directory), the listing will show the name of the link, but will show the file type and inode number of the target.  Here is an example listing showing an fls of a directory followed by an istat of a hard link that it contains.

 $ ./fls -o 409640 -f hfs \\\\.\\PhysicalDrive1 39668
 r/r 39669:      .com.apple.timemachine.supported
 r/r 270:        .DS_Store
 d/d 39671:      private
 l/l 39681:      User Guides And Information
 d/d 39682:      Users
 d/d 32974:      usr
 l/l 39873:      var
 
 
 $ ./istat -o 409640 -f hfs \\\\.\\PhysicalDrive1 270
 File Path: /^^^^HFS+ Private Data/iNode270
 Catalog Record: 270
 Allocated
 Type:   File
 Mode:   rrw-rw-r--
 Size:   12292
 uid / gid: 501 / 80
 Link count:     24
 
 File Name: iNode270
 This is a hard link to a file
 Admin flags: 0
 Owner flags: 0
 Has extended attributes
 Has security data (ACLs)
 File type:      0000
 File creator:   0000
 Is invisible
 Text encoding:  0 = MacRoman
 Resource fork size:     0
 
 Times:
 Created:        2009-02-26 11:54:19 (Eastern Standard Time)
 Content Modified:       2009-03-27 21:53:00 (Eastern Daylight Time)
 Attributes Modified:    2009-04-03 14:16:01 (Eastern Daylight Time)
 Accessed:       2012-03-02 18:45:20 (Eastern Standard Time)
 Backed Up:      0000-00-00 00:00:00 (UTC)
 
 Data Fork Blocks:
 202135-202138
 
 Attributes:
 Type: ExATTR (4354-2)   Name: com.apple.metadata:_kTimeMachineNewestSnapshot   Resident   size: 50
 Type: ExATTR (4354-3)   Name: com.apple.metadata:_kTimeMachineOldestSnapshot   Resident   size: 50
 Type: ExATTR (4354-4)   Name: com.apple.system.Security   Resident   size: 68
 Type: DATA (4352-0)   Name: DATA   Non-Resident   size: 12292  init_size: 12292
 
This listing shows that entry <tt>.DS_Store</tt> occurs in the listed directory and is a hard link.  The name of the target is <tt>iNode270</tt>, and it is a regular file.

If you [istat](/istat/) a hard linked directory, such as "usr" (3274) above, you will get a similar result:

 $ ./istat -o 409640 -f hfs \\\\.\\PhysicalDrive1 32974
 File Path: /.HFS+ Private Directory Data^/dir_32974
 Catalog Record: 32974
 Allocated
 Type:   Folder
 Mode:   drwxr-xr-x
 Size:   0
 uid / gid: 0 / 0
 Link count:     24
 
 File Name: dir_32974
 This is a hard link to a folder.
 Admin flags: 0
 Owner flags: 0
 Has extended attributes
 Has security data (ACLs)
 Is invisible
 Text encoding:  0 = MacRoman
 
 Times:
 Created:        2008-05-31 08:21:00 (Eastern Daylight Time)
 Content Modified:       2009-02-26 13:38:14 (Eastern Standard Time)
 Attributes Modified:    2009-04-03 14:16:06 (Eastern Daylight Time)
 Accessed:       2012-03-02 18:47:40 (Eastern Standard Time)
 Backed Up:      0000-00-00 00:00:00 (UTC)
 
 Attributes:
 Type: ExATTR (4354-2)   Name: com.apple.metadata:_kTimeMachineNewestSnapshot   Resident   size: 50
 Type: ExATTR (4354-3)   Name: com.apple.metadata:_kTimeMachineOldestSnapshot   Resident   size: 50
 Type: ExATTR (4354-4)   Name: com.apple.system.Security   Resident   size: 68
 Type: ExATTR (4354-5)   Name: com.apple.system.hfs.firstlink   Resident   size:6

The [istat](/istat/) of a file that occurs below such a hard linked directory in the file system hierarchy will show a path that begins with the link target, like this:

>  <tt>File Path: /.HFS+ Private Directory Data^/dir_32974/sbin</tt>

If you happen to [istat](/istat/) the inode number of an actual link (file or directory), then istat will show you the path to the link.  However, it will show all other information about the link target.  This includes, several lines down, the name of the link target file or directory.

### HFS+ Symbolic Links
Symbolic links are regular files that are specially marked, and contain the path of a "target" file as their data.  When using [fls](/fls/), symbolic links will show up as type <tt>l/l</tt>.  The listing above contains two examples of symbolic links.  You can find the target of the symbolic link by using [icat](/icat/) on it.

[istat](/istat/) recognizes symbolic links, and, at the end of the listing, will print the target path.
Note, that the target of a symbolic link does not need to exist in the file system.  In contrast, the target of a hard link must exist in a well-formed HFS+ file system.
