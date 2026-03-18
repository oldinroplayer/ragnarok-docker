#!/usr/bin/env python3

import glob
import os
import json
import shutil

ITEM_DB = "item_db.txt"
MOB_DB = "mob_db.txt"
MOB_SPAWN = "../../npc/re/mob_spawn.txt"

WEB_DIR = "/var/www/html/db"


def parse_items():

    items = {}
    item_info = {}

    with open(ITEM_DB, encoding="utf8", errors="ignore") as f:

        for line in f:

            if line.startswith("//") or not line.strip():
                continue

            cols = line.split(",")

            item_id = cols[0]
            aegis = cols[1]
            name = cols[2]

            items[item_id] = name

            item_info[item_id] = {
                "aegis": aegis,
                "name": name
            }

    return items, item_info


def parse_mobs():

    mobs = {}
    stats = {}

    with open(MOB_DB, encoding="utf8", errors="ignore") as f:

        for line in f:

            if line.startswith("//") or not line.strip():
                continue

            cols = line.split(",")

            mob_id = cols[0]
            name = cols[2]

            mobs[mob_id] = name

            stats[mob_id] = {
                "name": name,
                "level": cols[3],
                "hp": cols[4],
                "atk1": cols[9],
                "atk2": cols[10],
                "def": cols[11],
                "mdef": cols[12],
                "str": cols[13],
                "agi": cols[14],
                "vit": cols[15],
                "int": cols[16],
                "dex": cols[17],
                "luk": cols[18],
                "race": cols[21],
                "element": cols[22]
            }

    return mobs, stats


def parse_drops(items):

    item_to_mobs = {}
    mob_to_items = {}

    with open(MOB_DB, encoding="utf8", errors="ignore") as f:

        for line in f:

            if line.startswith("//") or not line.strip():
                continue

            cols = line.split(",")

            mob_id = cols[0]
            mob_name = cols[2]

            drop_cols = cols[31:]

            for i in range(0, len(drop_cols), 2):

                if i + 1 >= len(drop_cols):
                    break

                item_id = drop_cols[i]
                rate = drop_cols[i + 1]

                if item_id == "0":
                    continue

                item_name = items.get(item_id, "Unknown")

                drop = {
                    "item_id": int(item_id),
                    "item_name": item_name,
                    "rate": int(rate)
                }

                mob_to_items.setdefault(mob_id, []).append(drop)

                item_to_mobs.setdefault(item_id, []).append({
                    "mob_id": int(mob_id),
                    "mob_name": mob_name,
                    "rate": int(rate)
                })

    return item_to_mobs, mob_to_items



def parse_spawns():

    map_to_mobs={}
    mob_spawn={}

    spawn_files = glob.glob("../../npc/re/mobs/**/*.txt", recursive=True)

    print("Spawn files found:",len(spawn_files))

    for file in spawn_files:

        with open(file, encoding="utf8", errors="ignore") as f:

            for line in f:

                if "monster" not in line:
                    continue

                parts=line.split(",")

                if len(parts) < 4:
                    continue

                mapname=parts[0].strip()

                try:
                    mob_id=parts[3].strip()
                except:
                    continue

                mob_spawn.setdefault(mob_id,[])
                mob_spawn[mob_id].append(mapname)

                map_to_mobs.setdefault(mapname,[])
                map_to_mobs[mapname].append(mob_id)

    return mob_spawn, map_to_mobs

def write_json(name, data):

    with open(name, "w") as f:
        json.dump(data, f, indent=2)


def move_files():

    os.makedirs(WEB_DIR, exist_ok=True)

    for f in [
        "items.json",
        "item_info.json",
        "item_to_mobs.json",
        "mob_to_items.json",
        "mob_stats.json",
        "mob_spawn.json",
        "map_to_mobs.json"
    ]:

        shutil.move(f, WEB_DIR + "/" + f)


def main():

    print("Parsing items...")
    items, item_info = parse_items()

    print("Parsing mobs...")
    mobs, stats = parse_mobs()

    print("Parsing drops...")
    item_to_mobs, mob_to_items = parse_drops(items)

    print("Parsing spawn data...")
    mob_spawn, map_to_mobs = parse_spawns()

    write_json("items.json", items)
    write_json("item_info.json", item_info)
    write_json("item_to_mobs.json", item_to_mobs)
    write_json("mob_to_items.json", mob_to_items)
    write_json("mob_stats.json", stats)
    write_json("mob_spawn.json", mob_spawn)
    write_json("map_to_mobs.json", map_to_mobs)

    move_files()

    print("Database generated successfully.")


if __name__ == "__main__":
    main()
