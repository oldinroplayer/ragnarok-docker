#!/usr/bin/env python3

import subprocess
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

MEDAL_ID=env.get("MEDAL_ITEM_ID","29000")

script=subprocess.check_output(
["python3","tools/generate_medal.py"]
).decode().strip()

lines=[]

with open(DB) as f:
    for line in f:

        if line.startswith(f"{MEDAL_ID},"):

            parts=line.split("{")

            new=f"{parts[0]}{{ {script} }},{{}}"

            lines.append(new+"\n")

        else:
            lines.append(line)

with open(DB,"w") as f:
    f.writelines(lines)

print("Medalha de Honra generated:")
print(script)
