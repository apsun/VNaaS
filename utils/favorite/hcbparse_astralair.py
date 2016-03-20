#!/usr/bin/env python3

import sys
import hcbparse


# Address of the (supposed) SetText() function
SET_TEXT_ADDR = 0x5a7b3


# Where to begin parsing strings as character lines
ENTRY_POINT = 0xb709b


# Character definitions
CHARACTER_LIST = [
    hcbparse.Character(1,  0x0004, "雪々"),
    hcbparse.Character(2,  0x0216, "落葉"),
    hcbparse.Character(3,  0x037a, "一夏"),
    hcbparse.Character(4,  0x048d, "りんね"),
    hcbparse.Character(5,  0x05a0, "コロナ"),
    hcbparse.Character(6,  0x0678, "琴里"),
    hcbparse.Character(7,  0x0750, "幸"),
    hcbparse.Character(8,  0x0828, "葉月"),
    hcbparse.Character(9,  0x0900, "ひなた"),
    hcbparse.Character(10, 0x09d8, "美晴"),
    hcbparse.Character(11, 0x0ab0, "千川"),
    hcbparse.Character(12, 0x0b88, "累"),
    hcbparse.Character(13, 0x0c60, "まりも"),
    hcbparse.Character(14, 0x0d38, "椎菜"),
    hcbparse.Character(15, 0x0e10, "柚子"),
    hcbparse.Character(16, 0x0ee8, "渡部"),
    hcbparse.Character(17, 0x0fbe, "大樹"),
    hcbparse.Character(18, 0x10d1, "白羽"),
    hcbparse.Character(19, 0x11e4, "アルビレオ"),
    hcbparse.Character(20, 0x1332, "ばあちゃん"),
    hcbparse.Character(21, 0x1cf0, "陸"),
]


def main():
    if len(sys.argv) != 3:
        print("usage: python3 hcbparse_astralair.py Snow.hcb output.txt")
        return

    with open(sys.argv[2], "w", encoding="utf-8") as out_file:
        with open(sys.argv[1], "rb") as hcb_file:
            hcbparse.parse_lines(CHARACTER_LIST, SET_TEXT_ADDR, ENTRY_POINT, hcb_file, out_file)


if __name__ == "__main__":
    main()
