######################################################################
##
##
## Collegiate Automation Main Module
##
##
######################################################################


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
    #If for any reason an exception is thrown here then subsequent code will not be executed
    Configurations.setParameters(configFileLocation)

    #Name of the buffer feature class
    BullsRing.BR_campusBoundaryBuffer = Configurations.Configurations_campusBoundaryFeatureClass + "_buffer"

    #Store all the domain values in a dictionary with the domain code as the "key" and the
    #domain description as the "value" (domainDictionary[code])
    domainDictionary = {int(Configurations.Configurations_bullsEye) : "Bulls Eye", \
        int(Configurations.Configurations_bullsRing) : "Bulls Ring", \
            int(Configurations.Configurations_nonCollegiate) : "Non Collegiate"}

    ##  Main script block
    ##-------------------------

    #Set workspace variable
    #Supports enterprise, file geodatabases
    env.workspace = Configurations.Configurations_workspace

    #Backup geocodes feature layer
    Utility_Functions.backupInitialStoresFC (Configurations.Configurations_workspace, \
        Configurations.Configurations_storesFeatureClass)

    #Call function to delete BRMDL fields in stores feature class
    Utility_Functions.deleteBRMDLFieldsInStores(Configurations.Configurations_BRMDL, \
        Configurations.Configurations_storesFeatureClass)

    #Call function to add collegiate field
    Utility_Functions.addField(Configurations.Configurations_storesFeatureClass, \
        Configurations.Configurations_fieldname,Configurations.Configurations_fieldAlias,Configurations.Configurations_fieldType)

    #Call function to add IPEDS ID Field
    Utility_Functions.addField(Configurations.Configurations_storesFeatureClass, \
        Configurations.Configurations_IPEDSFieldName,Configurations.Configurations_IPEDSFieldAlias, \
            Configurations.Configurations_IPEDSFieldType)

    #Call function to Create Domain, store domain values in a dictionary, and add domain to the
    # feature class and to the collegiate  field
    #Call add domain function
    Utility_Functions.addDomain(Configurations.Configurations_workspace, \
        Configurations.Configurations_domainName,Configurations.Configurations_domainDescription \
        ,Configurations.Configurations_fieldType, \
            Configurations.Configurations_domainType)

    #Call assign domain values function
    Utility_Functions.addValuesToDomain(Configurations.Configurations_workspace, \
        Configurations.Configurations_domainName, domainDictionary)

    #Call assign domain to field
    #Call function here
    Utility_Functions.assignDomainToField(Configurations.Configurations_storesFeatureClass, \
        Configurations.Configurations_fieldname, Configurations.Configurations_domainName)


    #Call intersect to get collegiate bull eyes
    #Call function here
    BullsEye.intersect(Configurations.Configurations_workspace, \
        Configurations.Configurations_storesFeatureClass,Configurations.Configurations_fieldname, \
            Configurations.Configurations_campusBoundaryFeatureClass, Configurations.Configurations_bullsEye)


    #Run Bulls eye and non collegiate stores analysis
    #execute Bulls Ring and non collegiate records too
    BullsRing.executeBullsRings();
    print "Am done with Bull Ring\n"

    #Export to text file#
    textFile = Configurations.Configurations_outputFolder + "/" +  \
     Configurations.Configurations_outputTextFile + ".txt"

    #Define text file export fields exportFields
    exportFieldsAlias = [Configurations.Configurations_OBJECTIDFieldAlias,Configurations.Configurations_storeIDFieldAlias, \
        Configurations.Configurations_fieldAlias, Configurations.Configurations_BullRingClassFieldAlias, \
            Configurations.Configurations_IPEDSFieldAlias]

    #Define export field field aliases. This are the column headers on the output text file
    exportFields = ["OBJECTID",Configurations.Configurations_storeIDField, \
        Configurations.Configurations_fieldname,  \
            Configurations.Configurations_bullRingClass,Configurations.Configurations_IPEDSFieldName]

    Utility_Functions.exportToTextfile(Configurations.Configurations_workspace, \
        Configurations.Configurations_storesFeatureClass, \
            exportFields, exportFieldsAlias,textFile)

    print "\nCollegiate Definition run successfully"

except:
    ## Return any Python specific errors and any error returned by the geoprocessor
    ##
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "PYTHON ERRORS:\n Main FunctionTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
            str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
    msgs = "Geoprocesssing  Errors :\n" + arcpy.GetMessages(2) + "\n"

    ##dd custom informative message to the Python script tool
    arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
    arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

    ##For debugging purposes only
    ##To be commented on python script scheduling in Windows
    print pymsg
    print "\n" +msgs

