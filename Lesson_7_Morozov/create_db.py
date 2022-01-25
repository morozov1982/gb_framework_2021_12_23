from sqlite3 import connect

connect_ = connect('db.sqlite')
cursor_ = connect_.cursor()
with open('create_db.sql') as f:
    text = f.read()
cursor_.executescript(text)
cursor_.close()
connect_.close()
