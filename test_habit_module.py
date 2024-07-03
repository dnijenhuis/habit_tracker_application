"""In this test module, all functions in the C_Habit_class module are tested. These are adding habits, providing lists
of habits and deleting habits.
"""
import pytest
import sqlite3

from datetime import datetime
from unittest import mock

import database_and_table_creation_module
import habit_module
import date_module
import progression_module


def test_add_habit(capsys):
    """This test function first empties the db and then makes sure that there is a database and tables. Then it
    calls the add_habit functions and provides input.

    Finally, it retrieves this habit (and all columns) from the table and asserts that the stored data is similar to
    the input given earlier.
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

    # Make sure there is a db and tables, and that the Habit_table does not contain the test habit_name.
    database_and_table_creation_module.check_and_create_database('test_Habit_app_database.db')
    database_and_table_creation_module.create_habit_table('Habit_table', 'test_Habit_app_database.db')

    # Provide input regarding the test habit to the add_habit function.
    with mock.patch('builtins.input', side_effect=['count midi chlorians', 'force sensitivity', '1']):
        habit_module.Habit.add_habit('test_Habit_app_database.db')

    stored_print = capsys.readouterr()  # This variable only gets used to prevent prints getting in the test report.

    connection = sqlite3.connect('test_Habit_app_database.db', detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Habit_table WHERE habit_name='count midi chlorians'")
    habit = cursor.fetchone()
    connection.close()

    # Tests to verify the habit was added correctly.
    assert habit is not None
    assert habit[0] == 'count midi chlorians'
    assert habit[1] == 'force sensitivity'
    assert habit[2] == 'weekly'
    # Also the automatically generated timestamp is checked. There is a very small but existing chance that this assert
    # function gives a 'fail' sometimes: theoretically, there is a chance that the habits are added (including their
    # timestamps) in minute x, while the rest of the test function including the assert functions are run in minute x+1.
    # However, correcting for this possibility, if possible at all, was not worth the effort in my opinion.
    assert habit[3] == datetime.now().strftime('%Y-%m-%d %H:%M')

    # Delete the test habit from the table.
    connection = sqlite3.connect('test_Habit_app_database.db', detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Habit_table WHERE habit_name='count midi chlorians'")
    connection.commit()
    connection.close()


def test_add_habit_invalid_input(capsys):
    """This test function tests whether the add_habit function correctly gives error messages when invalid input
    is given.
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

    # Ensure the test db and table exist.
    database_and_table_creation_module.check_and_create_database('test_Habit_app_database.db')
    database_and_table_creation_module.create_habit_table('Habit_table', 'test_Habit_app_database.db')

    # Call the add_habit function and provide it with mocked input regarding a test habit.
    # The mocked input is for every user prompt first given in a wrong format (-, !, 2), and then in the correct format.
    # This should result in 3 different error messages followed by 1 confirmation message.
    with mock.patch('builtins.input',
                    side_effect=['execute order-66', 'execute order 66', 'finally!', 'finally', '2', '1']):
        habit_module.Habit.add_habit('test_Habit_app_database.db')

    # Store the printed output to the stored_print variable.
    stored_print = capsys.readouterr()

    # Then it is tested whether the 3 error messages occurred, and whether the confirmation error occurred.
    assert "Habit name must only contain alphabetic characters and numbers. Please try again." in stored_print.out
    assert "Habit description must only contain alphabetic characters and numbers. Please try" in stored_print.out
    assert "Invalid input, please enter 0 for daily or 1 for weekly." in stored_print.out
    assert "You have added the habit 'execute order 66'. This is a 'weekly' habit." in stored_print.out

    # Connect to database again and check whether, indeed, there is no incorrect test habit in the Habit_table.
    connection = sqlite3.connect('test_Habit_app_database.db', detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Habit_table WHERE habit_name='execute order-66'")
    habit = cursor.fetchone()
    assert habit is None
    connection.close()

    # Lastly, also the good test habit is removed from the database.
    connection = sqlite3.connect('test_Habit_app_database.db', detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Habit_table WHERE habit_name='execute order 66'")
    connection.commit()
    connection.close()


def test_provide_habit_list(capsys):
    """This test function tests whether the full list of habits is correctly provided when the provide_habit_list
    function is called from the main menu. """
    # First, it is made sure that the test_db is emptied for a fresh start.
    dbconnection = sqlite3.connect('test_Habit_app_database.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = dbconnection.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    for table_name in tables:
        c.execute(f"DROP TABLE IF EXISTS {table_name[0]}")
    dbconnection.commit()
    dbconnection.close()

    # Then, it is made sure that the database and tables exist.
    database_and_table_creation_module.check_and_create_database('test_Habit_app_database.db')
    database_and_table_creation_module.create_habit_table('Habit_table', 'test_Habit_app_database.db')

    # The add_habit function is called four times. Two daily habits and two weekly habits are added.
    with mock.patch('builtins.input', side_effect=['kill younglings', 'anything for love', '0']):
        habit_module.Habit.add_habit('test_Habit_app_database.db')
    with mock.patch('builtins.input', side_effect=['do or do not', 'there is no try', '0']):
        habit_module.Habit.add_habit('test_Habit_app_database.db')
    with mock.patch('builtins.input', side_effect=['build death star', 'project manager needed', '1']):
        habit_module.Habit.add_habit('test_Habit_app_database.db')
    with mock.patch('builtins.input', side_effect=['kill jar jar binks', 'please', '1']):
        habit_module.Habit.add_habit('test_Habit_app_database.db')

    # Then the actual provide_habit_list function is called and the print is stored in the stored_print variable.
    habit_module.Habit.provide_habit_list('Habit_table', 'test_Habit_app_database.db')

    stored_print = capsys.readouterr()

    # Next, the prints are checked to make sure they contain all the relevant information. Not the piece of code I am
    # most proud of though. I first tried to paste the whole desired table layout into the 'assert' function.
    # This did not take, so I decided to assert the various elements separately. Hereby I took into account that by
    # first adding the habits, already several data was printed (two prints for habit names and periodicity).
    # I decided not to spend much more time on this test function since the function could be very easily tested by
    # just calling forth the list through the main menu and checking the contents and layout. Spending much more time
    # on 'automating' this through this test function would, in my opinion, defeat its purpose.
    assert "These are all your habits." in stored_print.out
    assert "Habit name" in stored_print.out
    assert "Description" in stored_print.out
    assert "Periodicity" in stored_print.out
    assert ("------------------------------------------------------------"
            "---------------------------------------------------------") in stored_print.out
    assert stored_print.out.count("kill younglings") == 2
    assert stored_print.out.count("do or do not") == 2
    assert stored_print.out.count("build death star") == 2
    assert stored_print.out.count("kill jar jar binks") == 2

    # 2 daily or weekly habits, printed twice: after adding and after printing the list.
    assert stored_print.out.count("daily") == 4
    assert stored_print.out.count("weekly") == 4

    # A connection to the db is again setup and the test habits are deleted.
    connection = sqlite3.connect('test_Habit_app_database.db', detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Habit_table WHERE habit_name='kill younglings'")
    cursor.execute("DELETE FROM Habit_table WHERE habit_name='do or do not'")
    cursor.execute("DELETE FROM Habit_table WHERE habit_name='build death star'")
    cursor.execute("DELETE FROM Habit_table WHERE habit_name='kill jar jar binks'")
    connection.commit()
    connection.close()


def test_provide_habit_list_per_periodicity(capsys):
    """This test function makes sure that the habit lists per periodicity are correctly and completely provided when
    the provide_habit_list_per_periodicity function is called."""

    # First, it is made sure that the test_db is emptied for a fresh start.
    dbconnection = sqlite3.connect('test_Habit_app_database.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = dbconnection.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    for table_name in tables:
        c.execute(f"DROP TABLE IF EXISTS {table_name[0]}")
    dbconnection.commit()
    dbconnection.close()

    # Then, it is made sure that the database and tables exist.
    database_and_table_creation_module.check_and_create_database('test_Habit_app_database.db')
    database_and_table_creation_module.create_habit_table('Habit_table', 'test_Habit_app_database.db')

    # The add_habit function is called four times and two daily habits, and two weekly habits are added.
    with mock.patch('builtins.input', side_effect=['kill younglings', 'anything for love', '0']):
        habit_module.Habit.add_habit('test_Habit_app_database.db')
    with mock.patch('builtins.input', side_effect=['do or do not', 'there is no try', '0']):
        habit_module.Habit.add_habit('test_Habit_app_database.db')
    with mock.patch('builtins.input', side_effect=['build death star', 'project manager needed', '1']):
        habit_module.Habit.add_habit('test_Habit_app_database.db')
    with mock.patch('builtins.input', side_effect=['kill jar jar binks', 'please', '1']):
        habit_module.Habit.add_habit('test_Habit_app_database.db')

    # First, for the actual testing, the list of daily habits are called and tested.
    with mock.patch('builtins.input', side_effect=['0']):  # Input of 0 calls daily habits.
        habit_module.Habit.provide_habit_list_per_periodicity('Habit_table',
                                                               'test_Habit_app_database.db')

    stored_print = capsys.readouterr()

    assert "These are all your daily habits, including their description and creation date." in stored_print.out
    assert "Habit name" in stored_print.out
    assert "Description" in stored_print.out
    assert "Creation date and time" in stored_print.out
    assert ("---------------------------------------------------------"
            "--------------------------------------------") in stored_print.out
    assert "kill younglings   " in stored_print.out
    assert "do or do not   " in stored_print.out
    # The following 2 are weekly habits, which should not be printed (except in the print after adding the habits).
    # Several spaces were added after habit name, so that the print after adding the habit does not count.
    assert "build death star   " not in stored_print.out
    assert "kill jar jar binks   " not in stored_print.out

    # And now the list of weekly habits will be called and tested.
    with mock.patch('builtins.input', side_effect=['1']):  # Input of 1 calls weekly habits.
        habit_module.Habit.provide_habit_list_per_periodicity('Habit_table',
                                                               'test_Habit_app_database.db')

    stored_print = capsys.readouterr()

    assert "These are all your weekly habits, including their description and creation date." in stored_print.out
    assert "Habit name" in stored_print.out
    assert "Description" in stored_print.out
    assert "Creation date and time" in stored_print.out
    assert ("----------------------------------------------------"
            "-------------------------------------------------") in stored_print.out
    assert "build death star   " in stored_print.out
    assert "kill jar jar binks   " in stored_print.out
    # The following 2 are daily habits, which should not be printed (except in the print after adding the habits).
    # Several spaces were added after habit name, so that the print after adding the habit does not count.
    assert "kill younglings   " not in stored_print.out
    assert "do or do not   " not in stored_print.out

    # The database connection is set up again and the test habits are deleted from the Habit_table.
    connection = sqlite3.connect('test_Habit_app_database.db', detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Habit_table WHERE habit_name='kill younglings'")
    cursor.execute("DELETE FROM Habit_table WHERE habit_name='do or do not'")
    cursor.execute("DELETE FROM Habit_table WHERE habit_name='build death star'")
    cursor.execute("DELETE FROM Habit_table WHERE habit_name='kill jar jar binks'")
    connection.commit()
    connection.close()


def test_delete_habit(capsys):
    """This function tests whether the deletion of a habit from the Habit_table and Progression_table works correctly.
    Though the test first passed, it did no longer work after I moved the PyCharm project to another folder in
    preparation of uploading it to GitHub. I kept getting the 'Database is locked' error when I called this test
    function. Accessing the delete_habit function directly and through the main menu did not raise any database
    issues.

    I have not been able to find out what the cause of this problem was. After an afternoon of trying I chose for
    a workaround and I adjusted the settings of the database in such a way that multiple access sessions at the same
    time were allowed (PRAGMA settings below). This is not the way this type of problem should be fixed. However,
    since the tested function showed no issues and the database lock error only seemed to occur in combination
    with the test_delete_habit function. Therefore, I preferred to spend time on other issues instead of fixing this
    error in the test function."""
    # First, it is made sure that the test_db is emptied for a fresh start.
    dbconnection = sqlite3.connect('test_Habit_app_database.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = dbconnection.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    for table_name in tables:
        c.execute(f"DROP TABLE IF EXISTS {table_name[0]}")
    dbconnection.commit()
    dbconnection.close()

    # Initiate the test db including the relevant tables.
    database_and_table_creation_module.check_and_create_database('test_Habit_app_database.db')
    database_and_table_creation_module.create_habit_table('Habit_table', 'test_Habit_app_database.db')
    database_and_table_creation_module.create_progression_table('Progression_table', 'test_Habit_app_database.db')

    # Make sure that the test habit is not (or no longer) in the tables.
    connection = sqlite3.connect('test_Habit_app_database.db', detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA synchronous=NORMAL;")
    cursor.execute("DELETE FROM Habit_table WHERE habit_name='train force push'")
    cursor.execute("DELETE FROM Progression_table WHERE habit_name='train force push'")
    connection.commit()
    connection.close()

    # Provide the add_habit function with the mocked input of the test habit and combine Habit_table and Date_table
    # into the Progression_table.
    with mock.patch('builtins.input', side_effect=['train force push', 'ouch', '0']):
        habit_module.Habit.add_habit('test_Habit_app_database.db')
    date_module.Date.update_dates('test_Habit_app_database.db', 'Date_table')
    progression_module.Progression.combine_habits_dates('test_Habit_app_database.db',
                                                         'Habit_table', 'Date_table',
                                                         'Progression_table')

    # Next, check whether the test habit has been added to the Habit_table and store it in the variable 'habit'.
    connection = sqlite3.connect('test_Habit_app_database.db', detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA synchronous=NORMAL;")
    cursor.execute("SELECT * FROM Habit_table WHERE habit_name='train force push'")
    habit = cursor.fetchone()
    connection.close()

    # Assert whether the variable 'habit' exists AND is equal to the name of the test habit.
    # Now these assertions pass, we are sure that the test habit is in fact in the database, so it can be deleted.
    assert habit is not None
    assert habit[0] == 'train force push'

    # Repeat the procedure above for the Progression_table
    connection = sqlite3.connect('test_Habit_app_database.db', detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA synchronous=NORMAL;")
    cursor.execute("SELECT * FROM Progression_table WHERE habit_name='train force push'")
    habit = cursor.fetchone()
    connection.close()

    assert habit is not None
    assert habit[
               1] == 'train force push'  # In the Progression_table, the habit_name is not the first but second column.

    # Call the delete function and provide the mocked input regarding the test habit.
    with mock.patch('builtins.input', side_effect=['train force push']):
        habit_module.Habit.delete_habit('test_Habit_app_database.db')

    # Store the printed messages regarding the deletion into the variable stored_print and assert whether it
    # contains, in fact, the confirmation message.
    stored_print = capsys.readouterr()

    assert "Habit 'train force push' and its related progressions have been deleted." in stored_print.out

    # Finally, check the relevant tables if they do no longer contain the test habit.
    connection = sqlite3.connect('test_Habit_app_database.db', detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA synchronous=NORMAL;")
    cursor.execute("SELECT * FROM Habit_table WHERE habit_name='train force push'")
    habit = cursor.fetchone()
    connection.close()

    assert habit is None

    connection = sqlite3.connect('test_Habit_app_database.db', detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA synchronous=NORMAL;")
    cursor.execute("SELECT * FROM Progression_table WHERE habit_name='train force push'")
    habit = cursor.fetchone()
    connection.close()

    assert habit is None


if __name__ == '__main__':
    pytest.main()
