---
name: xlsx
description: Gerar e processar planilhas Excel
---

Criar e processar planilhas Excel para relatórios do Admin Dashboard.

## Dependência

Requer `openpyxl`:
```bash
pip install openpyxl
```

## Ler Excel

```python
import pandas as pd

# Planilha simples
df = pd.read_excel("arquivo.xlsx")

# Aba específica
df = pd.read_excel("arquivo.xlsx", sheet_name="Dados")

# Todas as abas
todas_abas = pd.read_excel("arquivo.xlsx", sheet_name=None)
```

## Criar Excel

### Básico
```python
import pandas as pd

df = pd.DataFrame({
    "Município": ["São Paulo", "Rio de Janeiro", "Belo Horizonte"],
    "Beneficiários": [100000, 80000, 50000],
    "Valor Total": [60000000, 48000000, 30000000]
})

df.to_excel("relatorio.xlsx", index=False)
```

### Com Múltiplas Abas
```python
with pd.ExcelWriter("relatorio_completo.xlsx") as writer:
    df_bf.to_excel(writer, sheet_name="Bolsa Família", index=False)
    df_bpc.to_excel(writer, sheet_name="BPC", index=False)
    df_tsee.to_excel(writer, sheet_name="TSEE", index=False)
```

### Com Formatação
```python
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill

wb = Workbook()
ws = wb.active
ws.title = "Relatório"

# Cabeçalho
headers = ["Município", "UF", "Beneficiários", "Valor"]
for col, header in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col, value=header)
    cell.font = Font(bold=True)
    cell.fill = PatternFill(start_color="366092", fill_type="solid")
    cell.font = Font(color="FFFFFF", bold=True)

# Dados
for row, (mun, uf, benef, valor) in enumerate(dados, 2):
    ws.cell(row=row, column=1, value=mun)
    ws.cell(row=row, column=2, value=uf)
    ws.cell(row=row, column=3, value=benef)
    ws.cell(row=row, column=4, value=valor)

# Ajustar largura das colunas
for col in ws.columns:
    ws.column_dimensions[col[0].column_letter].width = 15

wb.save("relatorio_formatado.xlsx")
```

## Relatórios do Tá na Mão

### Relatório de Cobertura
```python
def gerar_relatorio_cobertura():
    # Query do banco
    dados = await get_cobertura_por_municipio()

    df = pd.DataFrame(dados)
    df.columns = ["Município", "UF", "População", "Beneficiários", "Cobertura %"]

    with pd.ExcelWriter("cobertura.xlsx") as writer:
        df.to_excel(writer, sheet_name="Cobertura", index=False)

        # Resumo por UF
        resumo = df.groupby("UF").agg({
            "População": "sum",
            "Beneficiários": "sum"
        })
        resumo["Cobertura %"] = resumo["Beneficiários"] / resumo["População"] * 100
        resumo.to_excel(writer, sheet_name="Resumo UF")
```

### Relatório de Programas
```python
def gerar_relatorio_programas():
    df = pd.DataFrame({
        "Programa": ["Bolsa Família", "BPC", "TSEE", "Auxílio Gás"],
        "Beneficiários": [21000000, 5000000, 12000000, 5500000],
        "Valor Médio": [600, 1412, 50, 100],
        "Orçamento Mensal": [12600000000, 7060000000, 600000000, 550000000]
    })

    df.to_excel("programas.xlsx", index=False)
```

## Dicas

- Usar `index=False` para não exportar índice do DataFrame
- Especificar `engine='openpyxl'` se tiver problemas de compatibilidade
- Para arquivos grandes, considerar CSV em vez de Excel
