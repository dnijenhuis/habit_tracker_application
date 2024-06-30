"""This module provides the functions needed to display the habit progression data per day. It also lets the user
update this data: to a '1' (habit completed) or back to a '0' (not completed). This module is called from the main
menu of the application (and ofcourse from test modules).
"""

import sqlite3
from datetime import datetime, timedelta


def update_function(database):
    """This function lets the user display and interact with the data on habit progression/completion. It consists of
    various (sub) functions which display the current day's data to the user, and which allow the user to switch to
    previous and next days (including the data on these days). Furthermore, the (sub) functions allow the user to
    update their progression data regarding their habits. When a certain habit on a certain date has been set to '1'
    (completed) it can be set back to '0' (not completed) again if the users wishes to do so.
    """
    # Connecting to the database.
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Here I store 'the current date' into the variable current_date because it is used in multiple sub functions.
    current_date = datetime.today()

    def display_day_data():
        """This function is the first sub function that is called after calling the update_function from the main
        menu. It first prints the weekday and date. Then, it prints the columns using friendly user column names.
        Next, it queries the Progression_table for all the data on the habits on that specific date, and displays them.
        """
        # Store the day to be displayed into the variable display_date. This is done with a weekday and date format.
        # Then the user-friendly column names are printed.
        display_date = str(current_date.strftime('%A, %d %B %Y'))
        print("")
        print("Date: " + display_date)
        print("Habit Progression:")
        print(f"{'Date':<12} {'Habit Name':<31} {'Completed':<10}")
        print("-" * 53)

        # The Progression_table is queried for the date, habits and 'completed' column regarding the displayed date.
        cursor.execute(
            """SELECT date, habit_name, completed FROM Progression_table WHERE date = ? ORDER BY habit_name""",
            (current_date.strftime('%Y-%m-%d'),))
        rows = cursor.fetchall()

        # Through a for loop, each loop assigns the datapoints from the respective rows (the row variable) to the
        # variables date, habit_name and 'completed'. Next, these variables are printed and the loop starts over.
        for row in rows:
            date, habit_name, completed = row
            print(f"{date:<12} {habit_name:<31} {completed:<10}")

    def go_back_to_previous_day():
        """This function can be called from the within the progression menu. It first refers to the variable
        current_date in the (higher) outer update_function. Then, it subtracts 1 day from this date. Next, it calls
        the display_day_data function (again) which, again, prints the columns and habit progression data for the
        previous day. Furthermore, the function prevents the user from going back farther into the past than the first
        of May 2024. This date has been set based on the (hard coded) starting date of the Date_table."""
        nonlocal current_date
        minimum_date = datetime(2024, 5, 2)

        if current_date > minimum_date:
            current_date -= timedelta(days=1)
            display_day_data()
        else:
            print("You cannot go back further than 01-05-2024.")

    def go_to_next_day():
        """This function can be called from the within the progression menu. It first refers to the variable
        current_date in the (higher) outer update_function. Then, it adds 1 day to this date. Next, it calls
        the display_day_data function (again) which, again, prints the columns and habit progression data for the
        previous day. Furthermore, the function prevents the user from displaying future days."""
        nonlocal current_date
        maximum_date = datetime.today() - timedelta(days=1)
        if current_date < maximum_date:

            current_date += timedelta(days=1)
            display_day_data()
        else:
            print("You cannot go further than today.")

    def update_habit_progression():
        """The functions: display_day_data, go_back_to_previous_day and go_to_next_day, query and display the habit
        data per day. This function, the update_habit_progression function, allows the users to update the habit data.

        It first queries all the habit names from the Progression_table. Then it prompts the user for which habit
        they want to update. Next, the user is prompted what the new status should be: 1 (completed) or 0 (not
        completed).
        This input is then used to perform an update task on the Progression_table: the row where the habit name is
        equal to the user input, and the date is equal to the current_date (the currently displayed date), the value
        in the 'completed' column gets set to a value equal to the user input.
        """

        # Query all the habit names from the Habit Table and store data into the habits variable.
        cursor.execute("""SELECT habit_name FROM Progression_table""")
        habits = [row[0] for row in cursor.fetchall()]

        # Prompt the user for the habit that they want to update and store this data into the variable habit_name.
        print("")
        habit_name = input(f"Type the name of the habit of which you wish to update your progression. ").strip().lower()

        # Next, check whether the habit name that the user provided exists. If not, an error message is printed.
        if habit_name not in habits:
            print("Invalid habit name.")
            return

        # If the user gave a valid habit name, the user is prompted again to ask how to update the habit on the
        # displayed day. The user can give a '1' for completed or a '0' for not completed. If the user inserts a
        # different value than 1 or 0, an error message is printed.
        print("")
        new_status = input("Enter new status (1 for completed, 0 for not completed): ")

        try:
            new_status = int(new_status)
            # If the user provides a valid input (1 or 0), the Progression_table is updated with the new_status (1 or 0)
            # at the displayed date (current_date) for the habit name the user provided (habit_name).
            cursor.execute("""UPDATE Progression_table SET completed = ? WHERE date = ? AND habit_name = ?""",
                           (new_status, current_date.strftime('%Y-%m-%d'), habit_name))
            print("")
            print("Habit progression updated successfully.")

            # Close database.
            conn.commit()

        except ValueError:
            print("")
            print("Invalid input. Please enter 1 or 0.")

        display_day_data()

    # This is the function which is executed when the higher function update_function is called from the main menu.
    display_day_data()

    # This while loop generates the 'progression' menu for the user. The loop prompts the user for input and then,
    # based on this input, it calls the functions for displaying the data on the previous day, the next day, to
    # update the progression, or the go back to the app's main menu.
    while True:
        print("")
        command = input("What do you want to do? Previous day (1), next day (2), update progression (3) or back to "
                        "main menu (m): ").strip().lower()
        if command == '1':
            go_back_to_previous_day()
        elif command == '2':
            go_to_next_day()
        elif command == '3':
            update_habit_progression()
        elif command == 'm':
            break
        else:
            print("Invalid input. Please enter '1', '2', '3', or 'm'.")

    # Close the database.
    conn.close()
