#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      scragun
#
# Created:     23/02/2018
# Copyright:   (c) scragun 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
import sys
import os
import time
arcpy.env.workspace = (r"E:\Programming\Week6\LabData")
print ("starting program")

def main():
    global iteration
    global feature_count


    workspace = raw_input("Location of new GDB")
    newGDBname = raw_input("Name the GDB.  EX: new_corvallis.gdb")

    #does geodatabase exist
    if arcpy.Exists("new_corvallis.gdb"):
        arcpy.Delete_management("new_corvallis.gdb")


    #create GDB feature sets

    arcpy.CreateFileGDB_management (workspace, newGDBname)
    newGDBpath = os.path.join(workspace, newGDBname)

    PointLess1000 = arcpy.CreateFeatureDataset_management(newGDBpath,"Point_Less_1000")

    PointGreat1000 = arcpy.CreateFeatureDataset_management(newGDBpath, "Points_greater_1000")

    Lineless1000 = arcpy.CreateFeatureDataset_management(newGDBpath, "Polyines_less_1000")

    LineGreat1000 = arcpy.CreateFeatureDataset_management(newGDBpath, "Polyines_greater_1000")

    PolygonLess1000 = arcpy.CreateFeatureDataset_management(newGDBpath, "Polygons_less_1000")

    PolygonGreat1000 = arcpy.CreateFeatureDataset_management(newGDBpath, "Polygon_greater_1000")


    arcpy.env.workspace = (r"E:\Programming\Week6\LabData\Corvallis.gdb")

    fc_list = arcpy.ListFeatureClasses()
    iteration = 0
    feature_count = 0
    for fc in fc_list:
        feature_count += 1
        description = arcpy.Describe(fc)
        fcname = description.name
        fcshape = description.shapetype

        print ("{} is a {}".format(fcname,fcshape))

        get_fccount = arcpy.GetCount_management(fc)
        fccount = int(get_fccount.getOutput(0))
        iteration +=1
        underline = "_"
        name = "{}{}{}".format(fcname, underline, fccount)


        if (fcshape =="Point"):
            if(fccount <= 1000):
                arcpy.FeatureClassToFeatureClass_conversion(fc, PointLess1000, name)
                print("feature class {} is of type {} and has {}"
                        " records".format(fcname,fcshape,fccount))
            else:
                arcpy.FeatureClassToFeatureClass_conversion(fc, PointGreat1000, name)
                print("feature calss {} is of type {} and has {}"
                        " records".format(fcname, fcshape, fccount))
        if (fcshape == "Polyline"):
            if(fccount <= 1000):
                arcpy.FeatureClassToFeatureClass_conversion(fc, Lineless1000, name)
                print("feature class {} is of type {} and has < 1000"
                        " records".format(fcname, fcshape, fccount))
            else:
                arcpy.FeatureClassToFeatureClass_conversion(fc, LineGreat1000, name)
                print("feature class {} is of type {} and has {}"
                        " records.".format(fcname, fcshape, fccount))

        if(fcshape == "Polygon"):
            if(fccount<= 1000):
                arcpy.FeatureClassToFeatureClass_conversion(fc, PolygonLess1000, name)
                print("feature class {} is of type {} and has {}"
                        " records".format(fcname, fcshape, fccount))
            else:
                arcpy.FeatureClassToFeatureClass_conversion(fc, PolygonGreat1000, name)
                print("feature class {} is of type {} and has {}"
                        " records".format(fcname, fcshape, fccount))







if __name__ == '__main__':
    main()
