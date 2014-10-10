Collegiate_Automation Tool
=====================

Collegiate Automation Tool


To deploy do the following;

Unpack map package you have received to some appropriate location on your computer

Open Config.INI file in a text editor and change the existing workspace value from "E:\GIS Data\RED-BULL\Mapping Portal Enhancement - Release 1.0\4. Implementation\4.1 CODE\GIS\Collegiate_Definition_Automation\Deployment\CollegiateDefinition\collegiate_scratch.gdb"

 to your current workspace
 
Additionally, specify location of SDE connection file. This is where the campus boundary and Bull Ring Master Data list lie

Specify location of store geocodes

Specify location of the output file for importation to SAP

In Collegiate_Automation.py change confiFileLocation variable "configFileLocation=r"E:\GIS Data\RED-BULL\Mapping Portal Enhancement - Release 1.0\4. Implementation\4.1 CODE\GIS\Collegiate_Definition_Automation\Python_Scripts\GitHub\Collegiate_Automation\Config.ini"


  to your current location of the Config file

Execute Collegeiate_Automation.py file and at least supply path to Config file as one of the parameter items
