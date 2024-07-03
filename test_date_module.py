"""In this test module, the update_dates function is tested. This function makes sure that the table Date_table from
the Habit_app_database always contains a complete and up-to-date list of all the dates up to and including 'the
current date'.
"""
import pytest
import sqlite3

from datetime import date, datetime

import database_and_table_creation_module
import date_module


def test_update_dates():
    """This test function sets up a test db and Date_table. The update_dates function is called, after which
    the contents of the Date_table are asserted. The test include the number of rows (dates) in the table and the
    type of data in the table.
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

    # Next, the create_date_table function is called which creates the Date_table and inserts 1 value in it,
    # being May 1st, 2024.
    database_and_table_creation_module.create_date_table('Date_table', 'test_Habit_app_database.db')

    # Then, the update_dates function gets called, initializing the update of the dates up to 'the current date'.
    date_module.Date.update_dates('test_Habit_app_database.db', 'Date_table')

    # As a first test, the number of rows (dates) in the table will be checked against the expected number of rows,
    # which is the difference between: the day this test function runs on one hand, and May 1st, 2024 on the other hand.
    current_date = date.today()
    start_date = date(2024, 5, 1)
    difference_in_days = current_date - start_date

    # This variable needs to be corrected by +1 because when calculating the 'difference', one day less is taken
    # into account. Furthermore, the Difference_in_days var need to be converted from datetime to integer to add '1'.
    difference_in_days_including_today = difference_in_days.days + 1

    # Counting the number of rows in the Date_table.
    dbconnection = sqlite3.connect('test_Habit_app_database.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = dbconnection.cursor()
    c.execute("SELECT COUNT(*) FROM Date_table")
    number_of_rows_in_table = c.fetchone()[0]
    c.close()

    # Comparing the calculated variables. There may be no less, but also no more dates than expected.
    assert difference_in_days_including_today == number_of_rows_in_table

    # The next lines of code connect to the database and fetch all rows from the Date_table. Then, through a for loop,
    # all values are checked to assert if they are all datetime values.
    dbconnection = sqlite3.connect('test_Habit_app_database.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = dbconnection.cursor()
    c.execute("SELECT * FROM Date_table")

    rows = c.fetchall()

    for row in rows:
        date_value = row[0]
        try:
            date_value == datetime.strptime(date_value, '%Y-%m-%d')
        except ValueError:
            raise AssertionError("Not all values in the Date_table are date values")

    c.close()


if __name__ == '__main__':
    pytest.main()
