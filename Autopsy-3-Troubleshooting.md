---
layout: default
title: "Autopsy 3 Troubleshooting"
categories:
  - "Autopsy"

redirect_from:
  - "/index.php/Autopsy_3_Troubleshooting"
  - "/wiki/Autopsy_3_Troubleshooting"

last_modified: 2014-10-04
---

## **Autopsy launch issues.**
*** "JVM creation failed" pop up dialog shown when launching Autopsy.**

Cause: JVM is not able to allocate the requested 768m for heap size due to more memory requiring to load other native resources.

**Solution:**
reduce amount of memory allocated to jvm: 

as Administrator, edit the file: C:\Program Files (x86)\Autopsy\etc\autopsy.conf

and change the line:

default_options="--branding autopsy -J-Xms24m -J-Xmx768m -J-XX:MaxPermSize=256M -J Xverify:none"

to something like:

default_options="--branding autopsy -J-Xms24m -J-Xmx512m -J-XX:MaxPermSize=128M -J-Xverify:none"

save the file, and restart Autopsy.

If that didn't work, change the line to:

default_options="--branding autopsy"

Otherwise, the problem is in the registry.  Go to HKLM\SYSTEM\ControlSet001\Control\Session Manager\Environment and delete the _JAVA_OPTIONS key.  This is done in order to have autopsy.conf take precedence over the registry setting for the environmental variable.  You will then either have to reboot or go to the command prompt and clear the _JAVA_OPTIONS environmental variable with the command "SET _JAVA_OPTIONS=" (with no quotes).

## **Autopsy crashes after start when running within Virtual Machine, such as VMWare Fusion:**
Cause: Incompatibility between some virtual machine video drivers and java.
Solution: shut down the virtual machine, disable Video Acceleration (both 2D and 3D if available) in the virtual machine settings, restart the virtual machine, restart Autopsy.

## **Keyword Search fails to index files and search keywords**
Cause 1: Some antivirus / security products deny Solr from properly starting (examples: Dr. Web and Trend Micro OfficeScan).
Solution 1: add an exception rule for Solr or use another AV product

Cause 2: old Solr instance is already running and it was not properly shutdown, causing a conflict
Solution 2: kill old Solr instances of "java start.jar" and restart Autopsy

Cause 3: Solr instance communicates with Autopsy using a local TCP port on which Solr listens for connections.
The port is statically configured in C:\Users\USERNAME\AppData\Roaming\.autopsy\dev\config\KeywordSearch.properties
Another application on the system is already using the default TCP port 23232
Solution 3: change the default TCP port from 23232 to an available port in C:\Users\USERNAME\AppData\Roaming\.autopsy\dev\config\KeywordSearch.properties, property: IndexingServerPort
and restart Autopsy

## **UI/windows are not properly initialized**
Cause: Windows state was not properly saved during last Autopsy shutdown or platform has been upgraded and configuration is not backwards compatible.
Solution: Delete C:\Users\USERNAME\AppData\Roaming\.autopsy\config\Windows2Local and C:\Users\USERNAME\AppData\Roaming\.autopsy\config\Preferences

## ** All modules are disabled when application starts**
Cause: Modules have been disabled due to a critical error
Solution: Rename (or delete) C:\Users\USERNAME\AppData\Roaming\.autopsy\dev\config\Modules and restart Autopsy

## **Media player does not show videos (MacOSX and Linux)**
Cause: gstreamer dependency is not currently part of the development build (it is included in the Windows installer), it needs to be installed on the system
Solution: install gstreamer 0.10 in the standard user library locations, restart Autopsy

## **No physical drives detected in "Add Data Source" Wizard**
Cause: Some devices on some OSs require root/admin privileges to be discovered and opened/read
Solution: run Autopsy as Administrator

## **Some features (Timeline, Media Viewer) are not available and JavaFX initialization error is shown when Autopsy starts **
Cause: You are running an unofficial build of Autopsy and using JRE that does not contain JavaFX.  The Oracle JRE (not OpenJDK) is currently required for JavaFX support.  Download the latest JRE 7 from Oracle website and use that to launch autopsy in your development build.

## **Other issues**
We are actively working on testing and fixing known issues.  Please submit new issues at https://github.com/sleuthkit/autopsy/issues or use sleuthkit-users mailing list for the community support.
