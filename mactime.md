---
layout: default
title: "mactime"
categories:
  - "Tools"

redirect_from:
  - "/Mactime/"
  - "/index.php/Mactime"
  - "/index.php/mactime"
  - "/wiki/Mactime"
  - "/wiki/mactime"

last_modified: 2010-08-13
---

Back to [Help Documents](/Help-Documents/)

mactime creates an ASCII [timeline](/Timeline/) of file activity based on the output of the [fls](/fls/) tool. It can be used to detect anomalous behavior and reconstruct events. The [fls](/fls/) command must use the *-m* flag to generate a output with timestamps.

mactime reads the [body file](/Body-file/) (using the '-b' argument), which contains a line for each file or event.  mactime then sorts the data based on its temporal data and prints the result. It can optionally use a starting date or a date range to limit the data being printed.  

The following reads body.txt and outputs all activity starting in March of 2002. 

```
# mactime -b body.txt 2002-03-01 > tl.03.01.2002.txt
```

Some of the arguments for mactime help to make the output more readable. On a Unix system, the User and Group IDs can be mapped to actual names by using the '-p' and '-q' flags.  The '-z' flag can be used to specify the time zone, if it is different from the local timezone.

```
# mactime -b body.txt -z EST5EDT 2002-03-01 > tl.03.01.2002.txt
```

The [mactime output](/Mactime-output/) is text that contains the file activity. 

If you are going to include the resulting timeline in a document, then it maybe better to supply the '-d' argument to output in comma delimited format.  The resulting timeline can then be imported into a spread sheet and included as a table.

The '-i' option to 'mactime' creates an index summary file, including how many hits were found per day or hour.  Using '-d' with '-i' allows one to easily import data into a spread sheet that can be graphed to spot suspicious behavior.

```
# mactime -b body.txt -d -i hour data/tl-hour-sum.txt > timeline.txt
```

  
* [Automatically Updated man Page](http://www.sleuthkit.org/sleuthkit/man/mactime.html)
