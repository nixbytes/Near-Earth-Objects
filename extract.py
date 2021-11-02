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
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # TODO: Load NEO data from the given CSV file.
    neo_list = []
    with open(neo_csv_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)

        for neo in reader:
            params = {
                'designation': neo["pdes"],
                'name': neo["name"],
                'hazardous': neo["pha"],
                'diameter': neo["diameter"] or "nan",
            }

            neo_list.append(
                NearEarthObject(**params)
            )

    return neo_list
    #return ()


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # TODO: Load close approach data from the given JSON file.
    cad_collection = []
    with open(cad_json_path, 'r') as infile:
        json_data = json.load(infile)

        for key in json_data["data"]:
            params = {
                'designation': key[0],
                'time': key[3],
                'distance': key[4],
                'velocity': key[7]

            }

            cad_collection.append(CloseApproach(**params))

    return cad_collection
