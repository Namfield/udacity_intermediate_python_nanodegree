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

    # TODO: Write the results to a CSV file, following the specification in the instructions.
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
    # TODO: Write the results to a JSON file, following the specification in the instructions.
    # the list to store each entry corresponding to each close approach
    close_approach_entries = []
    # the dict to store info of a close approach
    close_approach_entry = {}
    # iterate over each close approach then extract each info
    for close_approach in results:
        close_approach_entry['datetime_utc'] = close_approach.time_str
        close_approach_entry['distance_au'] = close_approach.distance
        close_approach_entry['velocity_km_s'] = close_approach.velocity
        close_approach_entry['neo']['designation'] = close_approach_entry.neo.designation
        close_approach_entry['neo']['name'] = close_approach.neo.name if close_approach.neo.name else ''
        close_approach_entry['neo']['diameter_km'] = close_approach_entry.neo.diameter
        close_approach_entry['neo']['potentially_hazardous'] = True if close_approach.neo.hazardous else False
        # store each close approach entry to a list
        close_approach_entries.append(close_approach_entry)
    # write the all close_approaches to a json file
    with open(filename, 'w') as json_file:
        json.dump(close_approach_entries, json_file, indent = 4)
























# def write_to_json(results, filename):
#     # Create a list to store the serialized results
#     serialized_results = []

#     # Iterate over each CloseApproach object in the results stream
#     for approach in results:
#         # Create a dictionary to store the serialized data for each CloseApproach
#         serialized_approach = {}

#         # Serialize the CloseApproach attributes
#         serialized_approach['datetime_utc'] = datetime_to_str(approach.time)
#         serialized_approach['distance_au'] = approach.distance
#         serialized_approach['velocity_km_s'] = approach.velocity

#         # Serialize the NEO attributes
#         serialized_approach['neo'] = {}
#         serialized_approach['neo']['designation'] = approach.neo.designation
#         serialized_approach['neo']['name'] = approach.neo.name if approach.neo.name else ''
#         serialized_approach['neo']['diameter_km'] = approach.neo.diameter if approach.neo.diameter else float('nan')
#         serialized_approach['neo']['potentially_hazardous'] = approach.neo.hazardous

#         # Append the serialized approach to the list
#         serialized_results.append(serialized_approach)

#     # Write the serialized results to the JSON file
#     with open(filename, 'w') as file:
#         json.dump(serialized_results, file)
