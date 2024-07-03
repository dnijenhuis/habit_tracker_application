"""This test module asserts whether the sample data is correctly inserted into the database and its tables. It tests
this by using a test_db.
"""

import pytest
import sqlite3
import insert_sample_data_module


def test_insert_sample_data_before_distribution_of_app():
    """This test function first deletes the test db to make sure there is a fresh start. Then, it calls the function
    to be tested. This should generate the test db, the three tables, and insert the sample data. Then, several
    assertion tests are done to make sure that the necessary tables exist, they contain the expected number of
    columns and rows, that they contain the sample habits, the total number of completion check-offs, etc.
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

    # Call the tested function and provide it with the name of the test db and the three tables.
    insert_sample_data_module.insert_sample_data_before_distribution_of_app('test_Habit_app_database.db',
                                                                       'Habit_table',
                                                                       'Date_table',
                                                                       'Progression_table')

    # Connect to the test db.
    conn = sqlite3.connect('test_Habit_app_database.db')
    cursor = conn.cursor()

    # 1. Assert that the database contains the three expected tables.
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    table_names = [table[0] for table in tables]
    assert 'Habit_table' in table_names
    assert 'Date_table' in table_names
    assert 'Progression_table' in table_names
    assert len(table_names) == 3

    # 2. Assert that the Habit_table has 4 columns.
    cursor.execute("SELECT * FROM Habit_table LIMIT 1;")
    habit_table_column_count = len(cursor.description)
    assert habit_table_column_count == 4

    # 3. Assert that the Progression_table has 5 columns.
    cursor.execute("SELECT * FROM Progression_table LIMIT 1;")
    progression_table_column_count = len(cursor.description)
    assert progression_table_column_count == 5

    # 4. Assert that Habit_table has 5 rows.
    cursor.execute("SELECT COUNT(*) FROM Habit_table;")
    habit_table_row_count = cursor.fetchone()[0]
    assert habit_table_row_count == 5

    # 5. Assert that Progression_table has 180 rows.
    cursor.execute("SELECT COUNT(*) FROM Progression_table;")
    progression_table_row_count = cursor.fetchone()[0]
    assert progression_table_row_count == 180

    # 6. Assert that Habit_table contains the 5 sample habits.
    expected_habits = {'lightsaber training', 'meditate', 'practice force lightning', 'attend senate', 'wash robes'}
    cursor.execute("SELECT habit_name FROM Habit_table;")
    habits = {row[0] for row in cursor.fetchall()}
    assert expected_habits == habits

    # 7. Assert that the sum of the 5th column (the completion column) is indeed 91.
    cursor.execute("SELECT SUM(Completed) FROM Progression_table;")
    column_sum = cursor.fetchone()[0]
    assert column_sum == 91

    # Close the database.
    conn.close()


if __name__ == '__main__':
    pytest.main()
