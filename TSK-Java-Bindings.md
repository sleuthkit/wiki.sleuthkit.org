---
layout: default
title: "TSK Java Bindings"
categories:
  - "Development"

redirect_from:
  - "/index.php/TSK_Java_Bindings"
  - "/wiki/TSK_Java_Bindings"

last_modified: 2012-06-11
---

The Java bindings for [TSK](/The-Sleuth-Kit/) are in the official github repository as of version 4.0 in the ['bindings/java'](https://github.com/sleuthkit/sleuthkit/tree/master/bindings/java)(/https-githubcom-sleuthkit-sleuthkit-tree-master-bindings-java-bindings-java/) directory.  They populate the SQLite database with the file system metadata and then create Java classes that encapsulate the data.   These are used for [Autopsy 3](/Autopsy/). 

Refer to the [README.txt](https://github.com/sleuthkit/sleuthkit/blob/master/bindings/java/README.txt)(/https-githubcom-sleuthkit-sleuthkit-blob-master-bindings-java-READMEtxt-READMEtxt/) file for building and using the bindings.  The API Docs (and eventual Developer's Guide) are available [online](http://sleuthkit.org/sleuthkit/docs/jni-docs). 

# Developer Notes
This section contains some basic information on the Java/JNI code if you want to modify it.

* The SleuthkitJNI class has the static Java methods that refer to the native C++ methods.
* The naming convention thus far has been to end the native methods with "Nat" (loadDbNat(), for example). 
* When you make changes to the native method APIs, you can automatically make a new ".h" file by running the "jni" target in the "build.xml" ANT file.  It will place the .h file in the tsk_jni folder.
