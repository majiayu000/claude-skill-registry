---
name: csv-analyzer
description: Analisar datasets CSV
---

Análise de datasets CSV de benefícios sociais usando pandas.

## Carregar CSV

```python
import pandas as pd

# CSV padrão
df = pd.read_csv("arquivo.csv")

# CSV com encoding brasileiro
df = pd.read_csv("arquivo.csv", encoding="latin-1", sep=";")

# CSV grande (em chunks)
for chunk in pd.read_csv("arquivo.csv", chunksize=10000):
    processar(chunk)
```

## Análises Comuns

### Visão Geral
```python
# Primeiras linhas
df.head()

# Informações
df.info()

# Estatísticas
df.describe()

# Valores únicos por coluna
df.nunique()
```

### Contagens
```python
# Por programa
df["programa"].value_counts()

# Por UF
df["uf"].value_counts()

# Por faixa de valor
pd.cut(df["valor"], bins=[0, 100, 300, 600, 1000]).value_counts()
```

### Agregações
```python
# Valor total por UF
df.groupby("uf")["valor"].sum()

# Média por programa
df.groupby("programa")["valor"].mean()

# Contagem por município
df.groupby(["uf", "municipio"]).size()
```

## Datasets do Tá na Mão

### Bolsa Família
```python
df = pd.read_csv("backend/data/bolsa_familia.csv")
# Colunas esperadas: cpf, nis, valor, municipio_id, data_referencia
```

### BPC/LOAS
```python
df = pd.read_csv("backend/data/bpc.csv")
# Colunas: cpf, tipo (idoso/deficiente), valor, municipio_id
```

### TSEE (Tarifa Social)
```python
df = pd.read_csv("backend/data/tsee.csv")
# Colunas: cpf, distribuidora, desconto, municipio_id
```

### Farmácia Popular
```python
df = pd.read_csv("backend/data/farmacias.csv")
# Colunas: nome, endereco, lat, lng, municipio_id
```

## Limpeza de Dados

```python
# Remover duplicatas
df = df.drop_duplicates()

# Preencher nulos
df["valor"] = df["valor"].fillna(0)

# Converter tipos
df["cpf"] = df["cpf"].astype(str).str.zfill(11)
df["valor"] = pd.to_numeric(df["valor"], errors="coerce")

# Remover espaços
df["nome"] = df["nome"].str.strip()
```

## Exportar Resultados

```python
# CSV
df.to_csv("resultado.csv", index=False)

# JSON
df.to_json("resultado.json", orient="records", force_ascii=False)

# Resumo em markdown
resumo = df.groupby("uf")["valor"].sum().to_markdown()
```

## Visualização Rápida

```python
import matplotlib.pyplot as plt

# Barras por UF
df.groupby("uf")["valor"].sum().plot(kind="bar")
plt.title("Valor Total por UF")
plt.savefig("grafico.png")
```

## Dicas de Performance

- Datasets > 1GB: usar `chunksize`
- Muitas colunas: selecionar apenas necessárias com `usecols`
- Tipos conhecidos: especificar `dtype` para economizar memória
