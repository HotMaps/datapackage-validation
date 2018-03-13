# Datapackage validation script
This script uses json schema validation. Schemas are defined in 'schema' sub directory.
There is one script for each data type "vector", "raster" and "tabular".

The script handles required attributes, type verification and required content (enum).

If everything works fine the message "datapackage.json is OK is printed in terminal", otherwise it print the errors and the message "datapackage.json is not OK! Please check the file again.".

Note that if the script declares that your datapackage.json it does not mean that the data itself is conform. Further verification is needed to determine if the dataset is compliant.
The verification of the dataset is done during the data integration process.

## How to include it in your repository
Open terminal and go to the root of your repository.
Execute git command:
```Shell
git submodule add https://github.com/HotMaps/datapackage-validation.git
```
Then execute script with command:
```Shell     
python datapackage-validation/validate_datapackage.py
```
*This script has been tested using python3 but might work with python2.*


