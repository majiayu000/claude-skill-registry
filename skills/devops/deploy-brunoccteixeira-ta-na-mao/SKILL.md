---
name: deploy
description: Deploy com Docker e verificacao
---

## Comandos
```bash
# Desenvolvimento local
docker compose up -d

# Producao
docker compose -f docker-compose.prod.yml up -d

# Rebuild apos mudancas
docker compose up -d --build
```

## Health Checks

### Verificar Servicos
```bash
# API Backend
curl http://localhost:8000/health

# PostgreSQL
docker compose exec db pg_isready

# Redis
docker compose exec redis redis-cli PING
```

### Verificar Logs
```bash
# Todos os servicos
docker compose logs -f

# Servico especifico
docker compose logs -f backend
docker compose logs -f db
docker compose logs -f redis
```

## Rollback

### Voltar para versao anterior
```bash
# Parar servicos
docker compose down

# Voltar codigo
git checkout HEAD~1

# Reiniciar
docker compose up -d --build
```

### Backup do banco antes de deploy
```bash
docker compose exec db pg_dump -U postgres tanamao > backup_$(date +%Y%m%d).sql
```

## Troubleshooting

| Problema | Causa Provavel | Solucao |
|----------|----------------|---------|
| Container nao inicia | Porta ocupada | `lsof -i :8000` e matar processo |
| DB connection refused | PostgreSQL nao pronto | Aguardar ou `docker compose restart db` |
| Redis timeout | Redis nao iniciou | `docker compose restart redis` |
| Build falha | Cache corrompido | `docker compose build --no-cache` |
| .env nao carrega | Arquivo ausente | Copiar de `.env.example` |

## Checklist Pre-Deploy

- [ ] Testes passando (`pytest backend/tests/`)
- [ ] Variaveis de ambiente configuradas
- [ ] Migrations aplicadas (`alembic upgrade head`)
- [ ] Backup do banco realizado
- [ ] Health check OK apos deploy

## Arquivos
- `backend/Dockerfile`
- `backend/docker-compose.yml` (dev)
- `backend/docker-compose.prod.yml` (prod)
- `backend/.env` (nao commitar)
- `backend/.env.example` (template)
