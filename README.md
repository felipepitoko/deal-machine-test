
# Deal Machine Test - Plataforma de Análise de Mensagens

## Visão Geral
Este projeto é uma plataforma completa de análise de mensagens, construída com FastAPI, PostgreSQL e um frontend moderno em HTML/JS. Demonstra integração avançada entre backend e frontend, gestão de banco de dados e análise de texto com IA. O app foi desenvolvido como teste de habilidades em Python e IA, evidenciando boas práticas em APIs, conteinerização e experiência do usuário.

## Funcionalidades
- **Backend FastAPI**: API REST robusta para inserção, busca e análise de mensagens.
- **Banco de Dados PostgreSQL**: Armazenamento confiável de mensagens e metadados.
- **Análise com IA**: Extração automática de palavras-chave, intenção e sentimento usando regras e agente de IA.
- **Filtros Avançados**: Busque mensagens por usuário, palavra-chave, sentimento, intenção e período.
- **Endpoints Distintos**: Recupere todos os usuários, palavras-chave, sentimentos e intenções únicos para filtros dinâmicos.
- **Frontend Moderno**: Interface responsiva em HTML/JS com filtros ao vivo e visualização elegante das mensagens.
- **Conteinerização**: Inicialização com um único comando via Docker Compose, incluindo Adminer para inspeção do banco.

## Arquitetura
- **Backend**: Python 3.11, FastAPI, SQLAlchemy, Jinja2, Uvicorn
- **Banco de Dados**: PostgreSQL (com Adminer para gestão visual)
- **Frontend**: HTML, CSS (Tailwind), JavaScript (fetch API)
- **Agente IA**: Lógica plugável para análise de mensagens (`filters.py` e `analyze_agent.py`)

## Início Rápido
### Pré-requisitos
- Docker e Docker Compose instalados

### 1. Clone o repositório
```sh
git clone https://github.com/felipepitoko/deal-machine-test.git
cd deal-machine-test
```

### 2. Suba todos os serviços (API, DB, Adminer) com um comando
```sh
docker compose up --build
```
- A API estará disponível em [http://localhost:8000](http://localhost:8000)
- O frontend é servido na URL raiz.
- Adminer (UI do banco) em [http://localhost:8080](http://localhost:8080)
  - Sistema: PostgreSQL
  - Servidor: db
  - Usuário: example
  - Senha: example
  - Banco: postgres


### 3. Usando o App
- Acesse [http://localhost:8000](http://localhost:8000) no navegador.
- Busque e filtre mensagens usando a interface intuitiva.
- O sistema já vem com dados mock inseridos (basta rodar `python populate.py` após a API estar online, se quiser recarregar os dados).
- A análise é automática — experimente diferentes textos para ver a extração de palavras-chave, intenção e sentimento.
- Você pode conectar um bot do Telegram e enviar mensagens para o endpoint `/from_telegram/` para integração real com o Telegram.

### 4. Endpoints da API
- `POST /add_message/` — Adiciona nova mensagem (análise automática)
- `GET /list_messages/` — Lista/busca mensagens (filtro por usuário, palavra-chave, sentimento, intenção, data)
- `GET /distinct_usernames/` — Lista todos os usuários únicos
- `GET /distinct_keywords/` — Lista todas as palavras-chave únicas
- `GET /distinct_feelings/` — Lista todos os sentimentos únicos
- `GET /distinct_intentions/` — Lista todas as intenções únicas
- `POST /from_telegram/` — Ingestão e análise de mensagens no formato do Telegram

### 5. Personalização
- **Análise de Mensagens**: Edite `filters.py` e `analyze_agent.py` para alterar a extração de palavras-chave, intenções e sentimentos.
- **Modelos do Banco**: Veja `db_manager.py` para os modelos SQLAlchemy.
- **Frontend**: Edite `templates/index.html` e `static/script.js` para customizar a interface.

## Estrutura do Projeto
```
deal-machine-test/
├── api.py                # App FastAPI e endpoints
├── db_manager.py         # Modelos e gestão do banco
├── filters.py            # Lógica de análise de mensagens
├── analyze_agent.py      # Agente IA para análise avançada
├── requirements.txt      # Dependências Python
├── Dockerfile            # Build do container da API
├── compose.yaml          # Configuração Docker Compose
├── start.sh              # Entrypoint: cria tabelas e inicia API
├── static/
│   └── script.js         # JS do frontend
├── templates/
│   └── index.html        # HTML do frontend
└── ...
```

## Por que este projeto se destaca
- **Padrões Profissionais**: Separação clara de responsabilidades, tratamento de erros e arquitetura escalável.
- **DevOps Friendly**: Totalmente conteinerizado, fácil de implantar e pronto para uso.
- **Experiência do Usuário**: UI moderna, responsiva e com feedback em tempo real.
- **Extensível**: Fácil adicionar novas lógicas de análise, endpoints ou recursos de UI.

## Autor & Contato
Felipe Costa

---

**Pronto para entregar valor como Analista de Sistemas/Solutions builder!**

---

*Fique à vontade para entrar em contato para dúvidas ou sugestões.*
