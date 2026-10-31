#!/bin/bash

FILE_PATH="$HOME/Smart-System-Stats-Analyzer/Metrics/Container2.csv"
INGEST_SCRIPT_PATH="$HOME/Smart-System-Stats-Analyzer/Scripts/ingest.py"

mkdir -p "$(dirname "$FILE_PATH")"

if [ ! -f "$FILE_PATH" ]; then
printf "\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"\n" "Time_Stamp" "us_CPU%" "sy_CPU%" "wa_CPU%" "Disk_tot" "Disk_use" "Disk_ava" "tot_RAM" "used_RAM" "ava_RAM" >> "$FILE_PATH"
fi

while true;
do

lt=$(date +"%Y-%m-%d %H:%M:%S")

read c1 c2 c3 <<< $(top -bn 1 | tr ':,' ' ' | awk '/%Cpu/ {print $2, $4, $10}')

read r1 r2 r3 <<< $(df | awk '$NF == "/" {print $2, $3, $4}')
read d1 d2 d3 <<< $(free | awk 'NR==2 {print $2, $3, $7}')

printf "\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"\n" "$lt" "$c1" "$c2" "$c3" "$r1" "$r2" "$r3" "$d1" "$d2" "$d3"  >> "$FILE_PATH"

python3 "$INGEST_SCRIPT_PATH"

sleep 60
done