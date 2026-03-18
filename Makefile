SHELL := /bin/bash

SEED ?=
FORCE ?= --force

.PHONY: up down world logs doctor ps build

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

ps:
	docker compose ps

world:
	@if [ -z "$(SEED)" ]; then \
		echo "Uso: make world SEED=minha-seed"; \
		exit 1; \
	fi
	./new_world.sh "$(SEED)" "$(FORCE)"

logs:
	docker compose logs -f --tail=200

doctor:
	@echo "== Doctor =="
	@command -v docker >/dev/null || (echo "docker ausente" && exit 1)
	@command -v python3 >/dev/null || (echo "python3 ausente" && exit 1)
	@test -f .env || (echo ".env ausente" && exit 1)
	@test -f .env.rando || (echo ".env.rando ausente" && exit 1)
	@test -d data_base || (echo "data_base ausente" && exit 1)
	@echo "Ambiente básico OK"
