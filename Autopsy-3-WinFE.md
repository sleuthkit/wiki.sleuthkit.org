---
layout: default
title: "Autopsy 3 WinFE"
categories:
  - "Autopsy"

redirect_from:
  - "/index.php/Autopsy_3_WinFE"
  - "/wiki/Autopsy_3_WinFE"

last_modified: 2013-06-13
---

[Windows Forensics Environment](http://winfe.wordpress.com/) (WinFE) is a bootable operating system environment that can be used for forensic examinations.  It provides a live boot environment that allows you to examine a suspect computer in a forensically sound way.  Autopsy 3 works out of the box in [WinFE Lite](http://www.ramsdens.org.uk/), which is a build of WinFE.  

Due to some dependencies in Autopsy that aren’t available in the WinFE Lite environment, not all functionality exists. Specifically, you will be unable to view videos or open zip files.  

Here are the instructions for installing and running Autopsy 3 in WinFE Lite: 

1. Install [Autopsy 3](http://sleuthkit.org/autopsy) onto your forensics machine running Windows.
1. [Download](http://www.ramsdens.org.uk/download.html) the WinFE Lite build and put it in it's own folder on your forensics machine. We’ll call this folder {WINFE}
1. Copy the Autopsy 3 folder (in C:\Program Files (x86)\Autopsy by default) from your forensics machine into the "{WINFE}\X\Program Files" directory.
1. Double click to run “{WINFE}\MakeFELite.bat”.  An ISO will be created and put in the “{WINFE}\ISO” folder.
1. Use the ISO to create a bootable disk or USB drive that will run the WinFE Lite environment with Autopsy 3 now included.   The WinFE Lite page has information on how to turn the ISO image into a bootable USB device.
1. To test, reboot your Windows machine and select the option to boot from USB/CD/DVD instead of your hard drive and normal Windows installation.
1. To open Autopsy 3 in WinFE Lite, open task manager from the settings menu in the toolbar.
1. Under the applications tab, press the new task button and type “explorer” to open it as a new task.
1. Navigate to X:\Program Files\autopsy\bin and double click to run autopsy.exe.
1. Autopsy 3 will now run and you can operate as normal by selecting the disk for analysis in the Case Creation Wizard.
1. When Autopsy opens, select a non-write protected area to store your cases in.  This can be on the USB device you are using to boot from or an additional USB device that you mount read-write.

If you find work arounds to get the video player and ZIP extractor working, please let us know and update this page.
