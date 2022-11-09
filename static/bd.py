import sqlite3
con = sqlite3.connect('Films.db')
cur = con.cursor()
with open('bd.txt', encoding='utf8') as line, open('out.txt', 'w', encoding='utf8') as lene:
    a = line.readlines()
    n = 0
    for i in range(len(a)):
        f = a[i].strip()
        if f[0] == '#':
            n += 1
            count = [n, f.split('. ')[1].split(' (')[0], '', 'фильм', '', '', '', '', '']
            count[2] = f[f.index('(')+1:f.index('(')+5]
            if f[-2] != '.':
                count[3] = f[f.index('(')+10:f.index(')')]
        elif f.split()[0] == 'Производство:':
            count[4] = f.split(' ')[1]
        elif f.split()[0] == 'Жанры:':
            if f.split(' ')[1][-1] != ',':
                count[5] = f.split(' ')[1]
            else:
                count[5] = f.split(' ')[1][:-1]
        elif f.split()[0] in ('Первый релиз:', 'бюджет:', 'В ролях:'):
            count[6] += f
            count[6] += '\n'
        elif f.split()[0] == 'Синопсис:':
            count[6] += a[i+1].strip()
            count[6] += '\n'
        try:
            count[7] = str(float(f))
            print(tuple(count))
            cur.execute("""INSERT INTO Main (id, name, year, type, country, genre, discription, rate, img)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", tuple(count)).fetchall()
            con.commit()
        except Exception:
            pass
con.close()
