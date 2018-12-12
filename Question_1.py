#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      boswi
#
# Created:     22/02/2018
# Copyright:   (c) boswi 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------





import arcpy
import sys
import os
import time

timestart = time.time()
print("starting the program")

arcpy.env.overwriteOutput

def main():
    global feature_count

    #Create New GDB

arcpy.env.workspace = (r"E:\GIS Programming\Week_6\LabData")

newGDBname = r"new.gdb"
arcpy.CreateFileGDB_management(arcpy.env.workspace, "new.gdb")

newGDBpath = os.path.join(r"E:\GIS Programming\Week_6\LabData\new.gdb")

    #Revert to the Corvalis GDB worksapce

arcpy.env.workspace = (r"E:\GIS Programming\Week_6\Labdata\Corvallis.gdb")

    #Get a list of the fc's in corvallis.gdb

fc_list = arcpy.ListFeatureClasses()

    #Loop through each and retrieve their properties

iteration = 0
feature_count = 0
for fc in fc_list:
    feature_count += 1
    description = arcpy.Describe(fc)
    fcname = description.name
    fcshape = description.shapetype

    # Print out the fc name and shape for each fc

    print("{} is a {}".format(fcname,fcshape))

    # Count the number of feautres in eash fc
    get_fc_count = arcpy.GetCount_management(fc)
    fc_count = int(get_fc_count.getOutput(0))

    # Determine if the fc is of type point.  If so, process it
    if (fcshape == "Point"):
        if (fc_count < 100):
            print("feature class {} is of type {} and has < "
                      " 100 records".format(fcname, fcshape, fc_count))
        else:
            print(" feature class {} is of type {} and has >"
                      "100 records".format(fcname, fcshape, fc_count))
            iteration += 1
            underline = "_"
            name = "{}{}{}".format(fcname, underline, iteration)
            arcpy.FeatureClassToFeatureClass_conversion(fc,newGDBpath, name)


if __name__ == '__main__':
    main()

    endtime = time.time()
    totaltime = endtime - timestart
    minutes = int(totaltime / 60)
    x = totaltime % 60
    xx = feature_count

    print("{} features were examined and {} of them were"
          " points".format(feature_count, iteration))

    outstring = ("The script completed in {}.{} minutes.")
    print(outstring.format(minutes, int(x)))

sys.exit()


