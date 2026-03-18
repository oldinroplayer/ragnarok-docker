#!/usr/bin/env python3

import random
import os

# =========================
# ENV
# =========================

def load_env():
    env = {}
    with open(".env.rando") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                k, v = line.strip().split("=", 1)
                env[k] = v
    return env

env = load_env()

seed = os.environ.get("WORLD_SEED", "default")
random.seed(seed)

AMPLITUDE = float(env.get("AMPLITUDE", "1.0"))

DB = f"{env['RATHENA_ROOT']}/{env['ITEM_DB_PATH']}"

# =========================
# ITENS
# =========================

ITEMS = {
    "2214": "bunny",
    "2501": "muffler",
    "2401": "shoes",
    "2829": "clip"
}

# =========================
# BASE STATS (ESCALÁVEL)
# =========================

base_values = {
    "bAspdRate": (1, 5),
    "bAtk": (4, 12),
    "bMatk": (4, 12),
    "bCritical": (3, 10),
    "bHit": (5, 15),
    "bFlee": (5, 15),
    "bDef": (5, 20),
    "bMdef": (5, 20),
    "bMaxHP": (20, 80),
    "bMaxSP": (10, 50),
}

junk_stats = [
    "bAddRace,RC_DemiHuman",
    "bAddRace,RC_Brute",
    "bAddRace,RC_Undead",
    "bAddSize,Size_Small",
    "bAddSize,Size_Medium",
    "bAddSize,Size_Large",
]

# =========================
# TIERS
# =========================

tiers = {
    "C": 1.0,
    "B": 1.5,
    "A": 2.0,
    "A+": 2.5,
    "S": 3.0
}

# =========================
# ARQUÉTIPOS
# =========================

archetypes = {
    "melee": ["bAtk", "bAspdRate", "bCritical"],
    "ranged": ["bHit", "bCritical", "bAtk"],
    "magic": ["bMatk", "bMaxSP"],
    "tank": ["bDef", "bMaxHP"],
    "dodge": ["bFlee"],
    "hybrid": ["bAtk", "bMatk", "bHit"]
}

# =========================
# META DA SEED
# =========================

arch_list = list(archetypes.keys())
random.shuffle(arch_list)

favored = arch_list[0]
normal = arch_list[1:4]
cursed = arch_list[4:6]

print(f"[META] Favored: {favored}")
print(f"[META] Normal: {normal}")
print(f"[META] Cursed: {cursed}")
print(f"[META] Amplitude: x{AMPLITUDE}")

# =========================
# HELPERS
# =========================

def scale_value(stat, tier):
    minv, maxv = base_values.get(stat, (5, 15))

    base = random.randint(minv, maxv)
    v = int(base * tiers[tier] * AMPLITUDE)

    if stat == "bAspdRate":
        return min(v, 5)

    return v

def pick_stat():
    roll = random.random()

    if roll < 0.5:
        return random.choice(archetypes[favored])
    elif roll < 0.8:
        return random.choice(sum([archetypes[a] for a in normal], []))
    else:
        return random.choice(sum([archetypes[a] for a in cursed], []))

def tier_for_stat(stat):

    if stat in archetypes[favored]:
        return random.choice(["A", "A+", "S"])

    for a in normal:
        if stat in archetypes[a]:
            return random.choice(["B", "A"])

    for a in cursed:
        if stat in archetypes[a]:
            return random.choice(["C", "B"])

    return "C"

def roll_bonus():

    # junk
    if random.random() < 0.3:
        stat = random.choice(junk_stats)
        v = int(random.randint(10, 30) * AMPLITUDE)
        return f"bonus2 {stat},{v};"

    stat = pick_stat()
    tier = tier_for_stat(stat)
    v = scale_value(stat, tier)

    return f"bonus {stat},{v};"

def roll_debuff():
    stat = random.choice([
        "bDef", "bMdef", "bFlee", "bHit",
        "bMaxHP", "bMaxSP", "bAspdRate"
    ])

    v = int(random.randint(20, 60) * AMPLITUDE)

    if stat == "bAspdRate":
        v = int(random.randint(10, 40) * AMPLITUDE)

    return f"bonus {stat},-{v};"

# =========================
# BUILDERS
# =========================

def make_normal():
    return " ".join([roll_bonus() for _ in range(5)] + [roll_debuff()])

def make_bunny():
    parts = []

    for _ in range(5):
        stat = pick_stat()

        if random.random() < 0.5:
            tier = "S"
        else:
            tier = tier_for_stat(stat)

        v = scale_value(stat, tier)
        parts.append(f"bonus {stat},{v};")

    parts.append(roll_debuff())

    return " ".join(parts)

def make_clip(original):

    parts = [roll_bonus() for _ in range(4)]

    penalties = [
        "bonus bDef,-100; bonus bMdef,-100;",
        "bonus bMaxHP,-80;",
        "bonus bUseSPrate,100;",
        "bonus bFlee,-100;",
        "bonus bAspdRate,-50;"
    ]

    penalty = random.choice(penalties)

    return f"{original} {' '.join(parts)} {penalty}"

# =========================
# APPLY
# =========================

lines = []

with open(DB) as f:
    for line in f:

        if line.startswith("//") or line.strip() == "":
            lines.append(line)
            continue

        updated = False

        for item_id, kind in ITEMS.items():

            if line.startswith(f"{item_id},"):

                before = line.split("{", 1)[0]

                if kind == "bunny":
                    script = make_bunny()

                elif kind == "clip":
                    try:
                        original = line.split("{", 1)[1].split("}", 1)[0]
                    except:
                        original = ""
                    script = make_clip(original)

                else:
                    script = make_normal()

                new_line = f"{before}{{ {script} }},{{}},{{}}\n"
                lines.append(new_line)
                updated = True
                break

        if not updated:
            lines.append(line)

with open(DB, "w") as f:
    f.writelines(lines)

print("[OK] Gear rando aplicado (ULTIMATE MODE).")
