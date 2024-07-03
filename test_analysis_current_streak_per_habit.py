"""In this test module, the current streak in the sample data are compared to the longest streaks calculated by
the analysis_current_streak_per_habit module using the same sample data. The streaks have been calculated
outside of this application. This 'outside' calculation has been performed in three different ways to make sure that
the norm is correct and reliable: using Excel, ChatGPT 4o and manually. These methods resulted in the same outcomes:
    - lightsaber training, daily, longest streak ever: 32
    - meditate, daily, longest streak ever: 24
    - practice force lightning, weekly, longest streak ever: 6
    - attend senate, weekly, longest streak ever: 4
    - wash robes, weekly, longest streak ever: 3 (the sample data comes from not a particularly hygienic Sith Lord)

A characteristic of the first test function is that it calculates the 'current' streak as of the most recent date in the
Progression_table which is 5th of June 2024. The test does not call for an update of the Progression_table using the
Date_table because this would result in additional rows in the Progression_table for all dates between now and the
5th of June 2024. Since there will be no completions of habits in this time-period, the current streak should, by
default, all be '0'.

The second test function performs the same test but makes sure that after the insertion of the sample_data, the
Progression_table is updated with dates after the 5th of June 2024. Next, it asserts whether all 'current' streaks are
indeed equal to '0'.
"""
import pytest
import sqlite3

import analysis_current_streak_per_habit
import insert_sample_data_module
import progression_module


def test_calculate_daily_and_weekly_streaks(capsys):
    """This function sets up a test db and inserts it with sample data. Then, it calls the tested function and provides
    it with the tables with this sample data. Next, it asserts whether the output of this function is equal to the
    streaks calculated outside of this application.
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

    # Then, through the Insert_sample_data module, tables are generated and sample data is inserted into the tables.
    insert_sample_data_module.insert_sample_habit_data_and_dates('test_Habit_app_database.db',
                                                            'Habit_table',
                                                            'Date_table',
                                                            'Progression_table')
    insert_sample_data_module.insert_sample_progression_data('test_Habit_app_database.db',
                                                        'Habit_table',
                                                        'Date_table',
                                                        'Progression_table')

    # The operations above resulted in a test_db with a Habit_table and a Progression_table (also a Date_table
    # but this one is not relevant for this test). These two tables are needed as input for the
    # calculate_daily_and_weekly_streaks function.
    analysis_current_streak_per_habit.calculate_and_print_streaks('test_Habit_app_database.db',
                                                                    'Habit_table',
                                                                    'Progression_table')

    stored_print = capsys.readouterr()

    # The following assertions assert whether both the prints are correct and complete, and whether the calculated
    # streaks are equal to the norm as described in the docstrings of this module.
    assert "Habit: lightsaber training, current daily streak: 32" in stored_print.out
    assert "Habit: meditate, current daily streak: 0" in stored_print.out
    assert "Habit: practice force lightning, current weekly streak: 6" in stored_print.out
    assert "Habit: attend senate, current weekly streak: 4" in stored_print.out
    assert "Habit: wash robes, current weekly streak: 0" in stored_print.out


def test_calculate_daily_and_weekly_streaks_after_table_update(capsys):
    """This function sets up a test db and inserts it with sample data. Then, it calls the tested function and provides
    it with the tables with this sample data. Next, it updates the Progression_table so that it will contain dates up
    'today'. Next, the test function asserts whether the streaks calculated by the function are, indeed, 0 for each
    habit.
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

    # Then, through the Insert_sample_data module, tables are generated and sample data is inserted into the tables.
    insert_sample_data_module.insert_sample_habit_data_and_dates('test_Habit_app_database.db',
                                                            'Habit_table',
                                                            'Date_table',
                                                            'Progression_table')
    insert_sample_data_module.insert_sample_progression_data('test_Habit_app_database.db',
                                                        'Habit_table',
                                                        'Date_table',
                                                        'Progression_table')

    # Next, the Progression_table is updated to include all dates 'up to today'. This should create 5 lines (1 for each
    # habit) per date up to the current date.
    progression_module.Progression.combine_habits_dates('test_Habit_app_database.db',
                                                         'Habit_table',
                                                         'Date_table',
                                                         'Progression_table')

    # The operations above resulted in a test_db with a Habit_table, Date_table and a Progression_table.
    # In contrast to the previous test, the Progression_table contains also dates after 5th June 2024: from the
    # 6th of June up to today.

    # Next, the function to be tested is called.
    analysis_current_streak_per_habit.calculate_and_print_streaks('test_Habit_app_database.db',
                                                                    'Habit_table',
                                                                    'Progression_table')

    stored_print = capsys.readouterr()

    # The following assertions assert whether both the prints are correct and complete, and whether the calculated
    # streaks are equal to the norm as described in the docstrings of this module.
    assert "Habit: lightsaber training, current daily streak: 0" in stored_print.out
    assert "Habit: meditate, current daily streak: 0" in stored_print.out
    assert "Habit: practice force lightning, current weekly streak: 0" in stored_print.out
    assert "Habit: attend senate, current weekly streak: 0" in stored_print.out
    assert "Habit: wash robes, current weekly streak: 0" in stored_print.out


if __name__ == '__main__':
    pytest.main()
