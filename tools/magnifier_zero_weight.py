#!/usr/bin/env python3

import os


def load_env():
    env = {}
    with open(".env.rando") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                k, v = line.strip().split("=", 1)
                env[k] = v
    return env


env = load_env()

ROOT = env["RATHENA_ROOT"]
ITEM_DB = env["ITEM_DB_PATH"]

DB = f"{ROOT}/{ITEM_DB}"

MAGNIFIER_ID = "611"

print("Setting Magnifier weight to 0...")

lines = []

with open(DB) as f:

    for line in f:

        if line.startswith("//") or line.strip() == "":
            lines.append(line)
            continue

        cols = line.strip().split(",")

        if cols[0] == MAGNIFIER_ID:

            if len(cols) > 6:
                cols[6] = "0"

            line = ",".join(cols) + "\n"

            print("Magnifier updated:", line.strip())

        lines.append(line)

with open(DB, "w") as f:
    f.writelines(lines)

print("Done.")
