"""This module contains the functionality to calculate the length of the current daily and weekly streaks per habit.
It is called from the analytics module in the main menu of the app and prints the calculated streaks.
"""

import sqlite3
from datetime import datetime, timedelta


def calculate_daily_and_weekly_streaks(database, habit_table_name, progression_table_name):
    """This function calculates the streak for each habit. It is called by the calculate_and_print_streaks function in
     this module which, in turn, is called by the main menu. The function makes in its calculations a distinction
     between daily and weekly streaks by calling upon two other functions: count_daily_streak and count_weekly_streak.
     """
    # Connect to the database.
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Next, a dictionary is created in which the habits with corresponding streaks are stored.
    stored_streaks = {}

    # Query the Habit_table for every habit name and periodicity.
    cursor.execute(f"SELECT habit_name, habit_periodicity FROM {habit_table_name}")
    habits = cursor.fetchall()

    # Store today's date into the variable 'today'.
    today = datetime.today()

    # Using a for loop, for every habit, a query is performed where the dates and 'completed' status are retrieved and
    # up to 'today'. This data is then stored into the dates_and_completions variable. If the habit in that loop
    # iteration is a daily habit, it is fed into the count_daily_streak function. If it is a weekly habit, it is fed
    # into the count_weekly_streak function. These last two functions basically count the streak for the weekly and
    # daily habits.
    for habit, periodicity in habits:
        # the '<' symbol on the next line makes sure that 'today' is included in the query and streak calculation.
        cursor.execute(
            f"""SELECT date, completed FROM {progression_table_name} 
            WHERE habit_name = ? AND date <= ? ORDER BY date DESC""",
            (habit, today))

        # The dates_and_completions variable contains for every habit, pairs of 'date' and 'completed', ordered from
        # most recent to oldest.
        dates_and_completions = cursor.fetchall()

        if periodicity == 'daily':
            count = count_daily_streak(dates_and_completions)
        elif periodicity == 'weekly':
            count = count_weekly_streak(dates_and_completions, today)

        # Here the count with its habit gets stored in the dictionary stored_streaks defined above.
        stored_streaks[habit] = (periodicity, count)

    # Close the database.
    conn.close()

    # Then the stored streak data is returned from this function, back into the initially calculate_and_print_streaks
    # function that initially called this calculate_daily_and_weekly_streaks function.
    return stored_streaks


def count_daily_streak(daily_streak):
    """This function is called by the calculate_daily_and_weekly_streaks. From this function it gets fed daily habit
    data consisting of dates and 'completed' data, sorted from most recent to oldest.
    - First, the streak count is set to '0'.
    - Next, for every 'completed' value that is equal to '1' (completed habit), the count is increased with 1.
    - This continues, until a row is encountered where the completed is not equal to '1', breaking
      the for loop / streak.
    - Then the count value (being the daily streak) is returned to the calculate_daily_and_weekly_streaks after
    which it is stored with the habit name in stored_streaks.
    """
    count = 0
    for date, completed in daily_streak:
        if completed == 1:
            count += 1
        else:
            break
    return count


def count_weekly_streak(completions, today):
    """This function calculates the weekly streak: the number of weeks in which at least one day the habit was
    completed, including the current week. The streak count is first set to '0', and the current_week is
    first set to None. completed_days_in_week contains an empty set.

    For every date and completed value in the received data:
    - First, the date value is converted to a usable format.
    - The, the start date of the week (week_start is on a Monday) is determined for each date to determine which week
      it is in.
    - If the week has changed:
        - If there were any completed days in the previous week, the count is increased.
        - The current_week is updated to the new week, and completed_days_in_week is reset.
    - If the habit was completed on a given date, the date is added to completed_days_in_week.

    At the end, the last week is checked, and if there were any completed days, the count is incremented.
    """
    count = 0
    current_week = None
    completed_days_in_week = set()

    today_week_start = today - timedelta(days=today.weekday())

    for date, completed in completions:
        date_temp = datetime.strptime(date, '%Y-%m-%d')
        week_start = date_temp - timedelta(days=date_temp.weekday())

        if week_start != current_week:
            if current_week is not None:
                if len(completed_days_in_week) >= 1:
                    count += 1
                else:
                    break  # Reset streak if no completions in the previous week
            current_week = week_start
            completed_days_in_week = set()

        if completed == 1:
            completed_days_in_week.add(date_temp)

    # Correcting for the last week. In the code above the last week was initially not taken into account even though
    # during this week one or more 'completed' values were present.
    if len(completed_days_in_week) >= 1:
        count += 1

    # Ensure the current week is properly counted
    if current_week == today_week_start and len(completed_days_in_week) == 0:
        count = 0

    return count


def calculate_and_print_streaks(database, habit_table_name, progression_table_name):
    """This function gets called from the main menu and initializes the streak calculations. Next, it prints them
    using a for loop."""
    input_from_streak_calculation = calculate_daily_and_weekly_streaks(database, habit_table_name,
                                                                       progression_table_name)
    print("")
    for habit, (periodicity, count) in input_from_streak_calculation.items():
        print(f"Habit: {habit}, current {periodicity} streak: {count}")
