# Title: AI Chef User Directory
# Class: CS 361 - Software Engineering I
# Author: Mallory Huston
# Description: Defines the User class used in the AI Chef web service.

import json
from pathlib import Path
import os


def data_open(name):
    """open and read user's json file if it exists"""
    data_file = Path(name + ".json")
    if data_file.is_file():
        # open file and load into data
        with open(name + '.json', 'r') as in_file:
            return json.load(in_file)

    # database defaults to empty
    else:
        return {}


class User:
    """Represents a user, with credentials and recipes."""

    def __init__(self, name, pwd):
        """initialize data members"""
        # get user data
        self.channel = None
        self.connection = None
        self.frame = None
        self.root = None
        self._data = data_open(name)

        # save user details
        self._name = name
        self._pwd = pwd
        self._cred = {name: pwd}

        # create credential file if it does not exist
        cred_file = Path(name + ".txt")
        if cred_file.is_file() is False:
            with open(name + ".txt", 'w') as file:
                file.write(json.dumps(self._cred))

    def valid_index(self, pos):
        """check if the given index falls within the database"""
        pos = int(pos) - 1
        if 0 <= pos < len(self._data):
            return True
        else:
            return False

    def add_recipe(self, pos, recipe, request):
        """adds a recipe entry to user._data"""
        pos = int(pos) - 1

        # create database if no recipes
        if self._data == {}:
            self._data = {list(self._data.keys())[pos]: {recipe: request}}

        # add recipe to database
        else:
            self._data[list(self._data.keys())[pos]][recipe] = request

    def add_library(self, lib):
        """adds an empty library to self._data"""
        self._data[lib] = {}

    def show_library(self):
        """prints a numbered list of all libraries"""
        i = 1
        # print list
        for meal, request in self._data.items():
            print(str(i) + ". " + meal)

            # screen break every 10 recipes
            if i % 10 == 0:
                input("\nPress any key to continue...\n")

            i += 1

    def show_recipes(self, pos):
        """show recipes in a given library"""
        pos = int(pos) - 1
        # print recipes in order
        i = 1
        print("Recipes (meal): ")
        for meal in self._data[list(self._data.keys())[pos]].items():
            print(str(i) + ". " + meal)

            # screen break every 10 recipes
            if i % 10 == 0:
                input("\nPress any key to continue...\n")

            i += 1

    def show_all(self):
        """given the index of a library, prints a numbered list of all recipes"""

        # print library
        for j in range(len(self._data)):
            print(str(j + 1) + ". " + list(self._data.keys())[j])
            i = 1
            # print list
            for meal, request in self._data[list(self._data.keys())[j]].items():
                print("    " + meal)

                # screen break every 10 recipes
                if i % 10 == 0:
                    input("\nPress any key to continue...\n")

                i += 1

    def review_recipes(self, pos):
        """given the index of a library, prints recipes in self._data in meal"""
        pos = int(pos) - 1

        # print meal of recipe in order
        i = 1
        for meal in self._data[list(self._data.keys())[pos]].items():
            print("\nShowing recipe #" + str(i) + ".")
            print("Recipe: " + meal)
            input("Press any key to see next recipe...")
            i += 1

    def edit_recipe(self, lib, key, key_str, value):
        """edit a recipe to the user's database at the given position"""

        # retype indices and save database and recipe keys to a list
        lib = int(lib) - 1
        key = int(key) - 1
        lib_list = list(self._data)
        recipe_list = list(self._data[lib_list[lib]])

        # swap old key with new, then update value
        self._data[lib_list[lib]][key_str] = self._data[lib_list[lib]].pop(recipe_list[key])
        self._data[lib_list[lib]][key_str] = value

    def save_recipes(self):
        """saves self._data contents as a json to same directory"""
        with open(self._name + '.json', 'w') as out_file:
            out_file.write(json.dumps(self._data))

    def delete_recipe(self, lib, key):
        """delete a recipe in the user's database"""

        # retype indices
        lib = int(lib) - 1
        key = int(key) - 1

        lib_list = list(self._data)
        recipe_list = list(self._data[lib_list[lib]])

        del self._data[lib_list[lib]][recipe_list[key]]

    def delete_all(self):
        """deletes recipes from self._data and from hard drive"""
        # delete data
        self._data = {}
        # delete file if it exists
        data_file = Path(self._name + ".json")
        if data_file.is_file():
            os.remove(self._name + '.json')

    def no_recipes(self):
        """returns true if user has no recipes, otherwise false"""
        if self._data == {}:
            return True
        else:
            return False

    def print_recipe(self, result):
        """prints recipes in self._data"""
        print("\nFound the following matches: ")

        # print library
        for lib, data in result.items():
            print("Library name: " + lib)
            print("Recipes (meal): ")

            # print recipe and request if you wanted recipe cooked for tonight
            i = 1
            for meal, request in sorted(self._data.items()):
                print("\nShowing recipe #" + str(i) + ".")
                print("Meal: " + meal)
                input("Press any key to see request from the AI...")
                making_sure = input("\nWould you like me to make {meal} for you tonight? Y/N")

                if making_sure.lower() == "y":
                    print("Alright! Good choice! Here is your delicious {meal}!")

                if making_sure.lower() == "n":
                    input("That is alright. Press any key to see next recipe...")

                # screen break every 10 recipes
                if i % 10 == 0:
                    input("\nPress any key to continue...\n")
                i += 1
                
