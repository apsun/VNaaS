# VNaaS

Visual Novel as a Service, for all\* of your visual novel quote needs.

\*Precisely 0.6398%

## FAQ

### What is this?

[A demo is worth a thousand words!](http://vnaas.apsun.xyz/)

### Is there an API?

Certainly, [here's the documentation!](API.md)

### Which novels are available?

| Japanese                                 | English                                         |
|------------------------------------------|-------------------------------------------------|
| 星空のメモリア Wish upon a Shooting Star | Hoshizora no Memoria: Wish upon a Shooting Star |
| 星空のメモリア Eternal Heart             | Hoshizora no Memoria: Eternal Heart             |
| いろとりどりのセカイ                     | Irotoridori no Sekai                            |
| いろとりどりのヒカリ                     | Irotoridori no Hikari                           |
| 紅い瞳に映るセカイ                      | Akai Hitomi ni Utsuru Sekai                     |
| アストラエアの白き永遠                   | AstralAir no Shiroki Towa                       |

### What about (novel name here)?

Unfortunately, reverse engineering games is a tedious process, and I am
just a student with an unhealthy addiction for visual novels. If you
wish to see your favorite game added to the list, you can help by creating
a resource extractor module for that game (more info coming soon).

### My game has a fansub, will it be added to the database?

No, only official translations are allowed.

### What can I use this for?

Use your imagination! Examples include:

- [Quote app](https://github.com/apsun/QuoteLock)
- Browser homepage
- Twitter bot
- Email signature

### I cloned the repository, how do I run this?

You will have to generate the data yourself, but don't worry! All the tools
needed to do so are provided in the `utils` directory. For the supported games,
the steps are as follows:

1. Generate the database
    - Run `sqlite3 data.db < utils/schema.sql`
2. Populate the database
    - You will need the original .hcb files from the game!
    - Find the resource extractor script for the game in `utils/favorite/hcbinfo`
    - Run `python3 utils/favorite/hcbdecode.py data.db input.hcb path/to/extractor.py`
    - Repeat for any other games you wish to add
3. Start the web server
    - Run `python3 web/wsgi.py data.db`

### Shut up and take my donations!

Please support the developers of the games instead, they're the ones who
truly make this possible!

Of course, you may donate your time and effort instead - those are greatly
appreciated :-)

## Requirements

- Python 3
- [Flask](http://flask.pocoo.org/)
- [Tornado](http://www.tornadoweb.org/)
- [SQLite3](https://www.sqlite.org/download.html) (sqlite3 binary)

## License

All code is distributed under the [MIT License](http://opensource.org/licenses/MIT).
Everything else is strictly copyright its original owner.

## Special thanks to

[amaranthf](https://bbs.sumisora.org/read.php?tid=11010281)
