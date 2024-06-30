# Read Me file Habit Tracker App

### Installation manual

##### Downloading and extracting the application
- Download files from GitHub as a .ZIP file. 
- Extract the files to a folder of choice. Make sure that the directory does not require administrator privileges. This could cause database access errors when running the application and/or performing the tests. 

##### Installing Python
- Install Python (e.g. version 3.12) and make sure that you check the 'Pip' box under installation options.
- To download Python, you can search online for "python downloads" or use the following link: https://www.python.org/downloads/

##### Checking and downloading dependencies
- Open "Prompt". On a Windows machine you can do this by typing "prompt" into the search bar. 
- Enter "python --version" to make sure that you have Python correctly installed.
- Enter "pip --version" to make sure that you have Pip correctly installed. If not, reinstall Python and make sure to also install 'Pip'. 
- Enter the following commands to install the necessary packages:
    * "pip install pandas"
    * "pip install pytest"
    * "pip install hypothesis" (this should be installed by default though)
- The application is now installed and ready for use!

### Starting the application
- Open "Prompt". On a windows machine you can do this by typing "prompt" into the search bar. 
- Enter "cd" (or "cmd") followed by (a paste of) the directory path where you installed the application. 
- Enter "python A_Habit_tracker_app.py"
- Your application will now start.

### Using the application
- The application currently works based on a Command Line Interface (CLI). However, in the future, this can be updated to a Graphical User Interface (GUI) which provides a more interactive and visually intuitive way for the user to interact with the application.
- After starting the application, you see the main menu. Navigating the main menu and its functions is achieved by providing the application with typed input as indicated by the application, followed by pressing the enter button.
- From the main menu, you have several options:
    1. You can add a new habit. For this, you have to give a habit name, habit description and habit periodicity. Habits can be daily habits or weekly habits. Additionally, the creation date and time of this new habit is (automatically) stored. 
    2. You can delete habits as well. If you choose this option, be sure that you really want to delete the habit including all its progression data. After deletion, there is no way to restore the data. The sample habits can also be deleted through this option.
    3. By choosing the analytics sub menu, you get additional options for displaying analytics: 
        - A list of all current habits;
        - A list of all current habits per periodicity;
        - The current streaks for all habits;
        - The longest streak ever per habit.
    4. Also, from the main menu, you can choose to update your habit progress. By choosing this menu option, you first get an overview of habit completion per day. Here, you can register, per day and per habit, if you completed the habit. The number '1' stands for habit 'completed'. If you want to change this back to 'not completed', you can update the '1' to become a '0' again. All habits on all dates, can be changed at any point in time, and can be changed back and forth from '0' to '1' as often as needed. However, it is not possible to update future dates, or dates before May 1st, 2024. 
    5. Another option in the main menu, is to delete all data and reset the sample data. By choosing this options, all habits and habit progression are deleted and the app starts over with sample data.
    6. The application can be quit by choosing the last option in the main menu. 


### Testing the application
- Make sure you have installed the pytest module. See the section on 'Checking and downloading dependencies' of this README file to install this module.
- Enter "cd" (or "cmd") followed by (a paste of) the directory path where you installed the application. 
- Enter "pytest".
- To test the individual test modules and gain more insight into the tests, you can use an IDE such as PyCharm.

