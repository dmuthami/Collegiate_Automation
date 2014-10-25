#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      dmuthami
#
# Created:     23/10/2014
# Copyright:   (c) dmuthami 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# import system modules
import arcpy, os
from arcpy import env


#import custom module
import Configurations
from Utility_Functions import  domainDictionary as getCollegiateDomainDictionary

def fieldMappingsForCollegiateStore1(workspace,intable,fields,sdeTable):
    try:
        #Select non-bull ring features from feature layer
        #collegiate definition
        collegiateFieldwithDelimeter = arcpy.AddFieldDelimiters(workspace, \
            Configurations.Configurations_fieldname)

        # Select  Bulls eye records and bulls ring records only
        collegiateSQLExp =  collegiateFieldwithDelimeter + " = " + str(Configurations.Configurations_bullsEye) + " Or " + \
            collegiateFieldwithDelimeter + " = " + str(Configurations.Configurations_bullsRing)

        outputView1 = "output_view1"

        # The created crime_view layer will have fields as set in fieldinfo object
        arcpy.MakeTableView_management(intable, outputView1, collegiateSQLExp)

        # Create the required FieldMap and FieldMappings objects
        fm_storeid = arcpy.FieldMap()
        fm_value = arcpy.FieldMap()

        fms = arcpy.FieldMappings()

        # Get the field names of vegetation type and diameter for both original
        # files
        storeid_type = Configurations.Configurations_storeIDField
        value_type = Configurations.Configurations_fieldname

        # Add fields to their corresponding FieldMap objects
        fm_storeid.addInputField(outputView1, storeid_type)
        fm_value.addInputField(outputView1, value_type)

        # Set the output field properties for both FieldMap objects
        storeid_name = fm_storeid.outputField
        storeid_name.name = Configurations.Configurations_storeIDField
        fm_storeid.outputField = storeid_name

        value_name = fm_value.outputField
        value_name.name = Configurations.Configurations_valueFieldName
        fm_value.outputField = value_name

        # Add the FieldMap objects to the FieldMappings object
        fms.addFieldMap(fm_storeid)
        fms.addFieldMap(fm_value)

        #Append the output view to output table
        schemaType = "NO_TEST"#schema type method signature
        fieldMappings = "" #field  mappings
        subtype = "" # Whether to append to a certain subtype only

        #Bullring or bulls eye value

        arcpy.Append_management(outputView1, sdeTable, schemaType, fms, subtype)

        ##Update Fields
        #Get domain descriptions. need to substitute codes with the descriptions
        domainDict = getCollegiateDomainDictionary(workspace,Configurations.Configurations_domainName)

        # Start an edit session. Must provide the workspace.
        edit = arcpy.da.Editor(workspace)

        # Edit session is started without an undo/redo stack for versioned data
        #  (for second argument, use False for unversioned data)
        #Compulsory for above feature class participating in a complex data such as parcel fabric
        edit.startEditing(False, False)

        # Start an edit operation
        edit.startOperation()

        #Update cursor goes here
        with arcpy.da.UpdateCursor(sdeTable, fields) as cursor:
            for row in cursor:# loops per record in the recordset and returns an array of objects
                ##Set bull ring value it is set to default
                ## This should be a data dictionary read from file
                row[1] = Configurations.Configurations_flagAreaValue1
                row[2] = Configurations.Configurations_updateTypeValue
                row[0] = str(domainDict[int(row[0])]) #substitute coded value for its description
                # Update the cursor with the updated row object that contains now the new record
                cursor.updateRow(row)

        # Stop the edit operation.and commit the changes
        edit.stopOperation()

        # Stop the edit session and save the changes
        #Compulsory for release of locks arising from edit session. NB. Singleton principle is observed here
        edit.stopEditing(True)

        #delete the in memory feature layer just in case we need to recreate
        # table layer or maybe run script an additional time
        arcpy.Delete_management(outputView1)

    except:
            ## Return any Python specific errors and any error returned by the geoprocessor
            ##
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\n fieldMappingsForCollegiateStore1() Function : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
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

def fieldMappingsForCollegiateStore2(workspace,intable,fields,sdeTable):
    try:
        #Select non-bull ring features from feature layer
        #collegiate definition
        collegiateFieldwithDelimeter = arcpy.AddFieldDelimiters(workspace, \
            Configurations.Configurations_fieldname)

        # Select  Bulls eye records and bulls ring records only
        collegiateSQLExp =  collegiateFieldwithDelimeter + " = " + str(Configurations.Configurations_bullsEye) + " Or " + \
            collegiateFieldwithDelimeter + " = " + str(Configurations.Configurations_bullsRing)

        outputView1 = "output_view1"

        # The created crime_view layer will have fields as set in fieldinfo object
        arcpy.MakeTableView_management(intable, outputView1, collegiateSQLExp)

        # Create the required FieldMap and FieldMappings objects
        fm_storeid = arcpy.FieldMap()
        fm_value = arcpy.FieldMap()

        fms = arcpy.FieldMappings()

        # Get the field names of vegetation type and diameter for both original
        # files
        storeid_type = Configurations.Configurations_storeIDField
        value_type = Configurations.Configurations_IPEDSFieldName

        # Add fields to their corresponding FieldMap objects
        fm_storeid.addInputField(outputView1, storeid_type)
        fm_value.addInputField(outputView1, value_type)

        # Set the output field properties for both FieldMap objects
        storeid_name = fm_storeid.outputField
        storeid_name.name = Configurations.Configurations_storeIDField
        fm_storeid.outputField = storeid_name

        value_name = fm_value.outputField
        value_name.name = Configurations.Configurations_valueFieldName
        fm_value.outputField = value_name

        # Add the FieldMap objects to the FieldMappings object
        fms.addFieldMap(fm_storeid)
        fms.addFieldMap(fm_value)

        #Append the output view to output table
        schemaType = "NO_TEST"
        fieldMappings = ""
        subtype = ""

        arcpy.Append_management(outputView1, sdeTable, schemaType, fms, subtype)

        # Start an edit session. Must provide the workspace.
        edit = arcpy.da.Editor(workspace)

        # Edit session is started without an undo/redo stack for versioned data
        #  (for second argument, use False for unversioned data)
        #Compulsory for above feature class participating in a complex data such as parcel fabric
        edit.startEditing(False, False)

        # Start an edit operation
        edit.startOperation()

        #Update cursor goes here
        with arcpy.da.UpdateCursor(sdeTable, fields) as cursor:
            for row in cursor:# loops per record in the recordset and returns an array of objects
                ##Set bull ring value it is set to default
                ## This should be a data dictionary read from file
                row[0] = Configurations.Configurations_flagAreaValue2
                row[1] = Configurations.Configurations_updateTypeValue

                # Update the cursor with the updated row object that contains now the new record
                cursor.updateRow(row)

        # Stop the edit operation.and commit the changes
        edit.stopOperation()

        # Stop the edit session and save the changes
        #Compulsory for release of locks arising from edit session. NB. Singleton principle is observed here
        edit.stopEditing(True)

        #delete the in memory feature layer just in case we need to recreate
        # table layer or maybe run script an additional time
        arcpy.Delete_management(outputView1)
    except:
            ## Return any Python specific errors and any error returned by the geoprocessor
            ##
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\n fieldMappingsForCollegiateStore2() Function : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
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

def truncateFunction(truncateDataset):
    try:
        arcpy.TruncateTable_management(truncateDataset)
    except:
            ## Return any Python specific errors and any error returned by the geoprocessor
            ##
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\n truncateFunction() Function : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
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

#function appends records from the file geodatabase into the sde table
def appendSDETable(table,sdeTable):
    try:
        #truncate the sde table to accomodate new records
        truncateFunction(sdeTable)

        #Set append parameters
        schemaType = "NO_TEST"
        fieldMappings = ""
        subtype = ""

        #Run append parameters
        arcpy.Append_management(table, sdeTable, schemaType, fieldMappings, subtype)
    except:
            ## Return any Python specific errors and any error returned by the geoprocessor
            ##
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\n appendSDETable() Function : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
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

##Ouput collegiate defintion table into table
def outputSDETable():
    try:
        #Uncomment next line if an only if you want to debug code
        #Configurations.setParameters(r"E:\GIS Data\RED-BULL\Mapping Portal Enhancement - Release 1.0\4. Implementation\4.1 CODE\GIS\Collegiate_Definition_Automation\Python_Scripts\GitHub\Collegiate_Automation\Config.ini")

        #workspace variable
        env.workspace = Configurations.Configurations_workspace

        # Set data path
        intable = Configurations.Configurations_storesFeatureClass

        #Fields required to updated after supplying Bullseye, Bullsring operation
        fields1 =[Configurations.Configurations_valueFieldName,Configurations.Configurations_flagNameFieldName,\
            Configurations.Configurations_updateTypeFieldName]

        #Fields required to updated after supplying the IPEDS_ID
        fields2 =[Configurations.Configurations_flagNameFieldName, \
            Configurations.Configurations_updateTypeFieldName]

        #output sde table
        sdeTable = Configurations.Configurations_sdeTable

        #call function to truncate records in existing collegiate_store table
        truncateFunction(sdeTable)

        #Append BullsEye and BullsRing dataset
        fieldMappingsForCollegiateStore1(Configurations.Configurations_workspace,intable,fields1,sdeTable)

        #Append BullsEye and BullsRing dataset
        fieldMappingsForCollegiateStore2(Configurations.Configurations_workspace,intable,fields2,sdeTable)

        #Call function to output to append to sde table
        appendSDETable(sdeTable,Configurations.Configurations_realSDETable)

    except:
            ## Return any Python specific errors and any error returned by the geoprocessor
            ##
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\n addField Function : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
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

def main():
    pass

if __name__ == '__main__':
    main()

    #Write to SDE table
    outputSDETable()

