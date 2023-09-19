"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach

def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file and extracting the relevant information to create instances of the NearEarthObject class.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # Load NEO data from the given CSV file.
    # a list to store all neo instances
    neos = []

    # open the CSV file containing the neos data
    with open(neo_csv_path) as file:
        data = csv.DictReader(file)
        for elm in data:
            # extract necessary elements to create a neo instance from the csv file
            des = elm['pdes']
            name = elm['name']
            diameter = float(elm['diameter']) if elm['diameter'] else float('nan')
            # in the neos.csv file, 'hazardous' is present as 'Y' or 'N'
            # so we need to convert to the corresponding bool value
            hazardous = (elm['pha'] == 'Y')
            # create the neo instance then store in the list
            neos.append(NearEarthObject(des, name, diameter, hazardous))
        
    return neos

def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # Load close approach data from the given JSON file.
    # a list to store all CloseApproach instances
    approaches = []
    
    # open the json file containing the close approach data
    with open(cad_json_path) as file:
        data = json.load(file)
        # extract necessary elements to create a close approach instance
        fields = data["fields"]
        time_idx = fields.index('cd')
        distance_idx = fields.index('dist')
        velocity_idx = fields.index('v_rel')
        neo_des_idx = fields.index('des')
        cad_data = data['data']
        for elm in cad_data:
            time = elm[time_idx]
            distance = elm[distance_idx]
            velocity = elm[velocity_idx]
            neo_des = elm[neo_des_idx]
            approaches.append(CloseApproach(time, distance, velocity, neo_des))

    return approaches
