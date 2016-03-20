class Novel:
    def __init__(self, vndb_id, name, characters=None):
        self.vndb_id = vndb_id
        self.name = name
        self.characters = characters


class Character:
    def __init__(self, vndb_id, name, novels=None):
        self.vndb_id = vndb_id
        self.name = name
        self.novels = novels


class Line:
    def __init__(self, id, novel, character, text):
        self.id = id
        self.novel = novel
        self.character = character
        self.text = text
