#!/usr/bin/env python3

import sys
import hcbparse


# Address of the (supposed) SetText() function
SET_TEXT_ADDR = 0x4987f


# Where to begin parsing strings as character lines
ENTRY_POINT = 0x8c770


# Character definitions
CHARACTER_LIST = [
    hcbparse.Character(3930,  0x0004, "メア"),
    hcbparse.Character(3910,  0x00dc, "明日歩"),
    hcbparse.Character(3932,  0x017f, "こもも"),
    hcbparse.Character(3938,  0x0222, "こさめ"),
    hcbparse.Character(3939,  0x02c5, "衣鈴"),
    hcbparse.Character(3907,  0x0344, "千波"),
    hcbparse.Character(6159,  0x03c3, "雪菜"),
    hcbparse.Character(3940,  0x0442, "夢"),
    hcbparse.Character(6160,  0x04e5, "詩乃"),
    hcbparse.Character(6157,  0x0564, "万夜花"),
    hcbparse.Character(6163,  0x05e3, "鈴葉"),
    hcbparse.Character(6158,  0x0662, "飛鳥"),
    hcbparse.Character(6156,  0x06e1, "岡泉"),
    hcbparse.Character(6162,  0x0760, "総一朗"),
    hcbparse.Character(6161,  0x0882, "レン"),
    hcbparse.Character(19231, 0x0949, "大河"),
    hcbparse.Character(3882,  0x0c1e, "洋")
]


def main():
    if len(sys.argv) != 3:
        print("usage: python3 hcbparse_hoshimemo.py Memoria.hcb output.txt")
        return

    with open(sys.argv[2], "w", encoding="utf-8") as out_file:
        with open(sys.argv[1], "rb") as hcb_file:
            hcbparse.parse_lines(CHARACTER_LIST, SET_TEXT_ADDR, ENTRY_POINT, hcb_file, out_file)


if __name__ == "__main__":
    main()
