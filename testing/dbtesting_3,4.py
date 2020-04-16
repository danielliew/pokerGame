
import sqlite3

# set sql file path
sqlfilepath = '/Users/daniel/Desktop/code/PokerGame/testing/useraccounts.db'

name = 'bob'
username = 'bob123'
password = 'bobby'

def create(confirmed_password):
    if password == confirmed_password:
        balance = 10000
        # 10000 chips on the house
        host = sqlite3.connect(sqlfilepath)
        cursor = host.cursor()
        createCommands =  '''
                            INSERT INTO Accounts(name, username, password, balance)
                            VALUES(?,?,?,?)
                        '''
        cursor.execute(createCommands,(name, username, password, balance))
        host.commit()
        host.close()
        print('4. new record created.')
    else:
        print('3. failed to create new record as passwords did not match')

create('bobyy')
create('bobby')
