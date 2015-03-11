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
import logging
import arcpy
import traceback
from arcpy import env
from datetime import datetime

##Custom module containing functions
import Configurations
import Utility_Functions
import BullsEye
import BullsRing
import OutputToSDETable


try:
    #Set-up logging
    logger = logging.getLogger('myapp')
    Configurations.Configurations_cat_logfile = os.path.join(os.path.dirname(__file__), 'cat_logfile.log')
    hdlr = logging.FileHandler(Configurations.Configurations_cat_logfile)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)

    msg ="\n------------------------------------------------------------------\n"+"Start Time : " + datetime.now().strftime("-%y-%m-%d_%H-%M-%S")+ "\n------------------------------------------------------------------\n"

    print msg
	#Logging
    logger.info(msg)

    ##Obtain script parameter values
    ##location for configuration file
    ##Acquire it as a parameter either from terminal, console or via application
    configFileLocation=arcpy.GetParameterAsText(0)#Get from console or GUI being user input
    if configFileLocation =='': #Checks if supplied parameter is null
        #Defaults to below hard coded path if the parameter is not supplied. NB. May throw exceptions if it defaults to path below
        # since path below might not  be existing in your system with the said file name required
        configFileLocation=r"C:\DAVID-MUTHAMI\GIS Data\RED-BULL\Mapping Portal Enhancement - Release 1.0\4. Implementation\4.1 CODE\GIS\Collegiate_Definition_Automation\Python_Scripts\GitHub\Collegiate_Automation\Config.ini"

    ##Read from config file
    #If for any reason an exception is thrown here then subsequent code will not be executed
    Configurations.setParameters(configFileLocation)

    #Name of the buffer feature class
    baseName =os.path.basename(Configurations.Configurations_campusBoundaryFeatureClass)

    baseNameList=  baseName.split(".") #Split by period
    baseName = baseNameList[int(len(baseNameList) -1)]#get last name
    #campusBoundaryFeatureClassNew = Configurations.Configurations_workspace +"/"+ baseName # Name of new intermediate featureclass to be created for campus boundary buffers
    campusBoundaryFeatureClassNew =  baseName # Name of new intermediate featureclass to be created for campus boundary buffers

    BullsRing.BR_campusBoundaryBuffer = campusBoundaryFeatureClassNew + "_buffer" #variable pointing to the campus buffer

    #Store all the domain values in a dictionary with the domain code as the "key" and the
    #domain description as the "value" (domainDictionary[code])
    domainDictionary = {int(Configurations.Configurations_bullsEye) : "BULLSEYE", \
        int(Configurations.Configurations_bullsRing) : "BULLSRING", \
            int(Configurations.Configurations_nonCollegiate) : "Non Collegiate"}

    ##  Main Script Block
    ##-------------------------

    #Set workspace variable
    #Supports enterprise, file geodatabases
    env.workspace = Configurations.Configurations_workspace

    #Backup geocodes feature layer and copy geocodes from scratch geodatabase to collegiate_scratch geodatabase
    Utility_Functions.backupInitialStoresFC (logger,Configurations.Configurations_workspace, \
        Configurations.Configurations_workspaceScratch,Configurations.Configurations_storesFeatureClass)

    #Call function to delete BRMDL fields in stores feature class
    Utility_Functions.deleteBRMDLFieldsInStores(logger,Configurations.Configurations_BRMDL, \
        Configurations.Configurations_storesFeatureClass)

    #Call function to add collegiate field
    Utility_Functions.addField(logger,Configurations.Configurations_storesFeatureClass, \
        Configurations.Configurations_fieldname,Configurations.Configurations_fieldAlias,Configurations.Configurations_fieldType)

    #Call function to add IPEDS ID Field
    Utility_Functions.addField(logger,Configurations.Configurations_storesFeatureClass, \
        Configurations.Configurations_IPEDSFieldName,Configurations.Configurations_IPEDSFieldAlias, \
            Configurations.Configurations_IPEDSFieldType)

    #Call function to Create Domain, store domain values in a dictionary, and add domain to the
    # feature class and to the collegiate  field
    #Call add domain function
    Utility_Functions.addDomain(logger, Configurations.Configurations_workspace, \
        Configurations.Configurations_domainName,Configurations.Configurations_domainDescription \
        ,Configurations.Configurations_fieldType, \
            Configurations.Configurations_domainType)

    #Call assign domain values function
    Utility_Functions.addValuesToDomain(logger, Configurations.Configurations_workspace, \
        Configurations.Configurations_domainName, domainDictionary)

    #Call assign domain to field
    #Call function here
    Utility_Functions.assignDomainToField(logger, Configurations.Configurations_storesFeatureClass, \
        Configurations.Configurations_fieldname, Configurations.Configurations_domainName)


    #Call intersect to get collegiate bull eyes
    #Call function here
    BullsEye.intersect(logger,Configurations.Configurations_workspace, \
        Configurations.Configurations_storesFeatureClass,Configurations.Configurations_fieldname, \
            Configurations.Configurations_campusBoundaryFeatureClass, Configurations.Configurations_bullsEye)


    #Run Bulls eye and non collegiate stores analysis
    #execute Bulls Ring and non collegiate records too
    BullsRing.executeBullsRings(logger);

	#Logging
    msg = 'Bull ring execution is successful'
    logger.info(msg)
    print msg+"\n"

    ##Apends IPEDSID into the stores/geocodes feature class
    #update IPEDSID
    BullsRing.updateIPEDSID(logger, Configurations.Configurations_workspace, \
        Configurations.Configurations_storesFeatureClass, \
            Configurations.Configurations_campusBoundaryFeatureClass, \
                [Configurations.Configurations_CampusBoundaryIPEDSID,Configurations.Configurations_IPEDSFieldName])#IPEDS_ID from campus boundary, new IPEDS_ID (ipeds_id2) created by script

    ##Prepare for output in tab delimited text file

    #Export to text file#
    currentDate = datetime.now().strftime("-%y-%m-%d_%H-%M-%S") # Current time
    textFile = Configurations.Configurations_outputFolder + "/" +  \
     Configurations.Configurations_outputTextFile + str(currentDate)+".txt"

    #Define text file export fields exportFields
    exportFieldsAlias = [Configurations.Configurations_OBJECTIDFieldAlias,Configurations.Configurations_storeIDFieldAlias, \
        Configurations.Configurations_fieldAlias, Configurations.Configurations_BullRingClassFieldAlias, \
            Configurations.Configurations_IPEDSFieldAlias]

    #Define export field field aliases. This are the column headers on the output text file
    exportFields = ["OBJECTID",Configurations.Configurations_storeIDField, \
        Configurations.Configurations_fieldname,  \
            Configurations.Configurations_bullRingClass,Configurations.Configurations_IPEDSFieldName]

    Utility_Functions.exportToTextfile(logger, Configurations.Configurations_workspace, \
        Configurations.Configurations_storesFeatureClass, \
            exportFields, exportFieldsAlias,textFile)

    ##Prepare for output in sde table
    #call function to output to SDE table
    OutputToSDETable.outputSDETable(logger)

    msg ='Collegiate Definition run successfully'
    logger.info(msg)
    print "\n"+ msg

    str= "\n------------------------------------------------------------------\n"+\
        "End Time : "+datetime.now().strftime("-%y-%m-%d_%H-%M-%S") +\
          "\n------------------------------------------------------------------\n"
    print str
    logger.info(str)
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
	#Log messages
    logger.info("Collegiate Automation Main Script  : " +pymsg)
    logger.info("Collegiate Automation Main Script  : " +msgs)

