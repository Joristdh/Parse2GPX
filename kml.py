from os import walk
from time import sleep
from xml.etree.ElementTree import parse

from requests import post

API = 'https://api.open-elevation.com/api/v1/lookup'

"""
Convert all files in the kml folder to GPX files with elevation, but without timestamps. 
"""
for file in next(walk('kml'), (None, None, []))[2]:
    with open('gpx/' + file.replace('kml', 'gpx'), 'w') as gpx:
        gpx.write('<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n')
        gpx.write('<gpx xmlns="http://www.topografix.com/GPX/1/1" '
                  'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                  'xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd" '
                  'version="1.1" creator="gpx.py">\n')
        gpx.write('\t<trk>\n')
        gpx.write('\t\t<name>ski</name>\n')
        gpx.write('\t\t<type>Snowboarding</type>\n')

        for place in parse('kml/' + file).getroot()[0]:
            if place.tag.endswith('Placemark') and int(place[2][2][0].text) > 0:
                gpx.write('\n\t\t<trkseg>\n')

                # Convert to trackpoints
                data = {'locations': []}
                for coord in place[4][3].text.split(' '):
                    if len(coord) > 0:
                        [lat, lng] = coord.split(',')[:-1]
                        data['locations'].append({"latitude": float(lat), "longitude": float(lng)})

                res = post(url=API, json=data)
                while res.status_code == 429:
                    sleep(5)
                    res = post(url=API, json=data)

                for c in res.json()['results']:
                    gpx.write(f'\t\t\t<trkpt lat="{c["latitude"]}" lon="{c["longitude"]}">\n')
                    gpx.write(f'\t\t\t\t<ele>{c["elevation"]}</ele>\n')
                    gpx.write(f'\t\t\t\t<time>N/A</time>\n')
                    gpx.write(f'\t\t\t</trkpt>\n')

                gpx.write('\t\t</trkseg>')
        gpx.write('\n\t</trk>')
        gpx.write('\n</gpx>')
