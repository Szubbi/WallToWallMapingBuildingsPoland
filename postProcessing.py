import arcpy
import os
import logging

def postProcCities(prg_dir, detections_list, out_db_dir):
    
    logging.info('creating PRG lyr')
    arcpy.MakeFeatureLayer_management(prg_dir, r"memory\lyrPRG")
    
    for fc in detections_list:
        
        dst_dir = os.path.join(out_db_dir, fc.split('\\')[-1])
        
        if not arcpy.Exists(dst_dir):
        
            fcName = fc.split('\\')[-1]

            logging.info("working on: {}".format(fcName))

            arcpy.MakeFeatureLayer_management(fc, r"memory\lyrDetections")

            arcpy.SelectLayerByLocation_management(r"memory\lyrPRG", 
                                                   'WITHIN_A_DISTANCE', 
                                                   r"memory\lyrDetections", 
                                                   selection_type = 'NEW_SELECTION')

            arcpy.CopyFeatures_management(r"memory\lyrPRG", dst_dir)

            arcpy.SelectLayerByLocation_management("memory\lyrDetections",
                                                   'WITHIN_A_DISTANCE',
                                                   r"memory\lyrPRG",
                                                   selection_type = 'NEW_SELECTION')

            arcpy.SelectLayerByAttribute_management("memory\lyrDetections",
                                                   "SWITCH_SELECTION")

            arcpy.SelectLayerByAttribute_management("memory\lyrDetections",
                                                   "REMOVE_FROM_SELECTION",
                                                   "Confidence < 97")

            arcpy.management.Dissolve("memory\lyrDetections", "memory\lyrDetectionsDiss",
                                     multi_part = 'SINGLE_PART')

            arcpy.SelectLayerByAttribute_management("memory\lyrDetectionsDiss", "CLEAR_SELECTION")

            arcpy.management.FeatureToPoint("memory\lyrDetectionsDiss", r"memory\lyrPoints", "INSIDE")
            
            arcpy.management.AddField(dst_dir, "Confidence", "DOUBLE")

            arcpy.Append_management(r"memory\lyrPoints", dst_dir, 'NO_TEST')

            arcpy.management.AddField(dst_dir, "Arkusz", "TEXT", field_length = 35)
            arcpy.management.AddField(dst_dir, "Rok", "Short")
            arcpy.management.AddField(dst_dir, "NazwaPliku", "TEXT", field_length = 35)

            arcpy.management.CalculateField(dst_dir, "Arkusz", '"{}"'.format(fcName[3:fc.index('__')]))
            arcpy.management.CalculateField(dst_dir, "Rok", '"{}"'.format(fcName[-8:-4]))
            arcpy.management.CalculateField(dst_dir, "NazwaPliku", 
                                            '"{}.{}.{}.{}.tif"'.format(fcName[:fcName.index('__')+3], fcName[fcName.index('__')+3: fcName.index('__')+5], 
                                                                       fcName[fcName.index('__')+5:fcName.index('__')+9], fcName[fcName.index('__')+9:fcName.index('_00')]))
        else:
            
            fcName = fc.split('\\')[-1]
            logging.info("{} already done".format(fcName))

if __name__ == '__main__':

    logging.basicConfig(filename=r'',
                filemode='a',
                format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                datefmt='%H:%M:%S',
                level=logging.DEBUG)
    

    #adress database points
    prg_dir = r''
    #output location
    out_db_dir = r''
    #detections dir
    detections_dir = r''

    arcpy.env.workspace = detections_dir
    detections_list = arcpy.ListFeatureClasses()

    postProcCities(prg_dir, detections_list, out_db_dir)
    

    