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

##------------------Beginning of Functions--------------------------------------------

## Add Collegiate field
## Collegitae field has three codded value domains
## 0 :Bulls Eye
## 1:Bull Ring
## 2: Others
def addField(featureclass, fieldname, fieldAlias,fieldType):

    # Execute AddField twice for two new fields
    arcpy.AddField_management(featureclass, fieldname, fieldType, "", "", "",
                              fieldAlias, "NULLABLE")

    return ""

## Add Domains
def addDomain(workspace, domainName,domainDescription,fieldType, domainType):

    # Process: Create the coded value domain
    arcpy.CreateDomain_management(workspace, domainName, domainDescription, fieldType, domainType)

    return ""

## Add Domains
def addValuesToDomain(workspace, domainName, domainDictionary):

    # Process: Add valid material types to the domain
    #use a for loop to cycle through all the domain codes in the dictionary
    for code in domainDictionary:
        arcpy.AddCodedValueToDomain_management(workspace, domainName, code, domainDictionary[code])

    return ""

def assignDomainToField(storesFeatureClass,fieldname, domainName ):

    # Process: Constrain the collegiate definition values of the field
    arcpy.AssignDomainToField_management(storesFeatureClass, fieldname, domainName)
    return ""

def main():
    pass

if __name__ == '__main__':

    main()

    addField(featureclass, fieldname, fieldAlias,fieldType)

    addDomain(workspace, domainName,domainDescription,fieldType, domainType)

    addValuesToDomain(workspace, domainName, domainDictionary)

    assignDomainToField(storesFeatureClass,fieldname, domainName )

