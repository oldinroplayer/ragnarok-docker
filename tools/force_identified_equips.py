#!/usr/bin/env python3

import os


def load_env():
    env={}
    with open(".env.rando") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                k,v=line.strip().split("=",1)
                env[k]=v
    return env


env=load_env()

ROOT=env["RATHENA_ROOT"]
ITEM_DB=env["ITEM_DB_PATH"]

DB=f"{ROOT}/{ITEM_DB}"

print("Forcing equipment to drop identified...")

lines=[]

with open(DB) as f:

    for line in f:

        if line.startswith("//") or line.strip()=="":
            lines.append(line)
            continue

        cols=line.split(",")

        try:
            item_type=int(cols[3])
        except:
            lines.append(line)
            continue

        # equipamentos
        if item_type in [4,5,6,7]:

            # campo identified
            if len(cols) > 7:
                cols[7]="1"

            line=",".join(cols)

        lines.append(line)

with open(DB,"w") as f:
    f.writelines(lines)

print("Equipment identification forced.")
