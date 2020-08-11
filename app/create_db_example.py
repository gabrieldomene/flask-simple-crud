import sqlite3

conn = sqlite3.connect('./database/database.db')
c = conn.cursor()
c.execute('CREATE TABLE students (name TEXT NOT NULL, cpf INTEGER unique, state TEXT NOT NULL)')
print('table created')

students_info = [
  ('Gabriel', 19291, 'SP'),
  ('Joao', 3256, 'SP'),
  ('Maria', 45875, 'PR'),
  ('Rafael', 99195, 'SP'),
  ('Juliana', 656352, 'PR'),
  ('Cesar', 65412, 'PR'),
  ('Ricardo', 98763, 'SP'),
  ('Ana', 322314, 'SP'),
  ('Bia', 301234, 'SP'),
]
c.executemany('INSERT INTO students VALUES (?, ?, ?)', students_info)
conn.commit()
conn.close()