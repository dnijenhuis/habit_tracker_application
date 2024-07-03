"""This is the Habit_class module. It only contains the class 'Habit'. In this class, the functions for adding a habit,
storing it into the database, providing habit lists and deleting habits are contained.
"""

import sqlite3
from datetime import datetime


class Habit:
    """The class 'Habit' starts by defining the class and its attributes. Next, it defines functions related to
    creating and storing new habits, providing lists of current habits, and deleting habits.
    """

    def __init__(self, habit_name, habit_description, habit_periodicity, habit_creation_date):
        """Here the attributes of the class 'Habit' are defined.
        :param habit_name: This is the habit name that the user can give. It is the unique attribute/row and a string.
        :param habit_description: This is the description. This is a string.
        :param habit_periodicity: This is the periodicity, it is either daily or weekly.
        :param habit_creation_date: This is the date and time on which the habit has been created.

        Personal reflection: lately during the project I realized that not just the creating date, but also the time
        was required. I had to adjust the code and check whether this had implications for the rest of the app.
        """
        self.habit_name = habit_name
        self.habit_description = habit_description
        self.habit_periodicity = habit_periodicity
        self.habit_creation_date = habit_creation_date

    @classmethod
    def add_habit(cls, database):
        """This function allows the user to create a new habit. It is called upon from the main menu. It prompts
        the user for input on the habit name, description, and periodicity. Several limitations are implemented for
        stability and security: input is limited regarding length and usable characters. Also, the input is trimmed of
        unnecessary spaces, and it is converted to lower cases. To prevent querying issues in the analytical functions,
        the generating of data in the Progression_class, etc., a check is performed whether the Habit_name does not
        yet exist. This ensures unique data in this crucial attribute/column. The function automatically generates data
        for the habit_creation_date, which is exact at the minute (which should be exact enough considering its usage).

        The created variables are then stored in the variable 'new_habit' which is then stored in the database through
        the function 'save_to_database'.
        """
        # Input for the habit name.
        while True:
            habit_name = input("Enter the name of the habit (min 1 character, max 30 characters), or "
                               "type 'c' to cancel. ").strip().lower()
            if habit_name == 'c':
                return
            elif len(habit_name) > 30 or len(habit_name) < 1:
                print("Habit name must be between 1 and 30 long. ")
            elif not habit_name.replace(' ', '').isalnum():
                print("Habit name must only contain alphabetic characters and numbers. Please try again.")
            else:
                dbconnection = sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES)
                c = dbconnection.cursor()
                c.execute("SELECT COUNT(*) FROM Habit_table WHERE habit_name = ?", (habit_name,))
                count = c.fetchone()[0]
                if count > 0:
                    print("Habit name already exists. Please enter a different name.")
                else:
                    break

        # Input for the habit description.
        while True:
            habit_description = input("Enter the description of the habit (max 45 characters): ").strip().lower()
            if len(habit_description) > 45:
                print("Habit description must be 45 characters or fewer. Please try again.")
            elif not habit_description.replace(' ', '').isalnum():
                print("Habit description must only contain alphabetic characters and numbers. Please try again.")
            else:
                break

        # Input for the habit periodicity.
        while True:
            try:
                habit_periodicity_temp = int(
                    input("What is the interval of this habit? Type 0 for daily, 1 for weekly: ").strip())
                if habit_periodicity_temp not in [0, 1]:
                    print("Invalid input, please enter 0 for daily or 1 for weekly.")
                else:
                    habit_periodicity = "daily" if habit_periodicity_temp == 0 else "weekly"
                    break
            except ValueError:
                print("Invalid input, please enter 0 for daily or 1 for weekly.")

        # Habit creation date and time is automatically generated. The datetime is 'abbreviated' to the minute level.
        habit_creation_date = datetime.now().strftime('%Y-%m-%d %H:%M')

        # Storing the data into the variable new_habit, which is then used by the function save_to_database.
        new_habit = cls(habit_name, habit_description, habit_periodicity, habit_creation_date)
        new_habit.save_to_database(database)

    def save_to_database(self, database):
        """This function is called upon by the add_habit function which feeds the variable 'new_habit' into the
        save_to_database function. This variable contains data on the attributes of the new habit. Next, a connection
        to the database is set up and the new habit(data) is stored into the table 'Habit_table'. Then, the insertion
        is committed (made definitive) and the database is closed. Finally, a confirmation message is printed which
        can be seen from the main menu.
        """
        dbconnection = sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES)
        c = dbconnection.cursor()

        c.execute("INSERT INTO Habit_table (habit_name, habit_description, habit_periodicity, habit_creation_date) "
                  "VALUES (?, ?, ?, ?)",
                  (self.habit_name, self.habit_description, self.habit_periodicity, self.habit_creation_date))

        print("")
        print(f"You have added the habit '{self.habit_name}'. This is a '{self.habit_periodicity}' habit.")

        dbconnection.commit()
        dbconnection.close()

    def provide_habit_list(table, database):
        """This function is called from the main menu. It does not create an instance or call upon an instance,
        but accesses all instances instead.
        It first sets up a connection to the database and performs a complete query of the Habit_table. Next, it prints
        the habit names through a for loop. User-friendly names for the printed columns are used, so not the names
        of the columns in the table. Then, the database is closed.
        """
        # Connect to database.
        dbconnection = sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES)
        c = dbconnection.cursor()

        # Query all data from the Habit_table and store this in the variable all_habits.
        c.execute(f"SELECT * FROM {table}")
        all_habits = c.fetchall()

        # Then, user-friendly column names are printed (not the table column names) and the habit data itself is
        # printed using a for loop.
        print("")
        print("These are all your habits.")
        print(f"{'Habit name':<31} {'Description':<46} {'Periodicity':<15} {'Creation date and time':<20}")
        print("-" * 117)

        for habit in all_habits:
            name, description, periodicity, creation_date = habit
            print(f"{name:<31} {description:<46} {periodicity:<15} {creation_date:<20}")

        # The database is closed.
        dbconnection.close()

    def provide_habit_list_per_periodicity(table, database):
        """This function is quite similar to the provide_habit_list function. It first prompts the user for whether they
        want an overview of the daily or weekly habits. Next, based on the input of the user, it queries the database
        for either all daily or all weekly habits and prints these. User-friendly names are used, so not the names of
        the columns in the table. Then, it closes the database.
        """
        # Prompt user for input on which habits they want to see (daily or weekly).
        print("")
        specific_periodicity = int(input(
            "Of which specific periodicity would you like to see all the habits? Type 0 for daily, 1 for weekly: "))

        # Connect to database.
        dbconnection = sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES)
        c = dbconnection.cursor()

        # If the user wants to see all daily habits, all data from Habit_table is queried with a daily periodicity.
        # Next, user-friendly column names are printed (not the table column names) and the habit data itself is
        # printed using a for loop.
        if specific_periodicity == 0:
            c.execute(
                f"SELECT habit_name, habit_description, habit_creation_date FROM {table} "
                f"WHERE habit_periodicity='daily'")
            all_daily_habits = c.fetchall()
            print("")
            print("These are all your daily habits, including their description and creation date.")
            print(f"{'Habit name':<31} {'Description':<46} {'Creation date and time':<20}")
            print("-" * 101)
            for habit in all_daily_habits:
                name, description, creation_date = habit
                print(f"{name:<31} {description:<46} {creation_date:<20}")

        # If the user wants to see all weekly habits, all data from Habit_table is queried with a weekly periodicity.
        # Next, user-friendly column names are printed (not the table column names) and the habit data itself is
        # printed using a for loop.
        elif specific_periodicity == 1:
            c.execute(
                f"SELECT habit_name, habit_description, habit_creation_date FROM {table} "
                f"WHERE habit_periodicity='weekly'")
            all_weekly_habits = c.fetchall()
            print("")
            print("These are all your weekly habits, including their description and creation date.")
            print(f"{'Habit name':<31} {'Description':<46} {'Creation date and time':<20}")
            print("-" * 101)
            for habit in all_weekly_habits:
                name, description, creation_date = habit
                print(f"{name:<31} {description:<46} {creation_date:<20}")

        # Closing the database.
        dbconnection.close()

    @staticmethod
    def delete_habit(database):
        """This function deletes the habit selected by the user. First, it connects to the database, queries the
        Habit_table for all habits, and then prints all habits to the user using a for loop. Next, it prompts the
        user for the habit to be deleted which is stored into the variable 'habit_to_be_deleted'. If the user enters
        'c', the operation is cancelled and the user is returned to the main menu.

        Then, assuming the user enters the name of the habit to be deleted, the database is queried for all rows
        where the habit_name is equal to the entered name. If the habit is not found, this is printed. If the habit
        is found, the corresponding row in the Habit_table is deleted. Also, the corresponding row in the
        Progression_table is deleted to make sure that the habit does no longer show up when the user queries the
        database for data on streaks or when the user updates their progress. The deletion is made definitive by
        committing it to the database. Then, the database is closed.
        """
        # Connection to the database is set up.
        dbconnection = sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES)
        c = dbconnection.cursor()

        # All habit names in the Habit_table are queried and printed.
        c.execute("SELECT habit_name FROM Habit_table")
        all_habits = c.fetchall()
        print("These are all your habits: ")
        for i in all_habits:
            print(f"- {i[0]}")

        # The user is prompted for the habit they want to delete. They are also given the possibility to cancel.
        print("")
        habit_to_be_deleted = input(
            "Which habit do you want to delete? Enter the full name. Type 'c' to cancel: ").strip().lower()

        # If the user cancels, they go back to main menu.
        if habit_to_be_deleted.lower() == "c":
            print("Cancelled.")
            dbconnection.close()
            return

        # If the user enters a value different from 'c', the database is checked whether the habit exists. If it
        # exists, the habit data (all columns) is deleted from both the Habit_table and the Progression_table.
        c.execute("SELECT 1 FROM Habit_table WHERE habit_name = ?", (habit_to_be_deleted,))
        exists = c.fetchone() is not None
        if not exists:
            print("Habit name not found.")
        else:
            c.execute("DELETE FROM Habit_table WHERE habit_name = ?", (habit_to_be_deleted,))
            c.execute("DELETE FROM Progression_table WHERE habit_name = ?", (habit_to_be_deleted,))
            dbconnection.commit()
            print(f"Habit '{habit_to_be_deleted}' and its related progressions have been deleted.")

        # The database is closed.
        if dbconnection:
            dbconnection.close()
