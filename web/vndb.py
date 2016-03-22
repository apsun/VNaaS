import re
import sqlite3
import vntypes


def sql_add_where(has_where, clause):
    if has_where:
        return " AND " + clause
    else:
        return " WHERE " + clause


def get_all_novels(cursor, novel_id=None, character_id=None, name=None, include_chars=True):
    novel_query = """
        SELECT
            novels.vndb_id, novels.name
        FROM novel_characters
        JOIN novels ON
            novel_characters.novel_id = novels.vndb_id
    """
    params = []
    has_where = False
    if novel_id:
        novel_query += sql_add_where(has_where, "novels.vndb_id = ?")
        params.append(novel_id)
        has_where = True
    if character_id:
        novel_query += sql_add_where(has_where, "novel_characters.character_id = ?")
        params.append(character_id)
        has_where = True
    if name:
        novel_query += sql_add_where(has_where, "novels.name = ?")
        params.append(name)
        has_where = True

    novels = {}
    for row in cursor.execute(novel_query, params):
        if not row[0] in novels:
            novels[row[0]] = vntypes.Novel(row[0], row[1])
    novel_list = sorted(novels.values(), key=lambda n: n.vndb_id)

    if include_chars:
        for novel in novel_list:
            novel.characters = get_all_characters(cursor, novel_id=novel.vndb_id, include_novels=False)
    return novel_list


def get_novel(cursor, novel_id):
    try:
        return get_all_novels(cursor, novel_id=novel_id)[0]
    except IndexError:
        return None


def get_all_characters(cursor, character_id=None, novel_id=None, name=None, include_novels=True):
    char_query = """
        SELECT
            characters.vndb_id, characters.name
        FROM novel_characters
        JOIN characters ON
            novel_characters.character_id = characters.vndb_id
    """
    params = []
    has_where = False
    if character_id:
        char_query += sql_add_where(has_where, "characters.vndb_id = ?")
        params.append(character_id)
        has_where = True
    if novel_id:
        char_query += sql_add_where(has_where, "novel_characters.novel_id = ?")
        params.append(novel_id)
        has_where = True
    if name:
        char_query += sql_add_where(has_where, "characters.name = ?")
        params.append(name)
        has_where = True

    chars = {}
    for row in cursor.execute(char_query, params):
        if not row[0] in chars:
            chars[row[0]] = vntypes.Character(row[0], row[1])
    char_list = sorted(chars.values(), key=lambda c: c.vndb_id)

    if include_novels:
        for char in char_list:
            char.novels = get_all_novels(cursor, character_id=char.vndb_id, include_chars=False)
    return char_list


def get_character(cursor, character_id):
    try:
        return get_all_characters(cursor, character_id)[0]
    except IndexError:
        return None


def get_random_quote(cursor, novel_id=None, character_id=None, contains=None):
    query = """
        SELECT
            novels.vndb_id, novels.name,
            characters.vndb_id, characters.name, lines.line
        FROM lines
        JOIN novels ON
            lines.novel_id = novels.vndb_id
        JOIN characters ON
            lines.character_id = characters.vndb_id
    """
    params = []
    has_where = False
    if novel_id:
        query += sql_add_where(has_where, "novels.vndb_id = ?")
        params.append(novel_id)
        has_where = True
    if character_id:
        query += sql_add_where(has_where, "characters.vndb_id = ?")
        params.append(character_id)
        has_where = True
    if contains:
        query += sql_add_where(has_where, "lines.line LIKE '%' || ? || '%'")
        params.append(contains)
        has_where = True
    query += " ORDER BY RANDOM() LIMIT 1"
    row = cursor.execute(query, params).fetchone()
    if row is None:
        return None
    novel = vntypes.Novel(row[0], row[1])
    character = vntypes.Character(row[2], row[3])
    line = vntypes.Line(novel, character, row[4])
    return line
