# std_statistics.py
# Student Data Analysis (Statistics Window with Themed GUI + Menu Bar)

# Import tkinter for GUI
import tkinter as tk
from tkinter import messagebox

# Import pymysql for MySQL database connection
import pymysql

# Import matplotlib for charts
import matplotlib.pyplot as plt

# Import class to embed matplotlib charts inside Tkinter window
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Import Counter to count course frequencies
from collections import Counter



# Function to open Statistics Window
def statistics_window(root, dashboard_window):
    # Create a new top-level window (child of root)
    stat_win = tk.Toplevel(root)

    # Set title of the statistics window
    stat_win.title("Student Statistics")

    stat_win.state("zoomed")  # open statistics window full screen

    # Apply background color to match project theme
    stat_win.config(bg="#FFF4E6")  # Light beige background


    # BACK BUTTON
    back_btn = tk.Button(
        stat_win,
        text="Back to Dashboard",
        bg="#4B3832",      # Dark brown button background
        fg="white",        # White text
        activebackground="#854442",  # Active color (reddish brown)
        activeforeground="white",
        command=lambda: [stat_win.destroy(), dashboard_window.deiconify(), dashboard_window.state("zoomed")]  # Go back
    )
    back_btn.pack(pady=10)

    # CONNECT TO DATABASE
    try:
        # Establish connection with MySQL
        con = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="student_db"
        )
        cur = con.cursor()  # Create a cursor object to execute queries

        # SQL query: Count number of students per course
        cur.execute("SELECT course, COUNT(*) FROM students GROUP BY course")

        # Fetch all results from query
        data = cur.fetchall()

        # Close database connection
        con.close()

        # If no data found, show info message and exit function
        if not data:
            messagebox.showinfo("No Data", "No student records found!")
            return

        # Extract course names and counts into lists
        courses = [row[0] for row in data]
        counts = [row[1] for row in data]

        # Convert course data to Counter (for bar chart)
        course_counts = Counter(courses)

    except Exception as e:
        # If error occurs, show messagebox and exit
        messagebox.showerror("DB Error", str(e))
        return


    # FUNCTION TO SHOW PIE CHART
    def show_pie_chart():
        # Clear previous widgets (if any)
        for widget in stat_win.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()

        # Create figure
        fig, ax = plt.subplots(figsize=(6, 5))

        # Draw pie chart with percentages
        ax.pie(
            counts,
            labels=courses,
            autopct='%1.1f%%',
            startangle=140
        )
        ax.set_title("Distribution by Course")

        # Embed chart in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=stat_win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # FUNCTION TO SHOW BAR CHART
    def show_bar_chart():
        # Clear previous widgets (if any)
        for widget in stat_win.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()

        # Create figure
        fig, ax = plt.subplots(figsize=(6, 5))

        # Draw bar chart
        ax.bar(
            course_counts.keys(),
            course_counts.values(),
            color='skyblue'
        )
        ax.set_xlabel("Course")
        ax.set_ylabel("No. of Students")
        ax.set_title("Students per Course")

        # Embed chart in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=stat_win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # MENU BAR CREATION
    menu_bar = tk.Menu(stat_win)  # Create menu bar
    stat_win.config(menu=menu_bar)  # Attach menu to window

    # Create "View" menu
    view_menu = tk.Menu(menu_bar, tearoff=0, bg="#FFF4E6", fg="#4B3832")
    menu_bar.add_cascade(label="View", menu=view_menu)

    # Add Pie Chart and Bar Chart options under View
    view_menu.add_command(label="Pie Chart", command=show_pie_chart)
    view_menu.add_command(label="Bar Chart", command=show_bar_chart)

    # Show a welcome message in start
    messagebox.showinfo("Statistics", "Choose a chart from 'View' menu to display.")


