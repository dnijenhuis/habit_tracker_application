"""In this test module, the longest streaks ever in the sample data are compared to the longest streaks calculated by
the analysis_longest_streak_ever module using the same sample data. The longest streak ever has been calculated
outside of this application. This 'outside' calculation has been performed in three different ways to make sure that
the norm is correct: using Excel, ChatGPT 4o and manually. These methods resulted in the same outcomes:
    - lightsaber training, daily, streak: 32
    - meditate, daily, streak: 24
    - practice force lightning, weekly, streak: 6
    - attend senate, weekly, streak: 4
    - wash robes, weekly, streak: 3
"""
import pytest
import sqlite3

import analysis_longest_streak_ever
import insert_sample_data_module


def test_calculate_and_print_longest_streaks_ever(capsys):
    """This function first clears the test db and sets it up again with sample data. Then, it calculates the longest
    streaks ever using the function to be tested. Next, it asserts whether the longest streaks ever are equal to the
    longest streaks ever calculated outside of this application.
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
    # calculate_and_print_longest_streaks_ever function.
    analysis_longest_streak_ever.calculate_and_print_longest_streaks_ever('test_Habit_app_database.db',
                                                                            'Habit_table',
                                                                            'Progression_table')

    stored_print = capsys.readouterr()

    # The following assertions assert whether both the prints are correct and complete, and whether the calculated
    # streaks are equal to the norm as described in the docstrings of this module.
    assert "Habit: lightsaber training, longest daily streak ever: 32" in stored_print.out
    assert "Habit: meditate, longest daily streak ever: 24" in stored_print.out
    assert "Habit: practice force lightning, longest weekly streak ever: 6" in stored_print.out
    assert "Habit: attend senate, longest weekly streak ever: 4" in stored_print.out
    assert "Habit: wash robes, longest weekly streak ever: 3" in stored_print.out


if __name__ == '__main__':
    pytest.main()
