import time
#import date
import sqlite3


conn = sqlite3.connect('Users.db')
cruser = conn.cursor()

cruser.execute('SELECT Id, Name, Username, UserType,password FROM Users')
users= cruser.fetchall()

for user in users:
    print(user)
'''
cruser.execute('SELECT * FROM Users')
users= cruser.fetchall()

cruser.execute('DELETE FROM Users WHERE Id='' ')
for user in users:
    print(user)


#conn.execute("INSERT INTO Users VALUES('Administrator','admin','1','admin','Administrator','1')")
conn.commit()
conn.close()
'''
conn = sqlite3.connect('Items.db')
critems = conn.cursor()
critems.execute('SELECT * FROM Items')
items= critems.fetchall()

for item in items:
    print(item)

conn.close()



