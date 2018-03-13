# python 3.5
import sys
import json
from pprint import pprint
import os.path
import jsonschema


base_path = os.path.dirname(os.path.abspath(__file__))
print_with_color = True

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def _print(text, bcolor):
    if print_with_color:
        print(bcolor + text + bcolors.ENDC)
    else:
        print(text)

def validate_datapackage(file_path):
    # read datapackage.json (dp)
    try:
        if not os.path.exists(file_path):
            _print("datapackage.json file missing. Please make sure to place it at root of repository.", bcolors.FAIL)
            return

        dp = json.load(open(file_path))
        if not 'profile' in dp:
            _print("datapackage.json file missing 'profile' attribute."
                    + "The profile attriubte should specify if dataset is "
                    + "vector-data-resource, raster-data-resource "
                    + "or tabular-data-resource.", bcolors.FAIL)
            return

        profile = dp['profile']
        schema = None

        if profile == 'vector-data-resource':
            _print('vector-data-resource', bcolors.OKBLUE)
            schema = json.load(open(os.path.join(base_path, 'schema/vector-schema.json')))
        elif profile == 'raster-data-resource':
            _print('raster-data-resource', bcolors.OKBLUE)
            schema = json.load(open(os.path.join(base_path, 'schema/raster-schema.json')))
        elif profile == 'tabular-data-resource':
            _print('tabular-data-resource', bcolors.OKBLUE)
            schema = json.load(open(os.path.join(base_path, 'schema/tabular-schema.json')))
        else:
            _print('\'profile\' contains an unsupported value! Use only vector-data-resource, raster-data-resource or '
                  'tabular-data-resource', bcolors.FAIL)
            return

        # validate json
        v = jsonschema.Draft4Validator(schema)
        for error in sorted(v.iter_errors(dp), key=str):
            _print(error.message, bcolors.FAIL)

        if jsonschema.Draft4Validator(schema).is_valid(dp):
            _print('datapackage.json is OK.', bcolors.OKGREEN)
        else:
            _print('datapackage.json is not OK! Please check the file again.', bcolors.FAIL)

    except Exception as e:
        _print(str(e), bcolors.FAIL)
        return

d_file_path = os.path.join(os.path.dirname(base_path), 'datapackage.json')
print()
_print("#####################################", bcolors.HEADER)
_print(os.path.basename(base_path), bcolors.HEADER)
_print("#####################################", bcolors.HEADER)
validate_datapackage(d_file_path)
