#!/usr/bin/env python3
import sys
import hcbdecode
import hcbtext


def get_line_map(char_list, set_text_addr, entry_point, decoder):
    quotes = {}
    for line in hcbtext.read_lines(char_list, set_text_addr, entry_point, decoder, True):
        if line.char_vndb_id == 0:
            continue
        try:
            cq = quotes[line.char_vndb_id]
        except KeyError:
            cq = quotes[line.char_vndb_id] = []
        cq.append(line.text)
    return quotes


def hcb_to_py(output_path, hcb_path, novel_vndb_id, novel_name, char_list, set_text_addr, entry_point):
    with open(hcb_path, "rb") as hcb_file:
        dec = hcbdecode.HcbDecoder(hcb_file)
        quotes = get_line_map(char_list, set_text_addr, entry_point, dec)
        char_map = {c.vndb_id: c.name for c in char_list}
    with open(output_path, "w", encoding="utf-8") as out_file:
        out_file.write("# -*- coding: utf-8 -*-\n")
        out_file.write("# Generated with hcb2py\n")
        out_file.write("# Statistics:\n")
        for char_id, quote_list in quotes.items():
            out_file.write("#   ")
            out_file.write(char_map[char_id])
            out_file.write(" -> ")
            out_file.write(str(len(quote_list)))
            out_file.write(" quotes\n")
        out_file.write("from __future__ import unicode_literals\n")
        out_file.write("vndb_id = ")
        out_file.write(repr(novel_vndb_id))
        out_file.write("\n")
        out_file.write("name = ")
        out_file.write(repr(novel_name))
        out_file.write("\n")
        out_file.write("characters = ")
        out_file.write(repr(char_map))
        out_file.write("\n")
        out_file.write("quotes = ")
        out_file.write(repr(quotes))
        out_file.write("\n")


def main():
    if len(sys.argv) != 4:
        print("usage: hcb2db.py output.py input.hcb info.py")
        return

    output_path = sys.argv[1]
    hcb_path = sys.argv[2]
    script_path = sys.argv[3]

    script_module = {}
    with open(script_path, encoding="utf-8") as script:
        exec(script.read(), script_module)

    hcb_to_py(
        output_path, 
        hcb_path, 
        script_module["vndb_id"], 
        script_module["name"], 
        [hcbtext.Character(*c) for c in script_module["character_list"]],
        script_module["set_text_offset"],
        script_module["entry_point"])


if __name__ == "__main__":
    main()
