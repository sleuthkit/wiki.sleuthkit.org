---
layout: default
title: "NTFS File Recovery"
categories:
  - "File Systems"

redirect_from:
  - "/index.php/NTFS_File_Recovery"
  - "/wiki/NTFS_File_Recovery"

last_modified: 2010-09-18
---

This page outlines NTFS file recovery in [TSK](/The-Sleuth-Kit/). 

# NTFS File Structures (High-level)
## Allocated Files
This section describes (at a very high level) how [NTFS](/NTFS/) stores files.  All files and directories store their metadata in a Master File Table (MFT) entry.  NTFS directories have a tree structure that stores the name of its files and subdirectories.  The location of the tree can be found from the MFT entry (in fact, part of the tree is stored in the MFT entry).  The tree structure is kept in a sorted order.  Here is an overly simplified example.

```
bird.txt
          /    \
         /      \
     ant.txt   cat.txt
```

All file names that are before "bird.txt" alphabetically are stored to the left of it and all names after "bird.txt" are to the right of it. 

Each entry in the tree points to the MFT entry for the named file. Here is an example of the relationship between the name, MFT entry, and clusters.

```
cat.txt -> MFT Entry 314 -> Cluster 539
```

Each MFT entry also stores the [Metadata address](/Metadata-Address/) of the parent directory's MFT entry.  For example, the file <tt>C:\animals\cat.txt</tt> has a parent directory of <tt>C:\animals</tt>.  The parent directory of <tt>C:\animals</tt> is the root directory, which is <tt>C:\</tt>. 

## Deleted Files
When a file is deleted, several things occur. The MFT entry has a flag that is set to "unused" and the bitmap for the MFT entries is updated. The bitmap for the clusters is also updated, if needed. 

The more complex step is removal from the name tree.  The actual structure is much more complex than previously described. Each node in the tree has several names in it, not only one name. There are rules about the minimum and maximum numbers of names that can exist in each node. If the name being removed is at the end of the node, then it is marked as unused and it may remain there. If the node now does not have enough entries in it, then entries from nodes below it could be moved up and overwrite the deleted file name. If the name is in the middle of a node, then other names in the node will be shifted over and will overwrite the deleted name. In general, the file name is frequently overwritten when a file is deleted. 

# Finding Deleted Files
With most file systems, you can find deleted files by looking in the directory tree for deleted names.  With NTFS however, you will miss most file names because of the tree resorting.  Further, because the tree gets resorted frequently, the unused space at the end of a tree node (where we would expect to find the names of deleted files) may contain information about files that are still allocated (but whose name has been moved to a different node in the tree).  

Another technique exists though to find deleted files.  To find the deleted files for a specific parent directory, the MFT entry of the directory is determined and the MFT is scanned to find all unallocated entries that reference that directory as its parent directory. The file name is stored in the MFT entry so the full path can be determined using the path of the parent directory and the name stored in the file's MFT entry. 

# TSK Tools
Starting with TSK 3.0.0, the <tt>[fls](/Fls/)</tt> tool will combine both of the previously mentioned recovery techniques. It will go through the tree for a given directory and display the allocated names.  It will hide names that are marked as unallocated if they also exist as allocated names. <tt>fls</tt> will then go through the MFT to find unallocated entries that point back to the given directory. You will be able to tell how a deleted file was displayed because the <tt>fls</tt> output lists the file type as described in both the file name and MFT data structures.  Deleted files that were found by scanning the MFT will have a "-" in the place for the file name type.  For example, "-/r" instead of "r/r" for a regular file. 

In versions of TSK prior to v3, <tt>fls</tt> would process the directory tree and display all file names (including duplicates of names that were already found as being allocated - it will show these as having a "realloc" status). To find the deleted files that no longer have a file name, the <tt>[ifind](/Ifind/) -p</tt> tool must be used and it would process the MFT to look for entries that refer to a specific parent directory. 

# References
See also [Sleuth Kit Informer #16](http://www.sleuthkit.org/informer/sleuthkit-informer-16.html#ntfs)
