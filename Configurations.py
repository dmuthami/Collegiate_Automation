#-------------------------------------------------------------------------------
# Name:        Configurations
# Purpose:
#
# Author:      dmuthami
#
# Created:     29/09/2014
# Copyright:   (c) dmuthami 2014
# Licence:     GPL
#-------------------------------------------------------------------------------
import ConfigParser

#Import global traceback here
import traceback

#Workspace global variables
Configurations_workspace = ""
Configurations_workspaceScratch = ""
Configurations_campusBoundaryFeatureClass = ""
Configurations_storesFeatureClass = ""
Configurations_storesFeatureClassNew = ""
Configurations_BRMDL = ""
Configurations_realSDETable = ""

#collegiate field global variables
Configurations_fieldname = ""
Configurations_fieldAlias = ""
Configurations_fieldType = ""

#domain codes global variables
Configurations_bullsEye = ""
Configurations_bullsRing = ""
Configurations_nonCollegiate = ""

#domain parameters global variables
Configurations_domainName = ""
Configurations_domainDescription= ""
Configurations_domainType = ""

#join field global variables
Configurations_collegiateJoinField = ""
Configurations_BRMDLJoinField = ""
Configurations_domainType = ""
Configurations_bullRingClass = ""
Configurations_BullRingClassFieldAlias = ""

#buffer parameters global variables
Configurations_distancefield = ""
Configurations_linearUnit = ""
Configurations_sideType = ""
Configurations_endType = ""

#IPEDS
Configurations_IPEDSFieldName = ""
Configurations_IPEDSFieldAlias = ""
Configurations_IPEDSFieldType = ""
Configurations_CampusBoundaryIPEDSID = ""

#buffer parameters global variables
Configurations_outputFolder = ""
Configurations_outputTextFile = ""
Configurations_OBJECTIDFieldAlias = ""
Configurations_storeIDFieldAlias= ""
Configurations_storeIDField= ""

#output to SDE table parameters global variables
Configurations_valueFieldName = ""
Configurations_valueFieldAlias = ""
Configurations_sdeTable = ""
Configurations_flagAreaValue1 = ""
Configurations_updateTypeValue = ""
Configurations_flagAreaValue2 = ""
Configurations_flagNameFieldName = ""
Configurations_updateTypeFieldName = ""

def setParameters(configFileLocation):

    #Dirty way of working with global variables
    global Configurations_Config #Set global variable.Usually not favourable in Python
    global Configurations_Sections #Set global variable.Usually not favourable in Python

    Configurations_Config = ConfigParser.ConfigParser() #instantiate ini parser object

    #Read the Config file
    Configurations_Config.read(configFileLocation)

    #Set workspace parameters by calling the below function
    setWorkSpaceParameters()

    setCollegiateFieldParameters()

    setDomainParameters()

    #Domain codes
    setDomainCodes()

    #Join field parameters plus and bullring variables
    setJoinFieldParameters()

    setBufferParameters()

    #Call function to set parameters required to export output to text file
    setOutputParameters()

    #Call function to set parameters for IPEDS
    setIPEDSParameters()

    #Call function to set parameters for outputting to sde table
    setOutputToSDETableParameters()

    return ""

##Set parameters for writinng to output sde table
def setOutputToSDETableParameters():

    #read workspace location from Config file location
    global Configurations_valueFieldName # Needed to modify global copy of Configurations_valueFieldName
    Configurations_valueFieldName = Configurations_Config.get('OutPutToSDE', 'valueFieldName')

    #read workspace location from Config file location
    global Configurations_valueFieldAlias # Needed to modify global copy of Configurations_valueFieldAlias
    Configurations_valueFieldAlias = Configurations_Config.get('OutPutToSDE', 'valueFieldAlias')

    #read workspace location from Config file location
    global Configurations_sdeTable # Needed to modify global copy of Configurations_sdeTable
    Configurations_sdeTable = Configurations_Config.get('OutPutToSDE', 'sdeTable')

    #read workspace location from Config file location
    global Configurations_flagAreaValue1 # Needed to modify global copy of Configurations_flagAreaValue1
    Configurations_flagAreaValue1 = Configurations_Config.get('OutPutToSDE', 'flagAreaValue1')

    #read workspace location from Config file location
    global Configurations_updateTypeValue # Needed to modify global copy of Configurations_updateTypeValue
    Configurations_updateTypeValue = Configurations_Config.get('OutPutToSDE', 'updateTypeValue')

    #read workspace location from Config file location
    global Configurations_flagAreaValue2 # Needed to modify global copy of Configurations_flagAreaValue1
    Configurations_flagAreaValue2 = Configurations_Config.get('OutPutToSDE', 'flagAreaValue2')


    #read workspace location from Config file location
    global Configurations_flagNameFieldName # Needed to modify global copy of Configurations_flagNameFieldName
    Configurations_flagNameFieldName = Configurations_Config.get('OutPutToSDE', 'flagNameFieldName')

    #read workspace location from Config file location
    global Configurations_updateTypeFieldName # Needed to modify global copy of Configurations_updateTypeFieldName
    Configurations_updateTypeFieldName = Configurations_Config.get('OutPutToSDE', 'updateTypeFieldName')

    return ""

def setWorkSpaceParameters():
    #read workspace location from Config file location
    global Configurations_workspace # Needed to modify global copy of C_workspace
    Configurations_workspace = Configurations_Config.get('Workspace', 'workspace')

    #read workspace location from Config file location
    global Configurations_workspaceScratch # Needed to modify global copy of Configurations_workspaceScratch
    Configurations_workspaceScratch = Configurations_Config.get('Workspace', 'workspaceScratch')

    #read stores feature class location from Config file location
    global Configurations_storesFeatureClass # Needed to modify global copy of C_storesFeatureClass
    Configurations_storesFeatureClass = Configurations_Config.get('Workspace','storesFeatureClass')

    #read campus boundary feature class location from Config file location
    global Configurations_campusBoundaryFeatureClass # Needed to modify global copy of C_campusBoundaryFeatureClass
    Configurations_campusBoundaryFeatureClass = Configurations_Config.get('Workspace','campusBoundaryFeatureClass')

    #read campus boundary feature class location from Config file location
    global Configurations_BRMDL # Needed to modify global copy of Configurations_BRMDL
    Configurations_BRMDL = Configurations_Config.get('Workspace','BRMDL')

    #read campus boundary feature class location from Config file location
    global Configurations_realSDETable # Needed to modify global copy of Configurations_realSDETable
    Configurations_realSDETable = Configurations_Config.get('Workspace','realSDETable')

    return ""

def setCollegiateFieldParameters():

    #read field name for storing collegiate status  from Config file location
    global Configurations_fieldname # Needed to modify global copy of C_fieldname
    Configurations_fieldname = Configurations_Config.get('Collegiate_Field','fieldname')

    #read field alias name for collegiate status field from Config file location
    global Configurations_fieldAlias # Needed to modify global copy of C_fieldAlias
    Configurations_fieldAlias = Configurations_Config.get('Collegiate_Field','fieldAlias')

    #read field data type for collegiate status field from Config file location
    global Configurations_fieldType # Needed to modify global copy of C_fieldType
    Configurations_fieldType = Configurations_Config.get('Collegiate_Field','fieldType')

    return ""

def setIPEDSParameters():

    #read field name for storing collegiate status  from Config file location
    global Configurations_IPEDSFieldName # Needed to modify global copy of Configurations_IPEDSFieldName
    Configurations_IPEDSFieldName = Configurations_Config.get('IPEDS','IPEDSFieldName')

    #read field alias name for collegiate status field from Config file location
    global Configurations_IPEDSFieldAlias # Needed to modify global copy of Configurations_IPEDSFieldAlias
    Configurations_IPEDSFieldAlias = Configurations_Config.get('IPEDS','IPEDSFieldAlias')

    #read field data type for collegiate status field from Config file location
    global Configurations_IPEDSFieldType # Needed to modify global copy of Configurations_IPEDSFieldType
    Configurations_IPEDSFieldType = Configurations_Config.get('IPEDS','IPEDSFieldType')

    #read field data type for collegiate status field from Config file location
    global Configurations_CampusBoundaryIPEDSID # Needed to modify global copy of Configurations_CampusBoundaryIPEDSID
    Configurations_CampusBoundaryIPEDSID = Configurations_Config.get('IPEDS','CampusBoundaryIPEDSID')

    return ""

def setOutputParameters():

    #read field name for storing collegiate status  from Config file location
    global Configurations_outputFolder # Needed to modify global copy of Configurations_outputFolder
    Configurations_outputFolder = Configurations_Config.get('OutPut','outputFolder')

    #read field alias name for collegiate status field from Config file location
    global Configurations_outputTextFile # Needed to modify global copy of Configurations_outputTextFile
    Configurations_outputTextFile = Configurations_Config.get('OutPut','outputTextFile')

    #read field name for storing collegiate status  from Config file location
    global Configurations_OBJECTIDFieldAlias # Needed to modify global copy of Configurations_OBJECTIDFieldAlias
    Configurations_OBJECTIDFieldAlias = Configurations_Config.get('OutPut','OBJECTIDFieldAlias')

    #read field alias name for collegiate status field from Config file location
    global Configurations_storeIDFieldAlias # Needed to modify global copy of Configurations_storeIDFieldAlias
    Configurations_storeIDFieldAlias = Configurations_Config.get('OutPut','storeIDFieldAlias')

    #read field alias name for store id field from Config file location
    global Configurations_storeIDField # Needed to modify global copy of Configurations_storeIDField
    Configurations_storeIDField = Configurations_Config.get('OutPut','storeIDField')

    return ""

def setDomainParameters():

    #read field name for storing collegiate status  from Config file location
    global Configurations_domainName # Needed to modify global copy of Configurations_domainName
    Configurations_domainName = Configurations_Config.get('Domain_Parameters','DomainName')

    #read field alias name for collegiate status field from Config file location
    global Configurations_domainDescription # Needed to modify global copy of Configurations_domainDescription
    Configurations_domainDescription = Configurations_Config.get('Domain_Parameters','DomainDescription')

    #read field data type for collegiate status field from Config file location
    global Configurations_domainType # Needed to modify global copy of Configurations_domainType
    Configurations_domainType = Configurations_Config.get('Domain_Parameters','DomainType')

    return ""

def setDomainCodes():

    #read field name for storing collegiate status  from Config file location
    global Configurations_bullsEye # Needed to modify global copy of Configurations_bullsEye
    Configurations_bullsEye = Configurations_Config.get('Domain_Codes','BullsEye')

    #read field alias name for collegiate status field from Config file location
    global Configurations_bullsRing # Needed to modify global copy of Configurations_bullsRing
    Configurations_bullsRing = Configurations_Config.get('Domain_Codes','BullsRing')

    #read field data type for collegiate status field from Config file location
    global Configurations_nonCollegiate # Needed to modify global copy of Configurations_nonCollegiate
    Configurations_nonCollegiate = Configurations_Config.get('Domain_Codes','NonCollegiate')

    return ""

def setJoinFieldParameters():

    #read field name for storing collegiate status  from Config file location
    global Configurations_collegiateJoinField # Needed to modify global copy of Configurations_collegiateJoinField
    Configurations_collegiateJoinField = Configurations_Config.get('Join_Field_Parameters','CollegiateJoinField')

    #read field alias name for collegiate status field from Config file location
    global Configurations_BRMDLJoinField # Needed to modify global copy of Configurations_BRMDLJoinField
    Configurations_BRMDLJoinField = Configurations_Config.get('Join_Field_Parameters','BRMDLJoinField')

    #read field data type for collegiate status field from Config file location
    global Configurations_domainType # Needed to modify global copy of Configurations_domainType
    Configurations_domainType = Configurations_Config.get('Join_Field_Parameters','DomainType')

    #read field data type for bull ring class field from Config file location
    global Configurations_bullRingClass # Needed to modify global copy of Configurations_bullRingClass
    Configurations_bullRingClass = Configurations_Config.get('Join_Field_Parameters','BullRingClass')

    #read field data type for collegiate status field from Config file location
    global Configurations_BullRingClassFieldAlias # Needed to modify global copy of Configurations_BullRingClassFieldAlias
    Configurations_BullRingClassFieldAlias = Configurations_Config.get('Join_Field_Parameters','BullRingClassFieldAlias')

    return ""


def setBufferParameters():

    #read field name for storing collegiate status  from Config file location
    global Configurations_distancefield # Needed to modify global copy of Configurations_distancefield
    Configurations_distancefield = Configurations_Config.get('Buffer_Parameters','DistanceField')

    #read field alias name for collegiate status field from Config file location
    global Configurations_linearUnit # Needed to modify global copy of Configurations_BRMDLJoinField
    Configurations_linearUnit = Configurations_Config.get('Buffer_Parameters','LinearUnit')

    #read field data type for collegiate status field from Config file location
    global Configurations_sideType # Needed to modify global copy of Configurations_sideType
    Configurations_sideType = Configurations_Config.get('Buffer_Parameters','SideType')

    #read field data type for collegiate status field from Config file location
    global Configurations_endType # Needed to modify global copy of Configurations_endType
    Configurations_endType = Configurations_Config.get('Buffer_Parameters','EndType')

    return ""

def main():
    pass

if __name__ == '__main__':
    main()
    #Call function to initialize variables for tool execution
    setParameters(configFileLocation)
