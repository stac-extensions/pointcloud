#!/usr/bin/env python

# conda env create -f environment.yml
# conda activate stac-extensions-pointcloud
# ./pdal-to-stac.py

import sys
import json
from os import path
from pathlib import Path
import pdal

filename = "https://github.com/PDAL/data/raw/master/autzen/autzen-classified.copc.laz"

# pdal info --all call references hexbin, stats, and info filters
r = pdal.Reader.copc(filename)
hb = pdal.Filter.hexbin()
s = pdal.Filter.stats()
i = pdal.Filter.info()

pipeline: pdal.Pipeline = r | hb | s | i

count = pipeline.execute()

boundary = pipeline.metadata['metadata'][hb.type]
stats = pipeline.metadata['metadata'][s.type]
info = pipeline.metadata['metadata'][i.type]
copc = pipeline.metadata['metadata'][r.type]

def capture_date(pdalinfo):
    import datetime
    year = pdalinfo['creation_year']
    day = pdalinfo['creation_doy']
    date = datetime.datetime(int(year), 1, 1) + datetime.timedelta(int(day) - 1 if int(day) > 1 else int(day))
    return date.isoformat()+'Z'

def convertGeometry(geom, srs):
    from osgeo import ogr
    from osgeo import osr
    in_ref = osr.SpatialReference()
    in_ref.SetFromUserInput(srs)
    out_ref = osr.SpatialReference()
    out_ref.SetFromUserInput('EPSG:4326')

    g = ogr.CreateGeometryFromJson(json.dumps(geom))
    g.AssignSpatialReference(in_ref)
    g.TransformTo(out_ref)
    return json.loads(g.ExportToJson())


def convertBBox(obj):
    output = []
    output.append(float(obj['minx']))
    output.append(float(obj['miny']))
    output.append(float(obj['minz']))
    output.append(float(obj['maxx']))
    output.append(float(obj['maxy']))
    output.append(float(obj['maxz']))
    return output


output = {}

try:
    output['geometry'] = convertGeometry(
        boundary['boundary_json'],
        copc['comp_spatialreference']
    )
except KeyError:
    output['geometry'] = stats['bbox']['EPSG:4326']['boundary']

output['bbox'] = convertBBox(stats['bbox']['EPSG:4326']['bbox'])
output['id'] = path.basename(filename)
output['type'] = 'Feature'

assets = {'data': {'href': filename}}
properties = {}

properties['pc:schemas'] = info['schema']['dimensions']
properties['pc:statistics'] = stats['statistic']
properties['title'] = "USGS 3DEP LiDAR"
properties['providers'] = [
      {
        "name": "USGS",
        "description": "United States Geological Survey",
        "roles": [
          "producer",
        ],
        "url": "https://www.usgs.gov"
      }
]
properties['pc:type'] = 'lidar' # eopc, lidar, radar, sonar
try:
    properties['pc:density'] = boundary['avg_pt_per_sq_unit']
except KeyError:
    properties['pc:density'] = 0
properties['pc:count'] = count

properties['datetime'] = capture_date(copc)

output['properties'] = properties
output['assets'] = assets
output['stac_extensions'] = ['https://stac-extensions.github.io/pointcloud/v1.0.0/schema.json']
output['stac_version'] = '1.0.0'

example_dir = Path(__file__).parent
out_filename = str(example_dir/'example-autzen.json')

self_link = {'rel':'self',"href":'./example-autzen.json'}
lic_link = {'rel':'license',"href":'https://github.com/PDAL/data/blob/master/LICENSE'}
output['links'] = [self_link, lic_link]

with open(out_filename, 'w') as autzen_out:
    autzen_out.write(json.dumps(output, sort_keys=True, indent=2,
                                separators=(',', ': ')))
