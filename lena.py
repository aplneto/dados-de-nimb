'''
Esse script controla a criação e armazenamento de personagens

https://www.sqlitetutorial.net/sqlite-data-types/
https://www.sqlitetutorial.net/sqlite-create-table/
'''

import alpha.personagens
import sqlite3
import json

DB_FILE = "personagens.db"

conn = sqlite3.connect(DB_FILE)
cursos = conn.cursor()