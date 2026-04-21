# DevOps Study API

Projeto simples em Python criado para praticar Git, GitHub, CI/CD com GitHub Actions e Docker para a disciplina de DevOps.

## Funcionalidades

- `GET /` retorna informacoes basicas da API
- `GET /health` verifica a saude da aplicacao
- `GET /tasks` lista tarefas de estudo
- `GET /tasks?status=pending` filtra tarefas pendentes
- `GET /tasks?status=done` filtra tarefas concluidas
- `POST /tasks` cria uma nova tarefa

## Como executar localmente

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
python app.py
```

## Como rodar os testes

```bash
pytest
```

## Exemplo de requisicao

```bash
curl http://localhost:5000/health
```

## Docker

```bash
docker build -t devops-study-api .
docker run -d -p 5000:5000 --name devops-study-api devops-study-api
docker ps
```

O workflow de CD tambem valida o endpoint `/health` para garantir que o container sobe corretamente.
