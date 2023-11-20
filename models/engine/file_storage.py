#!/usr/bin/python3
"""This module is the storage engine of the objects"""

import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Class for serializtion and deserialization of base classes."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary `__objects` while values are instances"""

        return FileStorage.__objects

    # _____________________________________________________________________________________

    def new(self, obj):
        """Sets in `__objects` the `obj` with key <obj class name>.id"""

        # Create string format for the key of `__objects` attribute
        objects_key = f"{obj.__class__.__name__}.{obj.id}"

        # Set the instance to the key has been created (`objects_key`)
        FileStorage.__objects[objects_key] = obj

    # _____________________________________________________________________________________

    def save(self):
        """Serializes __objects to the JSON file at __file_path"""

        dict_of_obj = {}

        # Convert the `__objects` values (obj) to a dictionary representation
        for k, v in FileStorage.__objects.items():
            dict_of_obj[k] = v.to_dict()

        # Convert the dictionary representation to a json string representation
        with open(FileStorage.__file_path, "w", encoding="utf8") as wf:
            json.dump(dict_of_obj, wf)

    # _____________________________________________________________________________________

    def reload(self):
        """Deserializes JSON file into __objects."""

        try:
            # convert the json string representation to dictionary represen
            with open(FileStorage.__file_path, 'r') as rf:
                loaded_data = json.load(rf)

            # Create instance from the extracted dictionary representation
            for k, obj_dict in loaded_data.items():

                # Convert the values of the dictionary (obj_dict) to instances
                instance = eval(k.split(".")[0])(**obj_dict)
                FileStorage.__objects[k] = instance
        except FileNotFoundError:
            pass
