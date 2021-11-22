"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        "datetime_utc",
        "distance_au",
        "velocity_km_s",
        "designation",
        "name",
        "diameter_km",
        "potentially_hazardous",
    )

    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(fieldnames)

        for ca in results:
            time = ca.time_str
            distance = ca.distance
            velocity = ca.velocity
            neo_diameter = str(ca.neo.diameter)
            neo_name = ca.neo.name if ca.neo.diameter else ""
            neo_hazardous = str(ca.neo.hazardous)
            writer.writerow(
                [
                    time,
                    distance,
                    velocity,
                    ca._designation,
                    neo_name,
                    neo_diameter,
                    neo_hazardous,
                ]
            )


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    json_list = []
    with open(filename, "w") as write_file:
        dict = iter(results)
        while True:
            try:
                json_dict = next(dict)

                full_d = {
                    "datetime_utc": json_dict.time_str,
                    "distance_au": json_dict.distance,
                    "velocity_km_s": json_dict.velocity,
                    "designation": json_dict._designation,
                    "neo": {
                        "name": json_dict.neo.name,
                        "diameter_km": json_dict.neo.diameter,
                        "potentially_hazardous": json_dict.neo.hazardous,
                        "designation": json_dict.neo.designation,
                    },
                }
                json_list.append(full_d)
            except StopIteration:
                break

        json.dump(json_list, write_file, indent=5)
