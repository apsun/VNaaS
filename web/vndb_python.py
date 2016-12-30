import itertools
import random
import sys
import vntypes


# List of quote objects
quotes = []

# Map of character ID -> character object
characters = {}

# Map of novel ID -> novel object
novels = {}


def ifilter(pred, it):
    if sys.version_info[0] < 3:
        return itertools.ifilter(pred, it)
    else:
        return filter(pred, it)


def iteritems(d):
    if sys.version_info[0] < 3:
        return d.iteritems()
    else:
        return d.items()


def itervalues(d):
    if sys.version_info[0] < 3:
        return d.itervalues()
    else:
        return d.values()


def iterkeys(d):
    if sys.version_info[0] < 3:
        return d.iterkeys()
    else:
        return d.keys()


def initialize(**kwargs):
    global quotes
    global characters
    global novels

    file_dir = kwargs["file_dir"]
    file_list = kwargs["file_list"]
    for f in file_list:
        # Read the file into memory
        mod = getattr(__import__(file_dir + "." + f, {}, {}, [], 0), f)
        novel_id = mod.vndb_id
        novel_name = mod.name
        novel_characters = mod.characters
        novel_quotes = mod.quotes

        # Create novel object
        novel = vntypes.Novel(novel_id, novel_name, [])
        novels[novel_id] = novel

        # Add novel to all character objects
        for char_id, char_name in iteritems(novel_characters):
            if char_id not in characters:
                characters[char_id] = vntypes.Character(char_id, char_name, [])
            characters[char_id].novels.append(novel)
            novel.characters.append(characters[char_id])

        # Add quotes
        for char_id, char_quote_list in iteritems(novel_quotes):
            for char_quote in char_quote_list:
                quotes.append(vntypes.Quote(novel, characters[char_id], char_quote))


def on_connection_start(g):
    pass


def on_connection_end(g):
    pass


def novel_has_character(novel, character_id):
    for c in novel.characters:
        if c.vndb_id == character_id:
            return True
    return False


def character_has_novel(character, novel_id):
    for n in character.novels:
        if n.vndb_id == novel_id:
            return True
    return False


def get_all_novels(g, novel_id=None, character_id=None, name=None, include_chars=True):
    ret = []
    for n in itervalues(novels):
        if novel_id is not None and n.vndb_id != novel_id:
            continue
        if name is not None and n.name != name:
            continue
        if character_id is not None and not novel_has_character(n, character_id):
            continue
        nobj = vntypes.Novel(n.vndb_id, n.name, None)
        if include_chars:
            nobj.characters = get_all_characters(g, novel_id=n.vndb_id, include_novels=False)
        ret.append(nobj)
    ret.sort(key=lambda n: n.vndb_id)
    return ret


def get_novel(g, novel_id):
    try:
        return get_all_novels(g, novel_id=novel_id)[0]
    except IndexError:
        return None


def get_all_characters(g, character_id=None, novel_id=None, name=None, include_novels=True):
    ret = []
    for c in itervalues(characters):
        if character_id is not None and c.vndb_id != character_id:
            continue
        if name is not None and c.name != name:
            continue
        if novel_id is not None and not character_has_novel(c, novel_id):
            continue
        cobj = vntypes.Character(c.vndb_id, c.name, None)
        if include_novels:
            cobj.novels = get_all_novels(g, character_id=c.vndb_id, include_chars=False)
        ret.append(cobj)
    ret.sort(key=lambda c: c.vndb_id)
    return ret


def get_character(g, character_id):
    try:
        return get_all_characters(g, character_id=character_id)[0]
    except IndexError:
        return None


def get_random_quote(g, novel_ids=None, character_ids=None, contains=None):
    qs = quotes
    if novel_ids is not None:
        qs = ifilter(lambda q: q.novel.vndb_id in novel_ids, qs)
    if character_ids is not None:
        qs = ifilter(lambda q: q.character.vndb_id in character_ids, qs)
    if contains is not None:
        qs = ifilter(lambda q: contains in q.text, qs)
    if not isinstance(qs, list):
        qs = list(qs)

    try:
        q = random.choice(qs)
    except IndexError:
        return None

    nobj = vntypes.Novel(q.novel.vndb_id, q.novel.name)
    cobj = vntypes.Character(q.character.vndb_id, q.character.name)
    qobj = vntypes.Quote(nobj, cobj, q.text)
    return qobj
