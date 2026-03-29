---
layout: default
title: "Autopsy Keyword Search Module"
categories:
  - "Autopsy"

redirect_from:
  - "/index.php/Autopsy_Keyword_Search_Module"
  - "/wiki/Autopsy_Keyword_Search_Module"

last_modified: 2014-04-22
---

Autopsy uses [Lucene SOLR](https://lucene.apache.org/solr/) for indexed keyword searching.  

# Regular Expressions
Autopsy allows you to find files using regular expressions. it uses the Java syntax: http://docs.oracle.com/javase/7/docs/api/java/util/regex/Pattern.html

# Configuration
You can find the SOLR configuration in:
* Source: KeywordSearch/release/solr/
* Installed (Windows): INSTALL_DIR\autopsy\solr

Per-case, we store the index in:
* CASE_DIR\ModuleOutput\KeywordSearch\data

# Debugging
This section contains some tips for debugging SOLR issues.   See also the [Autopsy 3 Troubleshooting](/Autopsy-3-Troubleshooting/) page for ideas.

* Connect to the admin console using 
 * http://localhost:23232/solr/admin
* You can see query results with a string  like this (replace foo with the search term):
 * http://localhost:23232/solr/coreCase/select?q=foo
* You can get a debug query with this:
 * http://localhost:23232/solr/coreCase/select?q=foo&wt=xml&debugQuery=true
* You can do a regexp test query with this (replace foo with regexp):
 * http://localhost:23232/solr/coreCase/terms?terms.regex=foo&terms=true&terms.limit=20000&terms.regex.flag=case_insensitive&terms.fl=content_ws&timeAllowed=90000&debugQuery=false
* You can get results for a specific document (based on Autopsy's assigned object ID using) (replacing 1234 with the file's ID)
 * http://localhost:23232/solr/coreCase/select?q=id:1234&wt=xml&debugQuery=true
