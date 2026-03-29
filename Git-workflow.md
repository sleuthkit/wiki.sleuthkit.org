---
layout: default
title: "Git workflow"
categories:
  - "Development"

redirect_from:
  - "/index.php/Git_workflow"
  - "/wiki/Git_workflow"

last_modified: 2015-02-04
---

We are using a variation of the [gitflow](http://nvie.com/posts/a-successful-git-branching-model/) git branching model for The Sleuth Kit and Autopsy.  The differences to it are listed in the section below. This page contains a concise list of steps to do for various things. Much of it is identical to the more explanatory gitflow page. 

# Cheat Sheet
## Setting the Public Repo as a remote
This makes it easier to document how to merge in updates to develop into a feature branch.  We'll call it 'upstream'.

If you are in an Autopsy repo:

```
git remote add upstream https://github.com/sleuthkit/autopsy.git
```

If you are in a The Sleuth Kit repo:

```
git remote add upstream https://github.com/sleuthkit/sleuthkit.git
```

## Adding a Feature
1. Make a feature branch from develop on your fork:

```
$ git checkout develop
$ git fetch upstream
$ git merge upstream/develop
$ git checkout -b myfeature develop
```

2. Make the code changes to the branch and commit the changes.

3. Merge in the latest develop (in case changes were made to it since you started your feature branch.

```
$ git fetch upstream
$ git merge upstream/develop
```

4. Upload to your repo.

```
$ git push origin myfeature
```

5. Make a [pull request](https://help.github.com/articles/using-pull-requests) from myfeature to develop on the public repo. 

## Making A Release Branch
Created before we do the final release.

```
$ git checkout -b release-1.2 develop
[EDIT VERSION NUMBER]
$ git commit -a -m "Updated version number"
$ git push origin release-1.2
```

## Making Changes to Release Branch
Make commits to the release branch AND merge them into develop.  It is the responsibility of the developer at the time of the commits to merge them into develop.  This makes it easier than reconciling conflicts afterwards. 

## Finishing the Release Branch
Merges release branch to master

```
$ git checkout master
$ git merge --no-ff release-1.2
$ git tag -a 1.2
```

# Differences from gitflow
- We will have multiple develop branches if we are working on backward incompatible API changes on two major versions.  I.e. develop could be on the 3.1 version of Autopsy and we could have develop-3.2 with changes that are for 3.2 while we are also working on some minor changes to 3.1. 

- The developer needs to push to relevant branches at the same time (release and develop or develop and develop-3.2) and not rely on merging later.  The developer has the most context about how to resolve the conflicts.
