"""This is the Date_class module. It only contains the class 'Date_class'. It initializes the Date_class, and
it defines one function: update_dates. This function makes sure that the table Data_table in the database
always contains a complete and up-to-date list of all the dates up to and including 'the current date'. The function is
executed as soon as the application is started to make sure that all functions (such as updating progress) have a
complete and up-to-date list of dates to work with. It is also executed in several other modules, every time to make
sure that database operations are performed using an up-to-date table.
"""

import sqlite3
from datetime import date, timedelta

import database_and_table_creation_module


class Date:
    """The class 'Date' starts by defining the class, it only takes 'self' as an attribute. Next, it defines the
    function update_dates which updates the Date_table to include all dates up to and including 'the current date'.
    This table is then used by the 'Progression_class' module.
    """

    def __init__(self):
        self.dates = []

    def update_dates(database, date_table_name):
        """The function first connects to the Date_table in the database where it selects all rows (dates) in
        descending order. Then it fetches the first row, which is the most recent date in the table. This value (date)
        is stored in the variable last_date_in_table.

        Next, the variable most_recent_date is defined by adding 1 day to the variable last_date_in_table. So this
        is just the most recent date in the table + 1 day. Also, the date is transformed to ISO format (YYYY-MM-DD)
        because this makes later database querying easier and more reliable in my opinion.

        Then, the current_date variable is defined by the 'current' date.

        Finally, using a while loop, the function inserts new values (dates) into the Date_table, and it stops after
        the most recent date in the table is the current date. Then the insertions are committed and the database is
        closed.
        """
        # Make sure there is a date_table.
        database_and_table_creation_module.create_date_table(date_table_name, database)

        # Setting up the database connection.
        dbconnection = sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES)
        c = dbconnection.cursor()

        # Querying the Date_table for the most recent date in it and storing this 1 row in variable last_date_in_table.
        c.execute(f"SELECT Date FROM {date_table_name} ORDER BY Date DESC LIMIT 1")
        last_date_in_table = c.fetchone()

        most_recent_date = date.fromisoformat(last_date_in_table[0]) + timedelta(days=1)

        current_date = date.today()

        # Through the while loop new rows (dates) are added to the Date_table until all dates up to 'the current date'
        # are in the table.
        while most_recent_date <= current_date:
            c.execute(f"INSERT INTO {date_table_name} (Date) VALUES (?)", (most_recent_date.isoformat(),))
            most_recent_date += timedelta(days=1)

        # Closing the database.
        dbconnection.commit()
        dbconnection.close()
