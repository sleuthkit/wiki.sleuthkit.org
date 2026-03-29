---
layout: default
title: "Autopsy: Setting Up a Case"
categories:
  - "Autopsy"

redirect_from:
  - "/index.php/Autopsy:_Setting_Up_a_Case"
  - "/wiki/Autopsy:_Setting_Up_a_Case"

last_modified: 2013-03-10
---

## Setting Up a Case
This is a simple tutorial for beginners. This tutorial describes how to setup a case on a Linux machine (using the Autopsy browser). The steps are straightforward, so let's get started!

1. Bootup the browser, if you forgot how to [look here](http://cyberforensics.et.byu.edu/wiki/Install_Sleuthkit), and look for the command to startup Autopsy (near the end of the Linux or Ubuntu Install tutorial).
1. On the opening screen select "NEW CASE"
1. This section is the "CREATE A NEW CASE" so we will fill out a few things:
  1. "Case Name": name the case something that is descriptive; for instance: Office Issues
  1. "Description": write a short summary of the case; for instance: "The case of inappropriate material on Office computers."
  1. "Investigator Names": write the names of those working on the case
  1. Click "NEW CASE"
1. The new screen will say: "Creating Case: <name of your case>"
1. Select your name from the dropdown list, and then click "ADD HOST"
1. The next screen will show the options for "Add A NEW HOST"
  1. "Host Name": name the computer that you are investigating; for instance: "Desktop112"
  1. "Description": write a small description of the host; for instance: "This is computer with ID:Desktop112, suspect of illicit material"
  1. "Time Zone": write the time zone, if you want to specify it
  1. "Timeskew Adjustment": write the time adjustment; sometimes the computers being investigated may have their time off by minutes, use this field to correct the skew
  1. "Path of Alert Hash Database": there are databases that have [hashes](/hashes/) of known malicious files. If you have such a database, indicate the path to the database here
  1. "Path of Ignore Hash Database": there are database that have hashes that are known to be fine; that is they can be ignored, indicate the path to the database here, if you have one
1. Click "ADD HOST"
1. The next screen, "Adding host: <name of your host> to case <name of your case>", is where we will add a disc image to the case
1. Click "ADD IMAGE"
1. The next screen you will see a series of options, click "ADD IMAGE FILE", this is how we will add our disc image
1. Next, we'll enter the information needed to get the image
  1. "Location": enter the full path name to the image; for instance: */home/sleuth/Desktop/usbkey.image*
  1. "Type": choose the radio button of your image type:
    1. "Disk": if your image is a full disk image, choose this
    1. "Partition": if your image is only a partition of a Disk, select this option
  1. "Import Method": Autopsy will need to have the image in the *Evidence_Locker*directory, so choose one of the options:
    1. "Symlink": this imports the image from its current location
    1. "Copy": this copies the image from its location to the directory
    1. "Move": this moves the file to the *Evidence_Locker* directory
1. Next, we are on the "Image File Details" screen
  1. "Data Integrity": here we can choose if we want a MD5 hash to be calculated or not, and if we want to add the hash for the image to a file of hashes
  1. Click "ADD"
1. Over view data will be shown, click "OK"
That's it. We have successfully created a case, added a host, and an image. Now we can analyze the image!

### Other resources
Here are some other tutorials on setting up cases.
* [Tutorial 1](http://www.sleuthkit.org/autopsy/help/caseman.html): This is a case tutorial on sleuthkit.org, it is a great resource, which shows the basic steps to create a case.
* [Tutorial 2](http://computer-forensics.sans.org/blog/2009/05/11/a-step-by-step-introduction-to-using-the-autopsy-forensic-browser/): This tutorial has pictures, which makes it easy to follow, and see if you're on the right track.
