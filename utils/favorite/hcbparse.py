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
import hcbdecode


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


def main():
    if len(sys.argv) != 3:
        print("usage: python3 hcbparse.py output.txt input.hcb")
        return

    with open(sys.argv[1], "w", encoding="utf-8") as out_file:
        with open(sys.argv[2], "rb") as hcb_file:
            dec = hcbdecode.HcbDecoder(hcb_file)
            
            for offset, names in read_char_subroutines(dec):
                out_file.write("{0:08x}\n".format(offset))
                for name in names:
                    out_file.write("  {0}\n".format(name))


if __name__ == "__main__":
    main()
