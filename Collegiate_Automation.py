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
        # since path below might not  be existing in your system with the said file name required
        configFileLocation=r"E:\GIS Data\RED-BULL\Mapping Portal Enhancement - Release 1.0\4. Implementation\4.1 CODE\GIS\Collegiate_Definition_Automation\Python_Scripts\GitHub\Collegiate_Automation\Config.ini"

    ##Read from config file
    Configurations.setParameters(configFileLocation)

    ##set global variables
    #Workspace and workspace related variables
    workspace = Configurations.Configurations_workspace
    storesFeatureClass =Configurations.Configurations_storesFeatureClass
    campusBoundaryFeatureClass = Configurations.Configurations_campusBoundaryFeatureClass

    #Collegiate Defintion domains creation  variables
    fieldname = Configurations.Configurations_fieldname #Name of field to add to the feature class
    fieldAlias = Configurations.Configurations_fieldAlias #Field Alias to the field name specified above
    fieldType = Configurations.Configurations_fieldType



    ##Set variables for Bullring module
    #Initial variables initializing
    BullsRing.BR_workspace =  workspace
    BullsRing.BR_storesFeatureClass = storesFeatureClass
    BullsRing.BR_collegiateField = fieldname
    BullsRing.BR_BRMDL = Configurations.Configurations_BRMDL

    # Set required add domain parameters
    domainName = Configurations.Configurations_domainName
    domainDescription = Configurations.Configurations_domainDescription
    #fieldType as defined above
    domainType = Configurations.Configurations_domainType

    #Parameters for the add join
    BullsRing.BR_joinField1 = Configurations.Configurations_collegiateJoinField
    BullsRing.BR_joinTable = BullsRing.BR_BRMDL
    BullsRing.BR_joinField2 = Configurations.Configurations_BRMDLJoinField
    BullsRing.BR_field = Configurations.Configurations_bullRingClass

    #Buffer paramaeters
    BullsRing.BR_campusBoundaryFeatureClass = campusBoundaryFeatureClass
    BullsRing.BR_campusBoundaryBuffer = campusBoundaryFeatureClass+"_buffer"
    BullsRing.BR_bufferDistance = 0
    BullsRing.BR_distanceField = Configurations.Configurations_distancefield
    BullsRing.BR_linearUnit = Configurations.Configurations_linearUnit
    BullsRing.BR_sideType = Configurations.Configurations_sideType
    BullsRing.BR_endType = Configurations.Configurations_endType

    #Parametres for Bull ring coded value for collegiate definition bull ring
    bullsEye = Configurations.Configurations_bullsEye
    bullsRing = Configurations.Configurations_bullsRing
    nonCollegiate = Configurations.Configurations_nonCollegiate

    #Store all the domain values in a dictionary with the domain code as the "key" and the
    #domain description as the "value" (domainDictionary[code])
    domainDictionary = {int(bullsEye) : "Bulls Eye", int(bullsRing) : "Bulls Ring", int(nonCollegiate) : "Non Collegiate"}

    ##  Main script block
    ##-------------------------

    #Set workspace variable
    #Supports enterprise, file geodatabases
    env.workspace = workspace


    try:

        #Backup geocodes feature layer
        Utility_Functions.backupInitialStoresFC (workspace,storesFeatureClass)

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


    #Call intersect to get collegiate bull eyes
    try:

        #Set Bulls Eye Parameter
        BullsEye.BE_bullsEye =bullsEye

        #Call function here
        BullsEye.intersect(workspace,storesFeatureClass,fieldname, campusBoundaryFeatureClass, bullsEye)

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
        #set some parameters here

        BullsRing.BR_nonCollegiate = nonCollegiate
        BullsRing.BR_bullsEye = bullsEye
        BullsRing.BR_bullsRing = bullsRing

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

