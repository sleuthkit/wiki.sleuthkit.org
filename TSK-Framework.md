---
layout: default
title: "TSK Framework"
categories:
  - "Development"

redirect_from:
  - "/index.php/TSK_Framework"
  - "/wiki/TSK_Framework"

last_modified: 2013-03-10
---

The TSK Framework provides infrastructure and modules that can be used to write automated and end-to-end digital forensics systems.  The Framework is a command line interface that uses different modules to analyze disk images. The framework contains two applications: tsk_analyzeimg and tsk_validatepipeline, which are both located in the bin folder. tsk_analyzeimg is the main executable that uses a variety of modules for file analysis. A number of modules come preloaded with the framework, and can be found in the modules folder. The other executable, tsk_validatepipeline, is used to validate whether modules can be loaded into tsk_analyzeimg. Note that the contents of this page are based on the 4.0.2 version.

## **Carving with the Framework**
By default, the Framework comes with carving disabled. In order to data carve an image with TSK Framework, a user will need to download a separate file carver such as Scalpel. Scalpel is only available as a .tar file, but can be compiled in Windows using MinGW. Using Scalpel will also require configuring tsk_validatepipeline to enable carving.

## **tsk_analyzeimg Commands**
**-c framework_config_file**

Specifies a path to the framework configuration file. If you don’t use the –c       command to specify a specific file then tsk_analyzeimg will load the default configuration file.

**-p pipeline_config_file**

The command specifies a pipeline configuration file. If the –p command isn’t used, tsk_analyzeimg will search the current directory for a valid file. The –p command will also override any pipeline configuration that was specified with the –c command.

**-d output_directory**

The –d command specifies the location where the output results will be sent. If no directory is specified, the output will be saved to the same folder as the image that was scanned.

**-v** enables verbose mode for more debugging information.

**-V** prints the version of Sleuthkit to the console.

**-L** stops printing error messages to STDERR, but still logs them.

**-C** disables all carving and runs file analysis only.

## **The framework_config file**
The framework_config file is located in the bin folder. Take a moment to open the file in a word editor and view its contents. By default the config file has three paths: one for the config directory, another for the module directory, and a third for the Scalpel directory, though this last one is commented out and will not be read when the configuration file is run. 

The path for the config_dir is #PROG_DIR#, which indicates that the program will look for the configuration file in the program directory which contains the tsk_analyzeimg application, which in this case is the bin folder.

The path for the module directory starts with the PROG_DIR folder, then steps out to the parent folder with the .. command, and finally finds the modules folder. Sleuthkit 4.0.2 comes with a selection of modules out of the box, and custom modules can be added by the user by dropping them into the modules folder and configuring the pipeline_config file to read them.

Finally, the Scalpel tool has been commented out because Scalpel does not come installed with Sleuthkit 4.0.2 and must be configured separately. After installing Scalpel, the user must remove the  comment tags and replace the ‘path’ text with the directory that contains Scalpel.

## **The pipeline.config file**
The pipeline.config file is also located in the bin folder. Take a moment to open it.

The pipeline_config file is responsible for calling the various modules that will be run when the tsk_analyzeimg command is run. As can be seen above, this pipeline_config file has two types of modules: Pipeline type FileAnalysis, and Pipeline type PostProcessing. Each of these types calls a list of modules—1, and 3-6 for FileAnalysis, and 2-4 for PostProcessing. Note that module 2 has been commented out in the FinalAnalysis section, and that module 1 has been commented out in the PostProcessing section. This means that neither of these modules will be called when tsk_analyzeimg is run, but that the user can run them by removing the  comment tags and making sure that the module is configured properly.

The user can add new modules to the module folder and then call them from the pipeline_config file. Alternatively, a user can opt not to run a module by commenting it out in the pipeline_config file.

## **Modules (descriptions taken from the README files in the docs folder)**
**Entropy Module**: this module is a file analysis module that performs an entropy calculation for the contents of a given file. Entropy shows how random the file is and can be used to detect encrypted or compressed files.

**File Type Sig Module**: This module is a file analysis module that examines the file content to determine its type (i.e. PDF, JPEG).  It does this based on file signatures in libmagic.

**Hash Calc Module**: This module is a file analysis module that calculates MD5 or SHA-1 hash values of file content.  Hash values are used to detect known files and are used to later show that file content has not changed.

**Interesting Files Module**: This module is a post-processing module that looks for files matching criteria specified in a module configuration file. This module is useful for identifying all files of a given type (based on extension) or given name or contained in a directory of a given name. See the README for help on setting up a configuration file.

**LibExif Module**: This module is a file analysis module that will check JPEG files for an exif header, then parse any found headers for metadata of interest. Any metadata of interest will be posted to the blackboard.

**RegRipper Module**: This module is a report/post-processing module that runs the RegRipper executable against the common set of Windows registry files (i.e., NTUSER, SYSTEM, SAM and SOFTWARE). This module allows you to extract information from the system's registry. The module requires that RegRipper be installed separately on your system.

**Save Interesting Files Module**: This module is a post-processing module that saves files and directories that were flagged as being interesting by the InterestingFiles module. It is used to extract the suspicious files for further analysis. For example, you could use InterestingFiles to flag all files of a given type and then use this module to save them to a local folder for manual analysis.

**Summary Report Module**: This module is a post-processing module that creates a generic HTML report based on data in the blackboard.  This report will show the results from previously run analysis modules.  This report is intended to be used by developers so that they can see what their modules are posting to the blackboard and for users who want a very generic report.  In the future, module writers will hopefully make more customized reports. This report has one table per artifact type that was found during the analysis.  Each table will have a column for each attribute.  There is a row for each artifact.

**Tsk Hash Lookup Module**: This module is a file analysis module that looks up a file's MD5 hash value in one or more hash databases that have been indexed using the Sleuth Kit's hfind tool.  Hash databases are used to identify files that are 'known' and previously seen.  Known files can be both good (such as standard OS files) or bad (such as contraband).

**Zip Extraction Module**: This module extracts the files stored inside of ZIP files. This enables you to find all possible files with evidence. Files extracted from ZIP files are scheduled so that they can later be analyzed in a file anlaysis pipeline.

## **Running tsk_analyzeimg**
Open cmd and browse to the Sleuthkit framework directory, or open the Sleuthkit bin folder in Windows explorer and shift+right click to open a new command window in the current folder. 

The user manual by Brian Carrier specifies the following format for analyzeimg:

tsk_analyzeimg [-c framework_config_file] [-p pipeline_config_file] [-d outdir] [-CLvV] image_name

As mentioned before, not entering the –c and –p commands will run the default framework and pipeline config files in the bin directory. The –C, -c, -v, and –V commands are all optional. Thus, a basic command will call tsk_analyzeimg, specify an output directory, and specify a path to the image file. The command 'tsk_analyze -d C:\new E:lab7\usbkey.image' will run tsk_analyzeimg on an image file named ‘usbkey.image’ in the E:\lab7 directory, and save the output to a new folder in the C:\ directory.

Here are some additional links on the framework:

* [Official Site](http://sleuthkit.org/sleuthkit/framework.php)
* [User's and Developer's Guide](http://www.sleuthkit.org/sleuthkit/docs/framework-docs/index.html)
* List of [TSK Framework 3rd Party Modules](/TSK-Framework-3rd-Party-Modules/) 
* Blackboard [Artifact Examples](/Artifact-Examples/)

The source code for the framework is in the same [git](/Git/) repository as TSK core.
