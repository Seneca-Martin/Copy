import sqlite3

database = ('data/movements.db')

conn=sqlite3.connect(database)


def createCryptos ():
    try:
        conn.execute('''CREATE TABLE cryptos (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              symbol TEXT NOT NULL,
                              name TEXT NOT NULL
                        )''')
        print("se creo la tabla cryptos")                        
    except sqlite3.OperationalError:
        print("La tabla cryptos ya existe")                    
    

def createMovements ():
    try:
        conn.execute('''CREATE TABLE movements (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              date TEXT NOT NULL,
                              timme TEXT NOT NULL,
                              from_currency INTERGER NOT NULL,
                              from_quantity REAL NOT NULL,
                              to_currency INTERGER NOT NULL,
                              to_quantity REAL NOT NULL
                        )''')
        print("se creo la tabla movements")                        
    except sqlite3.OperationalError
        print("La tabla movements ya existe")                    

createCryptos()
createMovements()
conn.close()