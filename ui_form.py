# Importing all widgets and functions from tkinter library
from tkinter import *
# Importing messagebox for showing popup alerts and ttk for advanced widgets like Combobox, Treeview
from tkinter import messagebox, ttk
# Importing show_students function from student_records module
from student_records import show_students
# Importing pymysql for database connection
import pymysql
# Importing hashlib for password hashing (SHA-256)
import hashlib
# Importing root window object from db_login file
from db_login import root
# Importing custom statistics module as 'statistics'
import std_statistics as statistics
# Importing dashboard window (not used in this file directly)
from dashboard import dashboard_window
import student_records

# Global variable to keep track of currently open window
current_window = None


# LOGIN WINDOW
def open_login():
    """ Function to open login window """
    global current_window
    # If a window is already open, destroy it
    if current_window:
        current_window.destroy()
    # Show the main root window
    root.deiconify()
    root.title("Login Page")  # Set window title
    root.state("zoomed")      # make login full screen
    root.config(bg="#EDEADE") # Set background color
    current_window = root     # Store current window as root

    # Clear all old widgets if any exist
    for widget in root.winfo_children():
        widget.destroy()

    # Heading label
    Label(root, text="Login", font=("Arial", 16, "bold"), bg="#EDEADE", fg="#4B3832").pack(pady=10)

    # Declare global entries and role selection dropdown
    global e1, e2, role_combo_login

    # Username field
    Label(root, text="Username", bg="#EDEADE").pack(pady=(5,0))
    e1 = Entry(root, bd=2, relief="solid", font=("Arial",12))
    e1.pack(pady=5, fill=X, padx=50)

    # Password field
    Label(root, text="Password", bg="#EDEADE").pack(pady=(10,0))
    e2 = Entry(root, bd=2, relief="solid", show="*", font=("Arial",12))
    e2.pack(pady=5, fill=X, padx=50)

    # Role selection dropdown
    Label(root, text="Login As", bg="#EDEADE").pack(pady=(10,0))
    role_combo_login = ttk.Combobox(root, values=["student", "admin"], state="readonly", font=("Arial",12))
    role_combo_login.set("student")  # Default value set to student
    role_combo_login.pack(pady=5, fill=X, padx=50)

    # Login button
    Button(root, text="Login", command=login, bg="#4B3832", fg="white", width=15).pack(pady=15)

    # Signup link (clickable label)
    signup_label = Label(root, text="Don't have an account? Signup", fg="blue", bg="#EDEADE", cursor="hand2")
    signup_label.pack()
    signup_label.bind("<Button-1>", lambda e: open_signup())  # Open signup on click


# LOGIN FUNCTION
def login():
    """ Function to validate login """
    username = e1.get().strip()   # Get username
    password = e2.get().strip()   # Get password
    login_as = role_combo_login.get().strip()  # Get role type (student/admin)

    # Check empty fields
    if "" in (username, password, login_as):
        messagebox.showerror("Error", "All fields required!", parent=root)
        return

    # Encrypt password using SHA-256
    hashed_pwd = hashlib.sha256(password.encode()).hexdigest()

    try:
        # Connect to database
        con = pymysql.connect(host="localhost", user="root", password="", database="student_db")
        cur = con.cursor()
        # Verify credentials from users table
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, hashed_pwd))
        row = cur.fetchone()  # Fetch matching row
        con.close()
    except Exception as e:
        # Show error if database connection fails
        messagebox.showerror("DB Error", str(e), parent=root)
        return

    # If user exists
    if row:
        role = row[4]  # Get role column value
        root.withdraw()  # Hide login window
        # Check role and open respective dashboard
        if role == "admin":
            open_admin_dashboard(username)  # admin dashboard
        elif role == "student":
            open_student_details(username)  # student window
        else:
            messagebox.showerror("Error", f"User cannot login as {login_as}!", parent=root)
    else:
        messagebox.showerror("Error", "Invalid Username or Password!", parent=root)


# SIGNUP WINDOW
def open_signup():
    """ Function to open signup window """
    global current_window
    if current_window:
        current_window.withdraw()
    signup_win = Toplevel(root)  # Create new window
    current_window = signup_win
    signup_win.title("Signup Page")
    signup_win.state("zoomed") # for full screen
    signup_win.config(bg="#EDEADE")

    # Signup form heading
    Label(signup_win, text="Signup", font=("Arial", 16, "bold"), bg="#EDEADE", fg="#4B3832").pack(pady=10)

    # Username entry
    Label(signup_win, text="Username:", bg="#EDEADE", fg="#4B3832", font=("Arial", 10, "bold")).pack(pady=(5,0))
    user_entry = Entry(signup_win, bd=2, relief="solid", font=("Arial",12))
    user_entry.pack(pady=5, fill=X, padx=50)

    # Password entry
    Label(signup_win, text="Password:", bg="#EDEADE", fg="#4B3832", font=("Arial", 10, "bold")).pack(pady=(10,0))
    pass_entry = Entry(signup_win, bd=2, relief="solid", show="*", font=("Arial",12))
    pass_entry.pack(pady=5, fill=X, padx=50)

    # Email entry
    Label(signup_win, text="Email:", bg="#EDEADE", fg="#4B3832", font=("Arial", 10, "bold")).pack(pady=(10,0))
    email_entry = Entry(signup_win, bd=2, relief="solid", font=("Arial",12))
    email_entry.pack(pady=5, fill=X, padx=50)

    # Function for signup button
    def signup_action():
        user = user_entry.get().strip()
        pwd = pass_entry.get().strip()
        email = email_entry.get().strip()
        # Check empty fields
        if "" in (user, pwd, email):
            messagebox.showerror("Error", "All fields required!", parent=signup_win)
            return
        # Hash password
        hashed_pwd = hashlib.sha256(pwd.encode()).hexdigest()
        try:
            # Insert into users table with default role student
            con = pymysql.connect(host="localhost", user="root", password="", database="student_db")
            cur = con.cursor()
            cur.execute("INSERT INTO users(username,password,email,role) VALUES(%s,%s,%s,%s)",
                        (user, hashed_pwd, email, "student"))
            con.commit()
            con.close()
            messagebox.showinfo("Success", "Registered Successfully!", parent=signup_win)
            signup_win.destroy()  # Close signup window
            open_login()          # Return to login page
        except Exception as e:
            messagebox.showerror("DB Error", str(e), parent=signup_win)

    # Signup button
    Button(signup_win, text="Signup", command=signup_action, bg="#4B3832", fg="white", width=15).pack(pady=(20,5))
    # Back to login button
    Button(signup_win, text="Back to Login", command=lambda:[signup_win.destroy(), open_login()], bg="#4B3832", fg="white", width=15).pack()


# STUDENT DETAILS WINDOW
def open_student_details(username):
    """ Function to open student details window """
    global current_window
    if current_window:
        current_window.withdraw()
    detail_win = Toplevel(root)
    current_window = detail_win
    detail_win.title("Student Details")
    detail_win.state("zoomed")
    detail_win.config(bg="#EDEADE")

    # Logout button
    Button(detail_win, text="Logout", command=lambda:[detail_win.destroy(), open_login()], bg="#4B3832", fg="white").pack(pady=5)

    try:
        # Join users and students tables using email
        con = pymysql.connect(host="localhost", user="root", password="", database="student_db")
        cur = con.cursor()
        cur.execute("""SELECT u.username,u.password,u.email,s.name,s.age,s.course,s.phone 
                       FROM users u JOIN students s ON u.email=s.email 
                       WHERE u.username=%s""", (username,))
        row = cur.fetchone()
        con.close()
        if row:
            labels = ["Username","Password","Email","Name","Age","Course","Phone"]
            # Display all fetched details
            for i, val in enumerate(row):
                Label(detail_win, text=f"{labels[i]}: {val}", font=("Arial",12,"bold"), bg="#EDEADE", fg="#4B3832").pack(pady=5)
        else:
            messagebox.showerror("Error","Student details not found!", parent=detail_win)
    except Exception as e:
        messagebox.showerror("DB Error", str(e), parent=detail_win)


# ADMIN DASHBOARD
def open_admin_dashboard(username):
    """ Function to open admin dashboard """
    global current_window
    if current_window:
        current_window.withdraw()
    admin_win = Toplevel(root)
    current_window = admin_win
    admin_win.title("Admin Dashboard")
    admin_win.state("zoomed")
    admin_win.config(bg="#EDEADE")

    # Welcome label
    Label(admin_win, text=f"Welcome Admin: {username}", font=("Arial", 14, "bold"), bg="#EDEADE", fg="#4B3832").pack(pady=10)

    # Buttons for admin tasks
    Button(admin_win, text="Manage Students", command=lambda:[admin_win.withdraw(), student_records.show_students(root, admin_win)], bg="#4B3832", fg="white", width=20).pack(pady=10)
    Button(admin_win, text="Manage Users", command=lambda: show_users(admin_win), bg="#4B3832", fg="white", width=20).pack(pady=10)
    Button(admin_win, text="Logout", command=lambda:[admin_win.destroy(), open_login()], bg="#4B3832", fg="white", width=20).pack(pady=10)
    Button(admin_win,text="Show Statistics",command=lambda: [admin_win.withdraw(), statistics.statistics_window(admin_win, admin_win)],bg="#4B3832",fg="white",width=20).pack(pady=10)


# USER MANAGEMENT
def show_users(parent_window):
    """ Function to show users table """
    parent_window.withdraw()
    user_win = Toplevel(parent_window)
    user_win.state("zoomed")
    user_win.geometry("600x400")
    user_win.config(bg="#EDEADE")

    # BACK BUTTON
    Button(
        user_win,
        text="Back to Dashboard",
        bg="#4B3832", fg="white",
        command=lambda: [user_win.destroy(), parent_window.deiconify(), parent_window.state("zoomed")]
    ).pack(pady=10)

    # Define table columns
    cols = ("ID", "Username", "Email", "Role")
    tree = ttk.Treeview(user_win, columns=cols, show="headings")
    for col in cols:
        tree.heading(col, text=col)
    tree.pack(fill=BOTH, expand=True)

    try:
        # Fetch all users
        con = pymysql.connect(host="localhost", user="root", password="", database="student_db")
        cur = con.cursor()
        cur.execute("SELECT id, username, email, role FROM users")
        rows = cur.fetchall()
        con.close()
        # Insert users into treeview
        for row in rows:
            tree.insert("", END, values=row)
    except Exception as e:
        messagebox.showerror("DB Error", str(e), parent=user_win)


# STUDENT FORM
def open_student_form(admin_window):
    """ Function to open student form (admin use only) """
    admin_window.withdraw()
    global current_window
    if current_window:
        current_window.withdraw()
    student_win = Toplevel(root)
    current_window = student_win
    student_win.title("Student Form")
    student_win.state("zoomed")
    student_win.config(bg="#EDEADE")

    # Back button
    Button(
        student_win,
        text="Back to Dashboard",
        bg="#4B3832", fg="white",
        command=lambda: [student_win.destroy(), admin_window.deiconify()]
    ).pack(pady=5)

    # Frame for form fields
    left_frame = Frame(student_win, bg="#EDEADE")
    left_frame.pack(pady=20, padx=20)

    # Create input entries dynamically
    entries = {}
    for lbl_text in ["Name","Age","Course","Email","Phone"]:
        Label(left_frame, text=lbl_text, bg="#EDEADE", fg="#4B3832", font=("Arial", 12, "bold")).pack(pady=5)
        entry = Entry(left_frame, font=("Arial",12), bd=2, relief="solid")
        entry.pack(pady=5)
        entries[lbl_text.lower()] = entry  # Store entry by key

    # Function to insert student into DB
    def add_student():
        vals = [entries[key].get() for key in ["name","age","course","email","phone"]]
        # Check empty fields
        if "" in vals:
            messagebox.showerror("Error","All fields required!", parent=student_win)
            return
        try:
            # Insert into students table
            con = pymysql.connect(host="localhost", user="root", password="", database="student_db")
            cur = con.cursor()
            cur.execute("INSERT INTO students(name,age,course,email,phone) VALUES(%s,%s,%s,%s,%s)", tuple(vals))
            con.commit()
            con.close()
            messagebox.showinfo("Success","Student Added!", parent=student_win)
        except Exception as e:
            messagebox.showerror("DB Error", str(e), parent=student_win)

    # Add student button
    Button(left_frame, text="Add Student", command=add_student, bg="#4B3832", fg="white", width=15).pack(pady=10)
    # Show students button
    Button(left_frame, text="Show Students", command=show_students, bg="#4B3832", fg="white", width=15).pack(pady=10)


# PROGRAM START
open_login()       # Open login window first
root.mainloop()    # Run tkinter event loop
