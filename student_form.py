# student_form.py

# Importing all tkinter classes and functions
from tkinter import *
# Importing messagebox for showing alerts
from tkinter import messagebox
# Importing PIL for handling images (used if you add right-side images)
from PIL import Image, ImageTk
# Importing pymysql for database connection
import pymysql

# Importing root window from db_login file
from db_login import root


# STUDENT FORM WINDOW
def open_student_form():
    """ Function to open the Student Form window """

    # Hide root window when this window is open
    root.withdraw()

    # Create a new top-level window for student form
    student_win = Toplevel(root)
    student_win.title("Add Student")  # Window title
    student_win.state("zoomed")       # open student form in full screen
    student_win.config(bg="#EDEADE")  # Background color

    # BACK BUTTON
    # Button to go back to login window
    Button(student_win, text="Back to Login", font=("Arial", 10, "bold"),
           bg="#4B3832", fg="white",
           command=lambda: [student_win.destroy(), __back_to_login()]
           ).pack(pady=5)

    # MAIN FRAME
    main_frame = Frame(student_win, bg="#EDEADE")
    main_frame.pack(fill="both", expand=True)

    # Left Frame (Form section)
    left_frame = Frame(main_frame, bg="#EDEADE", width=350, height=500)
    left_frame.pack(side="left", fill="y")
    left_frame.pack_propagate(False)  # Prevent auto resizing

    # LEFT FORM CONTENT
    # Heading Label
    Label(left_frame, text="Add Student", font=("Arial", 16, "bold"),
          bg="#EDEADE", fg="#4B3832").pack(pady=(40, 10))

    # Name input
    Label(left_frame, text="Name", bg="#EDEADE", fg="#4B3832",
          font=("Arial", 12, "bold")).pack(pady=5)
    name_entry = Entry(left_frame, font=("Arial", 12), bd=2, relief="solid")
    name_entry.pack(pady=5, ipadx=5, ipady=3)

    # Age input
    Label(left_frame, text="Age", bg="#EDEADE", fg="#4B3832",
          font=("Arial", 12, "bold")).pack(pady=5)
    age_entry = Entry(left_frame, font=("Arial", 12), bd=2, relief="solid")
    age_entry.pack(pady=5, ipadx=5, ipady=3)

    # Course input
    Label(left_frame, text="Course", bg="#EDEADE", fg="#4B3832",
          font=("Arial", 12, "bold")).pack(pady=5)
    course_entry = Entry(left_frame, font=("Arial", 12), bd=2, relief="solid")
    course_entry.pack(pady=5, ipadx=5, ipady=3)

    # Email input
    Label(left_frame, text="Email", bg="#EDEADE", fg="#4B3832",
          font=("Arial", 12, "bold")).pack(pady=5)
    email_entry = Entry(left_frame, font=("Arial", 12), bd=2, relief="solid")
    email_entry.pack(pady=5, ipadx=5, ipady=3)

    # Phone input
    Label(left_frame, text="Phone", bg="#EDEADE", fg="#4B3832",
          font=("Arial", 12, "bold")).pack(pady=5)
    phone_entry = Entry(left_frame, font=("Arial", 12), bd=2, relief="solid")
    phone_entry.pack(pady=5, ipadx=5, ipady=3)

    # ADD STUDENT FUNCTION
    def add_student():
        """ Function to insert student details into database """
        name = name_entry.get()
        age = age_entry.get()
        course = course_entry.get()
        email = email_entry.get()
        phone = phone_entry.get()

        # Validation check (all fields required)
        if name == "" or age == "" or course == "" or email == "" or phone == "":
            messagebox.showerror("Error", "All fields are required!", parent=student_win)
            return

        # Insert into database
        con = pymysql.connect(host="localhost", user="root", password="", database="student_db")
        cur = con.cursor()
        cur.execute("INSERT INTO students(name, age, course, email, phone) VALUES(%s, %s, %s, %s, %s)",
                    (name, age, course, email, phone))
        con.commit()
        con.close()

        # Success message
        messagebox.showinfo("Success", "Student Added Successfully!", parent=student_win)

    # Button to call add_student function
    Button(left_frame, text="Add Student", command=add_student, font=("Arial", 12, "bold"),
           bg="#4B3832", fg="white", width=15).pack(pady=20)

    # Button to show student list
    Button(left_frame, text="Show Students", command=lambda: [student_win.destroy(), __open_show_students()], font=("Arial", 12, "bold"),
           bg="#4B3832", fg="white", width=15).pack(pady=5)

    # HELPER FUNCTIONS

    # Function to open student records (import inside to avoid circular import problem)
    def __open_show_students():
        from student_records import show_students
        show_students()

    # Function to return back to login page (import inside to avoid circular import problem)
    def __back_to_login():
        from ui_form import open_login
        open_login()
