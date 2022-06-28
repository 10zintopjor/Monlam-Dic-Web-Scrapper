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
    with open("./alt.csv") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            word1,word2 = row
            try:
                sqliteConnection = sqlite3.connect('alternatives.db')
                cursor = sqliteConnection.cursor()
                sqlite_insert_with_param = """INSERT INTO alt_word (word1,word2) VALUES (?, ?);"""
                data_tuple = (word1,word2)
                cursor.execute(sqlite_insert_with_param, data_tuple)
                sqliteConnection.commit()
                cursor.close()
            except:
                pass

def create_db():
    conn = sqlite3.connect('alternatives.db') 
    c = conn.cursor()

    c.execute('''
            CREATE TABLE IF NOT EXISTS alt_word
            ([word1] TEXT PRIMARY KEY, [word2] TEXT)
            ''')
              
    conn.commit()

if __name__ == "__main__":
    create_db()
    update()
    """ pos = get_pos("ཀ་ཡེ་")
    print(pos) """