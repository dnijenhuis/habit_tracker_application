"""In this test module, the main menu is tested. It is emphasized that only the functionality of the menu is tested.
The functionality of the called modules is not tested in this test module, but in their own respective test modules.

This test module first asserts whether the functions from the other modules are correctly called. Then, by iterating
through the main menu with mocked input, it asserts whether all (expected) menu messages have been printed, indicating
that the main menu functions correctly. Finally, some invalid inputs are tested to assert if the (expected) error
messages are printed.
"""

import pytest
from unittest.mock import patch
from unittest import mock
import sqlite3
import datetime
import main_habit_tracker_app

# The following lines of code were added at the very last of this project. This test_module kept giving
# warnings when the tests were executed through Windows Powershell. These warnings were due to 'depreciation' of
# the datetime adapter/converter. Basically, the lines make sure that conversion from ISO-format to datetime and back
# in relation to SQL databases is executed correctly. This also meant that I had to modify all the database connection
# lines. See, for example, the first function in database_and_table_creation_module.
sqlite3.register_adapter(datetime.datetime, lambda ts: ts.isoformat())
sqlite3.register_converter('timestamp', lambda s: datetime.datetime.fromisoformat(s.decode('utf-8')))


@patch('builtins.input', side_effect=['1', 'q'])  # Provide main menu with input.
@patch('habit_module.Habit.add_habit')  # This mocks the add_habit function. It does not actually get called.
def test_calling_add_habit(mock_add_habit, mock_input, capsys):
    """This function asserts whether the expected functions are called when mocking certain input. """
    with pytest.raises(SystemExit):  # The quit option in the main menu caused the test to error, this adjusts it.
        main_habit_tracker_app.main_menu()  # Starting the main menu.

    mock_add_habit.assert_called()

    # The following variable is only used to store the output so that the test report is not filled with it.
    stored_print = capsys.readouterr()


# In the following test_functions, basically the same procedure as above is performed multiple times.

@patch('builtins.input', side_effect=['2', 'q'])
@patch('habit_module.Habit.delete_habit')
def test_calling_delete_habit(mock_delete_habit, mock_input, capsys):
    """This function asserts whether the expected functions are called when mocking certain input. """
    with pytest.raises(SystemExit):
        main_habit_tracker_app.main_menu()

    mock_delete_habit.assert_called()
    stored_print = capsys.readouterr()


@patch('builtins.input', side_effect=['3', '1', 'm', 'q'])
@patch('habit_module.Habit.provide_habit_list')
def test_calling_habit_list(mock_provide_habit_list, mock_input, capsys):
    """This function asserts whether the expected functions are called when mocking certain input. """
    with pytest.raises(SystemExit):
        main_habit_tracker_app.main_menu()

    mock_provide_habit_list.assert_called()
    stored_print = capsys.readouterr()


@patch('builtins.input', side_effect=['3', '2', 'm', 'q'])
@patch('habit_module.Habit.provide_habit_list_per_periodicity')
def test_calling_habit_list_per_periodicity(mock_provide_habit_list_per_periodicity, mock_input, capsys):
    """This function asserts whether the expected functions are called when mocking certain input. """
    with pytest.raises(SystemExit):
        main_habit_tracker_app.main_menu()

    mock_provide_habit_list_per_periodicity.assert_called()
    stored_print = capsys.readouterr()


@patch('builtins.input', side_effect=['3', '3', 'm', 'q'])
@patch('analysis_current_streak_per_habit.calculate_and_print_streaks')
def test_calling_calculate_and_print_streaks(mock_calculate_and_print_streaks, mock_input, capsys):
    """This function asserts whether the expected functions are called when mocking certain input. """
    with pytest.raises(SystemExit):
        main_habit_tracker_app.main_menu()

    mock_calculate_and_print_streaks.assert_called()
    stored_print = capsys.readouterr()


@patch('builtins.input', side_effect=['3', '4', 'm', 'q'])
@patch('analysis_longest_streak_ever.calculate_and_print_longest_streaks_ever')
def test_calling_calculate_and_print_longest_streaks_ever(mock_calculate_and_print_longest_streaks_ever,
                                                          mock_input, capsys):
    """This function asserts whether the expected functions are called when mocking certain input. """
    with pytest.raises(SystemExit):
        main_habit_tracker_app.main_menu()

    mock_calculate_and_print_longest_streaks_ever.assert_called()
    stored_print = capsys.readouterr()


@patch('builtins.input', side_effect=['4', 'q'])
@patch('update_progression_module.update_function')
def test_calling_update_function(mock_update_function, mock_input, capsys):
    """This function asserts whether the expected functions are called when mocking certain input. """
    with pytest.raises(SystemExit):
        main_habit_tracker_app.main_menu()

    mock_update_function.assert_called()
    stored_print = capsys.readouterr()


@patch('builtins.input', side_effect=['reset', 'reset', 'q'])
# Both of the following patches are necessary to prevent actual database manipulation through the input above.
@patch('empty_database_module.delete_tables_themselves')
@patch('insert_sample_data_module.insert_sample_data_before_distribution_of_app')
def test_reset(mock_insert_sample_data_before_distribution_of_app, mock_delete_tables_themselves, mock_input, capsys):
    """This function asserts whether the expected functions are called when mocking certain input. """
    with pytest.raises(SystemExit):
        main_habit_tracker_app.main_menu()

    mock_delete_tables_themselves.assert_called()
    mock_insert_sample_data_before_distribution_of_app.assert_called()
    stored_print = capsys.readouterr()


def test_menu_input(capsys):
    """The following code iterates through the whole main menu and then checks if the menu flow
    functions correctly by asserting if all expected (menu)messages have been printed.
    """
    with mock.patch('builtins.input', side_effect=['1', 'c', '2', 'c', '3', '1', '3', '2', '0',
                                                   '3', '2', '1', '3', '3', '3', '4', '3', 'm', '4', 'm',
                                                   'reset', 'c', 'q']):
        try:
            main_habit_tracker_app.main_menu()
        except SystemExit:
            pass
    stored_print = capsys.readouterr()
    assert "This is the main menu of the Habit Tracker app." in stored_print.out
    assert "Cancelled." in stored_print.out
    assert "This is the analytics module. What do you want to do? " in stored_print.out
    assert "These are all your habits including their daily/weekly streaks. " in stored_print.out
    assert "These are all your habits including their longest daily/weekly streak ever. " in stored_print.out
    assert "Habit Progression:" in stored_print.out
    assert "This will delete all your data and progress." in stored_print.out
    assert "Application shut down." in stored_print.out


def test_menu_invalid_input(capsys):
    """The following code iterates through the whole main menu using invalid input, and then checks if the
    menu handles these correctly by asserting if the error messages have been displayed. Note that the error
    messages regarding invalid input in the called modules are tested in the tests for these respective modules.
    """
    with mock.patch('builtins.input', side_effect=['invalid', '3', 'invalid', 'reset', 'invalid', 'q']):
        try:
            main_habit_tracker_app.main_menu()
        except SystemExit:
            pass
    stored_print = capsys.readouterr()
    assert "This is the main menu of the Habit Tracker app." in stored_print.out
    assert "Invalid input, please type '1', '2', '3', '4' or 'q'. " in stored_print.out
    assert "Invalid input, please type '1', '2', '3', '4' or 'm'." in stored_print.out
    assert "Invalid input, reset aborted." in stored_print.out


if __name__ == '__main__':
    pytest.main()
