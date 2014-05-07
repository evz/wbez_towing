import json
from itertools import groupby
from operator import itemgetter
from datetime import datetime
from shapely.geometry import box
from shapely.wkt import loads
import math

RES = {
    '300m': 300,
    '400m': 400,
    '500m': 500,
    '750m': 750,
    '1km': 1000,
    '2km': 2000,
    '3km': 3000,
}

def getSizeInDegrees(meters, latitude):
    size_x = abs(meters / (111111.0 * math.cos(latitude)))
    size_y = meters / 111111.0
    return size_x, size_y

def breakit(fpath, key):
    geojson = json.load(open('build/%s' % fpath, 'rb'))
    res = fpath.split('_')[1]
    size_x, size_y = getSizeInDegrees(float(RES[res]), 41.83399079583358)
    top = {
        'type': geojson['type'],
        'crs': geojson['crs'], 
    }
    feats = []
    for f in geojson['features']:
        if f.get('geometry'):
            coords = f['geometry']['coordinates']
            pt = loads('POINT(%s %s)' % (coords[0], coords[1]))
            south, west = (pt.x - (size_x / 2)), (pt.y - (size_y /2))
            north, east = (pt.x + (size_x / 2)), (pt.y + (size_y / 2))
            f['properties']['geometry'] = box(south, west, north, east).__geo_interface__
            feats.append(f['properties'])
    feats = sorted(feats, key=itemgetter(key))
    for k,g in groupby(feats, itemgetter(key)):
        if k:
            outp = {
                'type': top['type'],
                'crs': top['crs'],
                'features': []
            }
            fs = list(g)
            for f in fs:
                d = {
                    'properties': {
                        'TOW_COUNT': f['TOW_COUNT'],
                        key: f[key],
                    }
                }
                d['geometry'] = f['geometry']
                d['type'] = 'Feature'
                outp['features'].append(d)
            k = '-'.join(k.split('-')[:-1])
            date = datetime.strptime(k, '%Y-%m-%d %H:%M:%S')
            yield date, outp
    
if __name__ == "__main__":
    import os
    files = os.listdir('build')
    for f in files:
        if f.endswith('geojson'):
            fname = f.split('.')[0]
            if 'year' in fname:
                for date, out in breakit(f, 'YEAR'):
                    outpath = 'finished_files/%s' % (date.year)
                    try:
                        os.makedirs(outpath)
                    except OSError:
                        pass
                    outp = open('%s/%s.geojson' % (outpath, fname), 'wb')
                    outp.write(json.dumps(out))
            else:
                for date, out in breakit(f, 'MONTH'):
                    outpath = 'finished_files/%s/%s' % (date.year, date.month)
                    try:
                        os.makedirs(outpath)
                    except OSError:
                        pass
                    outp = open('%s/%s.geojson' % (outpath, fname), 'wb')
                    outp.write(json.dumps(out))
