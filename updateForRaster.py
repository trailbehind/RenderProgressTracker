#!/usr/bin/env python
import sys
import logging
from optparse import OptionParser
import os
import django
from osgeo import gdal, ogr, osr
from django.contrib.gis.geos import Polygon


gdal.UseExceptions()

def GetExtent(gt,cols,rows):
    ''' Return list of corner coordinates from a geotransform

        @type gt:   C{tuple/list}
        @param gt: geotransform
        @type cols:   C{int}
        @param cols: number of columns in the dataset
        @type rows:   C{int}
        @param rows: number of rows in the dataset
        @rtype:    C{[float,...,float]}
        @return:   coordinates of each corner
    '''
    ext=[]
    xarr=[0,cols]
    yarr=[0,rows]

    for px in xarr:
        for py in yarr:
            x=gt[0]+(px*gt[1])+(py*gt[2])
            y=gt[3]+(px*gt[4])+(py*gt[5])
            ext.append([x,y])
        yarr.reverse()
    return ext


def rounded_extent(source_file, options):
    try:
        src_ds = gdal.Open(source_file)
    except RuntimeError, e:
        print 'Unable to open ' + source_file
        print e
        sys.exit(1)

    gt = src_ds.GetGeoTransform()
    cols = src_ds.RasterXSize
    rows = src_ds.RasterYSize
    ul, ll, lr, ur = GetExtent(gt,cols,rows)
    return  (int(round(ll[0])), int(round(ll[1])), int(round(ur[0])), int(round(ur[1])))


if __name__=='__main__':
    usage = "usage: %prog "
    parser = OptionParser(usage=usage,
        description="")
    parser.add_option("-d", "--debug", action="store_true", dest="debug")
    parser.add_option("-q", "--quiet", action="store_true", dest="quiet")
    parser.add_option("-s", "--state", action="store", dest="state")
    parser.add_option("-l", "--layer", action="store", dest="layer")

    (options, args) = parser.parse_args()
    
    logging.basicConfig(level=logging.DEBUG if options.debug else 
        (logging.ERROR if options.quiet else logging.INFO))

    if not options.layer:
        logging.error("layer option required")
        sys.exit(0)

    if not options.state:
        logging.error("state option required")
        sys.exit(0)
    
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RenderProgressTracker.settings")
    #django.setup() for 1.7
    from django.conf import settings
    from RenderProgress.models import Dataset, RenderBlock

    dataset, dataset_created = Dataset.objects.get_or_create(identifier=options.layer, 
        defaults={'name':options.layer})

    for path in args:
        if not os.path.exists(path):
            print path + " not found"
            continue
        extent = rounded_extent(path, options)
        identifier = "_".join([str(i) for i in extent])
        source_name = os.path.basename(path)
        block, created = RenderBlock.objects.get_or_create(identifier=identifier, 
            dataset=dataset, source=source_name)
        if created:
            block.bounds = Polygon.from_bbox(extent)
        
        block.state = options.state
        block.save()
