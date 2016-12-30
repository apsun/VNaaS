#!/usr/bin/env python
from __future__ import unicode_literals
import re
import flask
import vnjson
import vntypes


# Initialize data source backend
vndb = __import__("vndb_python")
vndb.initialize(
    file_dir="data",
    file_list=[
        "hoshimemo",
        "eternalheart",
        "iroseka",
        "irohika",
        "akaihitomi",
        "astralair",
    ]
)

# vndb = __import__("vndb_sqlite3")
# vndb.initialize(db_path=r"data/vnaas.db")


# This is our WSGI app
app = flask.Flask(__name__)


def ruby_to_html(s):
    return re.sub(r"\[(.+?)\|(.+?)\]", r"<ruby>\2<rp>(</rp><rt>\1</rt><rp>)</rp></ruby>", s)


def format_cite(quote):
    return "\u2015 " + quote.character.name + "\u3001" + quote.novel.name


def to_int(value, ignore_none):
    try:
        return int(value)
    except ValueError:
        flask.abort(400)
    except TypeError:
        if ignore_none:
            return None
        flask.abort(400)


def to_int_list(value):
    if value is None:
        return None
    value_list = value.split(",")
    try:
        return [int(x) for x in value_list]
    except ValueError:
        flask.abort(400)


def get_g():
    vndb.on_connection_start(flask.g)
    return flask.g


@app.teardown_appcontext
def close_connection(exception):
    vndb.on_connection_end(flask.g)


@app.route("/")
def index():
    g = get_g()
    quote = vndb.get_random_quote(g)
    return flask.render_template("index.html",
        quote_text=flask.Markup(ruby_to_html(quote.text)),
        quote_cite=format_cite(quote)
    )


@app.route("/novels")
def novels():
    g = get_g()
    character_id = flask.request.args.get("character_id")
    character_id = to_int(character_id, True)
    character = None
    if character_id is not None:
        character = vndb.get_character(g, character_id=character_id)
        if character is None:
            flask.abort(404)
    novel_list = vndb.get_all_novels(g, character_id=character_id)
    return flask.render_template("novels.html",
        novel_list=novel_list,
        character=character
    )


@app.route("/characters")
def characters():
    g = get_g()
    novel_id = flask.request.args.get("novel_id")
    novel_id = to_int(novel_id, True)
    novel = None
    if novel_id is not None:
        novel = vndb.get_novel(g, novel_id=novel_id)
        if novel is None:
            flask.abort(404)
    character_list = vndb.get_all_characters(g, novel_id=novel_id)
    return flask.render_template("characters.html",
        character_list=character_list,
        novel=novel
    )


@app.route("/api/v1/novels")
def get_all_novels():
    g = get_g()
    character_id = flask.request.args.get("character_id")
    character_id = to_int(character_id, True)
    name = flask.request.args.get("name")
    novels = vndb.get_all_novels(g, character_id=character_id, name=name)
    return flask.Response(vnjson.dumps(novels), mimetype="application/json")


@app.route("/api/v1/novels/<novel_id>")
def get_novel(novel_id):
    g = get_g()
    novel_id = to_int(novel_id, False)
    novel = vndb.get_novel(g, novel_id)
    if novel is None:
        flask.abort(404)
    return flask.Response(vnjson.dumps(novel), mimetype="application/json")


@app.route("/api/v1/characters")
def get_all_characters():
    g = get_g()
    novel_id = flask.request.args.get("novel_id")
    novel_id = to_int(novel_id, True)
    name = flask.request.args.get("name")
    characters = vndb.get_all_characters(g, novel_id=novel_id, name=name)
    return flask.Response(vnjson.dumps(characters), mimetype="application/json")


@app.route("/api/v1/characters/<character_id>")
def get_character(character_id):
    g = get_g()
    character_id = to_int(character_id, False)
    character = vndb.get_character(g, character_id)
    if character is None:
        flask.abort(404)
    return flask.Response(vnjson.dumps(character), mimetype="application/json")


@app.route("/api/v1/random_quote")
def get_random_quote():
    g = get_g()
    novel_ids = flask.request.args.get("novel_ids", flask.request.args.get("novel_id"))
    novel_ids = to_int_list(novel_ids)
    character_ids = flask.request.args.get("character_ids", flask.request.args.get("character_id"))
    character_ids = to_int_list(character_ids)
    contains = flask.request.args.get("contains")
    quote = vndb.get_random_quote(g, novel_ids=novel_ids, character_ids=character_ids, contains=contains)
    if quote is None:
        flask.abort(404)
    return flask.Response(vnjson.dumps(quote), mimetype="application/json")


def main():
    app.debug = True
    app.run(host="0.0.0.0", port=None)


if __name__ == '__main__':
    main()
