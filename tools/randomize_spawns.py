#!/usr/bin/env python3

import os
import random
import glob
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
MOB_DB=f"{ROOT}/db/re/mob_db.txt"

MODE=env.get("MOB_RANDO_CHAOTIC","medium")

seed=int(os.environ.get("WORLD_SEED_NUMERIC",0))
random.seed(seed)

print("Spawn randomizer mode:",MODE)

#################################
# carregar mobs
#################################

mobs=[]
tiers={}

with open(MOB_DB) as f:
    for line in f:

        if line.startswith("//") or line.strip()=="":
            continue

        cols=line.split(",")

        try:
            mob_id=int(cols[0])
            lvl=int(cols[4])
        except:
            continue

        mobs.append((mob_id,lvl))

#################################
# tiers
#################################

def tier(level):

    if level<=20: return 1
    if level<=40: return 2
    if level<=70: return 3
    if level<=99: return 4
    return 5

for mob_id,lvl in mobs:

    t=tier(lvl)

    tiers.setdefault(t,[])
    tiers[t].append(mob_id)

all_mobs=[m[0] for m in mobs]

#################################
# escolha
#################################

def choose_mob(original_id):

    if MODE=="high":
        return random.choice(all_mobs)

    orig_lvl=None

    for m,l in mobs:
        if m==original_id:
            orig_lvl=l
            break

    if orig_lvl is None:
        return random.choice(all_mobs)

    t=tier(orig_lvl)

    if MODE=="low":
        return random.choice(tiers.get(t,all_mobs))

    if MODE=="medium":

        candidates=[]

        for dt in [-1,0,1]:
            candidates+=tiers.get(t+dt,[])

        if not candidates:
            candidates=all_mobs

        return random.choice(candidates)

#################################
# localizar arquivos
#################################

SPAWN_FILES=glob.glob(f"{ROOT}/npc/re/mobs/**/*.txt",recursive=True)

print("Spawn files found:",len(SPAWN_FILES))

#################################
# regex spawn
#################################

pattern=re.compile(r'(\d+),(\d+)(?:,(\d+))?$')

#################################
# randomizar
#################################

for file in SPAWN_FILES:

    new_lines=[]

    with open(file) as f:

        for line in f:

            if "monster" not in line:
                new_lines.append(line)
                continue

            match=pattern.search(line)

            if not match:
                new_lines.append(line)
                continue

            mob_id=int(match.group(1))

            new_id=choose_mob(mob_id)

            newline=line.replace(str(mob_id),str(new_id),1)

            new_lines.append(newline)

    with open(file,"w") as f:
        f.writelines(new_lines)

print("Spawn randomization complete.")
