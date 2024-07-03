"""In this test module, the functions for checking if the database and the tables exist and creating them are tested.
Because this testing should not be done on the production database, I adjusted the B_Table_module in such a way
that it could take arguments (Database name and Table name) instead of hard-coding the Database name and tables into
the functions (as I did earlier). This allowed for the functions to be tested with a 'test_' database..
"""
# This is the only module where I use this os module. Before, I used it at multiple locations in the app. However, it
# is a module that has functions which tend to produce database access errors when running the app and/or testing. I
# replaced these functions with sqlite3 functions for checking whether tables existed.
import os
import sqlite3
import pytest

import database_and_table_creation_module


def test_check_and_create_database():
    """The test_db is first created, then removed, and then created again. Next, it is tested whether the inserted
    database name exists."""
    database_and_table_creation_module.check_and_create_database('test_Habit_app_database.db')
    os.remove('test_Habit_app_database.db')
    database_and_table_creation_module.check_and_create_database('test_Habit_app_database.db')
    assert os.path.exists('test_Habit_app_database.db')


def test_create_habit_table():
    """A connection is set up to with the test_db. Next, the table is created through the respective function and
    the test checks whether the table exists after calling the function.
    """
    # First, it is made sure that the test_db is emptied for a fresh start.
    dbconnection = sqlite3.connect('test_Habit_app_database.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = dbconnection.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    for table_name in tables:
        c.execute(f"DROP TABLE IF EXISTS {table_name[0]}")
    dbconnection.commit()
    dbconnection.close()

    # Then, the table gets created in the test db and its existence is asserted.
    database_and_table_creation_module.check_and_create_database('test_Habit_app_database.db')
    dbconnection = sqlite3.connect('test_Habit_app_database.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = dbconnection.cursor()
    database_and_table_creation_module.create_habit_table('Habit_table', 'test_Habit_app_database.db')
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Habit_table';")
    table = c.fetchone()
    assert table is not None


def test_create_date_table():
    """A connection is set up to with the test_db. Next, the table is created through the respective function and
    the test checks whether the table exists after calling the function.
    """
    # First, it is made sure that the test_db is emptied for a fresh start.
    dbconnection = sqlite3.connect('test_Habit_app_database.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = dbconnection.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    for table_name in tables:
        c.execute(f"DROP TABLE IF EXISTS {table_name[0]}")
    dbconnection.commit()
    dbconnection.close()

    # Then, the table gets created in the test db and its existence is asserted.
    database_and_table_creation_module.check_and_create_database('test_Habit_app_database.db')
    dbconnection = sqlite3.connect('test_Habit_app_database.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = dbconnection.cursor()
    database_and_table_creation_module.create_date_table('Date_table', 'test_Habit_app_database.db')
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Date_table';")
    table = c.fetchone()
    assert table is not None


def test_create_progression_table():
    """A connection is set up to with the test_db. Next, the table is created through the respective function and
    the test checks whether the table exists after calling the function.
    """
    # First, it is made sure that the test_db is emptied for a fresh start.
    dbconnection = sqlite3.connect('test_Habit_app_database.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = dbconnection.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    for table_name in tables:
        c.execute(f"DROP TABLE IF EXISTS {table_name[0]}")
    dbconnection.commit()
    dbconnection.close()

    # Then, the table gets created in the test db and its existence is asserted.
    database_and_table_creation_module.check_and_create_database('test_Habit_app_database.db')
    dbconnection = sqlite3.connect('test_Habit_app_database.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = dbconnection.cursor()
    database_and_table_creation_module.create_progression_table('Progression_table', 'test_Habit_app_database.db')
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Progression_table';")
    table = c.fetchone()
    assert table is not None


if __name__ == '__main__':
    pytest.main()
