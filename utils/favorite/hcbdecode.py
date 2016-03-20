#!/usr/bin/env python3
#
# Special thanks to: https://bbs.sumisora.org/read.php?tid=11010281
# File layout: [header offset][instructions][header][import entries]

import struct
import sys


class EndOfInstructions(Exception):
    pass


class EndOfFile(Exception):
    pass


class HcbHeader:
    def __init__(self, entry_point, count1, count2, resolution_index, title):
        self.entry_point = entry_point
        self.count1 = count1
        self.count2 = count2
        self.resolution_index = resolution_index
        self.title = title


class HcbImportEntry:
    def __init__(self, import_type, name):
        self.import_type = import_type
        self.name = name


class HcbOp:
    def __init__(self, offset, opname, *operands):
        self.offset = offset
        self.opname = opname
        self.operands = operands

    def __str__(self):
        op_str = "{0:08x}  {1}".format(self.offset, self.opname)
        if len(self.operands) == 0:
            return op_str
        operand_strs = ", ".join(hex(x) if isinstance(x, int) else str(x) for x in self.operands)
        return "{0:<22}{1}".format(op_str, operand_strs)


class HcbDecoder:
    def __init__(self, file):
        self.file = file
        self.headerloc = self.read_header_offset()
        self.entry_point = None

    def read_bytes(self, n=1):
        bs = self.file.read(n)
        if len(bs) < n:
            assert len(bs) == 0, str(len(bs)) + " remaining bytes in file"
            raise EndOfFile()
        return bs

    def read(self, n=1):
        bs = self.read_bytes(n)
        out = 0
        for i in range(n):
            out |= (bs[i] << (i * 8))
        return out

    def read_header_offset(self):
        return self.read(4)

    def read_float(self):
        bs = self.read_bytes(4)
        return struct.unpack("<f", bs)

    def read_string(self):
        str_len = self.read()
        if str_len == 0:
            return ""
        str_bytes = self.read_bytes(str_len)
        assert str_bytes[-1] == 0, "String does not end with NUL terminator: " + repr(str_bytes)
        str_bytes = str_bytes[:-1]
        decoded_str = str_bytes.decode("cp932")
        return decoded_str

    def get_offset(self):
        return self.file.tell()

    def seek_to_offset(self, offset):
        self.file.seek(offset)

    def read_op(self):
        offset = self.get_offset()
        if offset >= self.headerloc:
            raise EndOfInstructions()
        op = self.read()
        assert 0x01 <= op <= 0x27, "Unknown opcode: " + hex(op)
        if   op == 0x01: return HcbOp(offset, "initstack", self.read(), self.read())
        elif op == 0x02: return HcbOp(offset, "call", self.read(4))
        elif op == 0x03: return HcbOp(offset, "callsys", self.read(2))
        elif op == 0x04: return HcbOp(offset, "ret")
        elif op == 0x05: return HcbOp(offset, "ret1")
        elif op == 0x06: return HcbOp(offset, "jmp", self.read(4))
        elif op == 0x07: return HcbOp(offset, "jz", self.read(4))
        elif op == 0x08: return HcbOp(offset, "push0")
        elif op == 0x09: return HcbOp(offset, "push1")
        elif op == 0x0A: return HcbOp(offset, "pushi32", self.read(4))
        elif op == 0x0B: return HcbOp(offset, "pushi16", self.read(2))
        elif op == 0x0C: return HcbOp(offset, "pushi8", self.read())
        elif op == 0x0D: return HcbOp(offset, "pushfloat", self.read_float())
        elif op == 0x0E: return HcbOp(offset, "pushstr", self.read_string())
        elif op == 0x0F: return HcbOp(offset, "pushglobal", self.read(2))
        elif op == 0x10: return HcbOp(offset, "pushstack", self.read())
        elif op == 0x11: return HcbOp(offset, "unk0x11", self.read(2))
        elif op == 0x12: return HcbOp(offset, "unk0x12", self.read())
        elif op == 0x13: return HcbOp(offset, "pushtop")
        elif op == 0x14: return HcbOp(offset, "pushtemp")
        elif op == 0x15: return HcbOp(offset, "popglobal", self.read(2))
        elif op == 0x16: return HcbOp(offset, "stackcpy", self.read())
        elif op == 0x17: return HcbOp(offset, "unk0x17", self.read(2))
        elif op == 0x18: return HcbOp(offset, "unk0x18", self.read())
        elif op == 0x19: return HcbOp(offset, "neg")
        elif op == 0x1A: return HcbOp(offset, "add")
        elif op == 0x1B: return HcbOp(offset, "sub")
        elif op == 0x1C: return HcbOp(offset, "mul")
        elif op == 0x1D: return HcbOp(offset, "div")
        elif op == 0x1E: return HcbOp(offset, "mod")
        elif op == 0x1F: return HcbOp(offset, "bittest")
        elif op == 0x20: return HcbOp(offset, "and")
        elif op == 0x21: return HcbOp(offset, "or")
        elif op == 0x22: return HcbOp(offset, "eq")
        elif op == 0x23: return HcbOp(offset, "ne")
        elif op == 0x24: return HcbOp(offset, "gt")
        elif op == 0x25: return HcbOp(offset, "lte")
        elif op == 0x26: return HcbOp(offset, "lt")
        elif op == 0x27: return HcbOp(offset, "gte")

    def read_ops(self):
        try:
            while True:
                yield self.read_op()
        except EndOfInstructions:
            pass
        assert self.get_offset() == self.headerloc, "Misaligned instruction-header border"

    def read_header(self):
        entry_point = self.read(4)
        count1 = self.read(2)
        count2 = self.read(2)
        resolution_index = self.read(2)
        title = self.read_string()
        return HcbHeader(
            entry_point,
            count1,
            count2,
            resolution_index,
            title)

    def read_import_entry(self):
        import_type = self.read()
        name = self.read_string()
        return HcbImportEntry(
            import_type,
            name)

    def read_import_entries(self):
        try:
            while True:
                yield self.read_import_entry()
        except EndOfFile:
            pass


def decode_hcb(hcb_file, out_file):
    dec = HcbDecoder(hcb_file)

    out_file.write("============= INSTRUCTIONS =============\n")
    for op in dec.read_ops():
        out_file.write(str(op))
        out_file.write("\n")

    header = dec.read_header()
    out_file.write("\n================ HEADER ================\n")
    out_file.write("entry point      = " + hex(header.entry_point) + "\n")
    out_file.write("count1           = " + str(header.count1) + "\n")
    out_file.write("count2           = " + str(header.count2) + "\n")
    out_file.write("resolution index = " + str(header.resolution_index) + "\n")
    out_file.write("title            = " + header.title + "\n")

    out_file.write("\n============ IMPORT ENTRIES ============\n")
    for im in dec.read_import_entries():
        out_file.write(im.name)
        out_file.write("\n")


def main():
    if len(sys.argv) != 3:
        print("usage: python3 hcbdecode.py input.hcb output.txt")
        return

    with open(sys.argv[2], "w", encoding="utf-8") as out_file:
        with open(sys.argv[1], "rb") as hcb_file:
            decode_hcb(hcb_file, out_file)


if __name__ == "__main__":
    main()
