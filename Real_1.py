#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      gboswick
#
# Created:     24/02/2018
# Copyright:   (c) gboswick 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import sys
import os


def main():


# Assign workspace environment
    arcpy.env.workspace = (r"E:\GIS Programming\Week_6\LabData")

# Create new file geodatabase named new_corvallis

    second_GDB = r"Steve"
    arcpy.CreateFileGDB_management(arcpy.env.workspace, second_GDB)

    second_GDB_path = os.path.join(r"E:\GIS Programming\Week_6\LabData\Steve.gdb")

# Create 6 feature Datasets in new_corvallis
    pt_lt_1k = arcpy.CreateFeatureDataset_management(second_GDB_path, "point_less_1000", 6884)

    pt_gt_1k = arcpy.CreateFeatureDataset_management(second_GDB_path, "point_great_1000", 6884)

    pl_lt_1k = arcpy.CreateFeatureDataset_management(second_GDB_path, "polyline_less_1k", 6884)

    pl_gt_1k = arcpy.CreateFeatureDataset_management(second_GDB_path, "polyline_great_1k", 6884)

    pg_lt_1k = arcpy.CreateFeatureDataset_management(second_GDB_path, "polygon_less_1k", 6884)

    pg_gt_1k = arcpy.CreateFeatureDataset_management(second_GDB_path, "polygon_great_1k", 6884)

#Revert to the Corvalis GDB worksapce

    arcpy.env.workspace = (r"E:\GIS Programming\Week_6\Labdata\Corvallis.gdb")

#Get a list of the fc's in corvallis.gdb

    fc_list = arcpy.ListFeatureClasses()

#Loop through each and retrieve their properties

    iteration = 0
    feature_count= 0
    for fc in fc_list:
        feature_count += 1
        description = arcpy.Describe(fc)
        fcname= description.name
        fcshape=description.shapetype

#print out the fc name and the shape for each fc
        print ("{} is a {}".format(fcname,fcshape))

#count thee number of features in each fc

        get_fccount= arcpy.GetCount_management(fc)
        fc_count= int(get_fccount.getOutput(0))
        iteration += 1
        underline = "_"
        name = "{}{}{}".format(fcname, underline, iteration)

        if (fcshape == "Point"):
            if (fc_count <= 1000):
                arcpy.FeatureClassToFeatureClass_conversion(fc, pt_lt_1k, name)
                print("feature class {} has {} records and was placed in the "
                      " {} Feature Dataset".format(fcname, fc_count, "point_less_1000"))
            else:
                arcpy.FeatureClassToFeatureClass_conversion(fc, pt_gt_1k, name)
                print("feature class {} has {} records and was placed in the "
                      " {} Feature Dataset".format(fcname, fc_count, "point_great_1000"))

        if (fcshape == "Polyline"):
            if (fc_count <= 1000):
                arcpy.FeatureClassToFeatureClass_conversion(fc, pl_lt_1k, name)
                print("feature class {} has {} records and was placed in the "
                      " {} Feature Dataset".format(fcname, fc_count,"polyline_less_1k"))
            else:
                arcpy.FeatureClassToFeatureClass_conversion(fc, pl_gt_1k, name)
                print("feature class {} has {} records and was placed in the"
                      " {} Feature Dataset".format(fcname, fc_count,"polyline_great_1k"))

        if (fcshape == "Polygon"):
            if (fc_count <= 1000):
                arcpy.FeatureClassToFeatureClass_conversion(fc, pg_lt_1k, name)
                print("feature class {} has {} records and was placed in the "
                      " {} Feature Dataset".format(fcname, fc_count,"polygon_less_1k"))
            else:
                arcpy.FeatureClassToFeatureClass_conversion(fc, pg_gt_1k, name)
                print("feature class {} has {} records and was placed in the "
                      " {} Feature Dataset".format(fcname, fc_count,"polygon_great_1k"))





if __name__ == '__main__':
    main()
