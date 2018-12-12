#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      scragun
#
# Created:     21/02/2018
# Copyright:   (c) scragun 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import sys
import os
import time

timestart = time.time()
print ("starting the program")
arcpy.env.overwriteOutput

def main():
    global iteration
    global feature_count

    #create new GDB

    arcpy.env.workspace = (r"E:\Programming\Week6\LabData")

    newGDBname = r"new.gdb"

    #Check to see if GDB exists
    if arcpy.Exists("new.gdb"):
        arcpy.Delete_management("new.gdb")

    arcpy.CreateFileGDB_management (arcpy.env.workspace, newGDBname)


    newGDBpath = os.path.join(arcpy.env.workspace, newGDBname)



    #revert to the corvalis GDB workspace

    arcpy.env.workspace = (r"E:\Programming\Week6\LabData\Corvallis.gdb")

    #get a list of the fc's that are in the GDB

    fc_list = arcpy.ListFeatureClasses()

    #loop through each and retrieve thier properties


    iteration = 0
    feature_count = 0
    for fc in fc_list:
        feature_count += 1
        description = arcpy.Describe(fc)
        fcname = description.name
        fcshape = description.shapetype
        print ("{} is a {}".format(fcname,fcshape))

        #print out the fc name and the shape for each fc

        #print ("{} is a {}".format(fcname,fcshape))

        #count the number of features in each fc

        get_fccount = arcpy.GetCount_management(fc)
        fccount = int(get_fccount.getOutput(0))

        #determine if the fc is of the type Point.  If so, process it

        if (fcshape == "Point"):

            if (fccount < 100):
                print ("feature class {} is of type {} and has < 100 rcords"
                        .format(fcname, fcshape, fccount))
            else:
                print ("feature class {} is of type {} and has > 100 records"
                        .format(fcname, fcshape, fccount))

                iteration += 1

                underline = "_"

                name = "{}{}{}".format(fcname, underline, fccount)
                arcpy.FeatureClassToFeatureClass_conversion(fc,newGDBpath, name)



if __name__ == '__main__':
    main()


    timeend = time.time()
    timetotal = timeend - timestart
    minutes = int(timetotal/60)
    x = timetotal%60
    xx = feature_count

    print ("{} features were examined and {}"
            " of them were points" .format (feature_count, iteration))
    outstring = "The script completed in {}.{} minutes."
    print(outstring.format(minutes, int(x)))

    sys.exit()








