#!/usr/bin/env python3

import os
import random


def load_env():
    env={}
    with open(".env.rando") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                k,v=line.strip().split("=",1)
                env[k]=v
    return env


env=load_env()

seed=int(os.environ.get("WORLD_SEED_NUMERIC",0))
random.seed(seed)

stats=[
"bonus bStr,{v};",
"bonus bAgi,{v};",
"bonus bVit,{v};",
"bonus bDex,{v};",
"bonus bLuk,{v};",
"bonus bAtk,{v};",
"bonus bFlee,{v};",
"bonus bHit,{v};",
"bonus bDef,{v};",
"bonus bMdef,{v};",
"bonus bMaxHP,{v};",
"bonus bMaxSP,{v};",
"bonus bCritical,{v};",
"bonus bAspdRate,{v};",
]

count=random.randint(
    int(env["MEDAL_MIN_STATS"]),
    int(env["MEDAL_MAX_STATS"])
)

lines=[]

for i in range(count):

    stat=random.choice(stats)

    value=random.randint(
        int(env["MEDAL_STAT_VALUE_MIN"]),
        int(env["MEDAL_STAT_VALUE_MAX"])
    )

    lines.append(stat.format(v=value))

script=" ".join(lines)

print(script)
