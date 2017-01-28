#!/bin/bash
scriptdir=`dirname $0`
datapath="$scriptdir/../data"
outpath="$datapath/asm"
hcbpath="$datapath/hcb"
hcbdecodepath="$scriptdir/favorite/hcbdecode.py"
hcbinfopath="$scriptdir/favorite/hcbinfo"
pyexe=""
if command -v "python3" &>/dev/null; then
    pyexe="python3"
elif command -v "py" &>/dev/null; then
    pyexe="py"
else
    pyexe="python"
fi

echo "Creating output directory"
mkdir -p "$outpath"

echo ">> Hoshizora no Memoria"
$pyexe "$hcbdecodepath" "$outpath/hoshimemo.txt" "$hcbpath/Memoria.hcb"

echo ">> Hoshizora no Memoria Eternal Heart"
$pyexe "$hcbdecodepath" "$outpath/eternalheart.txt" "$hcbpath/Hoshimemo_EH.hcb"

echo ">> Irotoridori no Sekai"
$pyexe "$hcbdecodepath" "$outpath/iroseka.txt" "$hcbpath/World.hcb"

echo ">> Irotoridori no Hikari"
$pyexe "$hcbdecodepath" "$outpath/irohika.txt" "$hcbpath/Hikari.hcb"

echo ">> Akai Hitomi ni Utsuru Sekai"
$pyexe "$hcbdecodepath" "$outpath/akaihitomi.txt" "$hcbpath/Shinku.hcb"

echo ">> AstralAir no Shiroki Towa"
$pyexe "$hcbdecodepath" "$outpath/astralair.txt" "$hcbpath/Snow.hcb"

echo ">> AstralAir no Shiroki Towa Finale"
$pyexe "$hcbdecodepath" "$outpath/astralfinale.txt" "$hcbpath/AstralAirFinale.hcb"
