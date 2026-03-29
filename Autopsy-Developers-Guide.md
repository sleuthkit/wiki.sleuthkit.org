---
layout: default
title: "Autopsy Developer's Guide"
categories:
  - "Autopsy"

redirect_from:
  - "/index.php/Autopsy_Developer's_Guide"
  - "/wiki/Autopsy_Developer's_Guide"

last_modified: 2015-01-27
---

This page contains technical information on developing code for [Autopsy](/Autopsy/). 

There are two types of development that can occur with Autopsy:
* Development of Plug-in modules that you distribute
* Development of core infrastructure and the Autopsy framework

If you are looking for ideas on how you can contribute, then you may want to refer to the feature request and bug [trackers](/Trackers/).  They contain ideas that people have for the tools or bugs that need to be fixed.

# Module Development
Autopsy was developed to be a platform for plug-in modules.  The [Developer's Guide](http://www.sleuthkit.org/autopsy/docs/api-docs/) contains the API docs and information on how to write modules. When you create a module, add it to the list of [Autopsy 3rd Party Modules](/Autopsy-3rd-Party-Modules/). 

# Platform Development
* The [Developer Guidelines](/Developer-Guidelines/) defines how code and patches can be submitted and incorporated into the sleuthkit.org projects. 
* The [sleuthkit-developers](/sleuthkit-developers/) list exists to discuss the development of the sleuthkit.org tools.  Subscribe to ask and answer questions. 
* If you want to contribute documentation, then refer to the [Support](http://www.sleuthkit.org/support.php) page. 

The source code is stored in a [github](http://www.github.com/) repository. You can get the latest source tree from http://github.com/sleuthkit/autopsy. 

## Autopsy 3 Topics
* [Autopsy 3 Logging and Error Checking](/Autopsy-3-Logging-and-Error-Checking/) is a reference for how errors and log messages are made.
* [Autopsy 3 Module Versions](/Autopsy-3-Module-Versions/) is a reference on the versioning scheme of the internal modules.
* Adding extensions to the [Autopsy File Extension Mismatch Module](/Autopsy-File-Extension-Mismatch-Module/)
* Debugging the [Autopsy Keyword Search Module](/Autopsy-Keyword-Search-Module/)
* [Adding Artifacts and Attributes](/Adding-Artifacts-and-Attributes/) to the official code base
