from curses import def_prog_mode
import sqlite3
import csv
import re

from numpy import insert

def extract_db():
    con = sqlite3.connect("dic.sqlite")
    cur = con.cursor()
    with open("dic.csv","w") as f:
        writer = csv.writer(f)
        for row in cur.execute('SELECT word text,def text FROM monlamGrandDic'):
            word,desc = row     
            writer.writerow([word,desc])
    con.close()


def get_pos(word):
    con = sqlite3.connect("pos.sqlite")
    cur = con.cursor()
    cur.execute(f"SELECT def FROM word_pos WHERE word=?",(word,))
    pos = cur.fetchall()[0][0]
    if not pos:
        return None
    return pos

def extract_pos(definition):
    z = re.search("(.*)\r\n.*",definition)
    if z:
        return z.group(1)
    if not z:
        return     

def insert_val():
    con = sqlite3.connect("dic.sqlite")
    cur = con.cursor()
    rows = cur.execute(f"SELECT word,def FROM monlamGrandDic")
    for row in rows:
        yield row

def update():
    for row in insert_val():
        word,definition = row
        pos = extract_pos(definition)
        print(row)
        if not pos:
            continue    
        try:
            sqliteConnection = sqlite3.connect('test_database.db')
            cursor = sqliteConnection.cursor()
            sqlite_insert_with_param = """INSERT INTO word_pos (word,def) VALUES (?, ?);"""
            data_tuple = (word,pos)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            sqliteConnection.commit()
            cursor.close()
        except:
            print(row)            
0
def create_db():
    conn = sqlite3.connect('test_database.db') 
    c = conn.cursor()

    c.execute('''
            CREATE TABLE IF NOT EXISTS word_pos
            ([word] TEXT PRIMARY KEY, [def] TEXT)
            ''')
              
    conn.commit()

if __name__ == "__main__":
    pos = get_pos("ཀ་ཡེ་")
    print(pos)