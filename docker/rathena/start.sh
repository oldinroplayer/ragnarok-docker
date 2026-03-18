#!/bin/bash

set -e

echo "=== Configurando IPs do rAthena ==="

CONF_DIR="/datastoresetup/usr-bin-rathena/conf"

cd $CONF_DIR

echo "RO_IP=${RO_IP}"

sed -i "s/^char_ip:.*/char_ip: ${RO_IP}/" char_athena.conf
sed -i "s/^map_ip:.*/map_ip: ${RO_IP}/" map_athena.conf
sed -i "s/^char_ip:.*/char_ip: ragnarok-server/" map_athena.conf
sed -i "s/^login_ip:.*/login_ip: ragnarok-server/" char_athena.conf

sed -i "s/^bind_ip:.*/bind_ip: 0.0.0.0/" char_athena.conf || true
sed -i "s/^bind_ip:.*/bind_ip: 0.0.0.0/" map_athena.conf || true

echo "=== Configuração aplicada ==="

grep ip char_athena.conf
grep ip map_athena.conf

echo "=== Iniciando rAthena ==="

cd /

# inicia em background
sh launch-athena.sh &

echo "=== rAthena iniciado ==="

# aguarda inicialização
sleep 10

echo "=== Gerando database web ==="

cd /usr/bin/rathena/db/re

python3 /build_ro_database.py || echo "Database generation failed"

echo "=== Database gerada ==="

# manter container vivo mostrando logs
tail -f /usr/bin/rathena/log/map-server.log
