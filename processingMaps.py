import arcpy
import os
import time
from arcpy.ia import *
import logging

def detectBuidlings(raster_dir, outDB, model_dir):
    topo_sheet = raster_dir.split('\\')[-1]
    try:
        logging.info('Start working on {}'.format(topo_sheet))

        out_bud_dir = os.path.join(outDB, 'dl_'  + topo_sheet.replace('.','').replace('tif','_00'))

        DetectObjectsUsingDeepLearning(raster_dir, out_bud_dir, model_dir,
                                    "padding 64; nms_overlap 0.5; threshold 0.9; batch_size 4; return_bboxes False; tile_size 256")

        arcpy.management.AddFields(out_bud_dir, 
                                [['NazwaPliku', 'TEXT', 'NazwaPliku', 55, Topo], 
                                    ['Rok', 'TEXT', 'Rok', 35, Topo.split('.')[2]],
                                    ['Arkusz', 'TEXT', 'Arkusz', 35, Topo.split('_')[0]]])
        
        logging.info('{} Completed'.format(topo_sheet))

    except Exception as e:
        logging.exception('{} Exception: {}'.format(topo_sheet, e))



if __name__ == '__main__':

    logging.basicConfig(filename=r'',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
    
    raster_catalog_dir = r''
    out_db_dir = r''
    mask_rcnn_dir = r''

    arcpy.env.workspace = raster_catalog_dir

    for raster in arcpy.ListRasters():
        counter = 0
        raster_dir = os.path.join(raster_catalog_dir, raster)

        detectBuidlings(raster_dir, out_db_dir, mask_rcnn_dir)

        if counter%3 == 0:
            print('\033[95m One minute of break to cool down GPU')
            time.sleep(60)

        counter += 1




            
        