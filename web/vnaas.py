#!/usr/bin/env python3
import json
import re
import sqlite3
import sys
import flask
import vndb
import vnjson


app = flask.Flask(__name__)
database_path = None


def ruby_to_html(s):
    return re.sub(r"\[(.+?)\|(.+?)\]", r"<ruby>\2<rp>(</rp><rt>\1</rt><rp>)</rp></ruby>", s)


def format_cite(quote):
    return "― " + quote.character.name + "、" + quote.novel.name


def to_int(value, ignore_none):
    try:
        return int(value)
    except ValueError:
        flask.abort(400)
    except TypeError:
        if ignore_none:
            return None
        flask.abort(400)


def get_db():
    db = getattr(flask.g, "_database", None)
    if db is None:
        db = flask.g._database = sqlite3.connect(database_path)
    return db


@app.teardown_appcontext
def close_connection(excpetion):
    db = getattr(flask.g, "_database", None)
    if db is not None:
        db.close()
        flask.g._database = None


@app.route("/")
def index():
    db = get_db()
    quote = vndb.get_random_quote(db)
    return flask.render_template("index.html",
        quote_text = flask.Markup(ruby_to_html(quote.text)),
        quote_cite = format_cite(quote)
    )


@app.route("/api/v1/novels")
def get_all_novels():
    db = get_db()
    character_id = flask.request.args.get("character_id")
    character_id = to_int(character_id, True)
    name = flask.request.args.get("name")
    novels = vndb.get_all_novels(db, character_id=character_id, name=name)
    return flask.Response(vnjson.dumps(novels), mimetype="application/json")


@app.route("/api/v1/novels/<novel_id>")
def get_novel(novel_id):
    novel_id = to_int(novel_id, False)
    db = get_db()
    novel = vndb.get_novel(db, novel_id)
    if novel is None:
        flask.abort(404)
    return flask.Response(vnjson.dumps(novel), mimetype="application/json")


@app.route("/api/v1/characters")
def get_all_characters():
    db = get_db()
    novel_id = flask.request.args.get("novel_id")
    novel_id = to_int(novel_id, True)
    name = flask.request.args.get("name")
    characters = vndb.get_all_characters(db, novel_id=novel_id, name=name)
    return flask.Response(vnjson.dumps(characters), mimetype="application/json")

    
@app.route("/api/v1/characters/<character_id>")
def get_character(character_id):
    character_id = to_int(character_id, False)
    db = get_db()
    character = vndb.get_character(db, character_id)
    if character is None:
        flask.abort(404)
    return flask.Response(vnjson.dumps(character), mimetype="application/json")


@app.route("/api/v1/random_quote")
def get_random_quote():
    db = get_db()
    novel_id = flask.request.args.get("novel_id")
    novel_id = to_int(novel_id, True)
    character_id = flask.request.args.get("character_id")
    character_id = to_int(character_id, True)
    contains = flask.request.args.get("contains")
    quote = vndb.get_random_quote(db, novel_id=novel_id, character_id=character_id, contains=contains)
    if quote is None:
        flask.abort(404)
    return flask.Response(vnjson.dumps(quote), mimetype="application/json")


def main():
    if len(sys.argv) not in (2, 3):
        print("usage: python3 vnaas.py database.db [port]")
        return

    global database_path
    database_path = sys.argv[1]
    if len(sys.argv) == 3:
        port = int(sys.argv[2])
        app.debug = False
    else:
        port = None
        app.debug = True
    app.run(host="0.0.0.0", port=port)


if __name__ == '__main__':
    main()
