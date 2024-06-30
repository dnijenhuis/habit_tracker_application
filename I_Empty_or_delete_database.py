"""During development this module was used to quickly and easily empty or completely delete tables. This was useful
for development and testing. During the end of the project I decided to create an option in the main menu of the app
to reset the database and insert (again) the sample data. The reason for this was for to make sure that during the
grading of this project the sample data could be manipulated in every way possible, and then retrieved (again) and
used if needed.
"""
import sqlite3


def delete_tables_themselves(database, habit_table_name, date_table_name, progression_table_name):
    """This function deletes the tables from the input database. It is called from the main menu and allows the
    user to delete the tables and then insert the sample data (again). It is also used by the test modules.
    """
    dbconnection = sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES)
    c = dbconnection.cursor()

    c.execute(f"DROP TABLE IF EXISTS {habit_table_name}")
    c.execute(f"DROP TABLE IF EXISTS {date_table_name}")
    c.execute(f"DROP TABLE IF EXISTS {progression_table_name}")

    dbconnection.commit()
    dbconnection.close()
