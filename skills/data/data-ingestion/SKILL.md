---
name: data-ingestion
description: Jobs de ingestao de dados
---

## Jobs Disponiveis

| Job | Fonte | Comando |
|-----|-------|---------|
| IBGE | Estados/municipios | `python -m app.jobs.ingest_ibge` |
| Bolsa Familia | Portal da Transparencia | `python -m app.jobs.ingest_bolsa_familia` |
| BPC/LOAS | Dados reais | `python -m app.jobs.ingest_bpc_real` |
| Farmacia Popular | Unidades credenciadas | `python -m app.jobs.ingest_farmacia_real` |
| TSEE | Tarifa Social Energia | `python -m app.jobs.ingest_tsee` |
| Auxilio Gas | Auxilio Gas Brasil | `python -m app.jobs.ingest_auxilio_gas` |
| Seguro Defeso | Pescadores | `python -m app.jobs.ingest_seguro_defeso` |
| CadUnico | SAGI/MDS | `python -m app.jobs.ingest_sagi_cadunico` |
| Geometrias | Mapas municipais | `python -m app.jobs.ingest_mun_geometries` |
| Populacao | IBGE populacao | `python -m app.jobs.ingest_population` |

## Pre-requisitos
```bash
# 1. Estar no diretorio backend
cd backend

# 2. PostgreSQL rodando
docker compose up -d db

# 3. Variaveis de ambiente
source .env

# 4. Migrations aplicadas
alembic upgrade head
```

## Executar Ingestao Completa
```bash
cd backend

# Ordem recomendada
python -m app.jobs.ingest_ibge          # Base: estados e municipios
python -m app.jobs.ingest_population    # Populacao por municipio
python -m app.jobs.ingest_bolsa_familia # Maior programa
python -m app.jobs.ingest_bpc_real      # BPC/LOAS
python -m app.jobs.ingest_tsee          # Tarifa Social
python -m app.jobs.ingest_farmacia_real # Farmacias
```

## Verificar Ingestao
```sql
-- Contar registros por tabela
SELECT 'municipios' as tabela, COUNT(*) FROM municipios
UNION ALL
SELECT 'beneficiarios', COUNT(*) FROM beneficiarios
UNION ALL
SELECT 'programas', COUNT(*) FROM programas;
```

## Diretorio
```
backend/app/jobs/
├── ingest_ibge.py
├── ingest_bolsa_familia.py
├── ingest_bpc_real.py
├── ingest_farmacia_real.py
├── ingest_tsee.py
├── ingest_auxilio_gas.py
├── ingest_seguro_defeso.py
├── ingest_sagi_cadunico.py
├── ingest_mun_geometries.py
├── ingest_population.py
└── indexar_beneficiarios.py
```

## Troubleshooting

| Erro | Causa | Solucao |
|------|-------|---------|
| Connection refused | DB nao iniciado | `docker compose up -d db` |
| Table not found | Migrations pendentes | `alembic upgrade head` |
| API rate limit | Muitas requisicoes | Aguardar e retry |
| Memory error | Dataset grande | Processar em chunks |
