# Arquitetura do ambiente

## Componentes principais

- **rathena**: servidor do jogo (login/char/map + geração de database web).
- **db (MariaDB 10.5)**: persistência de contas/personagens/economia.
- **phpMyAdmin**: administração SQL para desenvolvimento.
- **robrowser**: cliente web para testes rápidos.

## Fluxo de dados e volumes

- `data_base/`: template limpo do rAthena (imutável no fluxo operacional).
- `data/`: runtime editável/randomizado montado no container `rathena`.
- `db_data` (volume Docker): persistência do MariaDB.

Fluxo típico:

1. `setup-rathena-data_base-external.sh` baixa base limpa.
2. `copia-base.sh` cria runtime inicial em `data/`.
3. `new_world.sh <seed> --force` recria `data/` a partir da base e aplica randomizers.
4. `docker compose up -d` sobe serviços com `db` saudável.

## Segurança e exposição de rede

Por padrão, as portas são publicadas em `127.0.0.1` (variável `BIND_IP`), reduzindo exposição externa acidental.

Portas publicadas:

- `3306` (MariaDB)
- `8080` (phpMyAdmin)
- `6900`, `6121`, `5121` (rAthena)
- `8003` (web/database)
- `8001`, `5999` (roBrowser/ws)

Para expor em rede local, use no `.env`:

```env
BIND_IP=0.0.0.0
```

## Operação e observabilidade

- Cada execução de `new_world.sh` gera log em `logs/world/<seed>-<timestamp>.log`.
- `scripts/randomize_world.sh` executa sanity check ao final.
- `make doctor` valida pré-requisitos mínimos do ambiente.

## Readiness e dependências

- `db` possui healthcheck (`mysqladmin ping`).
- `rathena` e `phpmyadmin` dependem de `db` saudável.

Isso reduz falhas de bootstrap por ordem de inicialização.
