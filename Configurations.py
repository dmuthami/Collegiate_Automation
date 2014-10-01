#-------------------------------------------------------------------------------
# Name:        Configurations
# Purpose:
#
# Author:      dmuthami
#
# Created:     29/09/2014
# Copyright:   (c) dmuthami 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import ConfigParser

C_workspace = ""
C_storesFeatureClass = ""
C_campusBoundaryFeatureClass = ""
C_fieldname = ""
C_fieldAlias = ""
C_fieldType = ""

def setParamameters():
    #Dirty way of working with global variables
    global C_Config
    global C_Sections

    C_Config = ConfigParser.ConfigParser()

    C_Config.read(r"E:\GIS Data\RED-BULL\Mapping Portal Enhancement - Release 1.0\4. Implementation\4.1 CODE\GIS\Collegiate_Definition_Automation\Python_Scripts\Config.ini")

    C_Sections = C_Config.sections()
    #['Others', 'SectionThree', 'SectionOne', 'SectionTwo']
    print C_Sections

    #call set global parameters
    setGlobalParameters()

    return ""

def setGlobalParameters():
    #read workspace location from config file location
    global C_workspace # Needed to modify global copy of C_workspace
    C_workspace = C_Config.get('Inputs', 'workspace')
    print C_workspace


    #read stores feature class location from config file location
    global C_storesFeatureClass # Needed to modify global copy of C_storesFeatureClass
    C_storesFeatureClass = C_Config.get('Inputs','storesFeatureClass')
    print C_storesFeatureClass

    #read campus boundary feature class location from config file location
    global C_campusBoundaryFeatureClass # Needed to modify global copy of C_campusBoundaryFeatureClass
    C_campusBoundaryFeatureClass = C_Config.get('Inputs','campusBoundaryFeatureClass')
    print C_campusBoundaryFeatureClass

    #read field name for storing collegiate status  from config file location
    global C_fieldname # Needed to modify global copy of C_fieldname
    C_fieldname = C_Config.get('Inputs','fieldname')
    print C_fieldname

    #read field alias name for collegiate status field from config file location
    global C_fieldAlias # Needed to modify global copy of C_fieldAlias
    C_fieldAlias = C_Config.get('Inputs','fieldAlias')
    print C_fieldAlias

    #read field data type for colegiate status field from config file location
    global C_fieldType # Needed to modify global copy of C_fieldType
    C_fieldType = C_Config.get('Inputs','fieldType')
    print C_fieldType

    return ""

def main():
    pass

if __name__ == '__main__':
    main()

    setParamameters()
