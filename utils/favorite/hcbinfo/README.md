# HCB info files

These are required by some of the scripts to parse the raw HCB data into
a usable form. Each file should contain the following:

- `vndb_id`: The game's ID number on [VNDB.org](http://vndb.org/).

- `name`: The name of the game.

- `set_text_offset`: The address of the function responsible for setting
  the textbox contents. You can find this by first running the HCB file
  through `hcbdecode.py` to generate the disassembly, then finding some
  text in the form `pushstr <text>`. After a few other instructions, there
  should be two consecutive `call` instructions; the second one is the
  address you want.

- `entry_point`: Where to start looking for lines in the HCB file. You
  can find this by finding the very first spoken line in the disassembly,
  then going backwards until you find an `initstack 0x0, 0x0` instruction.

- `character_list`: A list of 3-tuples. The elements are as follows:

 1. ID of the character on  [VNDB.org](http://vndb.org/).

 2. Character-specific set text function address. Find this by
   running the HCB file through `hcbparse.py` without a script file.
   This generates a list of addresses with the corresponding character's
   name(s).

 3. Name of the character.
