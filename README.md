# Student_Management_System

#  (Python + Tkinter + SQL)

A complete **Student Management System** built using **Python**, **Tkinter (GUI)**, and **SQL**.  
This project allows administrators or teachers to manage student data, track statistics, and perform CRUD operations (Create, Read, Update, Delete) efficiently through a clean graphical interface.

---

## 🧩 Features

✅ **User Authentication**
- Secure login system with username & password (via `db_login.py`)

✅ **Student Record Management**
- Add, edit, delete, and view student records
- Search and filter students dynamically

✅ **Dashboard**
- Centralized interface to navigate all modules
- Clean UI built with Tkinter frames and widgets

✅ **Statistics Visualization**
- Display data summaries and basic statistics (`std_statistics.py`)

✅ **Database Integration**
- SQLite backend with structured schema (`schema.sql`)
- Automatic table creation if not found (`create_data_tables.py`)

✅ **Modular Design**
- Each functionality handled in a separate Python file for clarity and scalability

---

## 🗂️ Project Structure

student_management_system/
│
├── 1. config.py # Database path, constants, and app-wide settings
├── 2. db.py # Handles all database queries and connections
├── 3. db_test_connect.py # Quick test to verify database connectivity
├── 4. create_data_tables.py # Initializes and creates all DB tables
├── 5. schema.sql # SQL schema file defining tables and constraints
│
├── 6. ui_form.py # Common form layouts and UI utilities
├── 7. db_login.py # MAIN FILE – Launches the app and handles login
├── 8. student_form.py # GUI form for adding or editing student info
├── 9. student_records.py # Displays and manages stored student records
├── 10. dashboard.py # Main dashboard navigation window
├── 11. std_statistics.py # Statistical view and summary calculations
│
└── README.md 


## 🧠 How It Works

1. **Login:**  
   Start the app from `db_login.py`.  
   The system checks credentials stored in the SQLite database.

2. **Dashboard:**  
   Once logged in, the dashboard provides quick access to different sections like Student Records, Statistics, and User Management.

3. **Student Management:**  
   Use `student_form.py` to add/edit details and `student_records.py` to view or remove existing ones.

4. **Database:**  
   Data is stored locally in SQLite (`student_data.db`), auto-created using `create_data_tables.py`.

---

## 🛠️ Technologies Used

| Component | Technology |
|------------|-------------|
| **Programming Language** | Python 3.x |
| **GUI Framework** | Tkinter |
| **Database** | SQLite3 |
| **IDE (optional)** | PyCharm / VS Code |
| **OS Support** | Windows, Linux, macOS |

---

## 🚀 How to Run the Project

### 🔹 Step 1: Clone the Repository
```bash
git clone https://github.com/<your-username>/student-management-system.git
cd student-management-system
🔹 Step 2: Create Virtual Environment (optional)
bash
Copy code
python -m venv venv
venv\Scripts\activate     # (Windows)
source venv/bin/activate  # (Mac/Linux)
🔹 Step 3: Install Dependencies
(Usually Tkinter and SQLite are built-in, but install pillow if used for images)

bash
Copy code
pip install pillow
🔹 Step 4: Initialize Database
bash
Copy code
python create_data_tables.py
🔹 Step 5: Run the App
bash
Copy code
python db_login.py

🙏 Acknowledgement
Special thanks to my mentor Aakash Nama
for his invaluable guidance and support throughout the development of this project. 💫

💡 Future Enhancements
Add user roles (Admin / Teacher)

Export student data to Excel or CSV

Add charts for visual insights (Matplotlib)

Implement attendance and grade tracking modules

👨‍💻 Author
Danish Khatri
📧 Email: [danishkhatri885@gmail.com]
🌐 LinkedIn: Danish Khatri
🔗 GitHub: danish008-dan

