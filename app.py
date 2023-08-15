from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize the database
def initialize_db():
    conn = sqlite3.connect('employee_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    email TEXT,
                    age INTEGER,
                    date TEXT,
                    salary REAL)''')
    conn.commit()
    conn.close()

initialize_db()

@app.route('/')
def index():
    employee_data = load_data()
    return render_template('index.html', employee_data=employee_data)

@app.route('/add', methods=['POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        date = request.form['date']
        salary = request.form['salary']

        if name and email and age and date and salary:
            try:
                conn = sqlite3.connect("employee_data.db")
                cursor = conn.cursor()

                cursor.execute("INSERT INTO employees (name, email, age, date, salary) VALUES (?, ?, ?, ?, ?)",
                               (name, email, age, date, salary))

                conn.commit()
                conn.close()

                flash('Employee added successfully', 'success')
            except sqlite3.Error as e:
                flash(f'Error adding employee: {e}', 'danger')
        else:
            flash('Please fill in all fields', 'danger')

        return redirect(url_for('index'))
    
@app.route('/add_employeee')
def add_employeee():
    return render_template('add_employeee.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    if request.method == 'GET':
        employee = get_employee(id)
        return render_template('edit.html', employee=employee)
    elif request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        date = request.form['date']
        salary = request.form['salary']

        if name and email and age and date and salary:
            try:
                conn = sqlite3.connect("employee_data.db")
                cursor = conn.cursor()

                cursor.execute("UPDATE employees SET name=?, email=?, age=?, date=?, salary=? WHERE id=?",
                            (name, email, age, date, salary, id))

                conn.commit()
                conn.close()

                flash('Employee updated successfully', 'success')
            except sqlite3.Error as e:
                flash(f'Error updating employee: {e}', 'danger')
        else:
            flash('Please fill in all fields', 'danger')

        return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_employee(id):
    try:
        conn = sqlite3.connect("employee_data.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM employees WHERE id=?", (id,))
        conn.commit()
        conn.close()

        flash('Employee deleted successfully', 'success')
    except sqlite3.Error as e:
        flash(f'Error deleting employee: {e}', 'danger')

    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search_employee():
    search_query = request.form['search_query'].strip().lower()

    if not search_query:
        return redirect(url_for('index'))

    employee_data = load_data(search_query)
    return render_template('index.html', employee_data=employee_data)

# Load data from the database
def load_data(search_query=None):
    try:
        conn = sqlite3.connect("employee_data.db")
        cursor = conn.cursor()

        if search_query:
            cursor.execute("SELECT * FROM employees WHERE lower(name) LIKE ?", ('%' + search_query + '%',))
        else:
            cursor.execute("SELECT * FROM employees")

        employee_data = cursor.fetchall()
        conn.close()

        return employee_data
    except sqlite3.Error as e:
        flash(f'Error loading data: {e}', 'danger')
        return []

# Load employee data by ID
def get_employee(id):
    try:
        conn = sqlite3.connect("employee_data.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM employees WHERE id=?", (id,))
        employee = cursor.fetchone()
        conn.close()

        return employee
    except sqlite3.Error as e:
        flash(f'Error loading employee data: {e}', 'danger')
        return None

if __name__ == '__main__':
    app.run(debug=True)
