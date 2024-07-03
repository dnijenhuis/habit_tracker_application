# Habit Tracker App

## Table of Contents
- [Installation Manual](#installation-manual)
  - [Downloading and Extracting the Application](#downloading-and-extracting-the-application)
  - [Installing Python](#installing-python)
  - [Checking and Downloading Dependencies](#checking-and-downloading-dependencies)
- [Starting the Application](#starting-the-application)
- [Using the Application](#using-the-application)
- [Testing the Application](#testing-the-application)

## Installation Manual

### Downloading and Extracting the Application
1. Download files from GitHub as a .ZIP file.
2. Extract the files to a folder of choice. Make sure the directory does not require administrator privileges to avoid database access errors when running the application or performing tests.

### Installing Python
1. Install Python (e.g., version 3.12) and ensure the 'Pip' box is checked under installation options.
2. Download Python from [python.org](https://www.python.org/downloads/).

### Checking and Downloading Dependencies
1. Open the Command Prompt. On a Windows machine, type `cd` or `cmd` into the search bar.
2. Verify Python installation:
    ```sh
    python --version
    ```
3. Verify Pip installation:
    ```sh
    pip --version
    ```
   If Pip is not installed, reinstall Python and be sure to install Pip.
4. Install the necessary packages:
    ```sh
    pip install pandas
    pip install pytest
    pip install hypothesis
    ```
   Note: `hypothesis` should be installed by default.

The application is now installed and ready for use!

## Starting the Application
1. Open the Command Prompt (`cmd`).
2. Navigate to the directory where you installed the application:
    ```sh
    cd path\to\application\directory
    ```
3. Start the application:
    ```sh
    python main_habit_tracker_app.py
    ```

## Using the Application
- The application operates through a Command Line Interface (CLI). A future update may include a Graphical User Interface (GUI) for a more interactive experience.
- Upon starting the application, you will see the main menu. Navigate the menu by typing the indicated input and pressing Enter.

### Main Menu Options:
1. **Add a New Habit**: Provide a habit name, description, and periodicity (daily or weekly). The creation date and time are stored automatically.
2. **Delete Habits**: Permanently delete a habit and its progression data. This action cannot be undone.
3. **Analytics Sub Menu**: Display various analytics:
    - List of all current habits.
    - List of habits by periodicity.
    - Current streaks for all habits.
    - Longest streak ever per habit.
4. **Update Habit Progress**: Register completion of habits per day. Enter `1` for completed and `0` for not completed. Changes can be made anytime, but future dates and dates before May 1st, 2024, cannot be updated.
5. **Reset Sample Data**: Delete all habits and progress, and reset to sample data.
6. **Quit Application**: Exit the application.

## Testing the Application
1. Ensure the `pytest` module is installed (see the 'Checking and Downloading Dependencies' section).
2. Navigate to the application directory:
    ```sh
    cd path\to\application\directory
    ```
3. Run tests:
    ```sh
    pytest
    ```
4. For detailed test insights, use an IDE such as PyCharm.
