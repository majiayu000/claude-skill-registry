---
name: mei-simplificado
description: Guia MEI com simulador de impacto nos benefícios sociais
---

Passo a passo para MEI voltado à população vulnerável, com simulador de impacto nos benefícios sociais.

## Contexto

- Empreendedorismo por necessidade é altíssimo na população de baixa renda
- Medo de perder Bolsa Família impede formalização
- MEI dá acesso a previdência, crédito e nota fiscal
- Obrigações do MEI são simples mas desconhecidas

## Pergunta Central: "Se eu virar MEI, perco o Bolsa Família?"

### Regra Atual
```
NÃO necessariamente.

O que importa é a RENDA PER CAPITA da família:
- Até R$218/pessoa -> Mantém Bolsa Família integral
- R$218 a R$660/pessoa -> Regra de proteção (2 anos garantidos)
- Acima de R$660/pessoa -> Perde gradualmente

O faturamento do MEI (até R$81.000/ano = R$6.750/mês) NÃO é
automaticamente considerado como renda.

O que conta como renda é o LUCRO LÍQUIDO:
  Faturamento - Despesas do negócio = Lucro

Exemplo:
  Faturamento: R$2.000/mês
  Despesas: R$1.200 (material, transporte, etc.)
  Lucro: R$800/mês
  Família de 4 pessoas: R$800 / 4 = R$200/pessoa
  -> MANTÉM o Bolsa Família
```

## Simulador de Impacto
```python
# backend/app/agent/tools/simulador_mei.py
async def simular_impacto_mei(
    faturamento_estimado: float,
    despesas_estimadas: float,
    membros_familia: int,
    renda_familiar_atual: float,
    beneficios_atuais: list[str],
) -> dict:
    """Simula impacto de abrir MEI nos benefícios atuais."""
    lucro = faturamento_estimado - despesas_estimadas
    nova_renda_total = renda_familiar_atual + lucro
    nova_renda_per_capita = nova_renda_total / membros_familia

    impactos = []

    if "bolsa_familia" in beneficios_atuais:
        if nova_renda_per_capita <= 218:
            impactos.append({
                "beneficio": "Bolsa Família",
                "status": "MANTÉM",
                "explicacao": "Sua renda por pessoa continua abaixo de R$218."
            })
        elif nova_renda_per_capita <= 660:
            impactos.append({
                "beneficio": "Bolsa Família",
                "status": "PROTEGIDO",
                "explicacao": "Você tem 2 anos de proteção. O benefício continua por 24 meses."
            })
        else:
            impactos.append({
                "beneficio": "Bolsa Família",
                "status": "PODE PERDER",
                "explicacao": "Sua renda ficaria acima do limite. Mas ganharia mais no total."
            })

    if "bpc" in beneficios_atuais:
        if nova_renda_per_capita <= 353:
            impactos.append({
                "beneficio": "BPC",
                "status": "MANTÉM",
                "explicacao": "Renda por pessoa abaixo de 1/4 do salário mínimo."
            })
        else:
            impactos.append({
                "beneficio": "BPC",
                "status": "PODE PERDER",
                "explicacao": "BPC tem regra de renda mais rígida."
            })

    das_mensal = 75.60
    ganho_liquido = lucro - das_mensal

    return {
        "impactos": impactos,
        "comparativo": {
            "renda_atual": renda_familiar_atual,
            "renda_com_mei": nova_renda_total,
            "custo_mei_mensal": das_mensal,
            "ganho_liquido_mensal": ganho_liquido,
            "vale_a_pena": ganho_liquido > 0,
        },
        "beneficios_mei": [
            "Aposentadoria por idade",
            "Auxílio-doença (após 12 meses)",
            "Salário-maternidade (após 10 meses)",
            "Nota fiscal (pode vender pra empresas)",
            "Conta bancária PJ (crédito mais fácil)",
        ],
    }
```

## Passo a Passo para Abrir MEI

### Requisitos
```
Pode ser MEI quem:
- Fatura até R$81.000 por ano (R$6.750/mês)
- Não é sócio de outra empresa
- Tem no máximo 1 empregado (salário mínimo ou piso da categoria)
- Exerce atividade permitida (lista no Portal do Empreendedor)
```

### Abertura (Gratuita)
```
1. Acesse: gov.br/mei
2. Faça login com Gov.br
3. Escolha sua atividade (ex: cabeleireiro, vendedor ambulante, costureira)
4. Informe endereço do negócio (pode ser sua casa)
5. Pronto! CNPJ sai na hora

ATENÇÃO: É DE GRAÇA. Se alguém cobrar, é golpe.
```

### Obrigações Mensais
```
Todo mês até dia 20:
  Pagar o DAS (boleto do MEI): ~R$75,60

  Como pagar:
  - App MEI (Receita Federal)
  - Site: gov.br/mei -> Pagamento
  - Débito automático (banco)
  - Boleto na lotérica

Todo ano até 31 de maio:
  Enviar DASN-SIMEI (declaração anual)
  - Site: gov.br/mei -> Declaração Anual
  - Informar quanto faturou no ano
  - Mesmo que faturou R$0, precisa declarar
```

## Arquivos Relacionados
- `backend/app/agent/tools/simulador_mei.py` - Simulador de impacto
- `backend/app/agent/tools/guia_mei.py` - Passo a passo
- `frontend/src/data/benefits/sectoral.json` - Benefícios setoriais

## Referências
- Portal do Empreendedor: https://gov.br/mei
- Lista de atividades MEI: https://www.gov.br/empresas-e-negocios/pt-br/empreendedor/quero-ser-mei
- Regras Bolsa Família + MEI: https://www.gov.br/mds/pt-br/noticias-e-conteudos/desenvolvimento-social/bolsa-familia
