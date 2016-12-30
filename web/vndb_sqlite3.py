import sqlite3
import vntypes


# Path to the database file
db_path = None


def initialize(**kwargs):
    global db_path
    db_path = kwargs["db_path"]


def get_database(g):
    return getattr(g, "_database", None)


def on_connection_start(g):
    db = get_database(g)
    if db is None:
        g._database = sqlite3.connect(db_path)


def on_connection_end(g):
    db = get_database(g)
    if db is not None:
        db.close()
        g._database = None


def sql_add_where(has_where, clause):
    if has_where:
        return " AND " + clause
    else:
        return " WHERE " + clause


def sql_build_in(int_list):
    return "({0})".format(",".join(map(str, int_list)))


def get_all_novels(g, novel_id=None, character_id=None, name=None, include_chars=True):
    novel_query = """
        SELECT
            novels.vndb_id, novels.name
        FROM novel_characters
        JOIN novels ON
            novel_characters.novel_id = novels.vndb_id
    """
    params = []
    has_where = False
    if novel_id is not None:
        novel_query += sql_add_where(has_where, "novels.vndb_id = ?")
        params.append(novel_id)
        has_where = True
    if character_id is not None:
        novel_query += sql_add_where(has_where, "novel_characters.character_id = ?")
        params.append(character_id)
        has_where = True
    if name is not None:
        novel_query += sql_add_where(has_where, "novels.name = ?")
        params.append(name)
        has_where = True

    novels = {}
    for row in get_database(g).execute(novel_query, params):
        if not row[0] in novels:
            novels[row[0]] = vntypes.Novel(row[0], row[1])
    novel_list = sorted(novels.values(), key=lambda n: n.vndb_id)

    if include_chars:
        for novel in novel_list:
            novel.characters = get_all_characters(g, novel_id=novel.vndb_id, include_novels=False)
    return novel_list


def get_novel(g, novel_id):
    try:
        return get_all_novels(g, novel_id=novel_id)[0]
    except IndexError:
        return None


def get_all_characters(g, character_id=None, novel_id=None, name=None, include_novels=True):
    char_query = """
        SELECT
            characters.vndb_id, characters.name
        FROM novel_characters
        JOIN characters ON
            novel_characters.character_id = characters.vndb_id
    """
    params = []
    has_where = False
    if character_id is not None:
        char_query += sql_add_where(has_where, "characters.vndb_id = ?")
        params.append(character_id)
        has_where = True
    if novel_id is not None:
        char_query += sql_add_where(has_where, "novel_characters.novel_id = ?")
        params.append(novel_id)
        has_where = True
    if name is not None:
        char_query += sql_add_where(has_where, "characters.name = ?")
        params.append(name)
        has_where = True

    chars = {}
    for row in get_database(g).execute(char_query, params):
        if not row[0] in chars:
            chars[row[0]] = vntypes.Character(row[0], row[1])
    char_list = sorted(chars.values(), key=lambda c: c.vndb_id)

    if include_novels:
        for char in char_list:
            char.novels = get_all_novels(g, character_id=char.vndb_id, include_chars=False)
    return char_list


def get_character(g, character_id):
    try:
        return get_all_characters(g, character_id=character_id)[0]
    except IndexError:
        return None


def get_random_quote(g, novel_ids=None, character_ids=None, contains=None):
    query = """
        SELECT
            novels.vndb_id, novels.name,
            characters.vndb_id, characters.name, quotes.text
        FROM quotes
        JOIN novels ON
            quotes.novel_id = novels.vndb_id
        JOIN characters ON
            quotes.character_id = characters.vndb_id
    """
    params = []
    has_where = False
    if novel_ids is not None:
        query += sql_add_where(has_where, "novels.vndb_id IN " + sql_build_in(novel_ids))
        has_where = True
    if character_ids is not None:
        query += sql_add_where(has_where, "characters.vndb_id IN " + sql_build_in(character_ids))
        has_where = True
    if contains is not None:
        query += sql_add_where(has_where, "quotes.text LIKE '%' || ? || '%'")
        params.append(contains)
        has_where = True
    query += " ORDER BY RANDOM() LIMIT 1"
    row = get_database(g).execute(query, params).fetchone()
    if row is None:
        return None
    novel = vntypes.Novel(row[0], row[1])
    character = vntypes.Character(row[2], row[3])
    quote = vntypes.Quote(novel, character, row[4])
    return quote
