# Troubleshooting por etapa

## Etapa 1 — Pré-requisitos

### Sintoma
`make doctor` falha.

### Causa comum
Dependências ausentes (`docker`, `python3`, `.env`, `.env.rando`, `data_base/`).

### Solução
1. Instale dependências.
2. Rode `./setup-rathena-data_base-external.sh`.
3. Rode `./copia-base.sh`.
4. Execute `make doctor` novamente.

---

## Etapa 2 — Subida do ambiente

### Sintoma
`rathena` ou `phpmyadmin` não iniciam.

### Causa comum
Banco ainda não saudável durante bootstrap.

### Solução
1. Verifique `docker compose ps`.
2. Confira `docker compose logs db`.
3. Aguarde healthcheck e suba novamente: `docker compose up -d`.

---

## Etapa 3 — Geração de mundo

### Sintoma
`new_world.sh` aborta antes da randomização.

### Causa comum
Falta de `--force`, ausência de `.env.rando` ou diretórios base.

### Solução
Use:

```bash
./new_world.sh minha-seed --force
```

E valide se existem:

- `data_base/db`
- `data_base/npc`
- `data_base/conf`

---

## Etapa 4 — Randomizers / sanity check

### Sintoma
Falha no `scripts/sanity_check_world.py`.

### Causa comum
Arquivos obrigatórios vazios, ausentes ou com IDs duplicados após randomização.

### Solução
1. Verifique logs em `logs/world/`.
2. Rode manualmente:
   ```bash
   python3 scripts/sanity_check_world.py
   ```
3. Refaça geração com outra seed para comparar.

---

## Etapa 5 — PIN ainda ativo

### Sintoma
PIN permanece habilitado.

### Causa comum
Alteração feita em template e não no runtime utilizado pelo servidor.

### Solução
Aplique em runtime (`/usr/bin/rathena/conf/char_athena.conf`) ou use fluxo do `casual.sh` para desativação.
