#!/usr/bin/env python3

import os
import random
import shutil


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

MOB_DB=f"{ROOT}/{env['MOB_DB_PATH']}"
ITEM_DB=f"{ROOT}/{env['ITEM_DB_PATH']}"

BACKUP=MOB_DB+".bak"

print("Creating backup...")
shutil.copy(MOB_DB,BACKUP)

seed=int(os.environ.get("WORLD_SEED_NUMERIC",0))
random.seed(seed)

print("Loading valid items...")

valid_items=[]

with open(ITEM_DB) as f:
    for line in f:

        if line.startswith("//") or line.strip()=="":
            continue

        item_id=line.split(",")[0]

        if item_id.isdigit():
            valid_items.append(int(item_id))

print("Items loaded:",len(valid_items))

print("Randomizing drops...")

lines=[]

DROP_START=int(env.get("DROP_START_COLUMN",31))

with open(MOB_DB) as f:
    for line in f:

        if line.startswith("//") or line.strip()=="":
            lines.append(line)
            continue

        cols=line.strip().split(",")

        for i in range(DROP_START,len(cols),2):

            if i+1>=len(cols):
                break

            cols[i]=str(random.choice(valid_items))
            cols[i+1]=str(random.randint(
                int(env["DROP_RATE_MIN"]),
                int(env["DROP_RATE_MAX"])
            ))

        lines.append(",".join(cols)+"\n")

with open(MOB_DB,"w") as f:
    f.writelines(lines)

print("Drops randomized safely.")
