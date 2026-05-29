---
name: resolvendo-entidades
description: |
  Resolve entidades do usuario para identificadores do sistema.

  USAR SEMPRE ANTES de skills que aceitam:
  - cliente, cnpj, grupo → resolver_grupo.py ou resolver_cliente.py
  - produto, cod_produto → resolver_produto.py
  - pedido, num_pedido → resolver_pedido.py
  - cidade, uf → resolver_cidade.py

  NAO USAR quando usuario fornece ID exato (CNPJ completo, cod_produto, num_pedido).
allowed-tools: Read, Bash, Glob, Grep
---

# Resolvendo Entidades

Skill dedicada a resolver termos humanos para identificadores do sistema.

---

## Indice

1. [CRITICO: Quando Usar Esta Skill](#critico-quando-usar-esta-skill)
2. [Fluxo Obrigatorio](#fluxo-obrigatorio)
3. [Mapeamento: Qual Script Usar?](#mapeamento-qual-script-usar)
4. [Scripts Disponiveis](#scripts-disponiveis)
5. [Regras de Negocio](#regras-de-negocio)
6. [Referencias Cruzadas](#referencias-cruzadas)
7. [References](#references)

---

## CRITICO: Quando Usar Esta Skill

**OBRIGATORIO usar ANTES de qualquer skill que aceite entidades do dominio.**

As entidades transitam por MULTIPLAS tabelas do sistema:

| Entidade | Tabelas onde existe |
|----------|---------------------|
| **CLIENTE (CNPJ)** | CarteiraPrincipal, Separacao, EmbarqueItem, Frete, EntregasMonitoradas, NFDevolucao, FaturamentoProduto |
| **PRODUTO** | CadastroPalletizacao, CarteiraPrincipal, Separacao, MovimentacaoEstoque, UnificacaoCodigos |
| **PEDIDO** | CarteiraPrincipal, Separacao, EmbarqueItem |

Sem resolver primeiro, o agente alucina ou falha em consultas.

---

## Fluxo Obrigatorio

```
1. Usuario: "entregas do Assai de SP"
            ↓
2. RESOLVER PRIMEIRO:
   resolver_grupo.py --grupo assai --uf SP
   → {"sucesso": true, "prefixos_cnpj": ["06.057.22"], "total": 15}
            ↓
3. ENTAO CONSULTAR:
   consultando_status_entrega.py --cnpj "06.057.22"
```

### Quando NAO Resolver

**NAO usar esta skill se usuario ja forneceu:**
- CNPJ completo: `06.057.22/0001-XX`
- cod_produto exato: `AZ001`
- num_pedido exato: `VCD2565291`

---

## Mapeamento: Qual Script Usar?

### Tabela de Decisao Rapida

| Se o usuario menciona... | Script | Exemplo de Uso |
|--------------------------|--------|----------------|
| "Atacadao", "Assai", "Tenda" | `resolver_grupo.py --grupo X` | `--grupo atacadao` |
| "Atacadao de SP" | `resolver_grupo.py --grupo X --uf Y` | `--grupo atacadao --uf SP` |
| "Atacadao loja 183" | `resolver_grupo.py --grupo X --loja Y` | `--grupo atacadao --loja 183` |
| "Carrefour", cliente nao-grupo | `resolver_cliente.py --termo X` | `--termo Carrefour` |
| "CNPJ 45.543.915" | `resolver_cliente.py --termo X` | `--termo 45.543.915` |
| "palmito", "azeitona" | `resolver_produto.py --termo X` | `--termo palmito` |
| "CI", "AZ VF" (abreviacao) | `resolver_produto.py --termo X` | `--termo "AZ VF"` |
| "VCD123", parte de pedido | `resolver_pedido.py --termo X` | `--termo VCD123` |
| "Sao Paulo", cidade | `resolver_cidade.py --cidade X` | `--cidade "Sao Paulo"` |
| "SP", "RJ" (UF) | `resolver_uf.py --uf X` | `--uf SP` |

### Regras de Decisao

1. **Se menciona grupo empresarial conhecido:**
   → `resolver_grupo.py`

2. **Se menciona cliente desconhecido ou CNPJ parcial:**
   → `resolver_cliente.py`

3. **Se menciona produto por nome/abreviacao:**
   → `resolver_produto.py`

4. **Se menciona pedido por numero parcial:**
   → `resolver_pedido.py`

5. **Se menciona cidade ou UF:**
   → `resolver_cidade.py` ou `resolver_uf.py`

---

## Scripts Disponiveis

### 1. resolver_grupo.py

Resolve grupos empresariais para lista de CNPJs.

```bash
source .venv/bin/activate && python .claude/skills/resolvendo-entidades/scripts/resolver_grupo.py [opcoes]
```

**Parametros:**

| Param | Obrig | Descricao |
|-------|-------|-----------|
| `--grupo` | Sim | Nome do grupo (atacadao, assai, tenda) |
| `--uf` | Nao | Filtrar por UF (SP, RJ, etc.) |
| `--loja` | Nao | Filtrar por identificador de loja (183, CENTRO) |
| `--fonte` | Nao | carteira, separacao, entregas (default: entregas) |

**Retorno:**
```json
{
  "sucesso": true,
  "grupo": "assai",
  "prefixos_cnpj": ["06.057.22"],
  "filtros": {"uf": "SP"},
  "cnpjs": ["06.057.22/0001-XX", "06.057.22/0002-YY"],
  "total": 15
}
```

### 2. resolver_cliente.py

Resolve cliente nao-grupo por CNPJ parcial ou nome.

```bash
source .venv/bin/activate && python .claude/skills/resolvendo-entidades/scripts/resolver_cliente.py --termo "Carrefour"
```

**Parametros:**

| Param | Obrig | Descricao |
|-------|-------|-----------|
| `--termo` | Sim | CNPJ parcial ou nome do cliente |
| `--fonte` | Nao | carteira, separacao, entregas (default: entregas) |
| `--limite` | Nao | Maximo de resultados (default: 50) |

**Retorno:**
```json
{
  "sucesso": true,
  "termo": "Carrefour",
  "estrategia": "NOME_PARCIAL",
  "clientes": [
    {"cnpj": "45.543.915/0001-XX", "nome": "CARREFOUR CENTRO", "cidade": "SAO PAULO", "uf": "SP"}
  ],
  "total": 3
}
```

### 3. resolver_produto.py

Resolve produto por termo ou abreviacao.

```bash
source .venv/bin/activate && python .claude/skills/resolvendo-entidades/scripts/resolver_produto.py --termo "palmito"
```

**Parametros:**

| Param | Obrig | Descricao |
|-------|-------|-----------|
| `--termo` | Sim | Nome, abreviacao ou caracteristica do produto |
| `--limite` | Nao | Maximo de resultados (default: 50) |

**Retorno:**
```json
{
  "sucesso": true,
  "termo": "palmito",
  "produtos": [
    {"cod_produto": "PAL001", "nome_produto": "PALMITO PUPUNHA 300G", "score": 8}
  ],
  "total": 15
}
```

### 4. resolver_pedido.py

Resolve pedido por numero parcial ou termo.

```bash
source .venv/bin/activate && python .claude/skills/resolvendo-entidades/scripts/resolver_pedido.py --termo "VCD123"
```

**Parametros:**

| Param | Obrig | Descricao |
|-------|-------|-----------|
| `--termo` | Sim | Numero parcial ou termo de busca |
| `--fonte` | Nao | carteira, separacao, ambos (default: ambos) |

**Retorno:**
```json
{
  "sucesso": true,
  "termo": "VCD123",
  "estrategia": "NUMERO_PARCIAL",
  "pedidos": [
    {"num_pedido": "VCD1234567", "cliente": "ATACADAO 183", "cnpj": "93.209.76/0001-XX"}
  ],
  "multiplos": true,
  "total": 5
}
```

### 5. resolver_cidade.py

Resolve cidade com normalizacao de acentos.

```bash
source .venv/bin/activate && python .claude/skills/resolvendo-entidades/scripts/resolver_cidade.py --cidade "itanhaem"
```

**Parametros:**

| Param | Obrig | Descricao |
|-------|-------|-----------|
| `--cidade` | Sim | Nome da cidade (com ou sem acentos) |
| `--fonte` | Nao | carteira, separacao, entregas (default: entregas) |

### 6. resolver_uf.py

Resolve UF para lista de CNPJs/pedidos.

```bash
source .venv/bin/activate && python .claude/skills/resolvendo-entidades/scripts/resolver_uf.py --uf SP
```

---

## Regras de Negocio

### Grupos Empresariais Mapeados

| Grupo | Prefixos CNPJ | Aliases |
|-------|---------------|---------|
| `atacadao` | 93.209.76, 75.315.33, 00.063.96 | Carrefour Atacadao |
| `assai` | 06.057.22 | Assai Atacadista |
| `tenda` | 01.157.55 | Tenda Atacado |

### Abreviacoes de Produto

| Abreviacao | Campo | Valor | Descricao |
|------------|-------|-------|-----------|
| CI | tipo_materia_prima | CI | Cogumelo Inteiro |
| CF | tipo_materia_prima | CF | Cogumelo Fatiado |
| AZ VF | tipo_materia_prima | AZ VF | Azeitona Verde Fatiada |
| AZ PF | tipo_materia_prima | AZ PF | Azeitona Preta Fatiada |
| AZ VI | tipo_materia_prima | AZ VI | Azeitona Verde Inteira |
| AZ PI | tipo_materia_prima | AZ PI | Azeitona Preta Inteira |
| BD | tipo_embalagem | BD% | Balde |
| VD | tipo_embalagem | VIDRO% | Vidro |
| BR | tipo_embalagem | BARRICA | Barrica |
| GL | tipo_embalagem | GALAO% | Galao |
| MEZZANI | categoria_produto | MEZZANI | Marca Mezzani |
| CAMPO BELO | categoria_produto | CAMPO BELO | Marca Campo Belo |
| IND | categoria_produto | INDUSTRIA | Destinado a industria |

### O Agente PODE Afirmar

- CNPJs de um grupo empresarial
- Produtos que casam com termo de busca
- Pedidos que casam com numero parcial
- Clientes encontrados por nome/CNPJ

### O Agente NAO PODE Inventar

- CNPJs de grupos nao mapeados
- Produtos sem match no CadastroPalletizacao
- Pedidos inexistentes
- Abreviacoes nao documentadas

---

## Referencias Cruzadas

### Skills que PRECISAM de Resolucao

| Skill | Parametros que precisam resolver |
|-------|----------------------------------|
| `gerindo-expedicao` | --grupo, --cliente, --produto, --pedido |
| `monitorando-entregas` | --cliente, --cnpj |
| `consultando-sql` | Qualquer filtro de entidade na query |
| `rastreando-odoo` | --partner (nome de parceiro) |

### Quando Delegar para Outra Skill

| Situacao | Skill a usar |
|----------|--------------|
| Apos resolver, consultar pedidos/estoque | `gerindo-expedicao` |
| Apos resolver, consultar entregas | `monitorando-entregas` |
| Apos resolver, consultar SQL | `consultando-sql` |
| Apos resolver, rastrear no Odoo | `rastreando-odoo` |

---

## References

| Gatilho na Pergunta | Reference a Ler | Motivo |
|---------------------|-----------------|--------|
| "quais grupos existem?" | `references/grupos_empresariais.md` | Lista completa de grupos e CNPJs |
| "abreviacoes de produto" | `references/abreviacoes_produto.md` | Mapeamento completo |
| "onde esta a entidade X?" | `references/entidades_por_tabela.md` | Tabelas que contem cada entidade |

---

## Exemplos de Uso

### Cenario 1: Resolver grupo antes de consultar entregas

```
Pergunta: "entregas pendentes do Assai de SP"

Passo 1 - Resolver:
   resolver_grupo.py --grupo assai --uf SP --fonte entregas
   → {"prefixos_cnpj": ["06.057.22"], "total": 15}

Passo 2 - Consultar:
   consultando_status_entrega.py --cnpj "06.057.22" --pendentes
   → {"total": 8, "entregas": [...]}

Resposta: "Encontrei 8 entregas pendentes do Assai em SP"
```

### Cenario 2: Resolver produto por abreviacao

```
Pergunta: "tem AZ VF na carteira do Atacadao?"

Passo 1 - Resolver produto:
   resolver_produto.py --termo "AZ VF"
   → {"produtos": [{"cod_produto": "AZ001", "nome": "AZEITONA VERDE FATIADA"}]}

Passo 2 - Resolver grupo:
   resolver_grupo.py --grupo atacadao
   → {"prefixos_cnpj": ["93.209.76", "75.315.33", "00.063.96"]}

Passo 3 - Consultar:
   (usar gerindo-expedicao com filtros resolvidos)
```

### Cenario 3: Multiplos resultados

```
Pergunta: "pedido 123"

Passo 1 - Resolver:
   resolver_pedido.py --termo 123
   → {"multiplos": true, "pedidos": ["VCD1234", "VCD5123", "VFB123"]}

Resposta: "Encontrei 3 pedidos com '123'. Qual voce quer?
   - VCD1234 (Atacadao 183)
   - VCD5123 (Assai Guarulhos)
   - VFB123 (Tenda Centro)"
```
