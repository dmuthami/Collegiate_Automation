#-------------------------------------------------------------------------------
# Name:        Bulls Ring Module
# Purpose:
#
# Author:      dmuthami
#
# Created:     26/09/2014
# Copyright:   (c) dmuthami 2014
# Licence:     GPL
#-------------------------------------------------------------------------------

#Import arcpy module
import os, sys
import arcpy
import traceback
from arcpy import env
import numpy
#Logging module
import logging
##Custom module containing functions
import Configurations

##define variables here
BR_workspace = ""
BR_storesFeatureClass = ""
BR_storesFeatureLayer = ""
BR_collegiateField = ""
BR_BRMDL = ""

BR_joinField1 = ""
BR_joinTable = ""
BR_joinField2 = ""
BR_field = ""

BR_bullRingClass = "" #Local variable for this module only

#Code value for bullRing
BR_codedValue = 1

#Buffer parameters
BR_campusBoundaryFeatureClass = "" #variable pointing to the campus boundary
BR_campusBoundaryBuffer = "" #variable pointing to the campus boundary buffer
BR_bufferDistance = "" #variable pointing to the buffer distance as per Bull Ring Master Data List (BRMDL)
BR_distanceField = ""
BR_linearUnit = ""
BR_sideType = ""
BR_endType = ""

##Define local functions

def joinStoresAndBRMDL(_log,workspace,storesFeatureClass, joinField1, joinTable, joinField2):
    try:
        # Disable qualified field names which is the default for add join tool
        env.qualifiedFieldNames = False

        # Join two feature classes by the Channel field and only carry
        # over the ll3 segment, bullring class and distance fields
        arcpy.JoinField_management (storesFeatureClass, joinField1, joinTable, joinField2)

    except:
            ## Return any Python specific errors and any error returned by the geoprocessor
            ##
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\n joinStoresAndBRMDL Function : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                    str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n" +\
                    "Line {0}".format(tb.tb_lineno)
            msgs = "Geoprocessing  Errors :\n" + arcpy.GetMessages(2) + "\n"

            ##Add custom informative message to the Python script tool
            arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
            arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

            ##For debugging purposes only
            ##To be commented on python script scheduling in Windows _log
            print pymsg
            print "\n" +msgs

    return ""

def createUniqueBRMD(_log,table,field):
    try:
        data = arcpy.da.TableToNumPyArray(table, [field])
        uniqueBullringClassList = numpy.unique(data[field])

    except:
            ## Return any Python specific errors and any error returned by the geoprocessor
            ##
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\n createUniqueBRMD Function : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                    str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n" +\
                    "Line {0}".format(tb.tb_lineno)
            msgs = "Geoprocessing  Errors :\n" + arcpy.GetMessages(2) + "\n"

            ##Add custom informative message to the Python script tool
            arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
            arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

            ##For debugging purposes only
            ##To be commented on python script scheduling in Windows _log
            print pymsg
            print "\n" +msgs
            _log.info( pymsg)
            _log.info(msgs)

    return uniqueBullringClassList

def createCampusBuffer(_log,campusBoundaryFeatureClass, campusBoundaryBuffer, bufferDistance, linearUnit, sideType, endType):
    try:
        # Buffer the campus boundary based on the bullring class buffer distance provided
        bufferDistance2 = str(bufferDistance) + " " + str(linearUnit)

        # Run buffer analysis tool
        arcpy.Buffer_analysis(campusBoundaryFeatureClass, campusBoundaryBuffer, bufferDistance2, sideType, endType)

    except:
            ## Return any Python specific errors and any error returned by the geoprocessor
            ##
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\n createCampusBuffer Function : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
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
            _log.info(pymsg)
            _log.info(msgs)

    return ""

def intersectBullsRing(_log, workspace,storesFeatureLayer,collegiateField, campusBoundaryBuffer, bullRingClass):
    try:
        #Do an intersect to get Bulls Rings collegiate stores
        arcpy.SelectLayerByLocation_management(storesFeatureLayer, 'intersect', campusBoundaryBuffer, "","SUBSET_SELECTION")

        # Determine the number of selected features in the stores feature layer
        # Syntax: arcpy.GetCount_management (in_rows)
        featCount = arcpy.GetCount_management(storesFeatureLayer)

        message = "Number of store features: {0}  that intersect bull Ring class {1}".format(featCount,bullRingClass)
        _log.info(message)
        print message

        #Define the fields object for the update cursor
        fields = (collegiateField)

        #Run an update cursor on the collegiate definition field name

        updateCollegiateFieldWithBullsRing(_log,workspace,storesFeatureLayer, fields, Configurations.Configurations_bullsRing)

    except:
            ## Return any Python specific errors and any error returned by the geoprocessor
            ##
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\n intersectBullsRing Function : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                    str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n" +\
                    "Line {0}".format(tb.tb_lineno)
            msgs = "Geoprocessing  Errors :\n" + arcpy.GetMessages(2) + "\n"

            ##Add custom informative message to the Python script tool
            arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
            arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

            ##For debugging purposes only
            ##To be commented on python script scheduling in Windows
            _log.info(pymsg)
            _log.info(msgs)
            print pymsg
            print "\n" +msgs
    return ""

def updateCollegiateFieldWithBullsRing(_log,workspace,storesFeatureLayer, fields, updateValue):
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
                row[0] = int(updateValue) # need to be as per the coded values of the domain called collegiate_definition

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
            pymsg = "PYTHON ERRORS:\n updateCollegiateFieldWithBullsRing Function : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                    str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n" +\
                    "Line {0}".format(tb.tb_lineno)
            msgs = "Geoprocessing  Errors :\n" + arcpy.GetMessages(2) + "\n"

            ##Add custom informative message to the Python script tool
            arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
            arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

            ##For debugging purposes only
            ##To be commented on python script scheduling in Windows _log,
            print pymsg
            print "\n" +msgs

			#Log file
            _log.info( pymsg)
            _log.info(msgs)

    return ""

def updateIPEDSID(_log,workspace,storesFeatureClass,campusBoundary,fields):
    try:
        # execute the function
        arcpy.Near_analysis(storesFeatureClass, campusBoundary)

        #Create feature layer
        storesFeatureLayer = storesFeatureClass + "_Lyr"

        # Create a feature layer from the vegtype featureclass
        arcpy.MakeFeatureLayer_management (storesFeatureClass,  storesFeatureLayer)

        # Join the feature layer to a table
        arcpy.JoinField_management(storesFeatureLayer, "NEAR_FID", campusBoundary, "OBJECTID",fields[0])

        ##Select non-bull ring features from feature layer
        #collegiate definition
        collegiateFieldwithDelimeter = arcpy.AddFieldDelimiters(Configurations.Configurations_workspace, \
            Configurations.Configurations_fieldname)

        # Select  Bulls eye records and bulls ring records only
        collegiateSQLExp =  collegiateFieldwithDelimeter + " = " + str(Configurations.Configurations_bullsEye) + " Or " + \
            collegiateFieldwithDelimeter + " = " + str(Configurations.Configurations_bullsRing)

        # Select desired features from veg_layer
        arcpy.SelectLayerByAttribute_management(storesFeatureLayer, "NEW_SELECTION", collegiateSQLExp)

        ## Below code
        ## Make (Non Collegiate) IPEDS null
        ##

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
                row[1] = row[0] #IPEDS_ID from campus boundarr into  new IPEDS_ID (ipeds_id2) for export into textfile or into the sde table

                # Update the cursor with the updated row object that contains now the new record
                cursor.updateRow(row)

        # Stop the edit operation.and commit the changes
        edit.stopOperation()

        # Stop the edit session and save the changes
        #Compulsory for release of locks arising from edit session. NB. Singleton principle is observed here
        edit.stopEditing(True)

        #delete the in memory feature layer just in case we need to recreate
        # feature layer or maybe run script an additional time
        arcpy.Delete_management(storesFeatureLayer)

    except:
            ## Return any Python specific errors and any error returned by the geoprocessor
            ##
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\n updateIPEDSID() Function : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                    str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n" +\
                    "Line {0}".format(tb.tb_lineno)
            msgs = "Geoprocessing  Errors :\n" + arcpy.GetMessages(2) + "\n"

            ##Add custom informative message to the Python script tool
            arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
            arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

            ##For debugging purposes only
            ##To be commented on python script scheduling in Windows _log
            print pymsg
            print "\n" +msgs
            _log.info( pymsg)
            _log (msgs)

    return ""

def executeBullsRings(_log):
    try:
        ## Set overwrite in workspace to true
        arcpy.env.overwriteOutput = True

        #variable pointer to the in-memory feature layer
        storesFeatureLayer = Configurations.Configurations_storesFeatureClass + '_lyr'

        ##Check that existing feature class doesn't have fields of Bull Ring Master Data List
        ##  If it has then delete them since they shall be appended in the next step by joinField method

        #Join Field of Bulls Ring Master Data List to the potential bulls ring feature layer/class
        joinStoresAndBRMDL(_log,Configurations.Configurations_workspace,Configurations.Configurations_storesFeatureClass, \
            Configurations.Configurations_collegiateJoinField, Configurations.Configurations_BRMDL, \
             Configurations.Configurations_BRMDLJoinField)

        # create a data dictionary from bull ring class and distance from
        #  Bull Ring Master Data list (BRMDL)
        list = createUniqueBRMD(_log,Configurations.Configurations_BRMDL,Configurations.Configurations_bullRingClass)

        #For each unique distance
        for item in list:
            #Handle exception just in case an item brings issues
            try:
                #check if item is a number in some cases its not a number and might cause some unexpected results in the query
                if numpy.isnan(item) == False:

                    ##Select non-bull ring features from feature layer
                    #collegiate definition
                    collegiateFieldwithDelimeter = arcpy.AddFieldDelimiters(Configurations.Configurations_workspace, \
                        Configurations.Configurations_fieldname)

                    # Select  Bulls eye records
                    collegiateSQLExp =  collegiateFieldwithDelimeter + " = " + str(Configurations.Configurations_bullsEye)

                    # Make a layer from stores feature class
                    arcpy.MakeFeatureLayer_management(Configurations.Configurations_storesFeatureClass, storesFeatureLayer)

                    #make a fresh selection here
                    arcpy.SelectLayerByAttribute_management(storesFeatureLayer, "NEW_SELECTION", collegiateSQLExp)

                    #Switch selection to select only non Bulls eye record
                    arcpy.SelectLayerByAttribute_management(storesFeatureLayer, "SWITCH_SELECTION")

                    # Determine the number of selected features in the stores feature layer
                    # Syntax: arcpy.GetCount_management (in_rows)
                    featCount = arcpy.GetCount_management(storesFeatureLayer)
                    msg = "Number of features: {0}".format(featCount)
                    print msg
                    _log.info("executeBullsRings() Function:"+ msg)

                    ##From Selection above,Select only non Bulls eye records for the bull ring held in variable named "item"
                    bullRingClassFieldwithDelimeter = arcpy.AddFieldDelimiters(Configurations.Configurations_workspace, \
                        Configurations.Configurations_bullRingClass)

                    collegiateSQLExp = bullRingClassFieldwithDelimeter + " = " + str(item)

                    #make a selection from existing selection here for the specific bull ring class
                    arcpy.SelectLayerByAttribute_management(storesFeatureLayer, "SUBSET_SELECTION", collegiateSQLExp)

                    ##Get buffer distance from the feature class
                    # Create an expression with proper delimiters for the bull ring class
                    expression = arcpy.AddFieldDelimiters(Configurations.Configurations_workspace, \
                     Configurations.Configurations_bullRingClass) + ' = ' + str(item)

                    bufferDistance = 0;#initialize variable first

                    # Use SearchCursor with list comprehension to return a
                    # unique set of values in the specified field

                    values = [row[0] for row in arcpy.da.SearchCursor(Configurations.Configurations_storesFeatureClass, [Configurations.Configurations_distancefield] \
                        , where_clause=expression)]

                    #Get unique values
                    uniqueValues = set(values)

                    #Get only top distance value
                    bufferDistance = float(uniqueValues.pop())
                    ##print(uniqueValues)

                    ##create buffer feature layer from the campus boundaries

                    #Check that buffer distance is greater than 1
                    if float(bufferDistance) > 0.0 :



                        #Call function to create campus buffer
                        createCampusBuffer(_log, Configurations.Configurations_campusBoundaryFeatureClass, BR_campusBoundaryBuffer, \
                         bufferDistance, Configurations.Configurations_linearUnit, \
                         Configurations.Configurations_sideType, Configurations.Configurations_endType)

                        ##intersect (with non bullring feature layer for the correct channel/segment) and if intersect returns something useful then set collegiate field to 1

                        #Pass Bull ring Class variable
                        bullRingClass = str(item)

                        #Updates of the selected records is done by calling another function within intersect called "updateCollegiateFieldWithBullsRing"
                        intersectBullsRing(_log, Configurations.Configurations_workspace, \
                            storesFeatureLayer,Configurations.Configurations_fieldname, \
                                BR_campusBoundaryBuffer, bullRingClass)

                    print ""
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
                ##To be commented on python script scheduling in Windows _log
                print pymsg
                print "\n" +msgs
                _log.info( pymsg)
                _log.info(msgs)
            ##Try except contract is in the loop

        ##Select the non bulls eye and non bulls ring records and set
        ##collegiate field to non

        #collegiate definition
        collegiateFieldwithDelimeter = arcpy.AddFieldDelimiters(Configurations.Configurations_workspace,Configurations.Configurations_fieldname)

        #make selection for bulls eye and bulls ring
        collegiateSQLExp =  collegiateFieldwithDelimeter + " = " + str(Configurations.Configurations_bullsEye) + " or " + \
         collegiateFieldwithDelimeter + " = " + str(Configurations.Configurations_bullsRing)


        #make a fresh selection here SWITCH_SELECTION
        arcpy.SelectLayerByAttribute_management(storesFeatureLayer, "NEW_SELECTION", collegiateSQLExp)

        #Switch selection to pick out non-collegiate records only

        arcpy.SelectLayerByAttribute_management(storesFeatureLayer, "SWITCH_SELECTION")

        #set update value to 2 or figure defined in Config.ini for non-collegiate records
        codedValue = str(Configurations.Configurations_nonCollegiate)

        #Call function to update collegiate field to value 2
        updateCollegiateFieldWithBullsRing(_log,Configurations.Configurations_workspace,storesFeatureLayer, \
            Configurations.Configurations_fieldname,  codedValue)

        #delete the in memory feature layer just in case we need to recreate
        # feature layer or maybe run script an additional time
        arcpy.Delete_management(storesFeatureLayer)


    except:
            ## Return any Python specific errors and any error returned by the geoprocessor
            ##
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\n executeBullsRings Function : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                    str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n" +\
                    "Line {0}".format(tb.tb_lineno)
            msgs = "Geoprocessing  Errors :\n" + arcpy.GetMessages(2) + "\n"

            ##Add custom informative message to the Python script tool
            arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
            arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

            ##For debugging purposes only
            ##To be commented on python script scheduling in Windows _log
            print pymsg
            print "\n" +msgs
            _log.info( pymsg)
            _log.info(msgs)
    return ""
##---End of definition for local functions

def main():
    pass

if __name__ == '__main__':
    main()

    #Run executor
    executeBullsRings(_log)

    #Updates IPEDSID
    updateIPEDSID(_log,workspace,storesFeatureClass,campusBoundary,fields)