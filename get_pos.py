import sqlite3


def get_pos(word):
    con = sqlite3.connect("pos.sqlite")
    cur = con.cursor()
    cur.execute(f"SELECT def FROM word_pos WHERE word=?",(word,))
    pos = cur.fetchall()[0][0]
    if not pos:
        return None
    return pos




if __name__ == "__main__":
    pos = get_pos("ཀ་ཡེ་")
    print(pos)