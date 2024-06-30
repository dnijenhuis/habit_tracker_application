"""This module tests the I_Empty_or_delete_database module which is (only) called from the main menu in order to
initialize an app reset. This test module asserts, using a test database, whether the tested function correctly
deletes the tables from the inputted database."""

import pytest
import sqlite3

import B_Table_module
import I_Empty_or_delete_database


def test_delete_tables_themselves():
    """This test function first sets up a test db. Next, it generates the tables for this test_db. Then, the tested
    function is called which deletes the tables again. Finally, the test function asserts whether there are, correctly,
    no more tables in the test db.
    """
    # First, it is made sure that the test_db is deleted for a fresh start.
    dbconnection = sqlite3.connect('test_Habit_app_database.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = dbconnection.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    for table_name in tables:
        c.execute(f"DROP TABLE IF EXISTS {table_name[0]}")
    dbconnection.commit()
    dbconnection.close()

    # Then, the tables are generated.
    B_Table_module.check_and_create_database('test_Habit_app_database.db')
    B_Table_module.create_habit_table('Habit_table', 'test_Habit_app_database.db')
    B_Table_module.create_date_table('Date_table', 'test_Habit_app_database.db')
    B_Table_module.create_progression_table('Progression_table', 'test_Habit_app_database.db')

    # The function delete_tables_themselves from the module I_Empty_or_delete_database is called, which should delete
    # all the tables.
    I_Empty_or_delete_database.delete_tables_themselves('test_Habit_app_database.db',
                                                        'Habit_table', 'Date_table',
                                                        'Progression_table')

    # Then it is asserted if there are, indeed, no more tables in the database.
    conn = sqlite3.connect('test_Habit_app_database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    assert len(tables) == 0

    conn.close()


if __name__ == '__main__':
    pytest.main()
