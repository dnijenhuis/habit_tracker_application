"""This test module asserts whether the update function correctly updates the database when it receives updates
regarding completion of habits from the user.
"""

import pytest
import sqlite3

import progression_module
import update_progression_module
import insert_sample_data_module
from unittest import mock
from datetime import datetime, timedelta


def test_update_function(capsys):
    """This test function asserts whether the update function correctly. It does this by calling the update_function
    from the update_progression_module and providing a test db with mocked input for 'today' and 'yesterday'. Next,
    it asserts whether the 'check-offs' have been correctly added to the database.
    Then, the function is called again and provided with different mock-input: unchecking the check-offs. Again, this
    test-function then asserts whether the unchecking has been correctly processed by the function and database.
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

    # Call the sample insertion function and provide it with the name of the test db and the three tables.
    insert_sample_data_module.insert_sample_data_before_distribution_of_app('test_Habit_app_database.db',
                                                                       'Habit_table',
                                                                       'Date_table',
                                                                       'Progression_table')

    # Combine the Habit_table, Date_table and Progression_table to make sure it contains all dates up to 'today'.
    progression_module.Progression.combine_habits_dates('test_Habit_app_database.db',
                                                         'Habit_table',
                                                         'Date_table',
                                                         'Progression_table')

    # Provide the function to be tested with mock input: the user meditated today and yesterday.
    with mock.patch('builtins.input', side_effect=['3', 'meditate', '1', '1', '3', 'meditate', '1', 'm']):
        update_progression_module.update_function('test_Habit_app_database.db')

    # Connect to the test db.
    conn = sqlite3.connect('test_Habit_app_database.db')
    cursor = conn.cursor()

    # Define today's and yesterday's date in the correct format.
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')

    # Check the completed value for today.
    cursor.execute("SELECT Completed FROM Progression_table WHERE date = ? AND habit_name = ?", (today, 'meditate'))
    today_completed = cursor.fetchone()
    assert today_completed[0] == 1

    # Check the value for yesterday.
    cursor.execute("SELECT Completed FROM Progression_table WHERE date = ? AND habit_name = ?", (yesterday, 'meditate'))
    yesterday_completed = cursor.fetchone()
    assert yesterday_completed[0] == 1

    # Again, provide the function to be tested with mock input: the user did NOT meditate today and yesterday.
    with mock.patch('builtins.input', side_effect=['3', 'meditate', '0', '1', '3', 'meditate', '0', 'm']):
        update_progression_module.update_function('test_Habit_app_database.db')

    # Check the completed value for today.
    cursor.execute("SELECT Completed FROM Progression_table WHERE date = ? AND habit_name = ?", (today, 'meditate'))
    today_completed = cursor.fetchone()
    assert today_completed[0] == 0

    # Check the value for yesterday.
    cursor.execute("SELECT Completed FROM Progression_table WHERE date = ? AND habit_name = ?", (yesterday, 'meditate'))
    yesterday_completed = cursor.fetchone()
    assert yesterday_completed[0] == 0

    # Prints are stored in this variable to prevent messing up the test report.
    stored_print = capsys.readouterr()

    # Close the database.
    conn.close()


if __name__ == '__main__':
    pytest.main()
