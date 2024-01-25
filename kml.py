from json import loads, dumps
from os import walk
from sys import argv
from time import sleep

from requests import post

API = 'https://api.open-elevation.com/api/v1/lookup'


def split_takeout_json():
    """
    Split the monthly Google Takeout JSON files in json dir into a file per day.
    Segments are filtered to only include related activities.
    """
    for take in next(walk('takeout'), (None, None, []))[2]:
        with open('takeout/' + take, 'r') as t:
            arr = []
            for obj in loads(t.read())['timelineObjects']:
                if 'activitySegment' in obj and 'activityType' in obj['activitySegment']:
                    if obj['activitySegment']['activityType'] in ['SKIING', 'SNOWBOARDING', 'IN_GONDOLA_LIFT']:
                        arr.append(obj['activitySegment'])
            days = set([x['duration']['endTimestamp'].split('T')[0] for x in arr])
            for day in days:
                with open('json/' + day + '.json', 'w') as d:
                    d.write('[')
            for obj in arr:
                with open('json/' + obj['duration']['endTimestamp'].split('T')[0] + '.json', 'a') as d:
                    d.write(dumps(obj) + ',')
            for day in days:
                with open('json/' + day + '.json', 'rb+') as d:
                    d.seek(-1, 2)
                    d.write(str.encode(']'))


if len(argv) > 1 and argv[1] == 'split':
    split_takeout_json()

"""
Convert daily takeout JSON to GPX. 
"""
for file in next(walk('json'), (None, None, []))[2]:
    with open('json/' + file, 'r') as jsn:
        with open('gpx/' + file.replace('json', 'gpx'), 'w') as gpx:
            gpx.write('<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n')
            gpx.write('<gpx xmlns="http://www.topografix.com/GPX/1/1" '
                      'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                      'xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd" '
                      'version="1.1" creator="gpx.py">\n')
            gpx.write('\t<trk>\n')
            gpx.write('\t\t<name>' + file.split('.')[0] + '</name>\n')
            gpx.write('\t\t<type>Snowboarding</type>')

            # Convert segments to trk
            for segment in loads(jsn.read()):
                if 'simplifiedRawPath' in segment:
                    gpx.write('\n\t\t<trkseg>\n')

                    # Gathers + fix coords
                    data = {'locations': []}
                    for p in segment['simplifiedRawPath']['points']:
                        data['locations'].append({"latitude": p["latE7"] / 1e7, "longitude": p["lngE7"] / 1e7})

                    # Get elevations
                    res = post(url=API, json=data)
                    while res.status_code == 429:
                        sleep(5)
                        res = post(url=API, json=data)

                    # Write track points
                    for c, p in zip(res.json()['results'], segment['simplifiedRawPath']['points']):
                        gpx.write(f'\t\t\t<trkpt lat="{c["latitude"]}" lon="{c["longitude"]}">\n')
                        gpx.write(f'\t\t\t\t<ele>{c["elevation"]}</ele>\n')
                        gpx.write(f'\t\t\t\t<time>{p["timestamp"]}</time>\n')
                        gpx.write(f'\t\t\t</trkpt>\n')

                    gpx.write('\t\t</trkseg>')

            gpx.write('\n\t</trk>')
            gpx.write('\n</gpx>')
