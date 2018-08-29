# python 3.5
import sys
import json
import os.path


def post_issue(name, description, issue_type='Dataset integration', tags=[]):
    print(name, description, issue_type, tags)

repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
repository_name = os.path.basename(repo_path)

"""
    VALIDATION
"""
print("Validation of " + repository_name)

# check that repository path is correct
if not os.path.isdir(repo_path):
    print('repo_path is not a directory')
    msg = 'repository path is not a directory'
    post_issue(name='Validation error ' + repository_name,
               description='The repository validation was not successful.\n' + msg,
               issue_type='Dataset Provider improvement needed')

content = os.listdir('.')

# check that datapackage file is not missing
dp_file_path = os.path.join(repo_path, 'datapackage.json')
if not os.path.isfile(dp_file_path):
    print('datapackage.json file missing or not in correct directory')
    msg = 'datapackage.json file missing or not in correct directory'
    post_issue(name='Validation error ' + repository_name,
               description='The repository validation was not successful.\n' + msg,
               issue_type='Dataset Provider improvement needed')

# check that data directory is present
data_dir_path = os.path.join(repo_path, 'data')
if not os.path.isdir(data_dir_path):
    print('data directory missing')
    msg = 'data directory missing'
    post_issue(name='Validation error ' + repository_name,
               description='The repository validation was not successful.\n' + msg,
               issue_type='Dataset Provider improvement needed')

# check properties
missing_properties = []
error_messages = []

# open file
# check if file construction is valid
try:
    with open(dp_file_path) as f:
        dp = json.load(f)
except json.decoder.JSONDecodeError as e:
    msg = 'JSON decoding raised an exception.\n' + str(e)
    print(msg)
    post_issue(name='Validation error ' + repository_name,
               description='The repository validation was not successful.\n' + msg,
               issue_type='Dataset Provider improvement needed')

# create tags from contributors (data providers)
try:
    contributors = dp['contributors']
    tags = []
    for c in contributors:
        print(c['title'])
        tags.append(c['title'])
except KeyError as e:
    pass


# profile
try:
    dp_profile = dp['profile']
except:
    dp_profile = None
    missing_properties.append('profile')
# resources
try:
    dp_resources = dp['resources']
except:
    missing_properties.append('resources')
    dp_resources = None

# check resources attributes
if dp_resources:
    if dp_profile == 'vector-data-resource':
        for dp_r in dp_resources:
            print('vector-data-resource')
            props = ['name', 'path', 'format', 'unit', 'vector']
            for p in props:
                try:
                    a = dp_r[p]
                    if p == 'name':
                        if len(a) > 50:
                            error_messages.append('resource/name length is too long (max 50 char.)')
                        if a.endswith(('.csv', '.tif', '.tiff', '.shp', '.geojson', '.txt')):
                            error_messages.append('resource/name should not contain a file extension (extension is in resource/path)')
                except KeyError as e:
                    missing_properties.append('resources/' + p)
            try:
                dp_path = dp_r['path']
                if not os.path.isfile(os.join(repo_path, dp_path)):
                    error_messages.append('attribute path does not link to an existing file')
            except:
                pass
            try:
                dp_vector = dp_r['vector']
                dp_epsg = dp_vector['epsg']
            except:
                missing_properties.append('vector/epsg')
            try:
                dp_vector = dp_r['vector']
                dp_geometry_type = dp_vector['geometry_type']
                if dp_geometry_type.lower() == 'polygon':
                    dp_geometry_type = 'MultiPolygon'
                elif dp_geometry_type.lower() == 'multipolygon':
                    dp_geometry_type = 'MultiPolygon'
                elif dp_geometry_type.lower() == 'point':
                    dp_geometry_type = 'Point'
                elif dp_geometry_type.lower() == 'multipoint':
                    dp_geometry_type = 'MultiPoint'
                elif dp_geometry_type.lower() == 'multilinestring':
                    dp_geometry_type = 'MultiLinestring'
                elif dp_geometry_type.lower() == 'linestring':
                    dp_geometry_type = 'Linestring'
                else:
                    error_messages.append('geometry_type is not set correctly (must be either (multi)point, (multi)linestring or (multi)polygon)')
            except:
                missing_properties.append('vector/geometry_type')
            try:
                dp_schema = dp_vector['schema']
            except:
                missing_properties.append('vector/schema')
            try:
                dp_schema = dp_vector['schema']
                if len(dp_schema) > 0:
                    for f in dp_schema:
                        f_name = f['name']
                        f_unit = f['unit']
                        f_type = f['type']
            except:
                error_messages.append('errors in schema definition (schema: [{name, unit, type},...])')
    elif dp_profile == 'raster-data-resource':
        print('raster-data-resource')
        for dp_r in dp_resources:
            props = ['name', 'path', 'unit', 'format', 'raster']
            for p in props:
                try:
                    a = dp_r[p]
                    if p == 'name':
                        if len(a) > 50:
                            error_messages.append('resource/name length is too long (max 50 char.)')
                        if a.endswith(('.csv', '.tif', '.tiff', '.shp', '.geojson', '.txt')):
                            error_messages.append('resource/name should not contain a file extension (extension is in resource/path)')
                except KeyError as e:
                    missing_properties.append('resources/' + p)
            try:
                dp_path = dp_r['path']
                if not os.path.exists(os.join(repo_path, dp_path)):
                    error_messages.append('attribute path does not link to an existing file')
            except:
                pass
            try:
                dp_raster = dp_r['raster']
                dp_epsg = dp_raster['epsg']
            except:
                missing_properties.append('raster/epsg')
    elif dp_profile == 'tabular-data-resource':
        print('tabular-data-resource')
        for dp_r in dp_resources:
            props = ['name', 'path', 'schema', 'encoding', 'format', 'dialect']
            for p in props:
                try:
                    a = dp_r[p]
                    if p == 'name':
                        if len(a) > 50:
                            error_messages.append('resource/name length is too long (max 50 char.)')
                        if a.endswith(('.csv', '.tif', '.tiff', '.shp', '.geojson', '.txt')):
                            error_messages.append('resource/name should not contain a file extension (extension is in resource/path)')
                except KeyError as e:
                    missing_properties.append('resources/' + p)
            # fields
            has_geom = False
            f_col_names = []
            try:
                dp_schema = dp_r['schema']
                if 'fields' in dp_schema:
                    dp_fields = dp_schema['fields']
                    if len(dp_fields) > 0:
                        for f in dp_fields:
                            f_name = f['name']
                            f_unit = f['unit']
                            f_type = f['type']
                            if f_type == 'geometry':
                                has_geom = True
                            f_col_names.append(f_name)
                else:
                    missing_properties.append('fields')
            except:
                error_messages.append('errors in schema definition (schema: fields: [{name, unit, type},...])')
            # geoms
            if 'spatial_resolution' in dp_r and 'spatial_key_field' in dp_r:
                if dp_r['spatial_key_field'] not in f_col_names:
                    error_messages.append('spatial_key_field does not refer to an existing field name')
            else:
                if not has_geom:
                    error_messages.append('no geometry provided (nuts/lau reference [attribute spatial_key_field and spatial_resolution] or geometry field)\n'
                                          + '\tThe dataset will be integrated as is but make sure that no geometry is needed.')

    else:
        err_msg = '\'profile\' contains an unsupported value! Use only vector-data-resource, raster-data-resource or tabular-data-resource'
        print(err_msg)
        error_messages.append(err_msg)

if len(error_messages) + len(missing_properties) > 0:
    str_error_messages = ''
    if len(error_messages) > 0:
        str_error_messages = 'Errors: \n' + '\n'.join(error_messages)
        if len(missing_properties) > 0:
            str_error_messages = str_error_messages + '\n'
    if len(missing_properties) > 0:
        str_error_messages = 'Missing properties: \n' + '\n'.join(missing_properties)
    print('Validation error for repository ' + repository_name + '\n' + str_error_messages)

    post_issue(name='Validation error ' + repository_name,
               description='The repository validation was not successful.\n' + str_error_messages,
               issue_type='Dataset Provider improvement needed',
               tags=tags)

    if len(error_messages) + len(missing_properties) == 1 and has_geom is False:
        pass # allow datasets without geometry
        print('Resource integration continuing despite geom error.')
    else:
        print('Resource integration aborted.')
else:
    print('Validation OK')
