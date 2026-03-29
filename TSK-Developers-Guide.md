---
layout: default
title: "TSK Developer's Guide"
categories:
  - "Development"

redirect_from:
  - "/index.php/Developer's_Guide"
  - "/index.php/TSK_Developer's_Guide"
  - "/wiki/Developer's_Guide"
  - "/wiki/TSK_Developer's_Guide"

last_modified: 2020-02-14
---

This page contains technical information on developing code for [TSK](/The-Sleuth-Kit/). If you are looking for a guide that helps to incorporate the TSK library into your tools, then refer to <http://sleuthkit.org/sleuthkit/docs/api-docs/latest/>. 

This page is a work in progress and more information will be posted.  Here are some starting points. 
* The [Developer Guidelines](/Developer-Guidelines/) define how code and patches can be submitted and incorporated into the distribution. 
* The <https://sourceforge.net/projects/sleuthkit/lists/sleuthkit-developers> list and <https://forum.sleuthkit.org> exist to discuss the development of the tools.  Subscribe, ask, and answer questions. 
* If you want to contribute documentation, then refer to the [Support](http://www.sleuthkit.org/support.php) page. 

# What To Do?
If you are looking for ideas on how you can contribute, then you may want to refer to the feature request and bug [trackers](/Trackers/).  They contain ideas that people have for the tools or bugs that need to be fixed.

# Technical Details
The source code is stored in a [github](http://github.org/) repository. You can get the latest source tree from <https://github.com/sleuthkit/sleuthkit>(https://github.com/sleuthkit/sleuthkit).  The latest released code is in the <tt>master</tt> branch.  There are branches for the major release branches (3.1, 3.2, etc.) and tags for each release. The github repository contains the history from the previous subversion repository.  Note that the previous subversion repository was created right before the 3.0.0 release and does not contain the previous CVS history.

# Coding Standards
Here are the standards that I have been trying to maintain in TSK for the past few years.  

* Spaces instead of tabs
* The C code uses GNU indent to handle the formatting (just do a 'make indent' in the directory).
* I have no good indenting solution for C++ code (GNU indent makes UGLY C++ code)
* C++ fields start with "m_"
* Arguments to C/C++ functions/methods start with "a_". 
* C names use underscores
* C structs are all upper case
* C variable names start with lower case
* C++ names use camel case
* C++ Classes start with a capital letter
* C++ objects start with a lower case letter

Not all of TSK is up to date on these standards as I have been updating them as I fix bugs and such.

# Design Docs
* [Design Documents](/Design-Documents/)
