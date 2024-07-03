"""This is the Progression_class module. It only contains the class: Progression. Its main functions
 are to set the attributes for the Progression class, and to define the combine_habits_dates function. This function
 generates the data for the Progression_table based on data from both the Habit_table and Date_table."""

import sqlite3

import date_module


class Progression:
    """In this class, first the attributes for the Progression class are defined. These exist of
    date_plus_habit_name, habit_name, habit_periodicity, date and completed. Next, the function combine_habits_dates
    is defined. It combines data from the Habit_table and Date_table, creates data for the attribute
    date_plus_habit_name which is stored in then Progression_table.
    """

    def __init__(self, date_plus_habit_name, habit_name, habit_periodicity, date, completed):
        """This initializes the Progression class and sets its attributes.
        :param date_plus_habit_name: This is the unique row identifier, which is combined by habit_name and date. It
        is not directly used in the app's current functions. However, in my opinion, every table should always have
        a unique identifier value. Additionally, this column/attribute could be used in future versions of the app.
        :param habit_name: This is the name of the habit, acquired from the Habit_table.
        :param habit_periodicity: The periodicity of the habit, also acquired from the Habit_table.
        :param date: The date, acquired from the Date_table.
        :param completed: This stands for whether a certain habit on a certain day is completed (1) or not (0).
        """
        self.date_plus_habit_name = date_plus_habit_name
        self.habit_name = habit_name
        self.habit_periodicity = habit_periodicity
        self.date = date
        self.completed = completed

    def combine_habits_dates(database, habit_table_name, date_table_name, progression_table_name):
        """This first connects to the database. Then, using a for loop, the function combines the habit_name from the
        Habit_table and the date from the Date_table into one new datapoint for the column date_plus_habit_name.
        The combine_habits_dates function is called by the main menu before functions regarding analytics and the
        update of progress are performed. This to make sure that those functions perform operations on a complete and
        up-to-date table.

        The function also generates a default value of '0' (integer) for the last column of the Progression_table:
        'completed'. This column represents whether on a certain date a certain habit has been completed (1) or not (0).
        The default value of 0 means not-completed. This column/value represents the actual progress of the user, which
        can be updated by the user, analyzed through analytics functions, and/or printed to the user.
        """
        # Setting up database connection.
        dbconnection = sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES)
        c = dbconnection.cursor()

        # Update Date_table if necessary.
        date_module.Date.update_dates(database, date_table_name)

        # Next, the habit names and periodicity's and fetched from the Habit_table, and the dates from the Date_table.
        # This data is respectively stored in the variables 'habits' and 'dates'.
        c.execute(f"SELECT habit_name, habit_periodicity FROM {habit_table_name}")
        habits = c.fetchall()
        c.execute(f"SELECT date FROM {date_table_name}")
        dates = c.fetchall()

        # Here the default value of the completion column is set to 0 (which means the habit is not completed)
        default_completed_value = 0

        # Through a for loop, for each date in the Date_table, unique combinations are made from the first columns of
        # both the Date_table and the Habit_table. These are the columns date and habit_name. These are then combined
        # and stored into the variable date_plus_habit_name: the unique identifier of the Progression_table.
        for date in dates:
            for habit in habits:
                date_plus_habit_name = f"{date[0]} - {habit[0]}"

                # Next, in the table Progression_table, it is checked whether the unique date_plus_habit_name already
                # exists. If it does not exist (count==0), the date_plus_habit_name is inserted into the table
                # including the other relevant data. This procedure makes sure that every row in the Progression_table
                # has a unique identifier (date_plus_habit_name). Namely, there should be not more than 1 occurrence
                # of every habit on every date.
                c.execute(f"SELECT COUNT(*) FROM {progression_table_name} WHERE date_plus_habit_name = ?",
                          (date_plus_habit_name,))
                if c.fetchone()[0] == 0:
                    c.execute(f"INSERT INTO {progression_table_name} (date_plus_habit_name, habit_name, "
                              f"habit_periodicity, date, completed) VALUES (?,?,?,?,?)",
                              (date_plus_habit_name, habit[0], habit[1], date[0], default_completed_value))

        # Committing insertions to the database and closing the database.
        dbconnection.commit()
        dbconnection.close()
