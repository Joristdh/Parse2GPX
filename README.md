# iSki2GPX
Simple script to convert the iSki track share to a GPX file. The output file will be named yyyy-mm-dd.gpx. I do not know how the script handles different timezones, but the *z* param in the *toDate(e, z)* method can be adjusted to your personal preference.

## Prerequisites
The scrips uses js2py, which can be installed using PIP. Python is also needed, of course

## Usage
> gpx.py *trackId*

You can find the trackId in the url when you share the iSki track: https://share.iski.cc/shares/share_iski/tracks/*XXXXX*. **Only copy the id, do not include the lang url parameter.**
You can input multiple trackIds by separating them with spaces:
>gpx.py *trackId1* *trackId2* *trackId3* 
