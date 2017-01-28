#!/bin/bash
scriptdir=`dirname $0`
datapath="$scriptdir/../data"
patchpath="$datapath/patch"
hcbpath="$datapath/hcb"

echo "Creating output directories"
mkdir -p "$patchpath"
mkdir -p "$hcbpath"

dlpatch() {
    # $1 = name of HCB
    # $2 = name of patch file
    # $3 = com|jp
    # $4 = patchdata|updatedata
    if [ ! -f "$hcbpath/$1.hcb" ]; then
        if [ ! -f "$patchpath/$2.zip" ]; then
            curl -s "http://www.favo-soft.$3/soft/patch/$2.zip" -o "$patchpath/$2.zip"
        fi
        unzip -q -j "$patchpath/$2.zip" "$2/$4/$1.hcb" -d "$hcbpath"
    fi
}

echo ">> Hoshizora no Memoria"
dlpatch "Memoria" "Memoria_update_v11" "com" "patchdata"

echo ">> Hoshizora no Memoria Eternal Heart"
dlpatch "Hoshimemo_EH" "EternalHeart_update_v12" "com" "patchdata"

echo ">> Irotoridori no Sekai"
dlpatch "World" "Iroseka_update_v11" "jp" "patchdata"

echo ">> Irotoridori no Hikari"
dlpatch "Hikari" "Hikari_update_v11" "jp" "patchdata"

# Akai Hitomi ni Utsuru Sekai doesn't have any patches :-(
# You're going to need a copy of the game...
# But you already had that, right? Riiiight?

echo ">> AstralAir no Shiroki Towa"
dlpatch "Snow" "WhiteEternity_update_v11" "jp" "updatedata"

echo ">> AstralAir no Shiroki Towa Finale"
dlpatch "AstralAirFinale" "AstralAir_finale_update_v11" "jp" "updatedata"
