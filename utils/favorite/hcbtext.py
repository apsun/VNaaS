#!/usr/bin/env python3
import sys
import hcbdecode
import hcbparse


MIN_TEXT_LEN = 6
IGNORED_CHARS = ["\u2026", "\u2500", "\uFF01", "\uFF1F", "\u3002"]


class Character:
    def __init__(self, vndb_id, sub_offset, name):
        self.vndb_id = vndb_id
        self.sub_offset = sub_offset
        self.name = name


class Line:
    def __init__(self, char_vndb_id, char_name, pushstr_offset, text):
        self.char_vndb_id = char_vndb_id
        self.char_name = char_name
        self.pushstr_offset = pushstr_offset
        self.text = text


# This is really hacky, but it's the only solution other than actually
# executing the instructions in a virtual machine and counting the
# stack pointer.
def read_lines(char_list, set_text_addr, entry_point, dec, skip_short=False):
    dec.seek_to_offset(entry_point)
    last_char = None
    last_text = None
    pushstr_offset = None
    addr_to_char_map = {x.sub_offset: x for x in char_list}
    for op in dec.read_ops():
        if op.opname == "call" and op.operands[0] in addr_to_char_map:
            last_char = addr_to_char_map[op.operands[0]]
        elif op.opname == "pushstr":
            last_text = op.operands[0]
            pushstr_offset = op.offset
        elif op.opname == "call" and op.operands[0] == set_text_addr:
            if not last_text:
                continue

            char_vndb_id = 0
            char_name = None
            if last_char:
                char_vndb_id = last_char.vndb_id
                char_name = last_char.name
            line = Line(char_vndb_id, char_name, pushstr_offset, last_text)
            last_char = None
            last_text = None
            pushstr_offset = None

            if skip_short:
                trimmed = line.text
                for c in IGNORED_CHARS:
                    trimmed = trimmed.replace(c, "")
                if len(trimmed) < MIN_TEXT_LEN:
                    continue

            yield line


def main():
    if len(sys.argv) != 4:
        print("usage: python3 hcbparse.py output.txt input.hcb info.py")
        return

    with open(sys.argv[1], "w", encoding="utf-8") as out_file:
        with open(sys.argv[2], "rb") as hcb_file:
            dec = hcbdecode.HcbDecoder(hcb_file)
            
            script_module = {}
            with open(sys.argv[3], encoding="utf-8") as script:
                exec(script.read(), script_module)

            char_list = [Character(*c) for c in script_module["character_list"]]
            set_text_addr = script_module["set_text_offset"]
            entry_point = script_module["entry_point"]
            for line in read_lines(char_list, set_text_addr, entry_point, dec):
                out_file.write("{0}\t\t{1}\n".format(line.char_name or "---", line.text))


if __name__ == "__main__":
    main()
