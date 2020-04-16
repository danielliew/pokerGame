import sqlite3

# set sql file path
sqlfilepath = '/Users/daniel/Desktop/code/PokerGame/testing/useraccounts.db'

# initialise or verify there is a SQL file to store Accounts
def initSQL():
    try:
        f = open(sqlfilepath,'r')
        f.close()
        print('2. useraccounts.db file exists.')
    except FileNotFoundError:
        host = sqlite3.connect(sqlfilepath)
        cursor = host.cursor()
        initCommands =  '''
                        CREATE TABLE Accounts(id INTEGER PRIMARY KEY, name TEXT,
                        username TEXT, password TEXT, balance FLOAT)
                        '''
        cursor.execute(initCommands)
        host.commit()
        host.close()
        print('1. useraccounts.db file created.')

initSQL()
initSQL()
