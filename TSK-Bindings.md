---
layout: default
title: "TSK Bindings"
categories:
  - "Development"

redirect_from:
  - "/index.php/TSK_Bindings"
  - "/wiki/TSK_Bindings"

last_modified: 2017-12-18
---

TSK comes with a C/C++ library.  if you want to use it in programs written in other languages, this is the page for you. It contains information for doing that.  

The first thing to point out is that the C/C++ code can generate a SQLite database.  One of the motivations for this feature is that you can then open the database from another language and perform queries on it.  This reduces the number of language-specific bindings that need to occur.  Because the database contains only metadata though, bindings are still needed to copy file content.

Here are a list of known bindings (in alphabetical order):
* [TSK Java Bindings](/TSK-Java-Bindings/)
* .NET: The [sleuthkit-sharp](http://sleuthkitsharp.codeplex.com) project contains .NET bindings.
* Python: The [pytsk](https://github.com/py4n6/pytsk) project contains Python bindings.
