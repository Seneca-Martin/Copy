import sqlite3

database = ('data/movements.db')

def inicialVerification():
    #Comprobamos si la DB está vacía o informada
    conn = sqlite3.connect(database)
    cursor =  conn.cursor()

    query = '''
            SELECT count (*) FROM cryptos;
            '''
    cursor.execute(query)
    n=cursor.fetchone()
    conn.close()
    if n[0]==0:
        return False
    else:
        return True

def CryptosDBInformed(cryptos):
    #Guadamos las cryptos obtenidas de la API en DBcryptos
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    query='''
            INSERT into cryptos
            (symbol, name)
            values (?, ?);
           '''

    try:
        for i in range (len(cryptos)):
            rows=cursor.execute(query, (cryptos[i][0], cryptos[i][1]))
    except sqlite3.Error as e:
        print('Error en sqlite:', e)
    
    conn.commit()
    conn.close()


def listCryptosIni():
    #Entrega lista con symbol y nombre de cryptos en las que ya se ha invertido mas los Euros---------------
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    query = '''
        SELECT symbol, name
        FROM cryptos  
        WHERE cryptos.id=13;
    '''
    rows=cursor.execute(query)
    cryptosInverts=[]
    text=''

    for row in rows:
        text= '{} - {}'.format(row[0], row[1])
        cryptosInverts.append(text)
        
    conn.close()
    return cryptosInverts

def listCryptos():
    #Entrega lista con symbol y nombre de cryptos que hay en DBcryptos
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    query = '''
            SELECT symbol, name FROM cryptos ORDER BY symbol;
    '''
    rows=cursor.execute(query)
    cryptos=[]
    text=''
    for row in rows:
        text= '{} - {}'.format(row[0], row[1])
        cryptos.append(text)
    
    conn.close()
    return cryptos


def listCryptosInvert():
    #Entrega lista con symbol y nombre de cryptos en las que ya se ha invertido mas los Euros---------------
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    #query2 = '''
       # SELECT symbol, name
       # FROM cryptos  
       # WHERE cryptos.id=13;
    #'''

    query = '''
        SELECT DISTINCT symbol, name
        FROM cryptos INNER JOIN movements
        WHERE  to_currency= cryptos.id OR cryptos.id=13 ORDER BY symbol;
    '''

    rows=cursor.execute(query)
    cryptosInverts=[]
    text=''
 
    for row in rows:
        text= '{} - {}'.format(row[0], row[1])
        cryptosInverts.append(text)
 
    conn.close()
    return cryptosInverts


def printMovementsDB():
    #devuelve movimientos existentes en DB
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    rows= cursor.execute('select date, time, from_currency, from_quantity, to_currency, to_quantity from movements order by date;')

    movements = []
    for row in rows:
        row = list(row)
        movements.append(row)

    conn.close()
    return(movements) 

def addNewMovement(data, time, from_currency, to_currency,from_quantity, to_quantity):
   #añadir nuevo movimiento en DB
    conn =  sqlite3.connect(database)
    cursor = conn.cursor()

    query = '''
        INSERT INTO movements
               (date, time, from_currency, from_quantity, to_currency, to_quantity)
               values (?, ?, ?, ?, ?, ?);
            '''
    try:
        rows = cursor.execute(query, (  data,
                                        time,
                                        from_currency, 
                                        from_quantity,
                                        to_currency,
                                        to_quantity,
        ))

    except sqlite3.Error as e:
        
        print('Error en base de datos : {}'.format(e))
    
    conn.commit()
    conn.close()

def MoneySpend(crypto, isfrom=True ):
    #busca en Base de Datos y devuelve la suma de las cantidades de una misma momenda en to (isfrom=false) o en from(isfrom=true) 
    if isfrom:
        fieldSelect = 'from_quantity'
        fieldWhere = 'from_currency'
    else:
        fieldSelect = 'to_quantity'
        fieldWhere = 'to_currency'

    conn =sqlite3.connect(database)
    cursor = conn.cursor()
    
    query = '''
        SELECT  {}
        FROM movements
        WHERE {} in (   SELECT id
                        FROM cryptos
                        WHERE symbol = ?);
    '''.format(fieldSelect, fieldWhere)

    try:
        rows=cursor.execute(query,(crypto,))
        valor=0
        try:
            for row in rows:
                valor+=row[0]
        except Exception as e:
            print('es en el for',e)
            
    except Exception as e:
        print('Error en base de datos:',e)
    conn.close()
    return(valor)

def getIdFromToCryptoDB(crypto, isCrytpo = True):
    # obteniendo el symbolo por el id o al reves dependiendo de si isCrypto
    if isCrytpo:
        fieldSelect = 'id'
        fieldWhere = 'symbol'
    else:
        fieldSelect = 'symbol'
        fieldWhere = 'id'
        
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    query='''
        SELECT {}
        FROM cryptos
        WHERE {}=?;
    '''.format(fieldSelect, fieldWhere)
    cursor.execute(query,(crypto,))
    n=cursor.fetchone()
    return (n[0])
  
def symbolCrytpo():
    #obteniendo los symbol de las cryptos de la tabla
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    query='''
        SELECT symbol
        FROM cryptos;
    '''
    rows=cursor.execute(query)
    symbol = []
    for row in rows:
        symbol.append(row[0])
    return (symbol)



