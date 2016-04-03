#!/usr/bin/env python3
#
# Each line follows this pattern:
#   Set<Character>(voiceID)
#   SetText(text)
#
# There is one Set<Character>() subroutine per character.
# The name to display (??? vs known) is determined by
# a global variable which is read inside Set<Character>().
# For MC lines, no voiceID is passed.
# For narrator lines, Set<Character>() is not called.
# The "current character" does not persist after SetText().

import sys
from . import hcbdecode


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


# Takes advantage of the fact that the Set<Character>() subroutines
# are at the start of the file, and always have initstack(3, 0) or
# (5, 0) in their prologue.
def read_char_subroutines(dec):
    initstack_offset = None
    current_char_names = None
    for op in dec.read_ops():
        if op.opname == "initstack" and op.operands in [(3, 0), (5, 0)]:
            if current_char_names:
                yield (initstack_offset, current_char_names)
            current_char_names = []
            initstack_offset = op.offset
        elif op.opname == "initstack":
            if current_char_names:
                yield (initstack_offset, current_char_names)
            break
        elif op.opname == "pushstr":
            current_char_names.append(op.operands[0])


# This is really hacky, but it's the only solution other than actually
# executing the instructions in a virtual machine and counting the
# stack pointer.
def read_lines(char_list, set_text_addr, entry_point, dec):
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
            yield line


def main():
    if len(sys.argv) not in (3, 4):
        print("usage: python3 hcbparse.py input.hcb output.txt [script.py]")
        return

    with open(sys.argv[2], "w", encoding="utf-8") as out_file:
        with open(sys.argv[1], "rb") as hcb_file:
            dec = hcbdecode.HcbDecoder(hcb_file)
            
            out_file.write("========= CHARACTER SUBROUTINES ========\n")
            for offset, names in read_char_subroutines(dec):
                out_file.write("{0:08x}\n".format(offset))
                for name in names:
                    out_file.write("  {0}\n".format(name))

            if len(sys.argv) == 3:
                return

            out_file.write("\n============ CHARACTER LINES ===========\n")
            script_path = sys.argv[3]

            script_module = {}
            with open(script_path, encoding="utf-8") as script:
                exec(script.read(), script_module)

            char_list = [Character(*c) for c in script_module["CHARACTER_LIST"]]
            set_text_addr = script_module["SET_TEXT_ADDR"]
            entry_point = script_module["ENTRY_POINT"]
            for line in read_lines(char_list, set_text_addr, entry_point, dec):
                    out_file.write("{0}\t\t{1}\n".format(line.char_name or "---", line.text))


if __name__ == "__main__":
    main()
