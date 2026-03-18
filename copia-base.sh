#!/bin/bash

set -e

CONTAINER="ragnarok-server"

echo "================================="
echo "Exportando base do rAthena"
echo "Container: $CONTAINER"
echo "================================="

mkdir -p data/db
mkdir -p data/npc
mkdir -p data/conf

echo
echo "Copiando DB..."
docker cp $CONTAINER:/usr/bin/rathena/db/. ./data/db/

echo
echo "Copiando NPC (com spawns)..."
docker cp $CONTAINER:/usr/bin/rathena/npc/. ./data/npc/

echo
echo "Copiando CONF..."
docker cp $CONTAINER:/usr/bin/rathena/conf/. ./data/conf/

echo
echo "================================="
echo "Verificando arquivos importantes"
echo "================================="

if [ ! -f data/db/re/mob_db.txt ]; then
    echo "ERRO: mob_db.txt não encontrado!"
fi

if [ ! -f data/npc/re/mob_spawn.txt ]; then
    echo "ERRO: mob_spawn.txt não encontrado!"
else
    echo "mob_spawn.txt OK"
fi

echo
echo "================================="
echo "Resumo:"
echo "================================="

du -sh data/db
du -sh data/npc
du -sh data/conf

echo
echo "Arquivos spawn:"
ls data/npc/re | grep spawn || true

echo
echo "Export concluído."
echo "================================="
