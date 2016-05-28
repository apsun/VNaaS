import json
import vntypes


class NovelJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, vntypes.Novel):
            base = {"id": o.vndb_id, "name": o.name}
            if o.characters is not None:
                base["characters"] = [self.default(c) for c in o.characters]
            return base
        elif isinstance(o, vntypes.Character):
            base = {"id": o.vndb_id, "name": o.name}
            if o.novels is not None:
                base["novels"] = [self.default(n) for n in o.novels]
            return base
        elif isinstance(o, vntypes.Line):
            return {
                "text": o.text,
                "character": self.default(o.character),
                "novel": self.default(o.novel)
            }
        else:
            return super().default(o)


def dumps(o):
    return json.dumps(o, cls=NovelJSONEncoder)
