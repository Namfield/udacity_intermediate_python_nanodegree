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
import models


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )

    # Write the results to a CSV file, following the specification in the instructions.
    # open the CSV file to write the results
    with open(filename, 'w') as csv_file:
        # create a csv wrier object
        writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
        # write the header row
        # write the sequence of headers defined in fieldnames tuple as the first row
        writer.writeheader()
        # iterate over results to write each close approach to the csv file
        for close_approach in results:
            # for each row, mapping each info of a close approach to the corresponding header
            row = {'datetime_utc': close_approach.time_str,
                   'distance_au': close_approach.distance,
                   'velocity_km_s': close_approach.velocity,
                   'designation': close_approach.neo.designation,
                   'name': close_approach.neo.name if close_approach.neo.name else '',
                   'diameter_km': close_approach.neo.diameter if close_approach.neo.diameter else 'nan',
                   'potentially_hazardous': 'True' if close_approach.neo.hazardous else 'False'}
            # write each row to the csv file
            writer.writerow(row)

def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    # Write the results to a JSON file, following the specification in the instructions.
    # the list to store each entry corresponding to each close approach
    close_approach_entries = []
    # iterate over each close approach then extract each info
    for close_approach in results:
        # the dict to store info of a close approach
        close_approach_entry = {}
        close_approach_entry['datetime_utc'] = close_approach.time_str
        close_approach_entry['distance_au'] = close_approach.distance
        close_approach_entry['velocity_km_s'] = close_approach.velocity
        close_approach_entry['neo'] = {
            'designation': close_approach.neo.designation,
            'name': close_approach.neo.name if close_approach.neo.name else '',
            'diameter_km': close_approach.neo.diameter,
            'potentially_hazardous': close_approach.neo.hazardous
        }
        # store each close approach entry to a list
        close_approach_entries.append(close_approach_entry)
    # write the all close_approaches to a json file
    with open(filename, 'w') as json_file:
        json.dump(close_approach_entries, json_file, indent = 4)