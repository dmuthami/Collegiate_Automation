#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      dmuthami
#
# Created:     25/09/2014
# Copyright:   (c) dmuthami 2014
# Licence:     GPL
#-------------------------------------------------------------------------------
import os, sys
import arcpy
import traceback
from arcpy import env
import Configurations

##------------------Beginning of Functions--------------------------------------------

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

## Export feature locations and attributes to an ASCII text file
def exportToASCII(workspace,input_features, export_ASCII):

    ##Set the overwriteOutput environment setting to True
    env.overwriteOutput = True

    #Transfer Field Domain Descriptions
    env.transferDomains = True

    # Local variables...
    #workspace = r"E:\GIS Data\RED-BULL\Mapping Portal Enhancement - Release 1.0\4. Implementation\4.1 CODE\GIS\Collegiate_Definition_Automation\Sample_Data\collegiate_sample_data.gdb"

    #input_features = "geocode_result"

    #export_ASCII = os.path.dirname(workspace) + "/collegiate_store.txt"

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
def domainDictionary(workspace,domainName):
    domains = arcpy.da.ListDomains(workspace)

    #create an empty dictionary
    domainDict = {}

    for domain in domains:
        #print('Domain name: {0}'.format(domain.name))
        if domain.name == domainName:
            coded_values = domain.codedValues
            for val, desc in coded_values.iteritems():
                print('{0} : {1}'.format(val, desc))
                domainDict[val] = desc
            break

    return domainDict
##Export to text  file via search cursor
# workspace: data source for the stores feature class
# input features: the feature class containing data to be exported
# fields: fields that will be included in the export
# text file parameter : the path to the output file
def exportToTextfile(workspace,input_features, fields, exportFieldsAlias,textfile):

    ##Set the overwriteOutput environment setting to True
    env.overwriteOutput = True

    #Transfer Field Domain Descriptions
    env.transferDomains = True

    # Local variables...
    #workspace = r"E:\GIS Data\RED-BULL\Mapping Portal Enhancement - Release 1.0\4. Implementation\4.1 CODE\GIS\Collegiate_Definition_Automation\Sample_Data\collegiate_sample_data.gdb"

    # Set the current workspace (to avoid having to specify the full path to the feature classes each time)
    arcpy.env.workspace = workspace

    #input_features = "geocode_result"

    #Store domain in a dictionary and acess stuff on it.
    domainDict = domainDictionary(workspace,Configurations.Configurations_domainName)

    # Establish Class fields
    #fields = yes.

    #Define output
    #textfile = os.path.dirname(workspace) + "/collegiate_store11.txt"

    #Open the report text file in write mode
    file = open (textfile, "w")

    #Add Header lines to report text file
    #file.write("Collegiate Store Table:\n")

    #Loop thru the fields aliases object for column headers
    ##    for field in exportFieldsAlias:
    ##        file.write(field + " ")

    #file.write("\n") #Force new line after writing the column headers

    #Custom header as per requirements from SAP
    #Store_is	Update type	Flag Name	Value
    file.write("Store ID"+ " " +  \
        "Update Type"+ " " \
        "Flag Name"+ " " \
        "Value"+ " " \
        + "\n")

    #file.write("OBJECT ID" + " " + "Store ID"+ " " + "Collegiate" + " " + "Bullring Class" + " "+ "IPEDS ID"+ "\n")

    # Create cursor to search gas mains by material
    with arcpy.da.SearchCursor(input_features, fields) as cursor:
        for row in cursor:
            #Get field values
            objectid = str(row[0])
            storeID = str(row[1])
            collegiate = str(row[2])
            bullringClass = str(row[3])
            ipedsID = str(row[4])

            #Write outputs to file now
            #file.write(objectid + " " + storeID + " " + collegiate + " " + bullringClass + " " + ipedsID + "\n")
            collegiateDescription = str(domainDict[int(collegiate)]) # Substitute code for description
            #Write to file as below
            # Store_is "Update type" "Flag Name" "Value"
            file.write(storeID + " " + "U" + " " + "FLG_AREA" + " " + collegiateDescription + "\n") #with bullring
            file.write(storeID + " " + "U" + " " + "YUS_FLG_COLLEGE" + " " + ipedsID + "\n") #with IPED
    #Close file to release handle
    file.close()

    #Return Nothing
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

    #Function that exports to ASCII
    exportToASCII(workspace,input_features, export_ASCII)

    #Exports to file but using search cursor
    exportToTextfile(workspace,input_features, fields, exportFieldsAlias, textfile)

