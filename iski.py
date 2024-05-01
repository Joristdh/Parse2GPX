from glob import glob
from os.path import splitext
from sys import argv
from urllib import request

from js2py import eval_js
from tqdm import tqdm

import json


# Use JS to convert timestamp to datestring. The z param allows for manual timezone correction
def to_date(e, z=2):
    js_date = eval_js(f'new Date({e})')
    return f'{js_date.getHours() - z:02}:{js_date.getMinutes():02}:{js_date.getSeconds():02}'


# If a file with the same name already exists, add _2, _3, etc. 
def get_unique_filename(filename):
    basename, ext = splitext(filename)
    count = len(glob(f"./gpx/{basename}*{ext}"))
    return f"{basename}{f'_{++count}' if count > 0 else ''}{ext}"


# The base url for iSki shares
base = 'https://share.iski.cc/shares/share_iski/tracks/'

for track_id in (pbar := tqdm(argv[1:])):

    # Parse the date from the page
    html = request.urlopen(base + track_id).read().decode('utf-8')
    date = html[html.find('<br />'):html.find(' °C')].split(' ')[-2].replace(',', '').split('/')
    date = f'{date[2]}-{date[0]}-{date[1]}'

    # Check if GPX file already exists
    gpx_filename = get_unique_filename(f'{date}.gpx')

    # Update progressbar
    pbar.set_description(gpx_filename)

    # Load and serialize data points
    data = json.loads(
        json.loads(json.dumps(request.urlopen(base + track_id + '/geometry.json').read().decode('utf-8'))))

    # Create GPX file template
    with open('gpx/' + gpx_filename, 'w') as file:
        file.write('<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n')
        file.write(
            '<gpx xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd" version="1.1" creator="gpx.py">\n')
        file.write('\t<trk>\n')
        file.write('\t\t<name>ski</name>\n')
        file.write('\t\t<type>Snowboarding</type>\n')
        file.write('\t\t<trkseg>\n')

        # Convert to trackpoints
        for p in data['path']:
            file.write(f'\t\t\t<trkpt lat="{p["lat"]}" lon="{p["lng"]}">\n')
            file.write(f'\t\t\t\t<ele>{p["elevation"]}</ele>\n')
            file.write(f'\t\t\t\t<time>{date}T{to_date(p["time"])}.000Z</time>\n')
            file.write(f'\t\t\t</trkpt>\n')

        file.write('\t\t</trkseg>')
        file.write('\t</trk>')
        file.write('</gpx>')
