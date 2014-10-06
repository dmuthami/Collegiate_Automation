#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      dmuthami
#
# Created:     25/09/2014
# Copyright:   (c) dmuthami 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os, sys
import arcpy
from arcpy import env

##------------------Beginning of Functions--------------------------------------------

## Add Collegiate field
## Collegitae field has three codded value domains
## 0 :Bulls Eye
## 1:Bull Ring
## 2: Others
def addField(featureclass, fieldname, fieldAlias,fieldType):

    try:
        # Execute AddField twice for two new fields
        arcpy.AddField_management(featureclass, fieldname, fieldType, "", "", "",
                                  fieldAlias, "NULLABLE")
    except:
            ## Return any Python specific errors and any error returned by the geoprocessor
            ##
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\n addField Function : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
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

## Add Domains
def addDomain(workspace, domainName,domainDescription,fieldType, domainType):

    try:
        # Process: Create the coded value domain
        arcpy.CreateDomain_management(workspace, domainName, domainDescription, fieldType, domainType)

    except:
            ## Return any Python specific errors and any error returned by the geoprocessor
            ##
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\n addDomain Function : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
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

## Add Values to colegiate Domain
def addValuesToDomain(workspace, domainName, domainDictionary):

    try:
        # Process: Add valid material types to the domain
        #use a for loop to cycle through all the domain codes in the dictionary
        for code in domainDictionary:
            arcpy.AddCodedValueToDomain_management(workspace, domainName, code, domainDictionary[code])

    except:
            ## Return any Python specific errors and any error returned by the geoprocessor
            ##
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\n addValuesToDomain Function : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
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

def assignDomainToField(storesFeatureClass,fieldname, domainName ):

    try:
        # Process: Constrain the collegiate definition values of the field
        arcpy.AssignDomainToField_management(storesFeatureClass, fieldname, domainName)

    except:
            ## Return any Python specific errors and any error returned by the geoprocessor
            ##
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\n assignDomainToField Function : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
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

##Backup function
def backupInitialStoresFC (BR_workspace,BR_storesFeatureClass):

    try:
        ## Set overwrite in workspace to true
        arcpy.env.overwriteOutput = True

        #variable pointer to the in-memory feature layer
        #this is local variable
        backupInitialStoresFeatureLayer = BR_storesFeatureClass + '_lyr'

        #Backup Feature class of he initial stores layer
        backupStoresFeatureClass = BR_storesFeatureClass + "_bak"

        # Make a layer from stores feature class
        arcpy.MakeFeatureLayer_management(BR_storesFeatureClass, backupInitialStoresFeatureLayer)

        #Create feature class from selection
        arcpy.CopyFeatures_management(backupInitialStoresFeatureLayer,backupStoresFeatureClass)

        #delete the in memory feature layer just in case we need to recreate
        # feature layer or maybe run script an additional time
        arcpy.Delete_management(backupInitialStoresFeatureLayer)
    except:
            ## Return any Python specific errors and any error returned by the geoprocessor
            ##
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\n backupInitialStoresFC Function : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
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

def deleteBRMDLFieldsInStores(BRMDL,storesFeatureClass):
    try:

        # Describe the input (need to test the dataset and data types)
        desc = arcpy.Describe(BRMDL)

        # Use ListFields to get a list of field objects
        fieldObjList = arcpy.ListFields(BRMDL)

        # Create an empty list that will be populated with field names
        fieldNameList = []

        # For each field in the object list, add the field name to the
        #  name list.  If the field is required, exclude it, to prevent errors
        for field in fieldObjList:
            if not field.required:
                fieldNameList.append(field.name)

        # Execute DeleteField to delete all fields in the field list.
        arcpy.DeleteField_management(storesFeatureClass, fieldNameList)

    except:
        ## Return any Python specific errors and any error returned by the geoprocessor
        ##
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\n deleteBRMDLFieldsInStores Function : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
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

    addField(featureclass, fieldname, fieldAlias,fieldType)

    addDomain(workspace, domainName,domainDescription,fieldType, domainType)

    addValuesToDomain(workspace, domainName, domainDictionary)

    assignDomainToField(storesFeatureClass,fieldname, domainName )

    backupInitialStoresFC (BR_workspace,BR_storesFeatureClass)

    deleteBRMDLFieldsInStores(BRMDL,storesFeatureClass)

