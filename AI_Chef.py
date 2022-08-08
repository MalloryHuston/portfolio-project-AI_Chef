# Title: AI Chef Search Interface
# Class: CS 361 - Software Engineering I
# Author: Mallory Huston
# Description: An artificially intelligent chef that cooks any available recipe you want
#              that runs via a command prompt interface.

import json
from pathlib import Path
from AI_Chef_User import User


# ---------------------------------------------------------------------------
#
# General use functionality
#
# ---------------------------------------------------------------------------

def print_divide():
    """prints a screen divide"""
    print("\n---------------------------------------------"
          "\n")


# ---------------------------------------------------------------------------
#
# Login page functionality
#
# ---------------------------------------------------------------------------

def authenticate(name, pwd):
    """checks username/pwd against existing credentials"""
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


def credential_input():
    """receives login input and logs user in"""
    name = input("\nUsername -> ")
    pwd = input("Password -> ")

    # authenticate input and access account
    if authenticate(name, pwd) is True:
        print("\nSuccess! Opening your account, " + name + ".")
        account(name, pwd)

    else:
        print("\nLogin failed. Please enter a valid Username and password.")
        return


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
            credential_input()

            # if return from successful account login, exit login loop
            break

        # return to previous screen
        if login_input == "2":
            print("\nReturning to previous screen.")
            return

        # invalid entry
        else:
            print("Error! Please enter a valid input.")
            continue


# ---------------------------------------------------------------------------
#
# Account page functionality
#
# ---------------------------------------------------------------------------

def add_library(user):
    """add collection to create recipe"""
    lib_name = input("\nEnter recipe library name: ")

    # confirm library
    print("\nYou have entered: " + lib_name)
    finalize = input("\nSave this collection? Y/N: ")

    # save library
    if finalize.lower() == "y":
        user.add_library(lib_name)
        input("Collection added! Press any key to return...")

    # do nothing
    elif finalize.lower() == "n":
        print("Library not saved.")
        return


def add_recipe_confirmation(user, pos):
    """gets and confirms recipe data for add recipe"""
    # prompt user for meal and request
    meal = input("\nPlease enter text for a simple recipe you love eating: ")
    request = input(f"Sounds like a delicious meal! Let me process making {meal} real quick. Press any key to "
                    "continue...")

    # confirm recipe
    print("\nYou have entered the following meal: " + meal)
    finalize = input(f"Would you like me to make this {meal} for you tonight? Y/N: ")

    # save recipe
    if finalize.lower() == "y":
        print(f"Fabulous! Your {meal} is now ready!")
        user.add_recipe(pos, meal, request)

    # do nothing
    elif finalize.lower() == "n":
        print("Understood. No hard feelings!")
        confirmation = input("\nWould you still like me to save this recipe for you anyway? WARNING: Any "
                             "unsaved changes will be lost. Y/N: ")

        if confirmation.lower() == "y":
            print("Recipe saved!")
            user.add_recipe(pos, meal, request)

        if confirmation.lower() == "n":
            print("Recipe not saved.")
            return

    else:
        print("Invalid entry. Press any key to return to account...")


def add_recipe(user):
    """adds a new recipe to a library for create recipe"""
    if user.no_recipes():
        print("\nYou have no libraries of recipes! Make a library first.")
        return

    else:
        print("\nYour libraries: ")
        user.show_library()
        pos = input("\nSelect a library to add the recipe to: ")

        # if user entry is valid, proceed to recipe creation
        if pos.isdigit() and user.valid_index(pos):
            add_recipe_confirmation(user, pos)

        # invalid pos input
        else:
            input("Invalid entry. Press any key to return to account...")


def create_recipe(user):
    """recipe creation routine: prompts user to create and add recipes to collections."""
    print_divide()
    # create recipe routine
    while True:
        recipe_input = input("\nWelcome to recipe creation! Please select an option: "
                             "\n1. Create new library - start here!"
                             "\n2. Add recipe to library"
                             "\n3. Return to previous screen"
                             "\n-> ")
        # new collection
        if recipe_input == "1":
            add_library(user)

        # new recipe
        elif recipe_input == "2":
            add_recipe(user)

        # return to previous screen
        elif recipe_input == "3":
            break

        else:
            input("\nInvalid input! Press any key to return...")
            continue


def display_recipes_review(user):
    """recipe reviewing function for display recipes"""
    print("\nShowing a list of all your saved recipes: ")
    user.show_all()

    pos = input("\nEnter the number of the library you wish to browse: ")

    # if valid entry, browse recipes for the given library
    if pos.isdigit() and user.valid_index(pos):
        user.review_recipes(pos)

        finalize = input("Would you like me to make a wonderful meal for you later? Y/N: ")

        # cook recipe
        if finalize.lower() == "y":
            user.show_recipes(pos)
            lib = input("\nGreat! Which recipe # do you want me to cook? ")

            if user.valid_index(lib):
                print(f"Fabulous! Recipe #{lib} is now ready!")

            else:
                print("Invalid entry!")

        # hold off on recipe for now
        if finalize.lower() == "n":
            print("Understood. No hard feelings!")

    # otherwise return to account
    else:
        input("Invalid entry! Press any key to return to account...")
        return


def display_recipes(user):
    """display recipes from edit/delete menu"""
    # check for recipes
    if user.no_recipes():
        print("\nYou currently have no recipes to view! Please make a new recipe from your account menu.")
        input("Press any key to return to the previous screen...")

    # show user's recipes
    else:
        display_recipes_review(user)

        input("\nNo more recipes to show. Press any key to return to account...")


def edit_recipes_confirmation(user, lib):
    """selects and confirms edits for a recipe in a library of edit recipes"""
    print("\nSelect recipe to edit:")
    user.show_recipes(lib)

    # get edit inputs for edit_recipe()
    key = input("\nEnter selection: ")
    meal = input("Enter meal: ")
    request = print(f"That {meal} looks yummy!")

    confirm = input("You entered meal: " + meal + ".\nKeep changes? Y/N: ")

    if confirm.lower() == "y":
        user.edit_recipe(lib, key, meal, request)
        finalize = input(f"Would you like me to make this {meal} for you tonight? Y/N: ")
        
        # cook recipe
        if finalize.lower() == "y":
            print(f"Fabulous! Your {meal} is now ready!")

        # hold off on recipe for now
        if finalize.lower() == "n":
            print("Understood. No hard feelings!")

    else:
        "Edit will not be saved."


def edit_recipes(user):
    """edit recipe option from edit/delete menu"""
    print("\nSelect a library:")
    user.show_library()

    lib = input("\nEnter selection: ")

    # get recipe to edit
    if user.valid_index(lib):
        edit_recipes_confirmation(user, lib)

    else:
        print("Invalid entry!")


def delete_one_confirmation(user, lib):
    """confirms and deletes one recipe for delete one"""
    print("\nSelect recipe to delete:")
    user.show_recipes(lib)

    key = input("\nEnter selection: ")
    confirm = input("Are you sure you want to delete this recipe? Y/N: ")

    # delete recipe
    if confirm.lower() == "y":
        user.delete_recipe(lib, key)

    else:
        "No changes made."


def delete_one(user):
    """delete one recipe from edit/delete menu"""
    print("\nSelect a library:")
    user.show_library()

    lib = input("\nEnter selection: ")

    # get recipe to delete
    if user.valid_index(lib):
        delete_one_confirmation(user, lib)

    else:
        print("Invalid entry!")


def delete_all(user):
    """delete all recipes from edit/delete menu"""
    delete = input("ARE YOU SURE you want to delete all your recipe(s)? Y/N: ")

    # delete all recipes in user object and hdd recipe file associated with user credentials
    if delete.lower() == "y":
        print("Recipes deleted!")
        user.delete_all()

    elif delete.lower() == "n":
        print("Recipes will not be deleted.")

    else:
        print("Invalid entry. Returning to account.")


def edit_delete_menu(user):
    """edit/delete menu selection from account"""
    edit_input = input("\nSelect an option below:"
                       "\n1. Edit a recipe"
                       "\n2. Delete a recipe"
                       "\n3. Delete ALL recipes"
                       "\n-> ")
    # edit a recipe
    if edit_input == "1":
        edit_recipes(user)

    # delete one recipe
    elif edit_input == "2":
        delete_one(user)

    # delete ALL
    elif edit_input == "3":
        delete_all(user)


def account(name, pwd):
    """account page routine"""
    # create user object with credentials
    user = User(name, pwd)

    while True:
        print_divide()
        # prompt user
        account_input = input("Welcome to your AI Chef account! Please enter the number of an option below:"
                              "\n1. View your recipes - cycles through each recipe in a library."
                              "\n2. Create new recipe or library - create and customize in just two steps!"
                              "\n3. Edit/delete your recipes - new!"
                              "\n5. Logoff"
                              "\n6. Help options"
                              "\n-> ")

        # display recipe
        if account_input == "1":
            display_recipes(user)

        # create recipe
        elif account_input == "2":
            create_recipe(user)

        # edit/delete
        elif account_input == "3":
            edit_delete_menu(user)

        # save recipes and logoff
        elif account_input == "5":
            user.save_recipes()
            break

        # help menu/invalid entry
        else:
            print("\nWelcome to user account help.")
            print("To navigate, please enter the number of the choice you wish after the -> symbol.")
            print("Any other key entry will bring you to the help menu.")
            input("To return to your account page, press any key...")
            continue


# ---------------------------------------------------------------------------
#
# Create new account page functionality
#
# ---------------------------------------------------------------------------

def user_name_select():
    """username and password selection for create account"""
    while True:
        user_name = input("\nEnter your new user name: ")

        # check if credential file exists
        cred_file = Path(user_name + ".txt")
        if cred_file.is_file():
            print("Error! That user name already exists. Please enter a new choice.")
            exit_create = input("Or type Q to return to the previous screen: ")

            # return to account creation screen
            if exit_create.lower() == "q":
                return

            else:
                continue

        # create new credentials
        else:
            user_pwd = input("Please enter a new password: ")

            print("\nAccount creation successful!")
            input("Logging into your account. Press any key to continue...")

            # log user into account
            account(user_name, user_pwd)
        return


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

        if create_input == "1":
            user_name_select()
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
