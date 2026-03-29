---
layout: default
title: "Blackboard"
categories:
  - "Development"

redirect_from:
  - "/index.php/Blackboard"
  - "/wiki/Blackboard"

last_modified: 2012-09-27
---

The blackboard is a storage concept that is used in both the [TSK Framework](/TSK-Framework/) and [Autopsy 3](/Autopsy/). It allows modules to communicate and post their results. 

As an example, if a module finds a web browser bookmark, it would make a "TSK_WEB_BOOKMARK" artifact on the blackboard.  The artifact would have attributes to define the URL, dates, etc. that are associated with the bookmark.  Later modules, the user interface, or reporting infrastructure could then query the blackboard for all bookmarks and they would be able to see this result.  

See the [Blackboard Page](http://sleuthkit.org/sleuthkit/docs/framework-docs/mod_bbpage.html) in the Framework guide for more details and the [Artifact Examples](/Artifact-Examples/) page for more examples.
