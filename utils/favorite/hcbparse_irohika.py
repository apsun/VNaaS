#!/usr/bin/env python3

import sys
import hcbparse


# Address of the (supposed) SetText() function
SET_TEXT_ADDR = 0x41138


# Where to begin parsing strings as character lines
# v1.1 entry point
ENTRY_POINT = 0x83526


# Character definitions
CHARACTER_LIST = [
    hcbparse.Character(1,  0x0004, "真紅"),
    hcbparse.Character(2,  0x019a, "加奈"),
    hcbparse.Character(3,  0x03d5, "澪"),
    hcbparse.Character(4,  0x05a8, "鏡"),
    hcbparse.Character(5,  0x06e8, "つかさ"),
    hcbparse.Character(6,  0x087e, "藍"),
    hcbparse.Character(7,  0x0904, "蓮"),
    hcbparse.Character(8,  0x0a17, "白"),
    hcbparse.Character(9,  0x0b2a, "鈴"),
    hcbparse.Character(10, 0x0d29, "あゆむ"),
    hcbparse.Character(11, 0x0eec, "時雨"),
    hcbparse.Character(12, 0x0fc4, "とおる"),
    hcbparse.Character(13, 0x114d, "蓮也"),
    hcbparse.Character(14, 0x1260, "青空"),
    hcbparse.Character(15, 0x13db, "さやか"),
    hcbparse.Character(16, 0x14ee, "静"),
    hcbparse.Character(17, 0x1ca1, "ユウマ"),
    hcbparse.Character(18, 0x1dd4, "悠馬"),
]


def main():
    if len(sys.argv) != 3:
        print("usage: python3 hcbparse_irohika.py Hikari.hcb output.txt")
        return

    with open(sys.argv[2], "w", encoding="utf-8") as out_file:
        with open(sys.argv[1], "rb") as hcb_file:
            hcbparse.parse_lines(CHARACTER_LIST, SET_TEXT_ADDR, ENTRY_POINT, hcb_file, out_file)


if __name__ == "__main__":
    main()
