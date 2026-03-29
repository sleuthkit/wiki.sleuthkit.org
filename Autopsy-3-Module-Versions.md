---
layout: default
title: "Autopsy 3 Module Versions"
categories:
  - "Autopsy"

redirect_from:
  - "/index.php/Autopsy_3_Module_Versions"
  - "/wiki/Autopsy_3_Module_Versions"

last_modified: 2013-07-26
---

# Basics
This page outlines how modules inside of Autopsy are numbered.  Note that these version numbers are different than the ones you see on the download page (i.e. 3.0.1). These are hidden from normal users and are used to make sure that modules are compatible. 

They are derived from NetBeans (http://wiki.netbeans.org/VersioningPolicy). 

Each module has three version numbers:
* Major Version is a single integer and increments when a backward incompatible change occurs.
* Implementation Version is a single integer and increments every release with code changes.  This number never resets. 
* Specification Version has a form of 1.2 and is comprised of the Major Version and the second number is incremented each time there is a backwards compatible change to the API.  This number increments somehow each time there is an API change. 

# Example Scenarios
## Creating a module
Open up its properties and go to API Versioning .

Give it a Major Release Version of 1, a Specification Version of 1.0, and an Implementation Version of 1 (If its a beta, you can start with 0, 0.0 , and 1).

Check Append Implementation Versions Automatically .

## No changes made to a module
No versioning actions are needed.

## No API changes (only internal changes)
Such as bug fixes or other internal implementation changes that don't affect the behavior of the public module API.
* Major stays the same
* Implementation Version increments (ex: 1 becomes 2)
* Specification stays the same. 

## Backwards compatible API changes
Such as adding new methods.
* Major stays the same
* Implementation Version increments (ex: 1 becomes 2)
* Increment the second number in the Specification Version (ex: 1.3 becomes 1.4).

## Incompatible API changes
Such as removing or changing existing methods or changing their behavior.
* Major increments (ex: 1 becomes 2)
* Implementation Version increments (ex: 1 becomes 2)
* Update the Specification Version to match the Major Release Version (ex: 1.3 becomes 2.0).
