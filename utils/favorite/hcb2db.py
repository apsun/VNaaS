#!/usr/bin/env python3
import sqlite3
import sys
import hcbdecode
import hcbtext


def insert_novel(cursor, novel_vndb_id, novel_name):
    cursor.execute("INSERT INTO novels VALUES(?, ?)", (novel_vndb_id, novel_name))


def insert_chars(cursor, char_list):
    for c in char_list:
        cursor.execute("INSERT OR IGNORE INTO characters VALUES(?, ?)", (c.vndb_id, c.name))


def insert_novel_char_links(cursor, novel_vndb_id, char_list):
    for c in char_list:
        cursor.execute("INSERT INTO novel_characters VALUES(?, ?)", (novel_vndb_id, c.vndb_id))


def insert_lines(cursor, novel_vndb_id, char_list, set_text_addr, entry_point, decoder):
    for line in hcbtext.read_lines(char_list, set_text_addr, entry_point, decoder, True):
        if line.char_vndb_id == 0:
            continue
        cursor.execute("INSERT INTO quotes VALUES(?, ?, ?)", (novel_vndb_id, line.char_vndb_id, line.text))


def hcb_to_db(db_path, hcb_path, novel_vndb_id, novel_name, char_list, set_text_addr, entry_point):
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    with open(hcb_path, "rb") as hcb_file:
        dec = hcbdecode.HcbDecoder(hcb_file)
        insert_novel(cursor, novel_vndb_id, novel_name)
        insert_chars(cursor, char_list)
        insert_novel_char_links(cursor, novel_vndb_id, char_list)
        insert_lines(cursor, novel_vndb_id, char_list, set_text_addr, entry_point, dec)
    db.commit()
    cursor.close()
    db.close()


def main():
    if len(sys.argv) != 4:
        print("usage: hcb2db.py output.db input.hcb info.py")
        return

    db_path = sys.argv[1]
    hcb_path = sys.argv[2]
    script_path = sys.argv[3]

    script_module = {}
    with open(script_path, encoding="utf-8") as script:
        exec(script.read(), script_module)

    hcb_to_db(
        db_path, 
        hcb_path, 
        script_module["vndb_id"], 
        script_module["name"], 
        [hcbtext.Character(*c) for c in script_module["character_list"]],
        script_module["set_text_offset"],
        script_module["entry_point"])


if __name__ == "__main__":
    main()
