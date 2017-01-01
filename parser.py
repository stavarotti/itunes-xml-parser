from json import dump
from os import listdir, makedirs
from os.path import exists, isfile, join
from sys import exc_info
import xml.etree.ElementTree as etree
import re

def to_camelcase(s):
  return re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), s)

# Folder path
xml_path = '/Users/steve/workspace/radio'

# Get the list of all files
xml_files = [f for f in listdir(xml_path) if isfile(join(xml_path, f)) and f != '.DS_Store']

# The list of all stations
station_list = {
  'stations': []
}

# The list of playlist properties in which we interested in capturing
station_model_props = set(['bitRate', 'dateAdded', 'description', 'location', 'name', 'persistentId'])

# Iterate through each file
for xml_file in xml_files:

  # Parse the file
  tree = etree.parse(join(xml_path, xml_file))

  # Get the root
  root = tree.getroot()

  try:
    station_nodes = root.findall('./dict/dict/dict')
    prop_name = ''
    station_genre = xml_file.replace('.xml', '')

    # Iterate over the station nodes
    for station in station_nodes:
      station_model = { 'genre': station_genre }
      # Iterate over each station. idx modulo 2 is the prop value.
      for idx, val in enumerate(list(station)):
        if ((idx + 1) % 2 == 0 and prop_name in station_model_props):
          station_model[prop_name] = val.text
          prop_name = ''
        else:
          prop_name = to_camelcase(val.text.replace(' ', '_').lower())
          if (prop_name == 'comments'):
            prop_name = 'description'

      # Add the station to the main entry list
      station_list['stations'].append(station_model)
  except:
    pass
    
# Write the contents to a file
output_path_directory = join(xml_path, 'output')

if not exists(output_path_directory):
    makedirs(output_path_directory)

with open(join(output_path_directory, 'stations.json'), 'w') as outfile:
  dump(station_list, outfile)

