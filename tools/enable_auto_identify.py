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

CONF=f"{ROOT}/conf/battle/items.conf"

print("Enabling auto identify for dropped items...")

lines=[]

with open(CONF) as f:
    for line in f:

        if "item_auto_identify" in line:
            lines.append("item_auto_identify: yes\n")
        else:
            lines.append(line)

with open(CONF,"w") as f:
    f.writelines(lines)

print("Auto identify enabled.")
