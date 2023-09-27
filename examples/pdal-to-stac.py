#!/usr/bin/env python

# conda install -c conda-forge pdal gdal

import sys
import json
import os
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
output['id'] = os.path.basename(filename)
output['type'] = 'Feature'

assets = {'data': {'href': filename}}
#assets['thumbnail'] =
properties = {}

properties['pc:schemas'] = info['schema']['dimensions']
properties['pc:statistics'] = stats['statistic']
properties['title'] = "USGS 3DEP LiDAR"
properties['item:provider'] = "USGS"
properties['item:license'] = 'LICENSE'
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

link = {'rel':'self',"href":filename}
output['links'] = [link]

with open('examples/example-autzen.json', 'w') as autzen_out:
    autzen_out.write(json.dumps(output, sort_keys=True, indent=2,
                                separators=(',', ': ')))
