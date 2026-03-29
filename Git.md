---
layout: default
title: "Git"
categories:
  - "Development"

redirect_from:
  - "/index.php/Git"
  - "/wiki/Git"

last_modified: 2012-05-16
---

This page outlines how to use git to get the Sleuth Kit source code.   It assumes basic familiarity with git, but maybe not all of the nuances of working with git submodules. 

## Getting a Copy of the Source
To get your first copy of the source code, you'll use 'git clone'.  There are a few variations though depending on what you intend to do with the source. The two variables are:
* Do you want access to only the core or do you also want to build the framework
* Do you intend to make changes and submit them for inclusion or do you only want to build the source

If you want only the core sleuthkit and don't want to make changes, use:

```
git clone git://github.com/sleuthkit/sleuthkit.git
```

If you want to build the framework, you'll need to use 'git clone --recursive' to pull in git submodules (more on this later).

```
git clone --recursive git://github.com/sleuthkit/sleuthkit.git
```
  

If you want to modify the code and submit changes, then [fork](http://help.github.com/fork-a-repo/) the github repository into your own github account.  Clone that repository into a local directory and push changes to it. Once you are happy with the changes, submit a pull request using the web app (for example).  We'll review them and merge them in. 

## Framework Submodules
The framework code uses git [submodules](http://git-scm.com/book/en/Git-Tools-Submodules) to bring those modules into the framework.  For example, the module that opens ZIP files is named c_ZIPExtractionModule.  It has its own [repository](http://github.com/sleuthkit/c_ZIPExtractionModule). The sleuthkit git repository includes the ZIP extraction module using git submodules into the 'framework/TskModules/c_ZIPExtractionModule' folder.  There are several submodules in that folder. 

The sleuthkit repository knows where to find the repositories that are included as submodules and it knows about a specific commit version that it wants from that repository. This is an important concept because it causes some confusion and is different from something like svn-externals. The sleuthkit repository is configured to know about a specific commit version on each module it pulls in.  The module repository may have newer commits, but many of the git commands will only bring in the "official commit". 

### Getting Module Updates
Time has progressed since your initial clone and you want to make sure your code is up to date.  Normally, you'd use 'git pull' to get the latest versions of the code.  This will work for the core sleuth kit code, but it will not update submodules if you do the pull from  the sleuthkit repository.  

To update all of the modules, you will need to:
1. Do a 'git pull' from the sleuthkit repository to get an updated '.gitmodules' file that lists what commit version that should be used.
1. Do a 'git submodule update' to pull in the submodule versions.  Note that this will frequently make the submodule no longer be on the master branch, so ensure that you do a 'git checkout master' in the submodule before you do any changes.

Note that newer versions of git support 'git pull --recurse-submodules'.  This will pull down the full repositories for all of the submodules, but it will not change the working directory to the new versions.  You will still need to do a 'git submodule update' for that to happen. 

### Overriding Official Module Versions
The previous section outlined how to get the official versions of the submodules.  However, there could be situations where the modules that sleuthkit pulls in are not the latest and greatest. This is either because we did not feel that they are ready for prime time or we messed up and forgot to update the sleuthkit repository.  To get the latest and greatest, the following all are equivalent:
* <tt>git submodule foreach git pull</tt>  (from inside of the sleuthkit repository -- gets all modules and updates references in sleuthkit repository)
* <tt>git pull</tt>  (from inside of the submodule -- this needs to be repeated for each submodule)

Note that all of these will update the sleuthkit repository to use the version of the modules that were pulled down.  So, you will see that a git status shows that your repository has changed.

### Committing Changes to Modules
If you want to make changes to an official module (c_FooModule for this example) and submit the changes, then follow these steps:

1.  Fork the main sleuthkit repository into your github account and clone it into a local repository / directory (remember to use --recursive on the clone).

2. Fork the c_FooModule repository into your github account.  You don't need to clone this, but you will need to use the URL later when we do a push.  We'll be using this repository to store your changes. 

3. Make the changes to the module in its 'framework/TskModules/c_FooModule' location. Before you make changes, ensure that you are on the master branch using 'git checkout master'.  By default, you are not on master with submodules. 

4. Commit the module changes by doing a 'git commit' from inside of the c_FooModule directory.  

5. Push the changes to the module fork in your github account.  For example:  

```
git remote add myfork git@github.com:user_name/c_FooModule.git
git push myfork
```

You need to add the remote host only once.
 
6. The previous commit will have updated your sleuthkit repository to reflect the new commit version.  So, you'll need to also do a commit and push to your sleuthkit fork on your github account. You can see when you need to do this commit when you see this:

```
% git status
modified:   test3 (new commits)
# On branch master
# Changed but not updated:
#   (use "git add <file>..." to update what will be committed)
#   (use "git checkout -- <file>..." to discard changes in working directory)
#
#	modified:   framework/TskModules/c_FooModule (new commits)
#
```

7. Issue pull requests for both the module and sleuthkit repositories.

An alternative method of pushing the changes to your repository instead of the 'remote add' step is to update the 'pushurl' for the default 'origin' repository to point to your copy.  Something like this from inside the module:

```
git config --add remote.origin.pushurl git@github.com:user_name/c_FooModule.git
```

If you do this, then you can simply do a 'git push' from inside the module and it will send the changes to your github repository instead of the sleuthkit repository.  You can then do a pull request to get it moved over.
