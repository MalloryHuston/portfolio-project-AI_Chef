# Title: AI Chef User Directory
# Class: CS 361 - Software Engineering I
# Author: Mallory Huston
# Description: An artificially intelligent chef that cooks any available recipe you want
#              that runs via a command prompt interface.

import json
from pathlib import Path
import os


class User:
    """Represents a user, with credentials and recipes."""
    # initialize data members
    def __init__(self, name, pwd):

        # open and read user's json file if it exists
        data_file = Path(name + ".json")
        if data_file.is_file():
            # open file and load into data
            with open(name + '.json', 'r') as in_file:
                self._data = json.load(in_file)

        # dictionary defaults to None
        else:
            self._data = {}

        # save user details
        self._name = name
        self._pwd = pwd
        self._cred = {name: pwd}

        # check if credential file exists
        cred_file = Path(name + ".txt")
        if cred_file.is_file() is False:
            # create credentials file if it did not exist
            with open(name + ".txt", 'w') as file:
                file.write(json.dumps(self._cred))

    def add_recipe(self, recipe, request):
        """adds a recipe entry to user._data"""
        # creates directory if no recipes
        if self._data == {}:
            self._data = {recipe: request}

        # adds recipe to directory
        else:
            self._data[recipe] = request

    def show_recipes(self):
        """prints a numbered list of recipes"""
        i = 1
        # print list
        for meal in sorted(self._data.items()):
            print(str(i) + ". " + meal)

            # screen break every 10 recipes
            if i % 10 == 0:
                input("\nPress any key to continue...\n")

            i += 1

    def print_recipe(self):
        """prints recipes in self._data"""
        # print recipe and question if you wanted recipe cooked for tonight
        i = 1
        for meal, request in sorted(self._data.items()):
            print("\nShowing recipe #" + str(i) + ".")
            print("Meal: " + meal)
            input("Press any key to see request from the AI...")
            print("Request: " + request)
            input("Press any key to see next recipe...")

            i += 1

    def save_recipes(self):
        """saves self.data contents as a json to same directory"""
        with open(self._name + '.json', 'w') as out_file:
            out_file.write(json.dumps(self._data))

    def delete(self):
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

def authenticate(name, pwd):
    """checks user name/pwd against existing credentials"""
    # check if user credential txt file exists
    file = Path(name + ".txt")
    if file.is_file():
        # open and read file
        with open(name + '.txt', 'r') as in_file:
            credential = json.load(in_file)

        # check if pwd matches file contents
        if str(credential[name]) == pwd:
            return True

    return False


def print_divide():
    """prints a screen divide"""
    print("\n---------------------------------------------"
          "\n")


def login():
    """login screen routine"""
    while True:
        print_divide()
        # prompt user
        login_input = input("Please select an option: "
                            "\n1. Enter Username"
                            "\n2. Return to previous screen"
                            "\n-> ")

        # attempt login
        if login_input == "1":
            name = input("\nUsername -> ")
            pwd = input("Password -> ")

            # authenticate input
            if authenticate(name, pwd) is True:
                # access account
                print("\nSuccess! Opening your account, " + name + ".")
                account(name, pwd)

            else:
                # retry
                print("\nLogin failed. Please enter a valid Username and password.")
                continue

            # if return from successful account login, exit login loop
            break

        # return to previous screen
        if login_input == "2":
            # go back to main screen
            print("\nReturning to previous screen.")
            return

        # invalid entry
        else:
            print("Error! Please enter a valid input.")
            continue


def account(name, pwd):
    """account page routine"""
    # create user object with credentials
    user = User(name, pwd)

    while True:
        print_divide()
        # prompt user
        account_input = input("Welcome to your AI Chef account! Please enter the number of an option below:"
                              "\n1. View your recipes"
                              "\n2. Create new recipe - customizable in just two steps!"
                              "\n3. Delete your recipes"
                              "\n4. Logoff"
                              "\n5. Help options"
                              "\n-> ")

        # display recipe
        if account_input == "1":
            # if user has no saved recipes, notify and return to menu
            if user.no_recipes():
                print("\nYou currently have no recipes to view! Please make a new recipe from your account menu.")
                input("Press any key to return to the previous screen...")

            # show user's recipes
            else:
                print("\nShowing a list of all of your recipes: ")
                # print list
                user.show_recipes
                # iterate through each recipe
                user.print_recipe()

                # notify user end of list has been reached
                input("\nNo more recipes to show. Press any key to return to account...")

        # create recipe
        elif account_input == "2":
            # prompt user for meal and request
            meal = input("\nPlease enter text for a simple recipe you love eating: ")
            request = input("Sounds like a delicious meal! Let me process making {meal} real quick. Press any key to continue...")

            # confirm recipe
            print("\nYou have entered front: " + meal )
            finalize = input("\nWould you like me to make this {meal} for you tonight? Y/N: ")

            # save recipe
            if finalize.lower() == "y":
                print("Fabulous! Your {meal} is now ready!")
                user.add_recipe(meal, request)

            # do nothing
            elif finalize.lower() == "n":
                print("Understood. No hard feelings!")
                confirmation = input("\nWould you still like me to save this recipe for you anyway? WARNING: Any unsaved changes will be lost. Y/N: ")

                if confirmation.lower() == "y":
                    print("Recipe saved!")
                    user.add_recipe(meal, request)

                if confirmation.lower() == "n":
                    print("Recipe not saved.")
                    continue

            else:
                print("Invalid entry. Returning to account.")

        # delete ALL recipes
        elif account_input == "3":
            # confirm choice to delete
            delete = input("Delete your recipe(s)? Y/N: ")

            # delete all recipes in user object and hold recipe file associated with user credentials
            if delete.lower() == "y":
                print("Recipes deleted!")
                user.delete()

            # do nothing
            elif delete.lower() == "n":
                print("Recipes will not be deleted.")
                continue

            else:
                print("Invalid entry. Returning to account.")

        # logoff user
        elif account_input == "4":
            # first, save data to hdd
            user.save_recipes()
            # return to previous menu
            break

        # help menu/invalid entry
        else:
            print("\nWelcome to user account help.")
            print("To navigate, please enter the number of the choice you wish after the -> symbol.")
            print("Any other key entry will bring you to the help menu.")
            input("To return to your account page, press any key...")
            continue


def create_account():
    """create a new user account"""
    while True:
        print_divide()
        # prompt user
        create_input = input("Welcome aboard to AI Chef! Please select an option: "
                             "\n1. Select your user name"
                             "\n2. Return to login screen"
                             "\n3. Help options"
                             "\n-> ")

        # display recipe
        if create_input == "1":

            # prompt user for user name and password
            while True:
                # get user name
                user_name = input("\nEnter your new user name: ")
                # check if credential file exists
                cred_file = Path(user_name + ".txt")
                if cred_file.is_file():
                    # print error message
                    print("Error! That user name already exists. Please enter a new choice.")
                    exit_create = input("Or type Q to return to the previous screen: ")

                    # return to account creation screen
                    if exit_create.lower() == "q":
                        break

                    else:
                        continue

                # get user password
                else:
                    user_pwd = input("Please enter a new password: ")

                    # create new user object with input
                    user = User(user_name, user_pwd)

                    # print success notification
                    print("\nAccount creation successful!")
                    input("Logging into your account. Press any key to continue...")

                    # log user into account
                    account(user_name, user_pwd)

                # exit function
                # user will only reach this point after successfully creating a new account,
                # logging in, then logging out
                return

        # return to previous screen
        elif create_input == "2":
            return

        # help menu/invalid input
        else:
            print("\nWelcome to account creation help.")
            print("To navigate, please enter the number of the choice you wish after the -> symbol.")
            print("Any other key entry will bring you to the help menu.")
            input("To return to account creation, press any key...")
            continue


if __name__ == '__main__':

    # initialize app
    while True:
        print_divide()

        # main menu prompt
        user_input = input("Welcome to AI Chef! Please choose an option: "
                           "\n1. Login"
                           "\n2. Create new account"
                           "\n3. Exit AI Chef"
                           "\n4. Help options"
                           "\n-> ")

        # go to login screen
        if user_input == "1":
            login()

        # go to new account creation
        elif user_input == "2":
            create_account()

        # terminate program
        elif user_input == "3":
            break

        # all other key entries
        else:
            print("\nWelcome to AI Chef help.")
            print("To navigate, please enter the number of the choice you wish after the -> symbol.")
            print("Any other key entry will bring you to the help menu.")
            input("To return to the main menu, press any key...")
            continue
