---
layout: default
title: "Autopsy 3rd Party Modules"
categories:
  - "Autopsy"

redirect_from:
  - "/index.php/Autopsy_3rd_Party_Modules"
  - "/wiki/Autopsy_3rd_Party_Modules"

last_modified: 2019-02-15
---

**NOTE**: The list of Autopsy 3rd party modules has been moved to a  [github repository](https://github.com/sleuthkit/autopsy_addon_modules).  You can either browse the repository or download it, which includes some of the modules. 

Developers: to have your module listed, please issue a pull request based on the instructions [here](https://github.com/sleuthkit/autopsy_addon_modules/tree/master/DocsForDevelopers). 

The rest of the page is listed here temporarily in case not everything was moved to the github site. 

---

**LEGACY MATERIAL**

This page will list the third party modules that have been written for [Autopsy](/Autopsy/). Autopsy comes with a set of modules, but other developers are encouraged go write modules instead of stand-alone tools. 

Autopsy has many new frameworks and as more modules are written, this page will obviously get longer.

# Ingest Modules
Ingest modules in Autopsy run on each data source and file that are added to the case.  These modules are responsible for the big data analysis where they extract data from specific files and put the results in the embedded database. 

## Python Plugins
* Description: These are plugins that were developed for various artifacts which include:
<blockquote>Amazon Echosystem Parser, CCM RecentlyUsedApps, Cuckoo, File History, Jump_List_AD, MacFSEvents, MacOSX Recent, MacOSX Safari, Plist Parser, SAM Parse, Parse Shellbags, Parse SQLite Databases, Parse SQLite Deleted Records, Parse USNJ, Plaso, Process Amcache, Process EVTX, Process EVTX By EventID, Process Extract VSS, Process Prefetch Files, Process SRUDB, Shimcache Parser, Thumbcache Parser, Thumbs.db Parser, Volatility, Webcache, Windows Internals</blockquote>
* Author: Mark McKinnon
* Minimum Autopsy Version: 4.1.0
* Source URL: https://github.com/markmckinnon/Autopsy-Plugins
* Executable Installer: https://github.com/markmckinnon/Autopsy-Plugins/releases/download/v1.0/Autopsy_Python_Plugins.exe
* License: GNU General Public License Version 3.
* Installation Instructions:  Execute the Autopsy_Python_Plugins.exe file or download the Autopsy-plugins repository and unzip the files into the Python Module directory.

## Prefetch Parser
* Description: This module will process thru all the prefetch files in the C:\Windows\Prefetch directory and parse out the information in them.  It works on the following windows versions XP, Vista/7, 8/8.1 and 10.  Winner of the OSDFCon 2015 Python Module challenge.
* Author: Mark McKinnon
* Minimum Autopsy version: 3.1.3 for V3, 4.0.0 for V4, 4.1.0 for V41
* Source URL: https://github.com/markmckinnon/Autopsy-Plugins
* License: GNU General Public License Version 3.
* Installation Instructions:  Unzip the files into the Python Module directory.

## sdhash (Autopsy AHBM)
* Description: This module allows you to use sdhash to perform fuzzy hash matching. The investigator can match files against other files or sdhash reference sets during ingest, or search for similar files from the directory viewer or search results after ingest.  Released as part of OSDFCon 2013 Development contest.    

* Author: Petter Bjelland  

* Minimum Autopsy version: 3.0.7  

* Source URL: https://github.com/pcbje/autopsy-ahbm  

* Release Download: https://github.com/pcbje/autopsy-ahbm/releases  

* License: Apache 2.0  

* The video presentation is also uploaded to youtube: http://youtu.be/GBmZRufH_3o  

## SmutDetect Module
* Scans JPG, BMP, PNG & GIF files (selection of files based on file signatures) for pixels with skin tone and computes file percentage. Files are tagged with skin-tone percentage in increments of 10 to allow a categorised view of thumbnails.
* Author: Rajmund Witt
* Source URL: https://github.com/rajwitt/SmutDetect4Autopsy
* Release and Documentation URL: http://www.smutdetect.co.uk
* License: GPL 3.0
* Since Release 1.0.2 works with Autopsy 3.1.1

## Windows Registry Ingest Module
* Description: An ingest module that extracts Registry keys and values into derived directories and files so that they show up as nodes in the directory tree.  First place winner in the OSDFCon 2013 challenge.  

* Author: Willi Ballenthin  

* Minimum version of Autopsy required: 3.0.7  

* Source URL: https://github.com/williballenthin/Autopsy-WindowsRegistryIngestModule/  

* Release Download: https://github.com/williballenthin/Autopsy-WindowsRegistryIngestModule/tree/master/precompiled  

* License of source code: Apache 2

## Child Exploitation Hashset Modules
* Description: Hash lookup modules that integrate with [ProjectVic](http://www.projectvic.org) and C4All databases.  These allow you to use Autopsy in child exploitation investigations and leverage hashsets of pre-categorized images. 
* Author: Basis Technology
* Minimum Autopsy version: 3.1.0  

* Release Download: http://www.basistech.com/digital-forensics/autopsy/le-bundle/  

* License: Closed source

## VirusTotal Online Checker
* Description: Autopsy File Ingest Module to check file hashes against online VirusTotal Database
* Author: Mathias Vetsch, Luca Tännler
* Minimum Autopsy version: 4.1.0
* Source URL: https://github.com/mvetsch/VirusTotalOnlineChecker
* Release Download: http://www.nitcorn.ch/org-sleuthkit-autopsy-modules-virustotalonlinecheck.nbm
* License: GNU GENERAL PUBLIC LICENSE

## Copy-Move Module Package
* Description: A module package containing a File Ingest Module and its corresponding Data Content Viewer. Allows the user to identify Copy-Move forgeries within images in the datasource. Please read the readme before using the package.
* Author: Tobias Maushammer
* Minimum Autopsy version: 4.1.0
* Source URL: https://github.com/LoWang123/CopyMoveModulePackage
* Release Download: https://github.com/LoWang123/CopyMoveModulePackage/blob/master/de-fau-copymoveforgerydetection.nbm
* License: The MIT License (MIT)

## Image Fingerprint Module Package
* Description: A module package containing a File Ingest Module and its corresponding Data Content Viewers. Allows the user to create different perceptual hashes as fingerprints from images in the datasource. This also creates an additional database, which is managed from the expanded options menu of the ingest module. Images can be compared to images in the database. Please read the readme before using the package.
* Author: Tobias Maushammer
* Minimum Autopsy version: 4.1.0
* Source URL: https://github.com/LoWang123/ImageFingerprintModulePackage
* Release Download: https://github.com/LoWang123/ImageFingerprintModulePackage/blob/master/de-fau-imagefingerprintcomparison-modules.nbm
* License: The MIT License (MIT)

## Other Python Plugins
* Description: These are plugins that were developed for various artifacts which include:
  * Connected iPhones (Connected iPhone Analyzer)
  * Skype (Skype Analyzer)
  * IE Tiles
  * Google Drive
  * Google Chrome Saved Passwords Identifier
  * Windows Communication App Contact Extractor

* Author: Tom Van der Mussele
* Minimum (tested) Autopsy Version: 4.3.0
* Source URL: https://github.com/tomvandermussele/autopsy-plugins
* License: GNU General Public License Version 3.
* Installation Instructions:  Download the python module you want and place it in the %appdata%\Autopsy\Python_modules\ directory.

## Microsoft Office Telemetry File Parser
* Description: This module will process thru MS Office telemetry .tbl files in a datasource, parse them, and add corresponding blackboard artifacts.
* Author: Sam Koffman
* Minimum Autopsy version: 4.8.0
* Source URL: https://github.com/MadScientistAssociation/Autopsy-MSOT
* License: MIT License
* Installation Instructions:  Unzip the files into the Python module directory.

# Data Content Viewer Modules
Content viewer modules in Autopsy display a single file in some way. The standard application comes with viewers for hex, strings, and pictures.  These add-on modules allow you to view files in other ways.  They are available in the lower right hand corner of Autopsy. 

## Video Triage
* Description:  Analyzes video files and displays a series of images so that you can get a basic idea of what the video contains without viewing the entire thing.   

* Author: Basis Technology  

* Minimum Autopsy version: 3.0.7  

* Release Download: http://www.basistech.com/digital-forensics/autopsy/video-triage/  

* License: Closed source

## Windows Registry Content Viewer
* Description: Content viewer that analyzes a registry hive and allows you to navigate the tree and its key and value pairs.  Functions something like Regedit.exe.  Winner of the OSDFCon 2013 challenge.  

* Author: Willi Ballenthin  

* Minimum version of Autopsy required: 3.0.7  

* Source URL:  https://github.com/williballenthin/Autopsy-WindowsRegistryContentViewer  

* Release Download: https://github.com/williballenthin/Autopsy-WindowsRegistryContentViewer/blob/master/precompiled/com-williballenthin-autopsy-wrcv-3.0.7-20131001.nbm  

* License of source code: Apache 2

## Multi Content Viewer
* Description: Content viewer for dozens of file types: html, pdf, eml, emlx, rtf, doc, docx, xls, xlsx, ppt, pptx, odt, ods, odp, wps, wpd, sxw, eps, dbf, csv, tif, emf, wmf, odg, pcx, pbm, svg, pict, vsd, psd, cdr, dxf, and more. Also highlights and enables navigation through keyword hits on the rendered preview.  

* Author: Luis Filipe Nassif  

* Minimum version of Autopsy required: 3.1  

* Source URL:  https://github.com/lfcnassif/MultiContentViewer  

* Release Download: https://github.com/lfcnassif/MultiContentViewer/releases  

* License of source code: LGPL v3.0

# Report Modules
Report modules in Autopsy allow you to make final reports after your investigation is over. Standard modules in Autopsy include HTML and Excel. 

## FEA – Forensics Enhanced Analysis
* Description:  FEA comprises three separate tools: i) for email filtering and validation, ii) for credit card number validation and iii) for Bitcoin wallet addresses and private key search and validation.   

* Author: João Mota, Miguel Frade, Patrício Domingues  

* Minimum Autopsy version: 3.0.7  

* Source Code: https://bitbucket.org/psychodeath/fea-forensics-enhanced-analysis
* Video: https://vimeo.com/237483225
* License: Open source

## ForensicExpertWitnessReport
* Description:  Adds tagged evidence into structured and styled tables automatically and directly inside a forensic expert witness report, whilst coming with three pre-existing forensic expert witness report templates to choose from.    

* Author: Chris Wipat  

* Minimum Autopsy version: 3.0.7  

* Source URL: https://github.com/chriswipat/forensic_expert_witness_report_module  

* Release Download: https://github.com/chriswipat/forensic_expert_witness_report_module/releases/download/v1.0/ForensicExpertWitnessReport.nbm  

* License: GNU General Public License Version 3  

* Installation Instructions: https://github.com/chriswipat/forensic_expert_witness_report_module/blob/master/README.md

# Other
These modules are more free form and do not use one of the more structured extension points.

## Cyber Triage
* Description: Incident Response tool that automates collection and analysis to determine if a host is compromised or not. Can analyze live or dead systems.   

* Author: Basis Technology  

* Minimum version of Autopsy required: 3.1  

* Source URL:  http://www.cybertriage.com  

* Release Download: http://www.cybertriage.com  

* License of source code: Commercial
