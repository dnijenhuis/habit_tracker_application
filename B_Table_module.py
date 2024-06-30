"""This module runs directly after starting the application. It checks whether the database and the three tables needed
for the application exist. If they do not exist, they are created. For the database and each of its tables, the module
contains one separate function. Additionally, for the Date_table, it inserts the starting value for the table
(2024-05-01). This module is also called from various test_modules in order to create a test database and tables.
"""

import sqlite3


def check_and_create_database(database_name):
    """This function checks if the (test)database needed exists. If it does not exist yet, it is created. If some
    error occurs, this is printed to the user.
    """
    try:
        connection = sqlite3.connect(database_name, detect_types=sqlite3.PARSE_DECLTYPES)
        connection.close()
    except sqlite3.Error as error:
        print("")
        print(f"A database error occurred: {error}")


def create_habit_table(table_name, database_name):
    """This function checks first if the table Habit_table does not exist yet. If not, then it creates the table.
    The table has columns equal to the Habit class.
    """
    dbconnection = sqlite3.connect(database_name, detect_types=sqlite3.PARSE_DECLTYPES)
    c = dbconnection.cursor()

    c.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
                habit_name TEXT,
                habit_description TEXT,
                habit_periodicity TEXT,
                habit_creation_date TEXT
                )""")

    dbconnection.commit()
    dbconnection.close()


def create_date_table(table_name, database_name):
    """This function checks first if the table Date_table does not exist yet. If not, then it creates the table.
    The table has 1 column, equal to the 1 attribute of the Date class. Then, it first checks if the table is
    empty and insert 2024-05-01 into the table if the table is empty. This to make sure that the function
    update_dates in the class Date_class can work correctly.
    """
    dbconnection = sqlite3.connect(database_name, detect_types=sqlite3.PARSE_DECLTYPES)
    c = dbconnection.cursor()

    c.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
                Date TEXT
                )""")

    c.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = c.fetchone()[0]
    if count == 0:
        c.execute(f"INSERT INTO {table_name} (Date) VALUES ('2024-05-01')")

    dbconnection.commit()
    dbconnection.close()


def create_progression_table(table_name, database_name):
    """This function creates the Progression_table if it does not exist yet. The table has columns equal to the
    attributes of the Progression class.
    """
    dbconnection = sqlite3.connect(database_name, detect_types=sqlite3.PARSE_DECLTYPES)
    c = dbconnection.cursor()

    c.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
                date_plus_habit_name TEXT,
                habit_name TEXT,
                habit_periodicity TEXT,
                date TEXT,
                completed INTEGER
                )""")

    dbconnection.commit()
    dbconnection.close()
