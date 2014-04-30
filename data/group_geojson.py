import json
from itertools import groupby
from operator import itemgetter
from datetime import datetime

def breakit(fpath, key):
    geojson = json.load(open('build/%s' % fpath, 'rb'))
    top = {
        'type': geojson['type'],
        'crs': geojson['crs'], 
    }
    feats = []
    for f in geojson['features']:
        f['properties']['geometry'] = f['geometry']
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
