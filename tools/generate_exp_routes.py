import json

mobs=json.load(open("db/mob_stats.json"))
spawns=json.load(open("db/mob_spawn.json"))
expmod=json.load(open("db/mob_exp_mod.json"))

routes={}

for mob_id,mob in mobs.items():

    level=mob["level"]

    base=mob["base_exp"]
    job=mob["job_exp"]
    hp=mob["hp"]

    modifier=expmod.get(mob_id,1)

    score=(base+job)*modifier/(hp+1)

    for mapname in spawns.get(mob_id,[]):

        routes.setdefault(mapname,0)
        routes[mapname]+=score

sorted_maps=sorted(routes.items(), key=lambda x:x[1], reverse=True)

with open("db/exp_routes.json","w") as f:
    json.dump(sorted_maps,f,indent=2)
