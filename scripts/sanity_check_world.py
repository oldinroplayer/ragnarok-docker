#!/usr/bin/env python3
"""Validação básica pós-randomização."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    ROOT / "data" / "db" / "re" / "item_db.yml",
    ROOT / "data" / "db" / "re" / "mob_db.yml",
    ROOT / "data" / "npc" / "scripts_athena.conf",
]


def fail(msg: str) -> None:
    print(f"[SANITY][ERRO] {msg}")
    sys.exit(1)


def main() -> None:
    print("[SANITY] Iniciando validações de mundo...")

    for file_path in REQUIRED_FILES:
        if not file_path.exists():
            fail(f"Arquivo obrigatório ausente: {file_path}")
        if file_path.stat().st_size == 0:
            fail(f"Arquivo obrigatório vazio: {file_path}")

    item_db = REQUIRED_FILES[0].read_text(encoding="utf-8", errors="ignore")
    mob_db = REQUIRED_FILES[1].read_text(encoding="utf-8", errors="ignore")

    item_ids = [line.strip() for line in item_db.splitlines() if line.strip().startswith("Id:")]
    mob_ids = [line.strip() for line in mob_db.splitlines() if line.strip().startswith("Id:")]

    if len(item_ids) != len(set(item_ids)):
        fail("IDs duplicados detectados em item_db.yml")

    if len(mob_ids) != len(set(mob_ids)):
        fail("IDs duplicados detectados em mob_db.yml")

    print("[SANITY] OK - validações básicas concluídas.")


if __name__ == "__main__":
    main()
