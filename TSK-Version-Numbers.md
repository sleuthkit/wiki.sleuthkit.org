---
layout: default
title: "TSK Version Numbers"
categories:
  - "Development"

redirect_from:
  - "/index.php/TSK_Version_Numbers"
  - "/wiki/TSK_Version_Numbers"

last_modified: 2008-12-31
---

This page outlines the version numbering strategy in [TSK](/The-Sleuth-Kit/) 3.0.0 and beyond.  Prior to 3.0,0, there was little formal strategy beyond incrementing for each release and jumping ahead when big features were added.  

Starting with version 3, a 3 number version is being used: X.Y.Z. 
* X increases by 1 when a release has new major features and the Y and Z values reset to 0. 
* Y increases by 1 when a release has new minor features and the Z value resets to 0.
* Z increases by 1 when a release has bug fixes and no new features

For example, release 3.0.1 has bug fixes for the 3.0.0 release.  A 3.1.0 release has features that a 3.0.X release does not. 

Library Version: The TSK library has its own version number that is independent of the official release version. See the [Library Versioning](http://sources.redhat.com/autobook/autobook/autobook_91.html) section of the [Autoconf, Automake, and Libtool](http://sources.redhat.com/autobook/autobook/autobook_toc.html) document for the approach that we use. 

Developer's Note: A [branch](http://svn.sleuthkit.org/repos/sleuthkit/branches/) is made in the subversion repository for each major and minor release.  [Tags](http://svn.sleuthkit.org/repos/sleuthkit/tags/) are made for all releases.
