"""This is the main module of this application. It contains the main menu from which the user can access all other
modules and functions.

The A_Main_menu module starts by importing the relevant SQL and date modules. Next, it imports all the other
application's modules. Then, the application checks whether the necessary tables exist and, if not, creates them.
Finally, before the main_menu() is called, the application makes sure that the Date_table is up-to-date with all
dates 'up to today'. This is necessary for reliably, accurately and completely performing analyses and updating habit
progress.

The main menu contains multiple options regarding adding/deleting habits, retrieving lists of habits, calculating
streaks, resetting the application and sample data, and quiting the application.
"""

# Importing modules necessary for the main menu and/or for the other modules called from the main menu.
import sqlite3
import time
import datetime

# Importing the other (relevant) modules from this application.
import database_and_table_creation_module
import habit_module
import date_module
import progression_module
import analysis_current_streak_per_habit
import analysis_longest_streak_ever
import update_progression_module
import insert_sample_data_module
import empty_database_module

# Print start message.
print("Starting habit tracker application...")
time.sleep(1)

# The following lines of code were added at the very last of this project. The test_module kept generating
# warnings when the tests were executed through Windows Powershell. These warnings were due to 'depreciation' of
# the datetime adapter/converter. Basically, the lines make sure that conversion from ISO-format to datetime and back
# in relation to SQL databases is executed correctly.
sqlite3.register_adapter(datetime.datetime, lambda ts: ts.isoformat())
sqlite3.register_converter('timestamp', lambda s: datetime.datetime.fromisoformat(s.decode('utf-8')))

# Checking if the operational database and its three necessary tables exist and, if not, creating them.
database_and_table_creation_module.check_and_create_database('Habit_app_database.db')
database_and_table_creation_module.create_habit_table('Habit_table', 'Habit_app_database.db')
database_and_table_creation_module.create_date_table('Date_table', 'Habit_app_database.db')
database_and_table_creation_module.create_progression_table('Progression_table', 'Habit_app_database.db')

# Updating the Date_table with all dates up to 'the current date' so all other functions work with an up-to-date table.
date_module.Date.update_dates('Habit_app_database.db', 'Date_table')


def main_menu():
    """The main menu contains five options: Adding a habit, deleting a habit, entering the analytics module, resetting
    the database and the sample data, and updating the habit progress. The analytics module of the app contains, again,
    four options: retrieving a list of all current habits, retrieving a list of all current habits per periodicity,
    calculating and printing the streaks of all current habits, and, calculating and printing the longest streak ever
    of all current habits. The menu also provides options to 'go back' to the main menu and quit the application."""
    print("")
    print("This is the main menu of the Habit Tracker app. ")
    print("What do you want to do? ")
    print("- Type 1 to add a new habit. ")
    print("- Type 2 to delete a habit. ")
    print("- Type 3 to enter the analytics module of this app. ")
    print("- Type 4 to update the periodic completion of your habits. ")
    print("- Type 'reset' to delete all data and start over with sample data.")
    print("- Type 'q' to quit the application. ")
    main_menu_input = (input("Insert your choice: "))
    if main_menu_input == "1":
        print("")
        habit_module.Habit.add_habit('Habit_app_database.db')
    elif main_menu_input == "2":
        print("")
        habit_module.Habit.delete_habit('Habit_app_database.db')
    elif main_menu_input == "3":
        print("")
        print("This is the analytics module. What do you want to do? ")
        print("- Type 1 to show a list of all your habits. ")
        print("- Type 2 to show a list of all habits for a specific periodicity. ")
        print("- Type 3 to show the current streaks of all your habits. ")
        print("- Type 4 to show the longest streak ever per habit. ")
        print("- Type 'm' to return to the main menu. ")
        analytics_module_input = (input("Insert your choice: "))
        if analytics_module_input == "1":
            habit_module.Habit.provide_habit_list('Habit_table', 'Habit_app_database.db')
        elif analytics_module_input == "2":
            habit_module.Habit.provide_habit_list_per_periodicity('Habit_table', 'Habit_app_database.db')
        elif analytics_module_input == "3":
            # The combine_habits_dates function is called to make sure that the Progression_table is complete and
            # up to date before it is analyzed.
            progression_module.Progression.combine_habits_dates('Habit_app_database.db',
                                                                 'Habit_table',
                                                                 'Date_table',
                                                                 'Progression_table')
            print("")
            print("These are all your habits including their daily/weekly streaks. ")
            analysis_current_streak_per_habit.calculate_and_print_streaks('Habit_app_database.db',
                                                                            'Habit_table',
                                                                            'Progression_table')
        elif analytics_module_input == "4":
            # The combine_habits_dates function is called to make sure that the Progression_table is complete and
            # up to date before it is analyzed.
            progression_module.Progression.combine_habits_dates('Habit_app_database.db',
                                                                 'Habit_table',
                                                                 'Date_table',
                                                                 'Progression_table')
            print("")
            print("These are all your habits including their longest daily/weekly streak ever. ")
            analysis_longest_streak_ever.calculate_and_print_longest_streaks_ever(
                'Habit_app_database.db', 'Habit_table', 'Progression_table')
        elif analytics_module_input == "m":
            main_menu()
        else:
            print("")
            print("Invalid input, please type '1', '2', '3', '4' or 'm'. ")

    elif main_menu_input == "reset":
        print("")
        print("This will delete all your data and progress. The app will start over with sample data.")
        reset_input = (input("Are you sure? Type again 'reset' to reset, type 'c' to cancel the reset: "))
        if reset_input == 'reset':
            empty_database_module.delete_tables_themselves('Habit_app_database.db',
                                                                'Habit_table',
                                                                'Date_table',
                                                                'Progression_table')
            insert_sample_data_module.insert_sample_data_before_distribution_of_app('Habit_app_database.db',
                                                                               'Habit_table',
                                                                               'Date_table',
                                                                               'Progression_table')
            print("")
            print("Deleting database...")
            time.sleep(2)
            print("Database deleted.")
            print("")
            print("Reinitializing database and loading sample data...")
            time.sleep(2)
            print("Punch it Chewie!")
            time.sleep(1)
            print("Database ready.")
        elif reset_input == "c":
            main_menu()
        else:
            print("")
            print("Invalid input, reset aborted.")
    elif main_menu_input == "4":
        progression_module.Progression.combine_habits_dates('Habit_app_database.db',
                                                             'Habit_table', 'Date_table',
                                                             'Progression_table')
        update_progression_module.update_function('Habit_app_database.db')
    elif main_menu_input == "q":
        print("Application shut down.")
        quit()
    else:
        print("")
        print("Invalid input, please type '1', '2', '3', '4' or 'q'. ")
    main_menu()


# Here the main_menu() function gets called when the application has started and performed all initial imports, checks
# and updates. A 'main guard' was added to prevent errors when importing this module from the related test module.
if __name__ == '__main__':
    main_menu()
