"""This module contains the functionality to calculate the length of the longest daily/weekly streak per habit that
the user ever achieved. The module is called from the analytics module in the main menu of the app and prints the
calculated longest streaks ever.
"""

import sqlite3
from datetime import datetime, timedelta


def calculate_longest_streaks(database, habit_table_name, progression_table_name):
    """This functionCalculates the longest sequential completions for each habit, distinguishing between daily and
    weekly habits. It provides the calculate_and_print_longest_streaks_ever function with a dictionary of habits and
     their longest streaks ever.
    """
    # Make a connection to the database.
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Next, a dictionary is created in which the habits with corresponding record-streaks are stored.
    longest_streaks = {}

    # Query the Habit_table for every habit name and periodicity.
    cursor.execute(f"SELECT habit_name, habit_periodicity FROM {habit_table_name}")
    habits = cursor.fetchall()

    # Using a for loop, for every habit, a query is performed where the dates and 'completed' status are retrieved and
    # up to 'today'. This data is then stored into the dates_and_completions variable. If the habit in that loop
    # iteration is a daily habit, it is fed into the calculate_longest_daily_streak function. If it is a weekly habit,
    # it is fed into the calculate_longest_weekly_streak function. These last two functions basically count the longest
    # streak ever for the weekly and daily habits.
    for habit, periodicity in habits:
        cursor.execute(f"""SELECT date, completed FROM {progression_table_name}
        WHERE habit_name = ? ORDER BY date""", (habit,))
        dates_and_completions = cursor.fetchall()

        if periodicity == 'daily':
            longest_count = calculate_longest_daily_streak(dates_and_completions)
        elif periodicity == 'weekly':
            longest_count = calculate_longest_weekly_streak(dates_and_completions)

        # Here the count with its habit gets stored in the dictionary longest_streaks defined above. Periodicity is
        # only included so that it can be printed later on.
        longest_streaks[habit] = (longest_count, periodicity)

    # Close database and return the longest_streaks values to the calculate_and_print_longest_streaks_ever function.
    conn.close()
    return longest_streaks


def calculate_longest_daily_streak(completions):
    """This function calculates the longest daily streak based on the dates and completion status per date.

    First, it initializes the longest_count variable and sets it to '0'. Also, the last_date variable is initialized
    and gets a None value (the loop has not yet started by now, so it should have no value).

    Then, through the for loop, for every (normalized) date and completed status, it is checked whether the habit was
    completed ('1') on that date, and next, if the previous day there also was a check-off. If so, then the
    current_count is increased by 1. The longest count (ever), is the highest (max) of the current count and the
    previous longest count. In the end, the longest_count value gets returned to the calculate_longest_streaks function.
    """
    longest_count = current_count = 0
    last_date = None

    for date, completed in completions:
        date = datetime.strptime(date, '%Y-%m-%d')

        if completed == 1:
            if last_date is None or date == last_date + timedelta(days=1):
                current_count += 1
            else:
                current_count = 1

            longest_count = max(longest_count, current_count)
        else:
            current_count = 0

        last_date = date

    return longest_count


def calculate_longest_weekly_streak(completions):
    """This function calculates the longest weekly streak based on the dates and completion status per date.

    First it initializes the longest_count variable and sets it to '0'. Also, the current_week variable is initialized
    and gets a None value (the loop has not yet started by now, so it should have no value). completed_days_in_week
    contains an empty set.

    For every date and completed value in the received data:
    - First, the date value is converted to a usable format.
    - The, the start date of the week (week_start is on a Monday) is determined for each date to determine which week
      it is in.
    - If the week has changed:
        - If there were any completed days in the previous week, the count is increased.
        - The current_week is updated to the new week, and completed_days_in_week is reset.
        - Then the longest_count is determined. This is the highest of the longest count (so far) and the current_count.
        - The values are added to the set completed_days_in_week.

    At the end, the last week is checked, and if there were any completed days, the count is incremented.

    """
    longest_count = current_count = 0
    current_week = None
    completed_days_in_week = set()

    for date, completed in completions:
        date = datetime.strptime(date, '%Y-%m-%d')
        week_start = date - timedelta(days=date.weekday())

        if week_start != current_week:
            if current_week is not None:
                if len(completed_days_in_week) >= 1:
                    current_count += 1
                else:
                    current_count = 0
                longest_count = max(longest_count, current_count)
            current_week = week_start
            completed_days_in_week = set()

        if completed == 1:
            completed_days_in_week.add(date)

    # Correction for the last week.
    if len(completed_days_in_week) >= 1:
        current_count += 1
        longest_count = max(longest_count, current_count)

    return longest_count


def calculate_and_print_longest_streaks_ever(database, habit_table_name, progression_table_name):
    """This function gets called from the main menu and initializes the calculations of the longest streak ever per
    habit. Next, it prints them using a for loop."""
    input_from_streak_calculation = calculate_longest_streaks(database, habit_table_name, progression_table_name)
    print("")
    for habit, (count, periodicity) in input_from_streak_calculation.items():
        print(f"Habit: {habit}, longest {periodicity} streak ever: {count}")
