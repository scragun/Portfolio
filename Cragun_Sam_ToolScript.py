#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      scragun
#
# Created:     08/04/2018
# Copyright:   (c) scragun 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import sys
import os

def main():
    #workspace
    arcpy.env.overwriteOutput = True

    arcpy.env.workspace = arcpy.GetParameterAsText(0)


    #shapefiles to work with
    PD_num = arcpy.GetParameterAsText(1)
    landfills = arcpy.GetParameterAsText(2)
    rivers = arcpy.GetParameterAsText(3)
    roads = arcpy.GetParameterAsText(4)
    vapdbounds = arcpy.GetParameterAsText(5)


    #select buffer distances
    river_buffer = arcpy.GetParameterAsText(6)
    road_buffer = arcpy.GetParameterAsText(7)

    #create GDB
    name = 'landfillGDB_{}.gdb'.format(PD_num)
    path = 'C:\GISc450\Landfilltool'


    pathGDB = os.path.join(path, name)
##    if arcpy.Exists(name):
##        arcpy.Delete_management(name)

    arcpy.CreateFileGDB_management(path, name)

    #make layer for pd number
    #vapd_boundary_out = r'C:\GISc450\Landfilltool\vapd_boundary_out{}.shp'.format(PD_num)
    vapd_lyr =  r'C:\GISc450\Landfilltool\vapd_lyr'
    arcpy.MakeFeatureLayer_management(vapdbounds, vapd_lyr)

    #make clip
    arcpy.management.SelectLayerByAttribute(vapd_lyr, "NEW_SELECTION", "PD_NO = '{}'".format(PD_num))
    river_clip = arcpy.Clip_analysis(rivers, vapd_lyr, r'C:\GISc450\Landfilltool\river_clip')
    road_clip = arcpy.Clip_analysis(roads, vapd_lyr, r'C:\GISc450\Landfilltool\road_clip')
    landfill_clip = arcpy.Clip_analysis(landfills, vapd_lyr, r'C:\GISc450\Landfilltool\landfill_{}'.format(PD_num))

    #buffer
    river_clip_buffer = arcpy.analysis.Buffer(river_clip, r"C:\GISc450\Landfilltool\river_buffer_{}".format(PD_num), "{} Meters".format(river_buffer), "FULL", "ROUND","NONE", None, "PLANAR")
    road_clip_buffer = arcpy.analysis.Buffer(road_clip, r"C:\GISc450\Landfilltool\road_buffer_{}".format(PD_num), "{} Meters".format(road_buffer), "FULL", "ROUND","NONE", None, "PLANAR")
    #make layer
    landfill_clip_lyr = r'C:\GISc450\Landfilltool\landfill_clip_lyr'
    landfill_clip_lyr = arcpy.MakeFeatureLayer_management(landfill_clip, landfill_clip_lyr)
    river_buffer_lyr =  r'C:\GISc450\Landfilltool\river_buffer_lyr'
    river_buffer_lyr = arcpy.MakeFeatureLayer_management(river_clip_buffer, river_buffer_lyr)
    road_buffer_lyr =  r'C:\GISc450\Landfilltool\road_buffer_lyr'
    road_buffer_lyr = arcpy.MakeFeatureLayer_management(road_clip_buffer, road_buffer_lyr)
    river_clip_lyr = r'C:\GISC450\Landfilltool\river_clip_lyr'
    river_clip_lyr = arcpy.MakeFeatureLayer_management(river_clip, river_clip_lyr)


    #select by location
    river_intersect = arcpy.management.SelectLayerByLocation(landfill_clip_lyr, "INTERSECT", river_clip_lyr, "150 Meters", "NEW_SELECTION", "NOT_INVERT")
    #river_intersect = arcpy.management.SelectLayerByLocation(landfill_clip_lyr, "INTERSECT", river_buffer_lyr, 0, "NEW_SELECTION" "")
    road_intersect = arcpy.management.SelectLayerByLocation(landfill_clip_lyr, "INTERSECT", road_buffer_lyr, 0, "NEW_SELECTION", "")

    #export to GDB
    aaaa = arcpy.CopyFeatures_management(landfill_clip, r'C:\GISc450\Landfilltool\landfills{}'.format(PD_num))
    arcpy.FeatureClassToGeodatabase_conversion(aaaa, pathGDB)
    rd = arcpy.CopyFeatures_management(road_intersect, r'C:\GISc450\Landfilltool\road_intersection')
    arcpy.FeatureClassToGeodatabase_conversion(rd, pathGDB)
    rv = arcpy.CopyFeatures_management(river_intersect, r'C:\GISc450\Landfilltool\river_intersection')
    arcpy.FeatureClassToGeodatabase_conversion(rv, pathGDB)
    arcpy.FeatureClassToGeodatabase_conversion(river_clip_buffer, pathGDB)
    arcpy.FeatureClassToGeodatabase_conversion(road_clip_buffer, pathGDB)
    arcpy.FeatureClassToGeodatabase_conversion(landfill_clip, pathGDB)


    #getcount
    landfillclipcount = arcpy.GetCount_management(landfill_clip)
    road_landfill_count = arcpy.GetCount_management(rd)
    landfillcount = arcpy.GetCount_management(landfills)
    a = int(landfillclipcount.getOutput(0))
    c = int(road_landfill_count.getOutput(0))
    outroad = a - c

    #try river again because it doesn't work
    riverclip = arcpy.Clip_analysis(rivers, vapd_lyr, r'C:\GISc450\Landfilltool\riverclip')
    rivercliplayer = r'C:\GISC450\Landfilltool\rivercliplayer'
    river_buffer_lyr = arcpy.MakeFeatureLayer_management(riverclip, rivercliplayer)
    riverselect = arcpy.management.SelectLayerByLocation(landfill_clip_lyr, "INTERSECT", rivercliplayer, "150 Meters", "NEW_SELECTION", "NOT_INVERT")
    riverselection = arcpy.CopyFeatures_management(riverselect, r'C:\GISc450\Landfilltool\riverclip_{}'.format(PD_num))
    arcpy.FeatureClassToGeodatabase_conversion(riverselection, pathGDB)
    river_landfill_count = arcpy.GetCount_management(riverselection)
    b = int(river_landfill_count.getOutput(0))
    outriver = a - b


    #final clip
    clip = r'C:\GISc450\Landfilltool\river_road_clip_{}'.format(PD_num)
    clip = arcpy.analysis.Clip(rd, riverselection,r'C:\GISc450\Landfilltool\clip', None)
    arcpy.FeatureClassToGeodatabase_conversion(clip, pathGDB)
    clipcount = arcpy.GetCount_management(clip)

    #output
    arcpy.AddMessage("Run summary:")
    arcpy.AddMessage ("  where PD_NO = '{}'".format(PD_num))
    arcpy.AddMessage ("  PD {} selected".format(PD_num))
    arcpy.AddMessage ("  {} landfills were located in PD {}".format(landfillclipcount, PD_num))
    arcpy.AddMessage ("Criteria road distance = {}".format(road_buffer))
    arcpy.AddMessage ("Criteria river distance = {}".format(river_buffer))
    arcpy.AddMessage ("Road Buffer is complete")
    arcpy.AddMessage ("  {} landfills are within the {} meter road buffer".format(road_landfill_count, road_buffer))
    arcpy.AddMessage ("  {} landfills located more than {} meters from a road".format(outroad, road_buffer))
    arcpy.AddMessage ("River Buffer is complete")
    arcpy.AddMessage ("  {} landfills are within the {} meter river buffer".format(river_landfill_count, river_buffer))
    arcpy.AddMessage ("  {} landfills located more than {} meters from a river".format(outriver, river_buffer))
    arcpy.AddMessage ("*** {} landfills met the distance critera***".format(clipcount))

if __name__ == '__main__':
    main()
