import sqlite3
con = sqlite3.connect('static/Films.db')
cur = con.cursor()
count = cur.execute("""SELECT position, name, date FROM Watchlater ORDER BY position""").fetchall()
con.commit()
con.rollback()
con.close()
print(count)
