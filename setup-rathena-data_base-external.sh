#!/bin/bash

echo "================================="
echo "Baixando base limpa do rAthena"
echo "================================="

git clone --depth 1 https://github.com/rathena/rathena.git data_base

echo
echo "Base instalada em:"
echo "data_base/"
