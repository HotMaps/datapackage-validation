# Datapackage validation script
The script handles required attributes needed by the integration script.

If everything works fine the message "Validation OK" is printed in terminal. Otherwise it prints the errors detected.

Note that if the script declares that your repository is OK, it does not mean that the data itself is conform. It might still fail during the integration but this script minimizes the number of errors and prevents basic errors before pushing the dataset to GIT project.

## How to include it in your repository
Open terminal and go to the root of your repository.
Execute git command:
```Shell
git submodule add https://github.com/HotMaps/datapackage-validation.git
```
Make sure you have the required dependencies with command:
```Shell
pip install -r requirements.txt
```
*You might need to use pip3 in some distributions.*

Then execute script with command:
```Shell     
python datapackage-validation/validate_datapackage.py
```
*You might need to use python3 in some distributions.*

*This script has been tested using python3 but might work with python2.*
