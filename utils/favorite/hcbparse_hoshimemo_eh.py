#!/usr/bin/env python3

import sys
import hcbparse


# Address of the (supposed) SetText() function
SET_TEXT_ADDR = 0x51f35


# Where to begin parsing strings as character lines
ENTRY_POINT = 0x8d737


# Character definitions
CHARACTER_LIST = [
    hcbparse.Character(1,  0x0004, "メア"),
    hcbparse.Character(2,  0x00cb, "明日歩"),
    hcbparse.Character(3,  0x018c, "こもも"),
    hcbparse.Character(4,  0x024d, "こさめ"),
    hcbparse.Character(5,  0x02da, "衣鈴"),
    hcbparse.Character(6,  0x0343, "千波"),
    hcbparse.Character(7,  0x03ac, "雪菜"),
    hcbparse.Character(8,  0x0415, "夢"),
    hcbparse.Character(9,  0x04a2, "詩乃"),
    hcbparse.Character(10, 0x050b, "万夜花"),
    hcbparse.Character(11, 0x0574, "鈴葉"),
    hcbparse.Character(12, 0x05dd, "飛鳥"),
    hcbparse.Character(13, 0x0646, "岡泉"),
    hcbparse.Character(14, 0x06c5, "総一朗"),
    hcbparse.Character(15, 0x0752, "かーくん"),
    hcbparse.Character(16, 0x07bb, "レン"),
    hcbparse.Character(17, 0x086c, "大河"),
    hcbparse.Character(18, 0x0962, "伊麻"),
    hcbparse.Character(19, 0x0ab3, "姫榊"),
    hcbparse.Character(20, 0x0c63, "洋"),
]


def main():
    if len(sys.argv) != 3:
        print("usage: python3 hcbparse_hoshimemo_eh.py Hoshimemo_EH.hcb output.txt")
        return

    with open(sys.argv[2], "w", encoding="utf-8") as out_file:
        with open(sys.argv[1], "rb") as hcb_file:
            hcbparse.parse_lines(CHARACTER_LIST, SET_TEXT_ADDR, ENTRY_POINT, hcb_file, out_file)


if __name__ == "__main__":
    main()
