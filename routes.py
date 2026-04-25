from flask import request, Flask, render_template , redirect
import sqlite3
app=Flask(__name__)

def get_db():
    conn=sqlite3.connect('student.db')
    return conn


@app.route('/init')
def init():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER
    )
    ''')

    conn.commit()
    conn.close()

    return "hi"

@app.route('/')
def dashboard():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM students''')
    students=cursor.fetchall()
    conn.close()
    return render_template("student.html",students=students)


@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.form
    if not data:
        return {"message": "no data found"}
    name = data['name']
    if not name:
        return {"message": "student name not found"}
    age = data['age']
    if not age:
        return {"message": "student age not found"}

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO students (name,age) VALUES (?,?)""", (name, age))

    conn.commit()
    conn.close()
    return redirect("/")
@app.route('/add')
def add_page():
    return render_template("add.html")


@app.route('/students', methods=['GET'])
def students():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM students''')
    rows = cursor.fetchall()

    conn.close()

    students = []
    for row in rows:
        students.append({
            'id': row[0],
            'name': row[1],
            'age': row[2]
        })
    return {"status":"success",
            "students": students},200


@app.route('/student/<int:id>', methods=['GET'])
def get_student(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM students WHERE id = ?''', (id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        student = {
            'id': row[0],
            'name': row[1],
            'age': row[2]
        }
        return {"status":"success",
                "data":student},200
    else:
        return {"status":"error","message": "student not found"},404


@app.route('/edit/<int:id>')
def edit_student(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM students WHERE id = ?''', (id,))
    student = cursor.fetchone()
    conn.close()
    return render_template("edit.html",student=student)

@app.route('/update/<int:id>', methods=['POST'])
def get_update(id):
    data = request.form
    if not data :
        return {"message": "no data found"}

    name = data['name']
    if not name:
        return {"message": "student name not found"}
    age = data['age']
    if not age:
        return {"message": "student age not found"}

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''UPDATE students SET name = ?, age = ? WHERE id = ?''', (name, age, id))

    conn.commit()
    conn.close()

    return redirect("/")

@app.route('/delete/<int:id>', methods=['GET','POST'])
def delete_student(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM students WHERE id = ?''', (id,))
    conn.commit()
    conn.close()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)


