"""During development and testing of this application, this module was used. It imports sample data into the
Habit_table and Progression_table (data for the Date_table is generated automatically based on 'the current date').

When the application is distributed to the user, the sample data is also distributed as both a CSV-file and as loaded
habit data ready for analysis. During the end of the project I decided to create an option in the main menu of the app
to reset the database and insert (again) the sample data. The reason for this was for to make sure that during the
grading of this project the sample data could be manipulated in every way possible, and then retrieved (again) and
used if needed.
"""

import sqlite3
import pandas

import database_and_table_creation_module
import date_module


def insert_sample_habit_data_and_dates(database, habit_table_name, date_table_name, progression_table_name):
    """This function first makes sure the needed db and tables exist. Then, it updates the Date_table.
    Finally, the sample habits are inserted into the (test_)Habit_table."""
    # Run the following functions to make sure tables exist, and that the Date_table is complete and up-to-date.
    database_and_table_creation_module.check_and_create_database(database)
    database_and_table_creation_module.create_habit_table(habit_table_name, database)
    database_and_table_creation_module.create_date_table(date_table_name, database)
    database_and_table_creation_module.create_progression_table(progression_table_name, database)

    date_module.Date.update_dates(database, date_table_name)

    # Connecting to the database.
    dbconnection = sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES)
    c = dbconnection.cursor()

    # Insert the habit data into the Habit_table.
    c.execute(
        f"INSERT INTO {habit_table_name} (habit_name, habit_description, habit_periodicity, habit_creation_date) "
        f"VALUES (?, ?, ?, ?)",
        ('lightsaber training', 'single blade and double bladed', 'daily', '2024-05-01 14:50'))
    c.execute(
        f"INSERT INTO {habit_table_name} (habit_name, habit_description, habit_periodicity, habit_creation_date) "
        f"VALUES (?, ?, ?, ?)",
        ('meditate', 'meditate on the sith code', 'daily', '2024-05-01 14:51'))
    c.execute(
        f"INSERT INTO {habit_table_name} (habit_name, habit_description, habit_periodicity, habit_creation_date) "
        f"VALUES (?, ?, ?, ?)",
        ('practice force lightning', 'unlimited power', 'weekly', '2024-05-01 14:52'))
    c.execute(
        f"INSERT INTO {habit_table_name} (habit_name, habit_description, habit_periodicity, habit_creation_date) "
        f"VALUES (?, ?, ?, ?)",
        ('attend senate', 'boring but crucial', 'weekly', '2024-05-01 14:53'))
    c.execute(
        f"INSERT INTO {habit_table_name} (habit_name, habit_description, habit_periodicity, habit_creation_date) "
        f"VALUES (?, ?, ?, ?)",
        ('wash robes', 'be sure to use detergent for black fabric', 'weekly', '2024-05-01 14:54'))

    # Close database.
    dbconnection.commit()
    dbconnection.close()


def insert_sample_progression_data(database, habit_table_name, date_table_name, progression_table_name):
    """This function first makes sure the needed db and tables exist. Then, it inserts the sample progression data
    from the CSV-file into the (test_)Progression_table."""
    # Generate needed tables.
    database_and_table_creation_module.check_and_create_database(database)
    database_and_table_creation_module.create_habit_table(habit_table_name, database)
    database_and_table_creation_module.create_date_table(date_table_name, database)
    database_and_table_creation_module.create_progression_table(progression_table_name, database)

    # Connecting to the database.
    dbconnection = sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES)

    # Read the CSV file with the progression data and insert it into the Progression_table. Separation sign is the ';'.
    pandas.read_csv('Sample_data.csv', sep=';').to_sql(progression_table_name, dbconnection,
                                                         if_exists='append', index=False)

    # Close database.
    dbconnection.commit()
    dbconnection.close()


def insert_sample_data_before_distribution_of_app(database, habit_table_name, date_table_name, progression_table_name):
    """This function only combines the two functions above. By executing it, the sample data gets inserted into
    the database's tables."""
    insert_sample_habit_data_and_dates(database, habit_table_name, date_table_name, progression_table_name)
    insert_sample_progression_data(database, habit_table_name, date_table_name, progression_table_name)
