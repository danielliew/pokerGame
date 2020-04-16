
import sqlite3

# set sql file path
sqlfilepath = '/Users/daniel/Desktop/code/PokerGame/testing/useraccounts.db'

userWallet = 999
userUsername = 'bob123'

# update sql wallets
def updateSQL(exitFrom):
    # save current user progress if exited from play or gameover screen
    if exitFrom == 'play' or exitFrom == 'gameOver':
        host = sqlite3.connect(sqlfilepath)
        cursor = host.cursor()
        cursor.execute('UPDATE Accounts SET balance="{}" WHERE username="{}"'.format(userWallet, userUsername))
        cursor.execute('''
                SELECT balance FROM Accounts WHERE username=?
                ''',(userUsername,))
        updatedbalance = cursor.fetchone()
        host.commit()
        host.close()
        if updatedbalance[0] == userWallet:
            print('10. user record successfully updated.')
    else:
        print('9. no updating needed as user exited from a screen other than play/gameOver screen')

updateSQL('abc')
updateSQL('play')
