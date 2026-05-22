---
name: postgres
description: Queries SQL seguras (read-only)
---

Queries SQL seguras (READ-ONLY) no banco do Tá na Mão.

## Conexão

### Via Docker
```bash
docker compose exec db psql -U postgres -d tanamao
```

### Via psql direto
```bash
psql "postgresql://postgres:postgres@localhost:5432/tanamao"
```

## Queries de Consulta

### Contar Registros
```sql
-- Total por tabela
SELECT 'municipios' as tabela, COUNT(*) FROM municipios
UNION ALL
SELECT 'beneficiarios', COUNT(*) FROM beneficiarios
UNION ALL
SELECT 'programas', COUNT(*) FROM programas;
```

### Beneficiários por Programa
```sql
SELECT
    p.nome as programa,
    COUNT(b.id) as total_beneficiarios,
    SUM(b.valor) as valor_total
FROM beneficiarios b
JOIN programas p ON b.programa_id = p.id
GROUP BY p.nome
ORDER BY total_beneficiarios DESC;
```

### Buscar por CPF (mascarado)
```sql
SELECT
    CONCAT('***', RIGHT(cpf, 4)) as cpf_masked,
    programa_id,
    valor,
    data_referencia
FROM beneficiarios
WHERE cpf = '12345678901'
LIMIT 10;
```

### Municípios com Mais Beneficiários
```sql
SELECT
    m.nome as municipio,
    m.uf,
    COUNT(b.id) as total
FROM municipios m
LEFT JOIN beneficiarios b ON b.municipio_id = m.id
GROUP BY m.id, m.nome, m.uf
ORDER BY total DESC
LIMIT 20;
```

### Cobertura por Estado
```sql
SELECT
    m.uf,
    COUNT(DISTINCT m.id) as municipios,
    COUNT(b.id) as beneficiarios,
    SUM(b.valor) as valor_total
FROM municipios m
LEFT JOIN beneficiarios b ON b.municipio_id = m.id
GROUP BY m.uf
ORDER BY m.uf;
```

## Queries de Verificação

### Estrutura das Tabelas
```sql
\dt                     -- Listar tabelas
\d beneficiarios        -- Estrutura da tabela
\d+ beneficiarios       -- Estrutura detalhada
```

### Índices
```sql
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'beneficiarios';
```

### Tamanho das Tabelas
```sql
SELECT
    relname as tabela,
    pg_size_pretty(pg_total_relation_size(relid)) as tamanho
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;
```

## Regras de Segurança

1. **Apenas SELECT** - Nunca INSERT, UPDATE, DELETE direto
2. **Mascarar CPF** - Usar `RIGHT(cpf, 4)` em outputs
3. **Limitar resultados** - Sempre usar `LIMIT`
4. **Sem exports** - Não exportar dados para arquivos

## Exemplo com SQLAlchemy (código)

```python
from sqlalchemy import text

async def consultar_beneficiario(session, cpf: str):
    query = text("""
        SELECT programa_id, valor, data_referencia
        FROM beneficiarios
        WHERE cpf = :cpf
        LIMIT 10
    """)
    result = await session.execute(query, {"cpf": cpf})
    return result.fetchall()
```
