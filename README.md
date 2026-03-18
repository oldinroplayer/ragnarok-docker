# Ragnarok Procedural Server (rAthena + Docker)

Este projeto fornece um ambiente completo para execução de um **servidor Ragnarok Online baseado em rAthena** dentro de containers Docker, com foco em:

* automação de servidor
* geração procedural de mundos
* experimentação de sistemas de jogo
* debugging de servidores Ragnarok
* reprodutibilidade de ambientes

O projeto nasceu como um ambiente de desenvolvimento para explorar **modificações experimentais do rAthena**, incluindo randomização de conteúdo e análise automatizada da base do servidor.

---

# Filosofia do Projeto

Este projeto não tenta apenas "rodar um servidor Ragnarok".

Ele tenta transformar o servidor em algo **reprodutível, explorável e experimental**.

Algumas ideias centrais do projeto:

* servidores efêmeros
* mundos gerados por seed
* automação completa do ambiente
* separação clara entre dados base e dados modificados
* infraestrutura leve baseada em Docker

Isso permite experimentar ideias como:

* mundos aleatórios
* drops proceduralmente gerados
* progressão dinâmica de mapas
* variações de dificuldade

Cada mundo pode ser recriado usando apenas uma **seed**.

---

# Características do Projeto

O ambiente adiciona diversas camadas sobre o rAthena tradicional.

Principais funcionalidades:

### Ambiente containerizado

O servidor roda inteiramente dentro de containers Docker:

* rAthena (server)
* MariaDB
* phpMyAdmin
* roBrowserLegacy
* wsproxy

Isso garante que o ambiente seja **reproduzível em qualquer máquina**.

---

### Sistema de geração de mundos

O projeto inclui um sistema que permite gerar mundos diferentes usando seeds.

Script principal:

```
new_world.sh
```

Exemplo:

```
./new_world.sh wolfie-maxxer --force
```

Esse script executa automaticamente:

1. parar o servidor
2. restaurar a base limpa
3. aplicar randomizers
4. reiniciar o servidor

---

### Separação entre base limpa e dados modificáveis

Para evitar problemas de licença e permitir experimentação segura, o projeto separa:

```
data_base/
```

Base limpa do rAthena.

e

```
data/
```

Dados modificados pelo servidor e pelos randomizers.

A base original **não é incluída no repositório**.

---

### Ferramentas de análise do servidor

O projeto inclui diversas ferramentas para investigar o funcionamento do rAthena.

Exemplo:

```
tools/
```

Ferramentas de:

* parsing de database
* geração de documentação
* análise de configuração
* experimentos de randomização

---

# Arquitetura do Ambiente

O ambiente utiliza **Docker Compose** para orquestrar todos os serviços necessários.

Componentes principais:

| Serviço         | Função                 |
| --------------- | ---------------------- |
| rAthena         | servidor do jogo       |
| MariaDB         | banco de dados         |
| phpMyAdmin      | administração do banco |
| Apache          | servidor web           |
| roBrowserLegacy | cliente web            |
| wsproxy         | bridge websocket       |

---

# Estrutura do Projeto

```
ragnarok-docker/

docker/
    rathena/
        Dockerfile
        start.sh

tools/
scripts/

data/
data_base/

sql-init/

docs/

docker-compose.yml
new_world.sh
copia-base.sh
setup-rathena-data_base-external.sh
```

---

# Fluxo de Funcionamento

O funcionamento do ambiente segue algumas etapas claras.

### 1 — Base limpa

A base original do rAthena é baixada para:

```
data_base/
```

---

### 2 — Criação do ambiente modificável

O script:

```
copia-base.sh
```

copia arquivos necessários para:

```
data/
```

Essa pasta contém os arquivos realmente utilizados pelo servidor.

---

### 3 — Inicialização do servidor

O ambiente é iniciado com:

```
docker compose up -d
```

---

### 4 — Geração de mundos

Um novo mundo pode ser gerado executando:

```
./new_world.sh minha-seed --force
```

---

# Sistema de Seeds

Cada seed representa um mundo diferente.

Exemplo:

```
./new_world.sh wolfie-maxxer --force
```

Essa seed controla:

* randomização de drops
* randomização de estatísticas
* randomização de comportamento
* randomização de spawn

Isso permite explorar **variações infinitas de mundos Ragnarok**.

---

# Web Database Automática

O projeto inclui um sistema que gera automaticamente uma database navegável do servidor.

A database contém:

* lista de itens
* lista de monstros
* drops
* spawn de mobs
* busca rápida

Interface acessível em:

```
http://SEU_IP:8003/database.html
```

Essa database é gerada diretamente a partir dos arquivos do servidor.

---

# Cliente Web Integrado

O ambiente inclui um cliente Ragnarok executável no navegador:

```
roBrowserLegacy
```

Acesso:

```
http://SEU_IP:8003
```

Isso permite testar o servidor **sem instalar cliente local**.

---

# Instalação

Guia completo em:

```
docs/install.md
```

Resumo rápido:

```
git clone <repo>
cd ragnarok-docker

./setup-rathena-data_base-external.sh
./copia-base.sh

docker compose up -d
```

---

# Ferramentas Incluídas

O projeto inclui diversas ferramentas auxiliares.

Exemplos:

```
tools/
```

Algumas categorias:

### análise de database

Scripts que analisam:

* mob_db
* item_db
* spawn de mobs

---

### geração de documentação

Ferramentas que geram:

* database web
* relatórios do servidor

---

### randomizers experimentais

Alguns scripts experimentais incluem:

* randomização de drops
* randomização de estatísticas
* randomização de spawn
* randomização de AI

---

# Objetivos de Pesquisa

Este projeto também funciona como um laboratório para explorar ideias de design de jogo.

Alguns experimentos planejados incluem:

* progressão radial de mapas
* loot procedural
* cartas com efeitos aleatórios
* economia dinâmica de drops
* geração automática de documentação do servidor

---

# Observações sobre Licença

Arquivos originais do rAthena **não são incluídos no repositório**.

Eles são baixados automaticamente via script:

```
setup-rathena-data_base-external.sh
```

Isso evita redistribuição direta de arquivos do projeto rAthena.

---

# Status do Projeto

Projeto experimental em desenvolvimento.

Objetivos principais atuais:

* estabilidade do ambiente Docker
* melhoria dos randomizers
* evolução da database web
* exploração de design procedural em Ragnarok

---

# Autor

Projeto desenvolvido como ambiente experimental para estudo de:

* arquitetura de servidores Ragnarok
* automação de infraestrutura
* geração procedural de conteúdo
* engenharia de sistemas para jogos online


---

## Operação recomendada

Use os alvos de automação para operar o ambiente:

```bash
make doctor
make up
make world SEED=minha-seed
make logs
make down
```

Cada geração de mundo grava logs em `logs/world/` para rastreabilidade.


"This project is a server-side emulator modification tool. All game assets, images, and sounds are property of Gravity Co., Ltd. and are NOT included in this repository."

"Este projeto é uma ferramenta de modificação de emulador de servidor. Todos os recursos do jogo (assets), imagens e sons são propriedade da Gravity Co., Ltd. e NÃO estão incluídos neste repositório."

"Este proyecto es una herramienta de modificación de emuladores de servidor. Todos los recursos del juego (assets), imágenes y sonidos son propiedad de Gravity Co., Ltd. y NO están incluidos en este repositorio."

"본 프로젝트는 서버 에뮬레이터 수정 도구입니다. 게임의 모든 자산(에셋), 이미지, 사운드는 Gravity Co., Ltd.의 소유이며, 본 저장소에는 포함되어 있지 않습니다."
