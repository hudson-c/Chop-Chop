import json
import os


def does_recipe_id_exist():
    # Check if ID is in the JSON files
    print("check if id exist")


def get_database_address(json_file_name):
    return os.getenv("chop-chop-database") + "/" + json_file_name + ".json"


def get_JSON(file):
    # Opening JSON file
    f = open(file)

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Closing file
    f.close()

    return data


# get_JSON(sys.path.)
