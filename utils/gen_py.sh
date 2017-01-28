#!/bin/bash
scriptdir=`dirname $0`
datapath="$scriptdir/../data"
outpath="$datapath/py"
hcbpath="$datapath/hcb"
hcb2pypath="$scriptdir/favorite/hcb2py.py"
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
$pyexe "$hcb2pypath" "$outpath/hoshimemo.py" "$hcbpath/Memoria.hcb" "$hcbinfopath/hoshimemo_1.1.py"

echo ">> Hoshizora no Memoria Eternal Heart"
$pyexe "$hcb2pypath" "$outpath/eternalheart.py" "$hcbpath/Hoshimemo_EH.hcb" "$hcbinfopath/eternalheart_1.2.py"

echo ">> Irotoridori no Sekai"
$pyexe "$hcb2pypath" "$outpath/iroseka.py" "$hcbpath/World.hcb" "$hcbinfopath/iroseka_1.1.py"

echo ">> Irotoridori no Hikari"
$pyexe "$hcb2pypath" "$outpath/irohika.py" "$hcbpath/Hikari.hcb" "$hcbinfopath/irohika_1.1.py"

echo ">> Akai Hitomi ni Utsuru Sekai"
$pyexe "$hcb2pypath" "$outpath/akaihitomi.py" "$hcbpath/Shinku.hcb" "$hcbinfopath/akaihitomi_1.0.py"

echo ">> AstralAir no Shiroki Towa"
$pyexe "$hcb2pypath" "$outpath/astralair.py" "$hcbpath/Snow.hcb" "$hcbinfopath/astralair_1.1.py"

echo ">> AstralAir no Shiroki Towa Finale"
$pyexe "$hcb2pypath" "$outpath/astralfinale.py" "$hcbpath/AstralAirFinale.hcb" "$hcbinfopath/astralfinale_1.1.py"
