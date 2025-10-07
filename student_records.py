# student_records.py
# This file shows all student records in a new window.
# It supports Add, Update, Delete, Search, Import, Export operations.

import pymysql
import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Entry, Frame, Button, Label, END, filedialog
import csv
import pandas as pd   # For import feature
import ui_form  # to call open_login on back
from dashboard import dashboard_window


def show_students(root, dashboard_window):
    # Hide the main root window
    dashboard_window.withdraw()

    # Create new window for Student Records
    win = tk.Toplevel(root)
    win.title("All Students")
    win.state("zoomed")  # open records window full screen
    win.config(bg="#EDEADE")

    # BACK BUTTON
    tk.Button(
        win,
        text="Back to Dashboard",
        font=("Arial", 10, "bold"),
        bg="#4B3832", fg="white",
        command=lambda: [win.destroy(), dashboard_window.deiconify(), dashboard_window.state("zoomed")]
    ).pack(pady=10)

    #  MAIN FRAME
    frame = Frame(win, bg="#EDEADE")
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # TOP FORM (Entries for Add/Update/Delete)
    form_frame = Frame(frame, bg="#EDEADE")
    form_frame.pack(fill="x", pady=10)

    # Input fields
    id_entry = Entry(form_frame, font=("Arial", 12), bd=2, relief="solid")
    name_entry = Entry(form_frame, font=("Arial", 12), bd=2, relief="solid")
    age_entry = Entry(form_frame, font=("Arial", 12), bd=2, relief="solid")
    course_entry = Entry(form_frame, font=("Arial", 12), bd=2, relief="solid")
    email_entry = Entry(form_frame, font=("Arial", 12), bd=2, relief="solid")
    phone_entry = Entry(form_frame, font=("Arial", 12), bd=2, relief="solid")

    labels = ["ID", "Name", "Age", "Course", "Email", "Phone"]
    entries = [id_entry, name_entry, age_entry, course_entry, email_entry, phone_entry]

    # Place labels & entry fields in grid
    for i, (label, entry) in enumerate(zip(labels, entries)):
        Label(form_frame, text=label, bg="#EDEADE", font=("Arial", 12, "bold")).grid(
            row=i // 3, column=(i % 3) * 2, padx=5, pady=5
        )
        entry.grid(row=i // 3, column=(i % 3) * 2 + 1, padx=5, pady=5)

    # TREEVIEW TABLE
    cols = ("ID", "Name", "Age", "Course", "Email", "Phone")
    tree = ttk.Treeview(frame, columns=cols, show="headings", height=15)

    # Add scrollbars
    y_scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    x_scroll = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
    y_scroll.pack(side="right", fill="y")
    x_scroll.pack(side="bottom", fill="x")
    tree.pack(fill="both", expand=True, pady=10)

    # Define column headings
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=150)

    # FUNCTIONS
    def load_data():
        """Load all student records from database into treeview"""
        for item in tree.get_children():
            tree.delete(item)  # Clear existing rows
        try:
            con = pymysql.connect(host="localhost", user="root", password="", database="student_db")
            cur = con.cursor()
            cur.execute("SELECT id, name, age, course, email, phone FROM students")
            rows = cur.fetchall()
            con.close()
            for row in rows:
                tree.insert("", "end", values=row)  # Insert each row in table
        except Exception as e:
            messagebox.showerror("DB Error", str(e), parent=win)

    def clear_entries():
        """Clear all form entry boxes"""
        for entry in entries:
            entry.delete(0, END)

    def add_student():
        """Add a new student record"""
        try:
            con = pymysql.connect(host="localhost", user="root", password="", database="student_db")
            cur = con.cursor()
            cur.execute(
                "INSERT INTO students(name, age, course, email, phone) VALUES(%s, %s, %s, %s, %s)",
                (name_entry.get(), age_entry.get(), course_entry.get(), email_entry.get(), phone_entry.get())
            )
            con.commit()
            con.close()
            load_data()
            clear_entries()
            messagebox.showinfo("Success", "Student Added!", parent=win)
        except Exception as e:
            messagebox.showerror("DB Error", str(e), parent=win)

    def update_student():
        """Update existing student record"""
        try:
            con = pymysql.connect(host="localhost", user="root", password="", database="student_db")
            cur = con.cursor()
            cur.execute(
                "UPDATE students SET name=%s, age=%s, course=%s, email=%s, phone=%s WHERE id=%s",
                (name_entry.get(), age_entry.get(), course_entry.get(), email_entry.get(), phone_entry.get(), id_entry.get())
            )
            con.commit()
            con.close()
            load_data()
            clear_entries()
            messagebox.showinfo("Success", "Student Updated!", parent=win)
        except Exception as e:
            messagebox.showerror("DB Error", str(e), parent=win)

    def delete_student():
        """Delete a student record"""
        try:
            con = pymysql.connect(host="localhost", user="root", password="", database="student_db")
            cur = con.cursor()
            cur.execute("DELETE FROM students WHERE id=%s", (id_entry.get(),))
            con.commit()
            con.close()
            load_data()
            clear_entries()
            messagebox.showinfo("Success", "Student Deleted!", parent=win)
        except Exception as e:
            messagebox.showerror("DB Error", str(e), parent=win)

    def row_select(event):
        """When row is clicked, load data into form fields"""
        selected = tree.focus()
        if selected:
            values = tree.item(selected, "values")
            for entry, value in zip(entries, values):
                entry.delete(0, END)
                entry.insert(0, value)

    tree.bind("<ButtonRelease-1>", row_select)

    # BOTTOM BUTTONS
    btn_frame = Frame(win, bg="#EDEADE")
    btn_frame.pack(fill="x", pady=10)

    Button(btn_frame, text="Add", command=add_student, bg="#4B3832", fg="white", width=12).pack(side="left", padx=10)
    Button(btn_frame, text="Update", command=update_student, bg="#4B3832", fg="white", width=12).pack(side="left", padx=10)
    Button(btn_frame, text="Delete", command=delete_student, bg="#4B3832", fg="white", width=12).pack(side="left", padx=10)
    Button(btn_frame, text="Refresh", command=load_data, bg="#4B3832", fg="white", width=12).pack(side="left", padx=10)

    # SEARCH SECTION
    search_frame = Frame(win, bg="#EDEADE")
    search_frame.pack(fill="x", pady=10)

    Label(search_frame, text="Search (Name or Course):", bg="#EDEADE", font=("Arial", 12, "bold")).pack(side="left", padx=5)

    search_var = tk.StringVar()
    search_entry = Entry(search_frame, textvariable=search_var, font=("Arial", 12), bd=2, relief="solid", width=30)
    search_entry.pack(side="left", padx=5)

    def search_students(event=None):
        """Search students by name or course"""
        query = search_var.get()
        for item in tree.get_children():
            tree.delete(item)
        try:
            con = pymysql.connect(host="localhost", user="root", password="", database="student_db")
            cur = con.cursor()
            cur.execute(
                "SELECT id, name, age, course, email, phone FROM students WHERE name LIKE %s OR course LIKE %s",
                (f"%{query}%", f"%{query}%")
            )
            rows = cur.fetchall()
            con.close()
            for row in rows:
                tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("DB Error", str(e), parent=win)

    search_entry.bind("<Return>", search_students)  # Press Enter to search
    Button(search_frame, text="Search", command=search_students, bg="#4B3832", fg="white", width=12).pack(side="left", padx=5)
    Button(search_frame, text="Show All", command=load_data, bg="#4B3832", fg="white", width=12).pack(side="left", padx=5)

    # EXPORT & IMPORT
    file_frame = Frame(win, bg="#EDEADE")
    file_frame.pack(fill="x", pady=10)

    def export_csv():
        """Export student data to a CSV file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not file_path:
            return
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Age", "Course", "Email", "Phone"])  # Column headers
            for child in tree.get_children():
                writer.writerow(tree.item(child)["values"])
        messagebox.showinfo("Export Success", f"Data exported to {file_path}")

    def import_csv():
        """Import student data from a CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not file_path:
            return
        try:
            df = pd.read_csv(file_path)
            con = pymysql.connect(host="localhost", user="root", password="", database="student_db")
            cur = con.cursor()
            inserted_count = 0
            for _, row in df.iterrows():
                # Check if student ID already exists
                cur.execute("SELECT id FROM students WHERE id=%s", (row['ID'],))
                result = cur.fetchone()
                if not result:  # Insert only if ID does not exist
                    cur.execute(
                        "INSERT INTO students(id, name, age, course, email, phone) VALUES(%s,%s,%s,%s,%s,%s)",
                        (row['ID'], row['Name'], row['Age'], row['Course'], row['Email'], row['Phone'])
                    )
                    inserted_count += 1
            con.commit()
            con.close()
            load_data()
            messagebox.showinfo("Import Success", f"{inserted_count} new students imported successfully!")
        except Exception as e:
            messagebox.showerror("Import Error", str(e), parent=win)

    Button(file_frame, text="Export to CSV", command=export_csv, bg="green", fg="white", width=15).pack(side="left", padx=5)
    Button(file_frame, text="Import from CSV", command=import_csv, bg="blue", fg="white", width=15).pack(side="left", padx=5)

    # INITIAL LOAD
    load_data()  # Load all data when window opens
