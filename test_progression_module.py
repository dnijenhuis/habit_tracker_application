"""In this test module, first a test_db with all three tables is generated and inserted with sample data. Also is
generated a test_db2 database with only the Habit_table and Date_table, also both inserted with sample date.

Next, the to be tested combine_habits_dates function is called. The parameters are test_db2 and its two tables
(Habit_table and Date_table). This function then combines these tables into the third table: the Progression_table.

Next, the actual assertion tests whether the Progression_table in test_db (with hard-inserted sample data) and the
Progression_table in test_db2 (with data generated through the tested function) are, in fact, equal.
"""
import pytest
import sqlite3

import progression_module
import insert_sample_data_module


def test_combine_habits_dates():
    # First empty the two test_db's, recreate it and insert the sample data in the test tables. After these operations,
    # there is a test_Habit_app_database containing three tables with sample data. This data is 'hard' inserted in
    # the db.
    dbconnection = sqlite3.connect('test_Habit_app_database.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = dbconnection.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    for table_name in tables:
        c.execute(f"DROP TABLE IF EXISTS {table_name[0]}")
    dbconnection.commit()
    dbconnection.close()

    dbconnection = sqlite3.connect('test_Habit_app_database2.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = dbconnection.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    for table_name in tables:
        c.execute(f"DROP TABLE IF EXISTS {table_name[0]}")
    dbconnection.commit()
    dbconnection.close()

    insert_sample_data_module.insert_sample_habit_data_and_dates('test_Habit_app_database.db', 'Habit_table',
                                                            'Date_table', 'Progression_table')
    insert_sample_data_module.insert_sample_progression_data('test_Habit_app_database.db', 'Habit_table',
                                                        'Date_table', 'Progression_table')

    # Next, the sample habit_data is inserted into the Habit_table of test_Habit_app_database2 (test db2!) and the
    # Date_table is updated.

    insert_sample_data_module.insert_sample_habit_data_and_dates('test_Habit_app_database2.db', 'Habit_table',
                                                            'Date_table', 'Progression_table')
    #
    # Summarizing, there is now a test_db with all three tables filled with sample data. There is also a test_db2 with
    # only the Habit_table and Date_table filled with data.
    #
    # The next step is to call the combine_habits_dates function from the module E_Progression_class module that is
    # to be tested and provide it with the test_db2 tables (Habit_table and Date_table) which it should combine into
    # a Progression_table. This test_db2's Progression_table with hard inserted sample data, should be equal to the
    # generated test_db's Progression_table.

    progression_module.Progression.combine_habits_dates('test_Habit_app_database2.db',
                                                         'Habit_table',
                                                         'Date_table',
                                                         'Progression_table')

    # Next, the actual assertion starts to make sure the tables are, in fact, equal. Through a for loop, the first 4
    # columns and the first 180 rows of every table are fetched from both databases. The reasons for these constraints
    # are due to limits in using sampling data.
    #
    # More specifically, the constraints are:
    # - Only the first 4 columns of the progression table are tested. The sample data in the 'Completed' column of
    #   the hard-inserted data, are not taken into account. When the combine_habits_dates function is called for
    #   test_db2, the function 'thinks' (rightfully so) that there is new habit_data. So there are no completions yet.
    #   However, the hard inserted data in test_db1 has (for other testing purposes) hard data on the 'Completed'
    #   column.
    # - The first 180 rows limit is due to the fact that the hard-inserted sample progression data in test_db1 has
    #   36 days * 5 rows = 180 rows of data, whereas the called and tested function works with and needs an
    #   up-to-date Date_table.

    # The Habit_table and Date_table do not need to be asserted for equality since they are generated in the
    # same manner: through assertion. Additionally, asserting these tables for equality can lead to test failures in
    # the future when the used date_table gets more than 180 rows (days since May 1st, 2024).

    conn1 = sqlite3.connect('test_Habit_app_database.db')
    cursor1 = conn1.cursor()
    cursor1.execute(f"SELECT * FROM Progression_table LIMIT 180")  # Only the first 180 rows.
    data1 = cursor1.fetchall()
    conn1.close()

    conn2 = sqlite3.connect('test_Habit_app_database2.db')
    cursor2 = conn2.cursor()
    cursor2.execute(f"SELECT * FROM Progression_table LIMIT 180")  # Only the first 180 rows.
    data2 = cursor2.fetchall()
    conn2.close()

    # Extract only the first 4 columns for comparison.
    data1_sorted = sorted([row[:4] for row in data1])
    data2_sorted = sorted([row[:4] for row in data2])

    assert data1_sorted == data2_sorted


if __name__ == '__main__':
    pytest.main()
