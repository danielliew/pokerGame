
import sqlite3

# set sql file path
sqlfilepath = '/Users/daniel/Desktop/code/PokerGame/testing/useraccounts.db'

def checkLoginDetails(username, user_entered_password):
    found = False
    host = sqlite3.connect(sqlfilepath)
    cursor = host.cursor()
    cursor.execute('''
            SELECT balance, password FROM Accounts WHERE username=?
            ''',(username,))
    user = cursor.fetchone()
    host.commit()
    host.close()
    if user != None:
        password = user[1]
        if user_entered_password == password:
            found = True
            balance = user[0]
    return found

checked = checkLoginDetails('bob123', 'boby')
if not checked:
    print('5. incorrect password hence login denied')

checked = checkLoginDetails('bob124', 'bobby')
if not checked:
    print('6. incorrect username hence login denied')

checked = checkLoginDetails('bob124', 'boby')
if not checked:
    print('7. incorrect username and password hence login denied')

checked = checkLoginDetails('bob123', 'bobby')
if checked:
    print('8. login success')
