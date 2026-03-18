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

print("Allowing all items to be dropped...")

lines = []

with open(DB) as f:
    for line in f:

        if line.startswith("//") or line.strip() == "":
            lines.append(line)
            continue

        cols = line.split(",")

        if len(cols) < 8:
            lines.append(line)
            continue

        # dropable flag
        cols[7] = "0"

        lines.append(",".join(cols))

with open(DB, "w") as f:
    f.writelines(lines)

print("All items can now be dropped.")
