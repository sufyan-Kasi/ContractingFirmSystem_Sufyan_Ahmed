# Contracting Firm Management System

A desktop application built using **Python**, **PyQt5**, and **SQLite3** to manage operations of a contracting firm including:

- Client Management
- Project Management
- Payments Tracking
- Machine Inventory
- Employee Management
- Salary Records
- Login & Authentication
- Dashboard Overview

---

## 📂 Project Structure

CONTRACTING FIRM SOFTWARE/
│
├── main.py
│├── requirements.txt
│├── README.md
│├── .gitignore
│
├── database/
│ └── firm.db
│
├── modules/
│ ├── init.py
│ ├── auth.py
│ └── db_connection.py
│
└── ui/
├── login.ui
├── login_ui.py
├── dashboard.ui
├── dashboard_ui.py
├── main_window.ui
└── main_window_ui.py


---

## 🚀 Features

### ✔ Login System  
Secure login window using PyQt5.

### ✔ Dashboard  
Shows:
- Total clients  
- Total projects  
- Ongoing projects  
- Total payments  

### ✔ Clients  
Add, view, delete clients.

### ✔ Projects  
Add projects linked to clients, delete, view all.

### ✔ Payments  
Add payment linked to projects, delete, view all.

### ✔ Machines  
Add machine info, delete machine, list machines.

### ✔ Employees  
Add employee, update, delete, view employee list.

### ✔ Salaries  
Add salary record, delete salary, list salary records.

---

## 🛠 Installation

### 1️⃣ Install dependencies



pip install -r requirements.txt


### 2️⃣ Run the application



python main.py


---

## 🗄 Database

- Database is located at:  
  `database/firm.db`

To reset or recreate database, delete the file and rerun the app.

---

## 🛠 Troubleshooting

### ❗ UI Not Loading  
Regenerate UI Python files if you modify UI:



pyuic5 ui/login.ui -o ui/login_ui.py
pyuic5 ui/dashboard.ui -o ui/dashboard_ui.py


### ❗ Database Missing  
Delete `firm.db` and let app recreate it.

---

## 📌 Future Improvements (Optional)
- User roles (Admin / Employee)  
- Dark mode  
- Export to PDF/Excel  
- Dashboard charts  