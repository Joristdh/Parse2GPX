# [iSki|Takeout]2GPX
Simple script to export an iSki track or a Google Takeout timeline to a GPX file. The output file will be named yyyy-mm-dd.gpx. 

## Google Takeout
Works by parsing the semantic location history of the takeout. Some steps require manual corrections in-between. Ensure the activities are correctly labeled in the Google Maps timeline before initiating the takeout.

### Usage
> kml.py _split_

The script assumes separate daily JSON files in the **json** directory. There is a helper function that splits the monthly timeline files into days, filtered to only contain relevant activities. This function can be invoked by adding the _split_ argument.

## iSKI
I do not know how the script handles different timezones, but the *z* param in the *toDate(e, z)* method can be adjusted to your personal preference.

### Prerequisites
The scrips uses js2py, which can be installed using PIP. Python is also needed, of course.

### Usage
> iski.py *trackId*

You can find the trackId in the url when you share the iSki track: https://share.iski.cc/shares/share_iski/tracks/XXXXXXXX. 

**Only copy the id, do not include the lang url parameter.**

You can input multiple trackIds by separating them with spaces:
>iksi.py *trackId1* *trackId2* *trackId3* 

### iSKI ID Parser
You can use `iski_id_parser.py` to extract IDs from a file named `input.txt` in the same directory by running:
> iski_id_parser.py

You will get all found IDs seperated by spaces, which can then be copied and pasted for the iSKI parser.

This method can be useful if you are exporting multiple tracks, which were all shared from the app.

Example input.txt:
~~~
<iSKI username> in location
X Hm, Y Lifts, Z km  #iSKIhttps://share.iski.cc/shares/share_iski/tracks/<trackID>?lang=en
<iSKI username> in location
X Hm, Y Lifts, Z km  #iSKIhttps://share.iski.cc/shares/share_iski/tracks/<trackID>?lang=en
...
~~~