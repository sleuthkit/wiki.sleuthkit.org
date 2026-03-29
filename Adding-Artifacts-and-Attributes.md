---
layout: default
title: "Adding Artifacts and Attributes"
categories:
  - "Development"

redirect_from:
  - "/index.php/Adding_Artifacts_and_Attributes"
  - "/wiki/Adding_Artifacts_and_Attributes"

last_modified: 2015-01-29
---

This page outlines the steps that you need to undertake to add a new artifact or attribute to TSK/Autopsy.  Follow these before making a pull request. 

* **TSK:**
  * C++ Framework Code:
    * Add to TSK_ARTIFACT_TYPE or TSK_ATTRIBUTE_TYPE enums in framework/tsk/framework/services/TskBlackboard.h
    * Update the appropriate map in framework/tsk/framework/services/TskBlackboard.cpp
  * Java Code:
    * Add Artifacts to:
      * bindings/java/src/org/sleuthkit/datamodel/BlackboardArtifact.java
    * Add Attributes to:
      * bindings/java/src/org/sleuthkit/datamodel/BlackboardAttribute.java
      * Update BlackboardAttribute.getDisplayString() if the attribute needs any special display formatting.
    * For either, you will need to update the bundle file with the strings:
      * bindings/java/src/org/sleuthkit/datamodel/Bundle.properties

* **Autopsy:**
  * Update report code to make artifact visible in table:
    * Core/src/org/sleuthkit/autopsy/report/ReportGenerator.java
      * getArtifactTableColumnHeaders()
      * getOrderedRowDataAsStrings()
  * (Optional) For new artifacts - create a custom icon for the HTML report
    * Core/src/org/sleuthkit/autopsy/report/ReportHTML.java
      * useDataTypeIcon()
    * Icons stored in Core/src/org/sleuthkit/autopsy/report/images

* **Wiki:**
  * Add a description of the new artifact or attribute to [Artifact Examples](/Artifact-Examples/)
