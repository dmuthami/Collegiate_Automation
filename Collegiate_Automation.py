######################################################################
## Update Stand No Script
## Attach script in ArcMap in a custom toolbox
## Run script as a script tool
##
##Challenge:Create Geoprocessing service for running on the web.
##
######################################################################

##  Compute Stand No
##  Select OBJECTID, Stand_No and Local_Authority ID Fields from a parcels feature class that participates in
##  parcel fabric
##  Need to obtain edit lock on the respective feature dataset/parcel fabric

##  Import ArcPy module: Provides access to ArcGIS powerful ArcObjects
##  Import sys module : module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter
##  Import os modules: This module provides a portable way of using operating system dependent functionality e.g writing files
##  Import traceback :modules for debugging/ module provides a standard interface to extract, format and print stack traces of Python programs

import os, sys
import arcpy
import traceback
from arcpy import env

##Custom module containing functions
import Configurations
import Utility_Functions
import BullsEye
import BullsRing

##Set the overwriteOutput environment setting to True
##Comment out line in script to overwrite data
#env.overwriteOutput = True

try:
    ##Obtain script parameter values
    ##location for configuration file
    ##Acquire it as a parameter either from terminal, console or via application
    configFileLocation=arcpy.GetParameterAsText(0)#Get from console or GUI being user input
    if configFileLocation =='': #Checks if supplied parameter is null
        #Defaults to below hardcoded path if the parameter is not supplied. NB. May throw exceptions if it defaults to path below
        configFileLocation=r"E:\GIS Data\RED-BULL\Mapping Portal Enhancement - Release 1.0\6. Delivery & Closing\8.7 CODE\GIS\Collegiate_Definition_Automation\Python_Scripts\Config.ini"

    ##Read from config file
    Configurations.setParamameters()

    ##set global variables
    #Workspace and workspace related variables
    workspace = Configurations.C_workspace
    storesFeatureClass =Configurations.C_storesFeatureClass
    campusBoundaryFeatureClass = Configurations.C_campusBoundaryFeatureClass

    #Collegiate Defintion domains creation  variables
    fieldname = Configurations.C_fieldname #Name of field to add to the feature class
    fieldAlias = Configurations.C_fieldAlias #Field Alias to the field name specified above
    fieldType = Configurations.C_fieldType



    ##Set variables for Bullring module
    #Initial variables initializing
    BullsRing.BR_workspace =  workspace
    BullsRing.BR_storesFeatureClass = storesFeatureClass
    BullsRing.BR_collegiateField = fieldname
    BullsRing.BR_BRMDL = "BRMDL"

    #Parameters for the add join
    BullsRing.BR_joinField1 = "channel"
    BullsRing.BR_joinTable = BullsRing.BR_BRMDL
    BullsRing.BR_joinField2 = "LL3_rec_segment"
    BullsRing.BR_field = "bullring_class"

    #Buffer paramaeters
    BullsRing.BR_campusBoundaryFeatureClass = campusBoundaryFeatureClass
    BullsRing.BR_campusBoundaryBuffer = campusBoundaryFeatureClass+"_buffer"
    BullsRing.BR_bufferDistance = 0
    BullsRing.BR_distanceField = "distance_mi"
    BullsRing.BR_linearUnit = "Miles"
    BullsRing.BR_sideType = "FULL"
    BullsRing.BR_endType = "ROUND"

    #Parametres for Bull ring coded value for collegiate definition bull ring
    BullsRing.BR_codedValue = 1

    ##  Main script block
    ##-------------------------

    #set workspace variable
    #Supports enterprise, file geodatabases
    env.workspace = workspace

    #Call function to add collegiate field
    try:
        Utility_Functions.addField(storesFeatureClass,fieldname,fieldAlias,fieldType)
    except:
        ## Return any Python specific errors and any error returned by the geoprocessor
        ##
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
        msgs = "Geoprocesssing  Errors :\n" + arcpy.GetMessages(2) + "\n"

        ##dd custom informative message to the Python script tool
        arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
        arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

        ##For debugging purposes only
        ##To be commented on python script scheduling in Windows
        print pymsg
        print "\n" +msgs

    #Call function to Create Domain, store domain values in a dictionary, and add domain to the
    # feature class and to the collegiate  field

    # Set required add domain parameters
    domainName = "collegiate_definition"
    domainDescription = "Collegiate Definition Types"
    #fieldType as defined above
    domainType = "CODED"

    try:
        #Call add domain function
        Utility_Functions.addDomain(workspace, domainName,domainDescription,fieldType, domainType)
    except:
        ## Return any Python specific errors and any error returned by the geoprocessor
        ##
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
        msgs = "Geoprocesssing  Errors :\n" + arcpy.GetMessages(2) + "\n"

        ##dd custom informative message to the Python script tool
        arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
        arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

        ##For debugging purposes only
        ##To be commented on python script scheduling in Windows
        print pymsg
        print "\n" +msgs


    #Store all the domain values in a dictionary with the domain code as the "key" and the
    #domain description as the "value" (domainDictionary[code])
    domainDictionary = {0 : "Bulls Eye", 1 : "Bulls Ring", 2 : "Non Collegiate"}

    try:
        #Call assign domain values function
        Utility_Functions.addValuesToDomain(workspace, domainName, domainDictionary)
    except:
        ## Return any Python specific errors and any error returned by the geoprocessor
        ##
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
        msgs = "Geoprocesssing  Errors :\n" + arcpy.GetMessages(2) + "\n"

        ##dd custom informative message to the Python script tool
        arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
        arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

        ##For debugging purposes only
        ##To be commented on python script scheduling in Windows
        print pymsg
        print "\n" +msgs


    #Call assign domain to field
    try:
        #Call function here
        Utility_Functions.assignDomainToField(storesFeatureClass,fieldname, domainName )
    except:
        ## Return any Python specific errors and any error returned by the geoprocessor
        ##
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
        msgs = "Geoprocesssing  Errors :\n" + arcpy.GetMessages(2) + "\n"

        ##dd custom informative message to the Python script tool
        arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
        arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

        ##For debugging purposes only
        ##To be commented on python script scheduling in Windows
        print pymsg
        print "\n" +msgs


    #Call intersect to get collegiate bull rings
    try:
        #Call function here
        BullsEye.intersect(workspace,storesFeatureClass,fieldname, campusBoundaryFeatureClass)
    except:
        ## Return any Python specific errors and any error returned by the geoprocessor
        ##
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
        msgs = "Geoprocesssing  Errors :\n" + arcpy.GetMessages(2) + "\n"

        ##Add custom informative message to the Python script tool
        arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
        arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

        ##For debugging purposes only
        ##To be commented on python script scheduling in Windows
        print pymsg
        print "\n" +msgs


    ##Run Bulls eye and non collegiate stores analysis
    try:
        BullsRing.executeBullsRings();
        print "Am done with Bull Ring"
    except:
        ## Return any Python specific errors and any error returned by the geoprocessor
        ##
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
        msgs = "Geoprocesssing  Errors :\n" + arcpy.GetMessages(2) + "\n"

        ##Add custom informative message to the Python script tool
        arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
        arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

        ##For debugging purposes only
        ##To be commented on python script scheduling in Windows
        print pymsg
        print "\n" +msgs

    print "\nCollegiate Definition run successfully"

except:
    ## Return any Python specific errors and any error returned by the geoprocessor
    ##
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
            str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
    msgs = "Geoprocesssing  Errors :\n" + arcpy.GetMessages(2) + "\n"

    ##dd custom informative message to the Python script tool
    arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
    arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

    ##For debugging purposes only
    ##To be commented on python script scheduling in Windows
    print pymsg
    print "\n" +msgs

