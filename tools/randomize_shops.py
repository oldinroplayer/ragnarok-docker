#!/usr/bin/env python3

import os
import random
import re


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
SHOP_FILE=f"{ROOT}/{env['SHOP_FILE']}"
ITEM_DB=f"{ROOT}/{env['ITEM_DB_PATH']}"

seed=int(os.environ.get("WORLD_SEED_NUMERIC",0))
random.seed(seed)

print("Loading valid items...")

valid_items=[]

with open(ITEM_DB) as f:

    for line in f:

        if line.startswith("//") or line.strip()=="":
            continue

        cols=line.split(",")

        try:
            item_id=int(cols[0])
            item_type=int(cols[3])
        except:
            continue

        # apenas itens consumíveis ou equipamentos
        if item_type in [0,2,3,4,5]:
            valid_items.append(item_id)

print("Valid items:",len(valid_items))

print("Randomizing shops...")

with open(SHOP_FILE) as f:
    data=f.read()


def repl(match):

    price=match.group(2)

    item=random.choice(valid_items)

    return f"{item}:{price}"


data=re.sub(r"(\d+):(\d+)",repl,data)

with open(SHOP_FILE,"w") as f:
    f.write(data)

print("Shops randomized safely.")
