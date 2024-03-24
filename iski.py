from sys import argv
from urllib import request

from js2py import eval_js

import json
import os


# Use JS to convert timestamp to datestring. The z param allows for manual timezone correction
def toDate(e, z = 2):
    date = eval_js(f'new Date({e})')
    return f'{date.getHours()-z:02}:{date.getMinutes():02}:{date.getSeconds():02}'

# If a file with the same name already exists, add _2, _3, etc. 
def get_unique_filename(filename):
    base, ext = os.path.splitext(filename)
    count = 2
    new_filename = filename
    while os.path.exists(new_filename):
        new_filename = f"{base}_{count}{ext}"
        count += 1
    return new_filename

# The base url for iSki shares
base = 'https://share.iski.cc/shares/share_iski/tracks/'

total_ids = len(argv[1:])

for index, id in enumerate(argv[1:], start=1):
    print(f"({index}/{total_ids}) Saving {id} into file:", end=' ')

    # Parse the date from the page
    html = request.urlopen(base + id).read().decode('utf-8')
    date = html[html.find('<br />'):html.find(' °C')].split(' ')[-2].replace(',','').split('/')
    date = f'{date[2]}-{date[0]}-{date[1]}'

    # Load and serialize data points
    data = json.loads(json.loads(json.dumps(request.urlopen(base + id + '/geometry.json').read().decode('utf-8'))))

    # Check if GPX file already exists
    gpx_filename = f'{date}.gpx'
    gpx_filename = get_unique_filename(gpx_filename)

    print(gpx_filename)

    # Create GPX file template
    with open(gpx_filename, 'w') as file:
        file.write('<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n')
        file.write('<gpx xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd" version="1.1" creator="gpx.py">\n')
        file.write('\t<trk>\n')
        file.write('\t\t<name>ski</name>\n')
        file.write('\t\t<type>Snowboarding</type>\n')
        file.write('\t\t<trkseg>\n')

        # Convert to trackpoints
        for p in data['path']:
            file.write(f'\t\t\t<trkpt lat="{p["lat"]}" lon="{p["lng"]}">\n')
            file.write(f'\t\t\t\t<ele>{p["elevation"]}</ele>\n')
            file.write(f'\t\t\t\t<time>{date}T{toDate(p["time"])}.000Z</time>\n')
            file.write(f'\t\t\t</trkpt>\n')

        file.write('\t\t</trkseg>')
        file.write('\t</trk>')
        file.write('</gpx>')
