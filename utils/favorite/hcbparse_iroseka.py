#!/usr/bin/env python3
import sys
import hcbparse


# Address of the (supposed) SetText() function
SET_TEXT_ADDR = 0x375b1


# Where to begin parsing strings as character lines
# v1.1 entry point
ENTRY_POINT = 0x7367d


# v1.0 entry point
# ENTRY_POINT = 0x731fc


# Character definitions
CHARACTER_LIST = [
    hcbparse.Character( 1793, 0x0004, "真紅"),
    hcbparse.Character( 1888, 0x0124, "加奈"),
    hcbparse.Character( 1889, 0x0332, "澪"),
    hcbparse.Character( 1882, 0x0505, "鏡"),
    hcbparse.Character( 1794, 0x0645, "つかさ"),
    hcbparse.Character( 2163, 0x07db, "蓮"),
    hcbparse.Character( 2162, 0x08ee, "白"),
    hcbparse.Character( 2087, 0x0a01, "鈴"),
    hcbparse.Character( 2161, 0x0c00, "あゆむ"),
    hcbparse.Character( 2002, 0x0dc3, "時雨"),
    hcbparse.Character(38927, 0x1029, "とおる"),
    hcbparse.Character( 1792, 0x133d, "悠馬")
]


def main():
    if len(sys.argv) != 3:
        print("usage: python3 hcbparse_iroseka.py World.hcb output.txt")
        return

    with open(sys.argv[2], "w", encoding="utf-8") as out_file:
        with open(sys.argv[1], "rb") as hcb_file:
            hcbparse.parse_lines(CHARACTER_LIST, SET_TEXT_ADDR, ENTRY_POINT, hcb_file, out_file)


if __name__ == "__main__":
    main()
