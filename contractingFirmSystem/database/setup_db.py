import sqlite3

def create_database():
    conn = sqlite3.connect("database/firm.db")
    cur = conn.cursor()

    # --- USERS TABLE ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'employee'
        );
    """)

    # --- CLIENTS TABLE ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT,
            address TEXT
        );
    """)

    # --- PROJECTS TABLE ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            project_name TEXT NOT NULL,
            project_value REAL DEFAULT 0,
            start_date TEXT,
            end_date TEXT,
            status TEXT DEFAULT 'ongoing',
            FOREIGN KEY (client_id) REFERENCES clients(id)
        );
    """)
    
    # Payments Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (project_id) REFERENCES projects(id)
        )
    """)

    # Create a default admin user
    cur.execute("""
        INSERT OR IGNORE INTO users (username, password, role)
        VALUES ('admin', '123', 'admin');
    """)
    
    # --- MACHINES TABLE ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS machines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_name TEXT NOT NULL,
            machine_type TEXT,
            purchase_date TEXT,
            cost REAL DEFAULT 0,
            status TEXT DEFAULT 'available'
        );
    """)
    
    # --- Employees Table ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            cnic TEXT,
            designation TEXT,
            salary REAL,
            join_date TEXT DEFAULT CURRENT_DATE,
            status TEXT DEFAULT 'active'
        );
    """)
    # --- Employee_salary Table ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS employee_salaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            salary_amount REAL,
            month TEXT,
            date_paid TEXT,
            status TEXT,
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        );
    """)

    conn.commit()
    conn.close()
    print("Database setup complete: firm.db created successfully")
    

if __name__ == "__main__":
    create_database()