#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      dmuthami
#
# Created:     07/10/2014
# Copyright:   (c) dmuthami 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# Import system modules
import os, sys
import arcpy

from arcpy import env

## Export feature locations and attributes to an ASCII text file
def exportToASCII():

    ##Set the overwriteOutput environment setting to True
    env.overwriteOutput = True

    #Transfer Field Domain Descriptions
    env.transferDomains = True

    # Local variables...
    workspace = r"E:\GIS Data\RED-BULL\Mapping Portal Enhancement - Release 1.0\4. Implementation\4.1 CODE\GIS\Collegiate_Definition_Automation\Sample_Data\collegiate_sample_data.gdb"

    input_features = "geocode_result"

    export_ASCII = os.path.dirname(workspace) + "/collegiate_store.txt"

    try:
        # Set the current workspace (to avoid having to specify the full path to the feature classes each time)
        arcpy.env.workspace = workspace

        # Process: Export Feature Attribute to ASCII...
        arcpy.ExportXYv_stats(input_features, ["OBJECTID","store_id","collegiate", "bullring_class","distance_mi"], "SPACE", export_ASCII, "ADD_FIELD_NAMES")

    except:
            ## Return any Python specific errors and any error returned by the geoprocessor
            ##
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\n exportToASCII Function : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                    str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n" +\
                    "Line {0}".format(tb.tb_lineno)
            msgs = "Geoprocesssing  Errors :\n" + arcpy.GetMessages(2) + "\n"

            ##Add custom informative message to the Python script tool
            arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
            arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

            ##For debugging purposes only
            ##To be commented on python script scheduling in Windows
            print pymsg
            print "\n" +msgs

    return ""

def main():
    pass

if __name__ == '__main__':
    main()

    exportToASCII()
