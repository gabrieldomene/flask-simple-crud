from flask import ( Flask, request )
import sqlite3

def create_conn(db):
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)

    return conn

def update_student(conn, new_name, state, cpf):
    c = conn.cursor()
    c.execute("""UPDATE students SET name=?, state=? WHERE cpf=?""", (new_name, state, cpf))
    conn.commit()

def create_student(conn, student):
    c = conn.cursor()
    sql = """INSERT INTO students VALUES (?, ?, ?)"""
    c.execute(sql, student)
    conn.commit()

def delete_student(conn, cpf):
    c = conn.cursor()
    c.execute("""DELETE FROM students WHERE cpf=?""", (cpf, ))
    conn.commit()

app = Flask(__name__)

@app.route('/')
def index():
    return """/list - List all
/create?name=abc&cpf=123&state=ab - Create a student (name, cpf, state)
/delete?cpf=123 - Delete a student with cpf
/update?cpf=123&name=new_name&state=new_state - Update a student with cpf
    """

@app.route("/list/", defaults={"uf": None})
@app.route('/list/<uf>', methods=['GET'])
def listar(uf):
    conn = create_conn('./database/database.db')
    c = conn.cursor()
    data = {}
    if uf != None:
        symbol = (uf.upper(), )
        for idx, row in enumerate(c.execute('SELECT * FROM students WHERE state == "%s"' % symbol)):
            data.update({idx: {'name': row[0], 'cpf': row[1], 'state': row[2]}})
    else:
        for idx, row in enumerate(c.execute('SELECT * FROM students')):
            data.update({idx: {'name': row[0], 'cpf': row[1], 'state': row[2]}})
    conn.close()
    return data

@app.route('/create', methods=['POST'])
def create():
    conn = create_conn('./database/database.db')
    data = request.get_json()

    name = data['name'].capitalize()
    cpf = data['cpf']
    state = data['state'].upper()

    create_student(conn, student)
    conn.close()

    return data

@app.route('/update', methods=['PUT'])
def update():
    conn = create_conn('./database/database.db')
    data = request.get_json()

    new_name = data['name'].capitalize()
    cpf = data['cpf']
    new_state = data['state'].upper()

    update_student(conn, new_name, new_state, cpf)
    conn.close()

    return data

@app.route('/delete', methods=['DELETE'])
def delete():
    conn = create_conn('./database/database.db')
    data = request.get_json()

    cpf = data['cpf']
    print(type(cpf))
    delete_student(conn, cpf)
    conn.close()

    return data


if __name__ == '__main__':
    app.run(debug=True)


