# FAVORITE utility scripts

Scripts for games built using
[FAVORITE](http://www.favo.co.jp/soft/main.htm)'s FVP game engine.

### hcbdecode.py

Usage: `hcbdecode.py output.txt input.hcb`

Disassembles the binary instructions in the HCB file into a
human readable form.

### hcbparse.py

Usage: `hcbparse.py output.txt input.hcb`

Gets a list of characters and their corresponding set text
function addresses. Use this to fill the `character_list`
entry in the HCB info files.

### hcbtext.py

Usage: `hcbtext.py output.txt input.hcb info.py`

Gets all character/narrator text in the HCB file.
Requires a HCB info script (see the `hcbinfo` directory).

### hcb2db.py

Usage: `hcb2db.py output.db input.hcb info.py`

Adds all non-narrator quotes from the HCB file into the
database. The database file must already exist with the
correct schema; this script does not create it.

### hcb2py.py

Usage: `hcb2db.py output.py input.hcb info.py`

Similar to `hcb2db.py`, but instead of adding the lines
into a database, it creates a Python script containing
the lines instead. This can be imported into 