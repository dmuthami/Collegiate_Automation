#-------------------------------------------------------------------------------
# Name:        BullsEye Module
# Purpose:
#
# Author:      dmuthami
#
# Created:     25/09/2014
# Copyright:   (c) dmuthami 2014
# Licence:     GPL
#-------------------------------------------------------------------------------

##Import arcpy here
import os, sys
import arcpy
import traceback
from arcpy import env

##Custom module containing functions
import Configurations
from BullsRing import updateIPEDSID as updateIPEDSIDForBullsEye

#Configurations.Configurations_bullsEye;

## Interest geocodes with campus boundary
## gets bulls eye geocodes
## Update collegiate definition field to 0
## and hit out
##
def intersect(workspace,storesFeatureClass,collegiate_fieldname, campusBoundaryFeatureClass, bullsEye):
    try:
        try:
            ##Try creating the below layer. If it exists in memory then an exception will be thrown
            #variable pointer to the in-memory feature layer
            storesFeatureLayer = storesFeatureClass + '_lyr'

        except:
            try:
                #delete the in memory feature layer
                # something terrible must have happened since we run the tool and now we have to destroy the
                # the memory imprint of the feature layer
                arcpy.Delete_management(storesFeatureLayer)

                #variable pointer to the in-memory feature layer
                storesFeatureLayer = storesFeatureClass + '_lyr'

            except:
                ## Return any Python specific errors and any error returned by the geoprocessor
                ##
                tb = sys.exc_info()[2]
                tbinfo = traceback.format_tb(tb)[0]
                pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                        str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
                msgs = "Geoprocessing  Errors :\n" + arcpy.GetMessages(2) + "\n"

                ##Add custom informative message to the Python script tool
                arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
                arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

                ##For debugging purposes only
                ##To be commented on python script scheduling in Windows
                print pymsg
                print "\n" +msgs

        # Make a layer from stores feature class
        arcpy.MakeFeatureLayer_management(storesFeatureClass, storesFeatureLayer)

        #Do an intersect to get Bulls Rings collegiate stores
        arcpy.SelectLayerByLocation_management(storesFeatureLayer, 'intersect', campusBoundaryFeatureClass)

        #Define the fields object for the update cursor
        fields = (collegiate_fieldname)

        #Run an update cursor on the collegiate definition field name
        domainsCodedValue = Configurations.Configurations_bullsEye

        #Call and update bulls eye
        updateCollegiateFieldWithBullsEye(workspace,storesFeatureLayer, fields,domainsCodedValue)

        #Call function to update the IPEDS ID
        updateIPEDSID(workspace,storesFeatureLayer,Configurations.Configurations_IPEDSFieldName,campusBoundaryFeatureClass, \
         Configurations.Configurations_CampusBoundaryIPEDSID)

        #delete the in memory feature layer just in case we need to recreate
        # feature layer or maybe run script an additional time
        arcpy.Delete_management(storesFeatureLayer)
    except:
            ## Return any Python specific errors and any error returned by the geoprocessor
            ##
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\n intersect Function : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                    str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n" +\
                    "Line {0}".format(tb.tb_lineno)
            msgs = "Geoprocessing  Errors :\n" + arcpy.GetMessages(2) + "\n"

            ##Add custom informative message to the Python script tool
            arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
            arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

            ##For debugging purposes only
            ##To be commented on python script scheduling in Windows
            print pymsg
            print "\n" +msgs

    return ""

def updateCollegiateFieldWithBullsEye(workspace,storesFeatureLayer, fields, domainsCodedValue):

    try:
        # Start an edit session. Must provide the workspace.
        edit = arcpy.da.Editor(workspace)

        # Edit session is started without an undo/redo stack for versioned data
        #  (for second argument, use False for unversioned data)
        #Compulsory for above feature class participating in a complex data such as parcel fabric
        edit.startEditing(False, False)

        # Start an edit operation
        edit.startOperation()

        #Update cursor goes here
        with arcpy.da.UpdateCursor(storesFeatureLayer, fields) as cursor:
            for row in cursor:# loops per record in the recordset and returns an array of objects
                ##Set bull ring value it is set to default
                ## This should be a data dictionary read from file
                row[0] = int(domainsCodedValue)
                # Update the cursor with the updated row object that contains now the new record
                cursor.updateRow(row)

        # Stop the edit operation.and commit the changes
        edit.stopOperation()

        # Stop the edit session and save the changes
        #Compulsory for release of locks arising from edit session. NB. Singleton principle is observed here
        edit.stopEditing(True)
    except:
            ## Return any Python specific errors and any error returned by the geoprocessor
            ##
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\n updateCollegiateFieldWithBullsEye Function : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                    str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n" +\
                    "Line {0}".format(tb.tb_lineno)
            msgs = "Geoprocessing  Errors :\n" + arcpy.GetMessages(2) + "\n"

            ##Add custom informative message to the Python script tool
            arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
            arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

            ##For debugging purposes only
            ##To be commented on python script scheduling in Windows
            print pymsg
            print "\n" +msgs

    return ""

#Function calls another module that updates the IPEDS ID
def updateIPEDSID(workspace,storesFeatureLayer,IPEDSID,campusBoundaryBuffer, campusBoundaryIPEDS):

    #Function calls another module that updates the IPEDS ID
    updateIPEDSIDForBullsEye(workspace,storesFeatureLayer,IPEDSID,campusBoundaryBuffer, campusBoundaryIPEDS)

    return ""
##-------------Main----------------
def main():
    pass

if __name__ == '__main__':
    main()
    ##intersect
    intersect(workspace,storesFeatureClass,collegiate_fieldname, campusBoundaryFeatureClass)
