#!/bin/bash
scriptdir=`dirname $0`
datapath="$scriptdir/../data"
dbpath="$datapath/vnaas.db"
hcbpath="$datapath/hcb"
hcb2dbpath="$scriptdir/favorite/hcb2db.py"
hcbinfopath="$scriptdir/favorite/hcbinfo"
sqliteexe="sqlite3"
pyexe=""
if command -v "python3" &>/dev/null; then
    pyexe="python3"
elif command -v "py" &>/dev/null; then
    pyexe="py"
else
    pyexe="python"
fi

echo "Creating database"
rm -f "$dbpath"
$sqliteexe "$dbpath" < "$scriptdir/schema.sql"

echo ">> Hoshizora no Memoria"
$pyexe "$hcb2dbpath" "$dbpath" "$hcbpath/Memoria.hcb" "$hcbinfopath/hoshimemo_1.1.py"

echo ">> Hoshizora no Memoria Eternal Heart"
$pyexe "$hcb2dbpath" "$dbpath" "$hcbpath/Hoshimemo_EH.hcb" "$hcbinfopath/eternalheart_1.2.py"

echo ">> Irotoridori no Sekai"
$pyexe "$hcb2dbpath" "$dbpath" "$hcbpath/World.hcb" "$hcbinfopath/iroseka_1.1.py"

echo ">> Irotoridori no Hikari"
$pyexe "$hcb2dbpath" "$dbpath" "$hcbpath/Hikari.hcb" "$hcbinfopath/irohika_1.1.py"

echo ">> Akai Hitomi ni Utsuru Sekai"
$pyexe "$hcb2dbpath" "$dbpath" "$hcbpath/Shinku.hcb" "$hcbinfopath/akaihitomi_1.0.py"

echo ">> AstralAir no Shiroki Towa"
$pyexe "$hcb2dbpath" "$dbpath" "$hcbpath/Snow.hcb" "$hcbinfopath/astralair_1.1.py"

echo ">> AstralAir no Shiroki Towa Finale"
$pyexe "$hcb2dbpath" "$dbpath" "$hcbpath/AstralAirFinale.hcb" "$hcbinfopath/astralfinale_1.1.py"
