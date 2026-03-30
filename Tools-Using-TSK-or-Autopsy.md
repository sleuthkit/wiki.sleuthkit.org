---
layout: default
title: "Tools Using TSK or Autopsy"
categories:
  - "Tools"

redirect_from:
  - "/index.php/Tools_Using_TSK"
  - "/index.php/Tools_Using_TSK_or_Autopsy"
  - "/wiki/Tools_Using_TSK"
  - "/wiki/Tools_Using_TSK_or_Autopsy"

last_modified: 2016-12-19
---

# Bootable CDs with [The Sleuth Kit](/The-Sleuth-Kit/) & [Autopsy](/Autopsy/)
(in alphabetical order)
* [BackTrack2](http://www.remote-exploit.org/backtrack.html)
* [CAINE (Computer Aided INvestigative Environment)- GUI Forensics Interface](http://www.caine-live.net/)
* [DEFT (Digital Evidence & Forensic Toolkit) - Xubuntu based](http://deft.yourside.it)
* [FCCU Gnu/Linux Forensic Boot CD (knoppix)](http://www.lnx4n6.be/)
* [Forensic and Incident Response Environment (FIRE)](http://fire.dmzs.com/)
* [Helix (knoppix)](http://www.e-fense.com/helix/)
* [Knoppix STD](http://www.knoppix-std.org/)
* [Local Area Security Linux](http://localareasecurity.com/)
* [Penguin Sleuth Kit (knoppix)](http://www.linux-forensics.com/downloads.html)
* [Network Security Toolkit (NST)](http://www.networksecuritytoolkit.org)
* [Plan-B](http://www.projectplanb.org/)
* [Snarl (FreeBSD)](http://snarl.eecue.com/)
* [HeX (Freesbie2)](http://www.rawpacket.org/projects/hex-livecd)
* [Stagos FSE (Ubuntu based)](http://infosecnewbie.blogspot.com/)
* [IRItaly Live CD Project (**Gentoo** based)](http://www.iritaly-livecd.org)
* [ForLEx Live CD - Forensic Linux Examination (**Debian** based)](http://www.forlex.it/index.php?option=com_content&view=section&layout=blog&id=7&Itemid=41&lang=it)

# Tools that Integrate The Sleuth Kit
(in alphabetical order)
* [Allin1](http://www.netmon.ch/allin1.html)
* [Archivematica](http://archivematica.org/)
* [Autopsy](/Autopsy/)
* [Cyber Triage - by Sleuth Kit Labs](https://cybertriage.com/)
* [NBTempo](http://scripts4cf.sourceforge.net/tools.html)
* [Nigilant32 for Windows](http://www.agilerm.net/publications_4.html)
* [Odyssey Digital Forensics Search](http://www.basistech.com/digital-forensics/odyssey.html)
* [PTK Forensics](http://ptk.dflabs.com) [PTK](/PTK/)
* [PyFlag](http://pyflag.sourceforge.net/)
* [Raw2Fs](http://scripts4cf.sourceforge.net/tools.html)
* [Revealer Toolkit](http://code.google.com/p/revealertoolkit)
* [Selective File Dumper](http://sfdumper.sourceforge.net/)
* [Zeitline](http://www.cerias.purdue.edu/homes/forensics/timeline.php)

# Add-ons / Patches for The Sleuth Kit and Autopsy
The following were written by Sleuth Kit users and provide additional capabilities. Note that a patch may not work with the current version.  

(in alphabetical order)
* Comeforth: [Script](http://sourceforge.net/project/showfiles.php?group_id=55685&package_id=128368) that uses TSK tools to process raw data. It is similar to lazarus, but Dan Higgens says that it provides a bit more flexibility for processing very large data sets.
* FUNDL - File Undeleter: [Script](http://sfdumper.sourceforge.net/fundl.htm) that uses TSK tools (fls and icat), for recovering the deleted files - Windows version [Script](http://sfdumper.sourceforge.net/fundl.htm).
* foremost: [Patch](http://brainspark.nl/?show=tools_sleuthkit) to use [foremost](http://foremost.sourceforge.net/) with Autopsy. By Pepijn Vissers (vissers at fox-it dot com).
* Forensic Hash Database: [Patch](http://www.forinsect.de/forensics/) to use hfind and sorter with the Forensic Hash Database. By Matthias Hofherr (matthias at mhofherr dot de).
* Index Search: [Patch](http://brainspark.nl/?show=tools_sleuthkit) to let Autopsy and The Sleuth Kit index the ASCII words in an image. This provides faster keyword searches in Autopsy than by just extracting the strings. By Paul Bakker ( bakker at fox-it dot com).
* Recoup Directory Contents: [Script](http://davehenk.blogspot.com/2007/06/recover-deleted-files.html) to run fls and icat on a directory to export the files and create the needed subdirectories. By Dave Henkewick (dave at hoax dot ca).
* Qt bindings for TSK: [qttsk](https://github.com/rpoisel/qttsk) provides the user with a graphical frontend to fls and icat. In the future mmls will also be supported. 
* Unicode: (NOTE: This patch is no longer needed as of version 2.03) [Patches](http://www.t-dori.net/forensics/) for the NTFS code in The Sleuth Kit to show Unicode names. By TAKAHASHI Motonobu (monyo at home dot monyo dot com) and tessy (tessy at tessy dot jp).

# Sleuth Kit Packages
The following packages have been contributed by Sleuth Kit users and/or distribution developers. NOTE: They have not been validated, reviewed, or tested by the original developers and have no warranties of any kind. Some packages may not be of the latest release, so check the version first.

* Ralf Spenneberg: [Ralf Spenneberg](http://www.spenneberg.com/6.html?subject=%2FForensics%2F)
* Oden Eriksson: [RPM Find](http://rpmfind.net/linux/rpm2html/search.php?query=sleuthkit)
* Thomas Rude: [crazytrain.com](http://www.crazytrain.com/down.html)
* Matthew Shannon: [src](http://sleuthkit.sourceforge.net/packages/shannon/sleuthkit-1.62-1.src.rpm), [i686](http://sleuthkit.sourceforge.net/packages/shannon/sleuthkit-1.62-1.i686.rpm) (Note that no Autopsy rpms match this rpm).
* Dag Wieers: [dag.wieers.com](http://dag.wieers.com/packages/sleuthkit/)
* Gentoo: [sleuthkit ebuilds](http://packages.gentoo.org/package/app-forensics/sleuthkit)
* OpenBSD: [OpenBSD Packages](http://www.openbsd.org/cgi-bin/cvsweb/ports/sysutils/sleuthkit/)
* FreeBSD: [FreeBSD Packages](http://www.freebsd.org/cgi/ports.cgi?query=^sleuthkit&stype=all)
* Debian: [Debian Packages (stable)](http://packages.debian.org/stable/admin/sleuthkit)
* Slackware: [Slackware Packages](http://www.linuxpackages.net/search_view.php?by=name&name=sleuthkit)

# Autopsy Packages
The following packages have been contributed by Autopsy users. NOTE: They have not been validated, reviewed, or tested by the original developers of Autopsy and have no warranties of any kind. Some packages may not be of the latest release, so check the version first.

* Ralf Spenneberg: [www.spenneberg.com](http://www.spenneberg.com/6.html?subject=%2FForensics%2F) (NOTE: If you use this RPM, make sure you use Ralf's Sleuth Kit RPM as well to ensure the binaries are in the correct place).
* Dag Wieers: [dag.wieers.com](http://dag.wieers.com/packages/autopsy/)
* Michael Scherer: [RPM Find](http://rpmfind.net/linux/rpm2html/search.php?query=autopsy&submit=Search+...&system=&arch=)
* Gentoo:  [Autopsy ebuilds](http://packages.gentoo.org/package/app-forensics/autopsy)
* FreeBSD: [FreeBSD Packages](http://www.freebsd.org/cgi/ports.cgi?query=^autopsy&stype=all)
* Debian: [Debian Packages (stable)](http://packages.debian.org/stable/admin/autopsy)
* Slackware: [Slackware Packages](http://www.linuxpackages.net/search_view.php?by=name&name=autopsy)
* Ubuntu: [Ubuntu Packages](http://packages.ubuntu.com/search?keywords=autopsy)
