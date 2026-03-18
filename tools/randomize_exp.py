import random
import json
import math

SEED = int(__import__("os").environ.get("WORLD_SEED_NUMERIC",0))

random.seed(SEED)

with open("db/mob_stats.json") as f:
    mobs = json.load(f)

exp_mod = {}

for mob_id, mob in mobs.items():

    # curva de bell
    value = random.gauss(1.0, 0.6)

    # clamp
    value = max(0.5, min(3.0, value))

    exp_mod[mob_id] = round(value,2)

with open("db/mob_exp_mod.json","w") as f:
    json.dump(exp_mod,f,indent=2)

print("Generated EXP modifiers for",len(exp_mod),"mobs")
