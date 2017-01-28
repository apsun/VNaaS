#!/bin/bash
scriptdir=`dirname $0`
datapath="$scriptdir/../data"
outpath="$datapath/text"
hcbpath="$datapath/hcb"
hcbtextpath="$scriptdir/favorite/hcbtext.py"
hcbinfopath="$scriptdir/favorite/hcbinfo"
pyexe=""
if command -v "python3" &>/dev/null; then
    pyexe="python3"
elif command -v "py" &>/dev/null; then
    pyexe="py"
else
    pyexe="python"
fi

echo ">> Hoshizora no Memoria"
$pyexe "$hcbtextpath" "$outpath/hoshimemo.txt" "$hcbpath/Memoria.hcb" "$hcbinfopath/hoshimemo_1.1.py"

echo ">> Hoshizora no Memoria Eternal Heart"
$pyexe "$hcbtextpath" "$outpath/hoshimemo_eh.txt" "$hcbpath/Hoshimemo_EH.hcb" "$hcbinfopath/eternalheart_1.2.py"

echo ">> Irotoridori no Sekai"
$pyexe "$hcbtextpath" "$outpath/iroseka.txt" "$hcbpath/World.hcb" "$hcbinfopath/iroseka_1.1.py"

echo ">> Irotoridori no Hikari"
$pyexe "$hcbtextpath" "$outpath/irohika.txt" "$hcbpath/Hikari.hcb" "$hcbinfopath/irohika_1.1.py"

echo ">> Akai Hitomi ni Utsuru Sekai"
$pyexe "$hcbtextpath" "$outpath/akaihitomi.txt" "$hcbpath/Shinku.hcb" "$hcbinfopath/akaihitomi_1.0.py"

echo ">> AstralAir no Shiroki Towa"
$pyexe "$hcbtextpath" "$outpath/astralair.txt" "$hcbpath/Snow.hcb" "$hcbinfopath/astralair_1.1.py"

echo ">> AstralAir no Shiroki Towa Finale"
$pyexe "$hcbtextpath" "$outpath/astralfinale.txt" "$hcbpath/AstralAirFinale.hcb" "$hcbinfopath/astralfinale_1.1.py"
