# Análise rápida do sistema e propostas de melhoria

## Visão geral do estado atual

O projeto está bem orientado para **experimentação reprodutível** com rAthena via Docker, com foco em geração procedural por seed e automação de mundo.

Pontos fortes identificados:

- Arquitetura simples de subir localmente com `docker compose`.
- Pipeline de geração de mundos claro (`new_world.sh` + `scripts/randomize_world.sh`).
- Separação entre base limpa (`data_base/`) e runtime mutável (`data/`).
- Conjunto amplo de randomizers para experimentação de gameplay.

## Riscos e gargalos observados

### 1) Exposição de serviços e segurança operacional

No `docker-compose.yml`, banco (`3306`), phpMyAdmin (`8080`) e portas do servidor estão publicados em host por padrão.

**Risco:** superfície de ataque elevada em ambientes não isolados.

### 2) Fragilidade no fluxo de geração

O script `new_world.sh` remove diretórios inteiros de dados (`rm -rf data/db data/npc data/conf`) antes de copiar a base.

**Risco:** perda de dados locais acidental e execução insegura se diretórios esperados não existirem/forem alterados.

### 3) Dependência implícita de ambiente e ordem

`scripts/randomize_world.sh` chama `docker exec ragnarok-server ...` e randomizers diretamente, assumindo container, path e estado válidos.

**Risco:** falhas difíceis de diagnosticar quando container não existe, está parado, ou quando pré-condições mudam.

### 4) Observabilidade mínima

Há pouca telemetria estruturada para rastrear uma geração: sem logs versionados por seed, sem sumário de alterações aplicadas.

**Risco:** baixa rastreabilidade para reproduzir bugs de balanceamento.

### 5) Documentação técnica curta em arquitetura

`docs/architecture.md` está extremamente resumido e não cobre fluxo completo de serviços, volumes, limites e operação.

**Risco:** onboarding mais lento e maior dependência de conhecimento tácito.

## Melhorias propostas (priorizadas)

## Prioridade alta (baixo esforço / alto impacto)

1. **Adicionar modo seguro de execução aos scripts (`set -euo pipefail`) e validações prévias.**
   - Verificar existência de `data_base/{db,npc,conf}` antes de apagar/copiar.
   - Validar dependências (`docker`, `python3`, `.env.rando`).

2. **Implementar confirmação/flag para operações destrutivas.**
   - Ex.: `./new_world.sh <seed> --force` para liberar `rm -rf`.

3. **Restringir exposição de portas por perfil de ambiente.**
   - Perfil `dev`: portas abertas.
   - Perfil `local-secure`: DB e phpMyAdmin somente `127.0.0.1`.

4. **Gerar log de execução por seed.**
   - Ex.: `logs/world/<seed>-<timestamp>.log` com etapas e ferramentas executadas.

## Prioridade média

5. **Padronizar healthchecks e readiness.**
   - `db` com healthcheck SQL.
   - `rathena` aguardando DB saudável antes de iniciar serviços dependentes.

6. **Adicionar Makefile/Tarefa única de operação.**
   - `make up`, `make down`, `make world SEED=...`, `make logs`, `make doctor`.

7. **Criar validação automática pós-randomização.**
   - Script de sanity check para detectar arquivos vazios, IDs duplicados, ranges inválidos.

8. **Documentar matriz de compatibilidade e troubleshooting por etapa.**
   - Sistema operacional, Docker versionado, requisitos de CPU/memória e causas comuns.

## Prioridade baixa (evolução)

9. **Introduzir perfis de randomização (casual/hardcore/chaos).**
   - Presets no `.env.rando` para acelerar testes de design.

10. **Criar snapshot de “manifesto do mundo”.**
   - Arquivo JSON final contendo seed, toggles, hashes de arquivos gerados e versão dos scripts.

11. **Pipeline CI para lint/check básico de scripts e Python tools.**
   - `shellcheck`, `ruff`/`flake8`, verificação de sintaxe.

## Plano sugerido de execução (2 semanas)

### Semana 1

- Hardening de `new_world.sh` e `scripts/randomize_world.sh` (flags seguras + pré-checks + logs).
- Revisão do `docker-compose.yml` para perfis e binding local.
- Expansão de `docs/architecture.md`.

### Semana 2

- Sanity checks pós-randomização.
- Makefile para operações comuns.
- Estrutura inicial de CI (lint + smoke checks).

## KPIs para medir melhora

- Tempo médio para gerar mundo (`new_world.sh`) sem erro.
- Taxa de falha por execução de randomizers.
- Tempo de onboarding de novo colaborador.
- Número de incidentes causados por ambiente/configuração.

## Conclusão

A base está muito boa para prototipagem rápida. O maior ganho agora é **maturidade operacional**: segurança mínima, validações robustas e observabilidade da geração por seed.
