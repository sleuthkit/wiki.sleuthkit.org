---
layout: default
title: "Developer Guidelines"
categories:
  - "Development"

redirect_from:
  - "/index.php/Developer_Guidelines"
  - "/wiki/Developer_Guidelines"

last_modified: 2014-08-11
---

This page contains the guidelines for developing code for [The Sleuth Kit](/The-Sleuth-Kit/) and [Autopsy](/Autopsy/).  These guidelines are not about the technical designs of the tools, rather they are about how code is contributed and merged in. Note that this document is a work in progress as the process is officially defined. 

# Communications
The [Sleuth Kit Developers](http://lists.sourceforge.net/lists/listinfo/sleuthkit-developers) e-mail list is the official communication forum for TSK and Autopsy development. Subscribe to participate in the development process. 

There are also [trackers](/Trackers/) on SourceForge and github to keep track of bugs and feature requests. 

# Source Code Branches
We are currently using a branching model based on [gitflow](http://nvie.com/posts/a-successful-git-branching-model/).  We have thoughts about using a variation of this in the near future, but it is basically what we are doing now.  You can find a cheatsheet on the [git workflow](/Git-workflow/) page. 

The basic take away of it is:
* master branch is the last stable release
* develop branch is where development is going on

Our thought is to make some slight variations on this, namely that:
* the develop branch will be called something like 'develop-X.Y' that signals the version that is being developed on that branch. 

# Submitting Patches / Code
All of the development is now done from our [github](http://www.github.com/sleuthkit/) projects.   To submit code to one of the projects, you will need to create a [pull request](http://help.github.com/articles/using-pull-requests).  The previously linked to page outlines how to generate a pull request, but the high-level overview is to:
* Create a github account
* Create a fork of sleuthkit, Autopsy, or another project into your account
* Clone the forked repo.
* Change to the develop branch
`git checkout develop`
* Create a branch based on the develop branch for the feature that you want to develop (i.e. a feature branch)
`git checkout -b feature_name`
* Make changes to the code in that branch and commit them
* Push that branch to your fork on github.com
`git push origin feature_name`
* Create a pull request for the feature branch to the develop branch.  Review the diff to make sure it is what you want. By default, it will be against the master branch and not develop.

The patches and code contributions will be reviewed and incorporated into the main development if they are approved. It is also helpful to submit test images and test cases that can be used to test the new code. 

Code submissions should follow the error handling, Unicode, and other conventions of the specific tool.  A more detailed list of tool-specific guidelines is being developed.

# Code Acceptance
Currently, these tools have a [Benevolent Dictator](http://producingoss.com/html-chunk/social-infrastructure.html#benevolent-dictator) model for incorporating code into the official distribution.  As more developers get involved, this can change. Acceptance is based on code quality and completeness.
