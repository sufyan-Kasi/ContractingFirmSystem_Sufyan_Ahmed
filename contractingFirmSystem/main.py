import sys
import sqlite3
from PyQt5 import QtWidgets
from ui.login_ui import Ui_MainWindow
from ui.dashboard_ui import Ui_DashboardWindow

# ---- DASHBOARD WINDOW ----
class DashboardApp(QtWidgets.QMainWindow):
    def __init__(self, username):
        super(DashboardApp, self).__init__()
        self.ui = Ui_DashboardWindow()
        self.ui.setupUi(self)
        
        # 1. Make window full screen
        self.showMaximized()

        # 2. Apply spacing and margins to all tabs
        tab_widget = self.ui.main_tabs
        for i in range(tab_widget.count()):
            page = tab_widget.widget(i)
            layout = page.layout()
            if not layout:
                layout = QtWidgets.QVBoxLayout(page)  
                page.setLayout(layout)
            layout.setSpacing(15)                  
            layout.setContentsMargins(20, 20, 20, 20)

        # 3. Fix all buttons inside central widget
        for button in self.ui.centralwidget.findChildren(QtWidgets.QPushButton):
            button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            button.setMaximumWidth(120)

        # 4. Make all tables expand properly (only horizontal stretch)
        for table in self.ui.centralwidget.findChildren(QtWidgets.QTableWidget):
            table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)  # stretch columns
            table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)  # keep rows natural

        # Increase font size for buttons
        for button in self.ui.centralwidget.findChildren(QtWidgets.QPushButton):
            font = button.font()
            font.setPointSize(12)  
            button.setFont(font)
            button.setMinimumHeight(35)  

        # Increase font size for labels
        for label in self.ui.centralwidget.findChildren(QtWidgets.QLabel):
            font = label.font()
            font.setPointSize(12)
            label.setFont(font)

        # Increase font size for LineEdits and TextEdits
        for edit in self.ui.centralwidget.findChildren((QtWidgets.QLineEdit, QtWidgets.QTextEdit, QtWidgets.QPlainTextEdit)):
            font = edit.font()
            font.setPointSize(12)
            edit.setFont(font)
            edit.setMinimumHeight(30) 

        # Increase font size for ComboBoxes
        for combo in self.ui.centralwidget.findChildren(QtWidgets.QComboBox):
            font = combo.font()
            font.setPointSize(12)
            combo.setFont(font)
            combo.setMinimumHeight(30)  

        # ------------------ Modern Dark Theme ------------------
        dark_stylesheet = """
        /* Main Window and central widget */
        QMainWindow, QWidget {
            background-color: #121212;
            color: #e0e0e0;
            font-family: "Segoe UI", Arial, sans-serif;
            font-size: 12pt;
        }

        /* Buttons */
        QPushButton {
            background-color: #2c2c2c;
            color: #e0e0e0;
            border: 1px solid #3a3a3a;
            border-radius: 6px;
            padding: 8px;
        }
        QPushButton:hover {
            background-color: #3a3a3a;
        }
        QPushButton:pressed {
            background-color: #505050;
        }

        /* Labels */
        QLabel {
            color: #e0e0e0;
        }

        /* LineEdits, TextEdits, PlainTextEdits */
        QLineEdit, QTextEdit, QPlainTextEdit {
            background-color: #1e1e1e;
            color: #e0e0e0;
            border: 1px solid #3a3a3a;
            border-radius: 4px;
            padding: 4px;
        }

        /* ComboBoxes */
        QComboBox {
            background-color: #1e1e1e;
            color: #e0e0e0;
            border: 1px solid #3a3a3a;
            border-radius: 4px;
            padding: 4px;
        }
        QComboBox QAbstractItemView {
            background-color: #1e1e1e;
            color: #e0e0e0;
            selection-background-color: #3a3a3a;
        }

        /* Tables */
        QTableWidget, QTableView {
            background-color: #1e1e1e;
            color: #e0e0e0;
            gridline-color: #3a3a3a;
            border: 1px solid #3a3a3a;
        }
        QHeaderView::section {
            background-color: #2c2c2c;
            color: #e0e0e0;
            padding: 4px;
            border: 1px solid #3a3a3a;
        }

        /* TabWidget */
        QTabWidget::pane {
            border: 1px solid #3a3a3a;
            margin: 10px;
        }
        QTabBar::tab {
            background: #2c2c2c;
            color: #e0e0e0;
            padding: 8px 15px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
        }
        QTabBar::tab:selected {
            background: #3a3a3a;
            font-weight: bold;
        }

        /* ScrollBars */
        QScrollBar:vertical, QScrollBar:horizontal {
            background: #1e1e1e;
            width: 12px;
            height: 12px;
            margin: 0px;
        }
        QScrollBar::handle {
            background: #3a3a3a;
            border-radius: 6px;
        }
        QScrollBar::handle:hover {
            background: #505050;
        }
        QScrollBar::add-line, QScrollBar::sub-line {
            background: none;
        }
        """

        self.setStyleSheet(dark_stylesheet)


        self.showMaximized()  
        self.username = username
        self.setWindowTitle(f"Dashboard - Logged in as {self.username}")

        self.ui.label.setText(f"Welcome, {self.username} ")

        self.ui.logout_button.clicked.connect(self.logout)

        self.load_overview_data()
        
        self.ui.add_client_button.clicked.connect(self.add_client)
        self.ui.delete_client_button.clicked.connect(self.delete_client)
        self.load_clients()
        
        self.populate_client_dropdown()
        self.populate_project_dropdown()
        self.load_projects()
        self.ui.add_project_button.clicked.connect(self.add_project)
        self.ui.delete_project_button.clicked.connect(self.delete_project)

        self.populate_project_dropdown()
        self.ui.add_payment_button.clicked.connect(self.add_payment)
        self.ui.delete_payment_button.clicked.connect(self.delete_payment)
        self.load_payments()
        
        self.ui.add_machine_button.clicked.connect(self.add_machine)
        self.ui.delete_machine_button.clicked.connect(self.delete_machine)
        self.load_machines()
        
        self.ui.add_employee_btn.clicked.connect(self.add_employee)
        self.ui.update_employee_btn.clicked.connect(self.update_employee)
        self.ui.delete_employee_btn.clicked.connect(self.delete_employee)
        self.ui.employees_table.itemClicked.connect(lambda _: self.on_employee_table_click())
        self.load_employees()
        
        self.load_salary_employees()
        self.load_salary_table()
        self.ui.add_salary_button.clicked.connect(self.add_salary_record)
        self.ui.delete_salary_button.clicked.connect(self.delete_salary_record)


    def logout(self):
        self.close()
        self.login_window = LoginApp()
        self.login_window.show()

    def load_overview_data(self):
        """Fetch total clients, projects, ongoing projects from database"""
        conn = sqlite3.connect("database/firm.db")
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM clients")
        total_clients = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM projects")
        total_projects = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM projects WHERE status='ongoing'")
        ongoing_projects = cur.fetchone()[0]

        conn.close()

        # update labels in UI
        self.ui.clients_count_label.setText(str(total_clients))
        self.ui.projects_count_label.setText(str(total_projects))
        self.ui.payments_sum_label.setText(str(ongoing_projects))
        
    def load_overview(self):
        conn = sqlite3.connect("database/firm.db")
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM clients")
        clients_count = cur.fetchone()[0]
        self.ui.clients_count_label.setText(str(clients_count))

        cur.execute("SELECT COUNT(*) FROM projects")
        projects_count = cur.fetchone()[0]
        self.ui.projects_count_label.setText(str(projects_count))

        cur.execute("SELECT IFNULL(SUM(amount), 0) FROM payments")
        payments_total = cur.fetchone()[0]
        self.ui.payments_sum_label.setText(f"Rs {payments_total}")

        conn.close()


    def load_clients(self):
        """Load all clients into the table"""
        conn = sqlite3.connect("database/firm.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM clients")
        clients = cur.fetchall()
        conn.close()

        self.ui.clients_table.setRowCount(len(clients))
        self.ui.clients_table.setColumnCount(4)
        self.ui.clients_table.setHorizontalHeaderLabels(["ID", "Name", "Contact", "Address"])

        for row_idx, row_data in enumerate(clients):
            for col_idx, value in enumerate(row_data):
                self.ui.clients_table.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(value)))

    def add_client(self):
        """Add new client to database"""
        name = self.ui.client_name_input.text()
        contact = self.ui.client_contact_input.text()
        address = self.ui.client_address_input.text()

        if not name:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Client name is required")
            return

        conn = sqlite3.connect("database/firm.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO clients (name, contact, address) VALUES (?, ?, ?)", (name, contact, address))
        conn.commit()
        conn.close()

        QtWidgets.QMessageBox.information(self, "Success", "Client added successfully!")
        self.ui.client_name_input.clear()
        self.ui.client_contact_input.clear()
        self.ui.client_address_input.clear()
        self.load_clients()

    def delete_client(self):
        """Delete selected client"""
        selected_row = self.ui.clients_table.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Selection Error", "Please select a client to delete")
            return

        client_id = self.ui.clients_table.item(selected_row, 0).text()
        conn = sqlite3.connect("database/firm.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM clients WHERE id=?", (client_id,))
        conn.commit()
        conn.close()

        QtWidgets.QMessageBox.information(self, "Deleted", "Client removed successfully!")
        self.load_clients()
        
    def load_projects(self):
        conn = sqlite3.connect("database/firm.db")
        cur = conn.cursor()
        cur.execute("""
            SELECT projects.id, clients.name, projects.project_name, 
                projects.project_value, projects.status
            FROM projects
            LEFT JOIN clients ON projects.client_id = clients.id
        """)
        rows = cur.fetchall()
        conn.close()

        self.ui.projects_table.setRowCount(len(rows))
        self.ui.projects_table.setColumnCount(5)
        self.ui.projects_table.setHorizontalHeaderLabels([
            "ID", "Client", "Project Name", "Value", "Status"
        ])

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.ui.projects_table.setItem(r, c, QtWidgets.QTableWidgetItem(str(val)))
        
    def populate_client_dropdown(self):
        self.ui.project_client_dropdown.clear()
        conn = sqlite3.connect("database/firm.db")
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM clients")
        clients = cur.fetchall()
        conn.close()

        for cid, name in clients:
            self.ui.project_client_dropdown.addItem(name, cid)

    def add_project(self):
        client_id = self.ui.project_client_dropdown.currentData()
        name = self.ui.project_name_input.text()
        value = self.ui.project_value_input.text()
        start = self.ui.project_start_date.text()
        end = self.ui.project_end_date.text()

        if not name:
            QtWidgets.QMessageBox.warning(self, "Error", "Project name required")
            return

        conn = sqlite3.connect("database/firm.db")
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO projects (client_id, project_name, project_value, start_date, end_date)
            VALUES (?, ?, ?, ?, ?)
        """, (client_id, name, value, start, end))
        conn.commit()
        conn.close()

        QtWidgets.QMessageBox.information(self, "Success", "Project added")
        self.load_projects()
        self.populate_project_dropdown()  # refresh payments dropdown
        
    def delete_project(self):
        row = self.ui.projects_table.currentRow()
        if row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Select a project to delete")
            return

        project_id = self.ui.projects_table.item(row, 0).text()

        conn = sqlite3.connect("database/firm.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM projects WHERE id=?", (project_id,))
        conn.commit()
        conn.close()

        QtWidgets.QMessageBox.information(self, "Deleted", "Project removed")
        self.load_projects()
        self.populate_project_dropdown()


    def populate_project_dropdown(self):
        """Load projects for payment selection"""
        self.ui.payment_project_dropdown.clear()
        conn = sqlite3.connect("database/firm.db")
        cur = conn.cursor()
        cur.execute("SELECT id, project_name FROM projects")
        projects = cur.fetchall()
        conn.close()

        for pid, name in projects:
            self.ui.payment_project_dropdown.addItem(name, pid)

    def load_payments(self):
        """Load payments into table"""
        conn = sqlite3.connect("database/firm.db")
        cur = conn.cursor()
        cur.execute("""
            SELECT p.id, pr.project_name, p.amount, p.date
            FROM payments p
            LEFT JOIN projects pr ON p.project_id = pr.id
        """)
        rows = cur.fetchall()
        conn.close()

        self.ui.payments_table.setRowCount(len(rows))
        self.ui.payments_table.setColumnCount(4)
        self.ui.payments_table.setHorizontalHeaderLabels([
            "ID", "Project", "Amount", "Date"
        ])

        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                self.ui.payments_table.setItem(r, c, QtWidgets.QTableWidgetItem(str(value)))

    def add_payment(self):
        """Insert new payment"""
        project_id = self.ui.payment_project_dropdown.currentData()
        amount = self.ui.payment_amount_input.text()
        date = self.ui.payment_date_input.text()

        if not amount:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Payment amount required")
            return

        conn = sqlite3.connect("database/firm.db")
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO payments (project_id, amount, date)
            VALUES (?, ?, ?)
        """, (project_id, amount, date))
        conn.commit()
        conn.close()

        QtWidgets.QMessageBox.information(self, "Saved", "Payment added!")
        self.load_payments()

    def delete_payment(self):
        row = self.ui.payments_table.currentRow()
        if row == -1:
            QtWidgets.QMessageBox.warning(self, "Select Payment", "Select a row to delete")
            return

        payment_id = self.ui.payments_table.item(row, 0).text()

        conn = sqlite3.connect("database/firm.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM payments WHERE id=?", (payment_id,))
        conn.commit()
        conn.close()

        QtWidgets.QMessageBox.information(self, "Deleted", "Payment removed")
        self.load_payments()
        
    def load_machines(self):
        conn = sqlite3.connect("database/firm.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM machines")
        rows = cur.fetchall()
        conn.close()

        self.ui.machines_table.setRowCount(len(rows))
        self.ui.machines_table.setColumnCount(6)
        self.ui.machines_table.setHorizontalHeaderLabels([
            "ID", "Name", "Type", "Purchase Date", "Cost", "Status"
        ])

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.ui.machines_table.setItem(r, c, QtWidgets.QTableWidgetItem(str(val)))
                
    def add_machine(self):
        name = self.ui.machine_name_input.text()
        type_ = self.ui.machine_type_input.text()
        date = self.ui.machine_purchase_date.text()
        cost = self.ui.machine_cost_input.value()
        status = self.ui.machine_status_dropdown.currentText()

        if not name:
            QtWidgets.QMessageBox.warning(self, "Error", "Machine name is required")
            return

        conn = sqlite3.connect("database/firm.db")
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO machines (machine_name, machine_type, purchase_date, cost, status)
            VALUES (?, ?, ?, ?, ?)
        """, (name, type_, date, cost, status))
        conn.commit()
        conn.close()

        QtWidgets.QMessageBox.information(self, "Success", "Machine added")
        self.load_machines()

    def delete_machine(self):
        row = self.ui.machines_table.currentRow()
        if row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Select a machine to delete")
            return

        machine_id = self.ui.machines_table.item(row, 0).text()

        conn = sqlite3.connect("database/firm.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM machines WHERE id=?", (machine_id,))
        conn.commit()
        conn.close()

        QtWidgets.QMessageBox.information(self, "Deleted", "Machine removed")
        self.load_machines()
        
    def load_employees(self):
        """Load employees into table"""
        try:
            conn = sqlite3.connect("database/firm.db")
            cur = conn.cursor()
            cur.execute("SELECT id, name, phone, cnic, designation, salary, status FROM employees")
            rows = cur.fetchall()
        finally:
            conn.close()

        self.ui.employees_table.setRowCount(len(rows))
        self.ui.employees_table.setColumnCount(7)
        self.ui.employees_table.setHorizontalHeaderLabels(["ID","Name","Phone","CNIC","Designation","Salary","Status"])

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.ui.employees_table.setItem(r, c, QtWidgets.QTableWidgetItem(str(val)))

    def add_employee(self):
        """Insert new employee"""
        try:
            name = self.ui.employee_name_input.text().strip()
            phone = self.ui.employee_phone_input.text().strip()
            cnic = self.ui.employee_cnic_input.text().strip()
            designation = self.ui.employee_designation_input.currentText()
            salary_text = self.ui.employee_salary_input.text().strip()

            if not name:
                QtWidgets.QMessageBox.warning(self, "Input Error", "Employee name is required")
                return

            # validate salary
            try:
                salary = float(salary_text) if salary_text else 0.0
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Input Error", "Salary must be a number")
                return

            conn = sqlite3.connect("database/firm.db")
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO employees (name, phone, cnic, designation, salary)
                VALUES (?, ?, ?, ?, ?)
            """, (name, phone, cnic, designation, salary))
            conn.commit()
            conn.close()

            QtWidgets.QMessageBox.information(self, "Success", "Employee added")
            # Clear inputs
            self.ui.employee_name_input.clear()
            self.ui.employee_phone_input.clear()
            self.ui.employee_cnic_input.clear()
            self.ui.employee_salary_input.clear()
            # Refresh table
            self.load_employees()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to add employee:\n{e}")

    def update_employee(self):
        """Update selected employee"""
        try:
            row = self.ui.employees_table.currentRow()
            if row == -1:
                QtWidgets.QMessageBox.warning(self, "Selection Error", "Select an employee to update")
                return

            emp_id = self.ui.employees_table.item(row, 0).text()
            name = self.ui.employee_name_input.text().strip()
            phone = self.ui.employee_phone_input.text().strip()
            cnic = self.ui.employee_cnic_input.text().strip()
            designation = self.ui.employee_designation_input.currentText()
            salary_text = self.ui.employee_salary_input.text().strip()

            if not name:
                QtWidgets.QMessageBox.warning(self, "Input Error", "Employee name is required")
                return

            try:
                salary = float(salary_text) if salary_text else 0.0
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Input Error", "Salary must be a number")
                return

            conn = sqlite3.connect("database/firm.db")
            cur = conn.cursor()
            cur.execute("""
                UPDATE employees
                SET name=?, phone=?, cnic=?, designation=?, salary=?
                WHERE id=?
            """, (name, phone, cnic, designation, salary, emp_id))
            conn.commit()
            conn.close()

            QtWidgets.QMessageBox.information(self, "Success", "Employee updated")
            self.load_employees()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to update employee:\n{e}")

    def delete_employee(self):
        """Delete selected employee"""
        try:
            row = self.ui.employees_table.currentRow()
            if row == -1:
                QtWidgets.QMessageBox.warning(self, "Selection Error", "Select an employee to delete")
                return

            emp_id = self.ui.employees_table.item(row, 0).text()
            confirm = QtWidgets.QMessageBox.question(self, "Confirm", "Delete this employee?",
                                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if confirm != QtWidgets.QMessageBox.Yes:
                return

            conn = sqlite3.connect("database/firm.db")
            cur = conn.cursor()
            cur.execute("DELETE FROM employees WHERE id=?", (emp_id,))
            conn.commit()
            conn.close()

            QtWidgets.QMessageBox.information(self, "Deleted", "Employee removed")
            self.load_employees()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to delete employee:\n{e}")

    def on_employee_table_click(self):
        """Load selected employee into form for editing"""
        row = self.ui.employees_table.currentRow()
        if row == -1:
            return
        try:
            emp_id = self.ui.employees_table.item(row, 0).text()
            name = self.ui.employees_table.item(row, 1).text()
            phone = self.ui.employees_table.item(row, 2).text()
            cnic = self.ui.employees_table.item(row, 3).text()
            designation = self.ui.employees_table.item(row, 4).text()
            salary = self.ui.employees_table.item(row, 5).text()

            self.ui.employee_name_input.setText(name)
            self.ui.employee_phone_input.setText(phone)
            self.ui.employee_cnic_input.setText(cnic)
            # set designation index safely
            idx = self.ui.employee_designation_input.findText(designation)
            if idx >= 0:
                self.ui.employee_designation_input.setCurrentIndex(idx)
            self.ui.employee_salary_input.setText(salary)
        except Exception:
            pass
        
    def load_salary_employees(self):
        conn = sqlite3.connect("database/firm.db")
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM employees WHERE status='active'")
        employees = cur.fetchall()
        conn.close()

        self.ui.salary_employee_dropdown.clear()

        for emp_id, name in employees:
            self.ui.salary_employee_dropdown.addItem(name, emp_id)
            
    def load_salary_table(self):
        self.ui.salary_table.setRowCount(0)

        conn = sqlite3.connect("database/firm.db")
        cur = conn.cursor()
        cur.execute("""
            SELECT es.id, e.name, es.salary_amount, es.month, es.date_paid, es.status
            FROM employee_salaries es
            JOIN employees e ON es.employee_id = e.id
            ORDER BY es.id DESC
        """)
        records = cur.fetchall()
        conn.close()

        self.ui.salary_table.setRowCount(len(records))
        self.ui.salary_table.setColumnCount(6)

        headers = ["ID", "Employee", "Amount", "Month", "Paid On", "Status"]
        self.ui.salary_table.setHorizontalHeaderLabels(headers)
        self.ui.salary_table.horizontalHeader().setStretchLastSection(True)

        for row, data in enumerate(records):
            for col, value in enumerate(data):
                self.ui.salary_table.setItem(row, col, QtWidgets.QTableWidgetItem(str(value)))

    def add_salary_record(self):
        employee_id = self.ui.salary_employee_dropdown.currentData()
        amount = self.ui.salary_amount_input.text()
        month = self.ui.salary_month_dropdown.currentText()
        date_paid = self.ui.salary_date_input.text()
        status = self.ui.salary_status_dropdown.currentText()

        if not amount:
            QtWidgets.QMessageBox.warning(self, "Missing Field", "Salary amount is required.")
            return

        conn = sqlite3.connect("database/firm.db")
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO employee_salaries (employee_id, salary_amount, month, date_paid, status)
            VALUES (?, ?, ?, ?, ?)
        """, (employee_id, amount, month, date_paid, status))

        conn.commit()
        conn.close()

        QtWidgets.QMessageBox.information(self, "Success", "Salary added successfully!")

        self.load_salary_table()
        
    def delete_salary_record(self):
        selected = self.ui.salary_table.currentRow()

        if selected < 0:
            QtWidgets.QMessageBox.warning(self, "Error", "Select a salary record to delete.")
            return

        salary_id = int(self.ui.salary_table.item(selected, 0).text())

        conn = sqlite3.connect("database/firm.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM employee_salaries WHERE id=?", (salary_id,))
        conn.commit()
        conn.close()

        QtWidgets.QMessageBox.information(self, "Deleted", "Salary record deleted.")
        self.load_salary_table()


# ---- LOGIN WINDOW ----
class LoginApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
         # ------------------ Dark Blue Login Theme ------------------
        login_stylesheet = """
        QWidget {
            background-color: #0D1B2A;
            color: #E0E0E0;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 12pt;
        }

        QLabel { color: #E0E0E0; }

        QLineEdit {
            background-color: #1B263B;
            color: #E0E0E0;
            border: 1px solid #415A77;
            border-radius: 5px;
            padding: 6px;
        }
        QLineEdit:focus { border: 1px solid #778DA9; }

        QPushButton {
            background-color: #415A77;
            color: #E0E0E0;
            border: 1px solid #778DA9;
            border-radius: 6px;
            padding: 8px;
            font-weight: bold;
        }
        QPushButton:hover { background-color: #778DA9; }
        QPushButton:pressed { background-color: #1B263B; }

        QComboBox {
            background-color: #1B263B;
            color: #E0E0E0;
            border: 1px solid #415A77;
            border-radius: 4px;
            padding: 4px;
        }
        QComboBox QAbstractItemView {
            background-color: #1B263B;
            color: #E0E0E0;
            selection-background-color: #415A77;
        }
        """
        self.setStyleSheet(login_stylesheet)  # <-- apply theme
        # ------------------ End Theme ------------------
        
        # fix password field echo mode here
        self.ui.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.login_button.clicked.connect(self.handle_login)

    def handle_login(self):
        username = self.ui.username_input.text()
        password = self.ui.password_input.text()

        conn = sqlite3.connect("database/firm.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()
        conn.close()

        if user:
            self.dashboard = DashboardApp(username)
            self.dashboard.load_overview()
            self.dashboard.show()
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Login Failed", "Invalid username or password")


# ---- MAIN APP ----
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginApp()
    window.show()
    sys.exit(app.exec_())
