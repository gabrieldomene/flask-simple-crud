from flask import ( Flask, request, redirect, url_for, render_template )
import sqlite3

class database:
    def __init__(self, name):
        self.name = name
    
    def connect(self):
        conn = None
        try:
            conn = sqlite3.connect(self.name)
            return conn
        except Error as e:
            print(e)

db = database('./database/database.db')

def update_student(conn, new_name, state, cpf):
    c = conn.cursor()
    match = c.execute("""SELECT EXISTS(SELECT 1 FROM students WHERE cpf=?)""", (cpf, ))
    if bool(match.fetchone()[0]):
        c.execute("""UPDATE students SET name=?, state=? WHERE cpf=?""", (new_name, state, cpf))
        conn.commit()

def create_student(conn, name, cpf, state):
    c = conn.cursor()
    c.execute("""INSERT INTO students VALUES(?, ?, ?)""", (name, cpf, state))
    conn.commit()

def delete_student(conn, cpf):
    c = conn.cursor()
    c.execute("""DELETE FROM students WHERE cpf=?""", (cpf, ))
    conn.commit()

def list_students(conn, uf):
    c = conn.cursor()
    data = {}
    if uf != None:
        symbol = (uf.upper(), )
        for idx, row in enumerate(c.execute('SELECT * FROM students WHERE state == "%s"' % symbol)):
            data.update({idx: {'name': row[0], 'cpf': row[1], 'state': row[2]}})
    else:
        for idx, row in enumerate(c.execute('SELECT * FROM students')):
            data.update({idx: {'name': row[0], 'cpf': row[1], 'state': row[2]}})
    return data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('./index.html'), 300

@app.route("/list/", defaults={"uf": None})
@app.route('/list/<uf>', methods=['GET'])
def listar(uf):
    conn = db.connect()
    data = list_students(conn, uf)
    conn.close()
    return data, 200

@app.route('/create', methods=['POST'])
def create():
    data = request.get_json()

    name = data['name'].capitalize()
    cpf = data['cpf']
    state = data['state'].upper()
    
    for key in data:
        if data[key] == '':
            return data, 404

    conn = db.connect()
    try:
        create_student(conn, name, cpf, state)
    except sqlite3.IntegrityError as err:
        return 'CPF already in DB', 409
    conn.close()

    return data, 201

@app.route('/update', methods=['PUT'])
def update():
    data = request.get_json()

    new_name = data['name'].capitalize()
    cpf = data['cpf']
    new_state = data['state'].upper()
    
    for key in data:
        if data[key] == '':
            return data, 404

    conn = db.connect()
    update_student(conn, new_name, new_state, cpf)
    conn.close()

    return data, 204

@app.route('/delete', methods=['DELETE'])
def delete():
    data = request.get_json()

    cpf = data['cpf']
    conn = db.connect()
    delete_student(conn, cpf)
    conn.close()

    return data, 200

@app.errorhandler(404)
def page_not_foun(e):
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)