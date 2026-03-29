---
layout: default
title: "Autopsy 3 Logging and Error Checking"
categories:
  - "Autopsy"

redirect_from:
  - "/index.php/Autopsy_3_Logging_and_Error_Checking"
  - "/wiki/Autopsy_3_Logging_and_Error_Checking"

last_modified: 2012-09-29
---

This page outlines the developer guidelines for consistent logging and error checking / handling. 

NOTE: This should be moved to the api-docs / doxygen docs.

# Logging
Logs are created at the user-level in Autopsy.  NetBeans provides a handler that writes log messages to the file $userdir$/var/logs/messages.log. That message log is also supplemented with custom Autopsy log files (in the same directory -- please check the Log file section below), which log additional information, augmented with timestamps. The path to the userdir directory can be found in the About window of Autopsy. It creates a new log file for each run, and also keeps the logs from the previous two runs.

Logging in Autopsy is done using the logging facility org.sleuthkit.autopsy.coreutils.Logger.  Always make sure to use that logger.  The autopsy logger is a wrapper over java.util.logging.Logger and follows the same API and conventions, but it also customizes the logging behavior.

To use the Autopsy logger, import it first into the namespace:

`
import org.sleuthkit.autopsy.coreutils.Logger;

import java.util.logging.Level;

`

Get a Logger instance and log a message with it:

`
    Logger logger = Logger.getLogger(CLASS.class.getName()); // Get an appropriate logger for the class CLASS

    logger.log(Level.WARNING, "LOG MESSAGE", EXCEPTION); // Make a new record with level WARNING, containing the message LOG MESSAGE 

    logger.log(Level.WARNING, "LOG MESSAGE", EXCEPTION); // Make a new record with level WARNING, containing the message LOG MESSAGE and the exception EXCEPTION
`

Along with the appropriate imports from java.util.logging that is all that's needed for a class to use the logging module.

Our use of the levels include:
* SEVERE: errors that critically affect the application
* WARNING: errors that might be recovered from
* INFO: User actions that could be useful for debugging 
* FINE: case lifecycle events

Descriptions of the meaning for each logging level can be found in the java.util.logging JavaDoc - <http://download.oracle.com/javase/6/docs/api/java/util/logging/Level.html>(/http-downloadoraclecom-javase-6-docs-api-java-util-logging-Levelhtml/)

Note: By virtue of being initialized from a module, the autopsy.log file may be miss some log statements that occur immediately after Autopsy is launched, when the NetBeans platform is loading modules. The messages.log file is created by NetBeans platform internals, and will contain all startup information.

 
# Error handling
Autopsy uses exceptions for error handling.  The exception should be caught and handled by the process that initiated the request and should try to recover from them (if possible. For example, the DataModel module is simply a NetBeans module around the TSK Datamodel JAR file.  It does not directly initiate any requests and therefore passes all of its exceptions up to the other module that used the DataModel module to get access to the image data. 

When an exception is caught, it should usually be logged and a message box can be displayed.  To automatically display the message boxes, a log handler is registered in Autopsy to display an error message box for every log record that has a level of WARNING or greater and an exception is passed in as an argument.

# Log files
Autopsy writes several log files that are located in Autopsy user directory root (the same as user.dir property or Places.getUserDirectory() ).
The log files can be useful to users (to submit bug reports) and developers (to test and debug code).

The effective location is:
* on a development build: in autopsy source root directory: build/testuserdir
* on a release build: ${USER_HOME}/.autopsy.  On Windows, it is c:/Users/${USERNAME}/AppData/Roaming/.autopsy

Currently Autopsy uses 3 log files enabled by default.  They use the java.util.Logger infrastructure. 
These log file rotate and have a number appended to it (the most recent log ends with .0)

* $user.dir/var/log/autopsy.log - the main Autopsy log file, containing all exceptions (no stack trace), warnings, errors and info messages from all modules. 
* $user.dir/var/log/autopsy_traces.log - same as autopsy.log, but also containing exception stack traces. 
* $user.dir/var/log/autopsy_actions.log - contains user actions as they were triggered by the user.
* $user.dir/var/log/tika.log - contains detailed errors / exceptions from Tika text extraction of individual files, including exception stack trace. High level Tika error messages are still logged in the main autopsy.log file, however details are in tika.log
* $user.dir/var/log/solr.log - contains detailed info and error messages from Solr indexer and searcher.  The file is populated by redirecting stdout and stderr from the Solr process.  In the development build, the stream is flushed after every message (for ease of debugging).

There is a log file disabled by default:
* $user.dir/sleuthkit.txt - populated by TSK backend as image is being added to the case.  The log can be enabled by clicking "Active verbose logging" in Autopsy Help / About menu.  The generated file is very large, therefore verbose logging should be disabled in normal operation. The log file is very useful for debugging TSK related issues. It does not rotate as the other Autopsy log files.
