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
        description="Update or query status for a raster")
    parser.add_option("-d", "--debug", action="store_true", dest="debug")
    parser.add_option("-q", "--quiet", action="store_true", dest="quiet")
    parser.add_option("-s", "--state", action="store", dest="state", 
        help="Set state, one of running, complete, failed")
    parser.add_option("-l", "--layer", action="store", dest="layer", 
        help="Layer name")
    parser.add_option("-c",  "--check", action="store_true", dest="check", 
        help="Check staus of block. if --state is specified check if state matches, else check if block exists.")

    (options, args) = parser.parse_args()
    
    logging.basicConfig(level=logging.DEBUG if options.debug else 
        (logging.ERROR if options.quiet else logging.INFO))

    if not options.layer:
        logging.error("layer option required")
        sys.exit(0)
    
    if not options.state and not options.check:
        logging.error("no set or check option specified, nothing to do")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RenderProgressTracker.settings")
    #django.setup() for 1.7
    from django.conf import settings
    from RenderProgress.models import Dataset, RenderBlock

    dataset, dataset_created = Dataset.objects.get_or_create(identifier=options.layer, 
        defaults={'name':options.layer})

    for path in args:
        if not os.path.exists(path):
            logging.error(path + " not found")
            continue
        extent = rounded_extent(path, options)
        identifier = "_".join([str(i) for i in extent])
        source_name = os.path.basename(path)
        if options.check:
            block = RenderBlock.objects.filter(identifier=identifier, dataset=dataset).first()
            if block:
                logging.info("block exists")
                if options.state:
                    if block.state == options.state:
                        logging.debug("State matches")
                        sys.exit(0)
                    else:
                        logging.debug("State does not match")
                        sys.exit(-1)
                else:
                    sys.exit(0)
            else:
                logging.info("block does not exist")
                sys.exit(-1)
        else:
            if options.state:
                block, created = RenderBlock.objects.get_or_create(identifier=identifier, 
                    dataset=dataset, source=source_name)
                if created:
                    block.bounds = Polygon.from_bbox(extent)
        
                block.state = options.state
                block.save()
