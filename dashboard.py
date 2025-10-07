# dashboard.py

# Import tkinter for GUI creation
import tkinter as tk

# Import student_records module to show student list window
import student_records

# Import statistics module to show statistics window
import statistics

# Global variable to keep track of current dashboard window
current_dashboard = None

# Function to create and open Dashboard Window
def dashboard_window(root):
    global current_dashboard
    # Create a new top-level window (separate from login/root)
    dashboard = tk.Toplevel(root)
    current_dashboard = dashboard  # store it for later
    # Set the title of the dashboard window
    dashboard.title("Dashboard")

    # Set fixed window size (width=400, height=400)
    dashboard.state("zoomed")  # make dashboard full screen

    # BUTTON 1: Show Students
    # Create a button to open the "Show Students" window
    btn_students = tk.Button(
        dashboard,
        text="Show Students",                 # Button label
        command= lambda:[dashboard.withdraw(), student_records.show_students()] # Calls the show_students function
    )
    # Place the button in the dashboard with some vertical padding
    btn_students.pack(pady=20)

    # BUTTON 2: Show Statistics
    # Create a button to open the "Show Statistics" window
    btn_stats = tk.Button(
        dashboard,
        text="Show Statistics",                          # Button label
        command=lambda:[current_dashboard.withdraw(), statistics.statistics_window(root,current_dashboard)]  # Calls statistics_window function
    )
    # Place the button in the dashboard with some vertical padding
    btn_stats.pack(pady=20)
