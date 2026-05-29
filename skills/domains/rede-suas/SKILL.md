---
name: rede-suas
description: Navegação na rede SUAS (CRAS/CREAS/CAPS/Centro POP)
---

Mapeamento completo dos equipamentos do Sistema Único de Assistência Social com fluxos de encaminhamento.

## Contexto

- SUAS tem proteção básica (CRAS) e especial (CREAS, Centro POP)
- 8.000+ CRAS, 2.800+ CREAS no Brasil
- Cidadão não sabe a diferença entre CRAS e CREAS
- Cada equipamento oferece serviços específicos

## Hierarquia SUAS

```
SUAS (Sistema Único de Assistência Social)
│
├── PROTEÇÃO SOCIAL BÁSICA (prevenção)
│   └── CRAS - Centro de Referência de Assistência Social
│       ├── PAIF - Serviço de Proteção e Atendimento Integral à Família
│       ├── SCFV - Serviço de Convivência e Fortalecimento de Vínculos
│       ├── CadÚnico - Cadastramento
│       └── Encaminhamentos para benefícios
│
├── PROTEÇÃO SOCIAL ESPECIAL - Média Complexidade
│   └── CREAS - Centro de Referência Especializado
│       ├── PAEFI - Atendimento a famílias com direitos violados
│       ├── Medidas Socioeducativas (adolescentes)
│       ├── Abordagem Social (população de rua)
│       └── Acompanhamento de vítimas de violência
│
├── PROTEÇÃO SOCIAL ESPECIAL - Alta Complexidade
│   ├── Abrigo Institucional (crianças, adultos, idosos)
│   ├── Casa de Passagem (acolhimento emergencial)
│   ├── Casa Lar (grupos pequenos)
│   ├── República (jovens egressos, idosos)
│   └── Família Acolhedora
│
└── GESTÃO
    ├── Conselho Municipal de Assistência Social (CMAS)
    ├── Fundo Municipal de Assistência Social (FMAS)
    └── Secretaria Municipal de Assistência Social
```

## Serviços por Equipamento

### CRAS
```
Em linguagem simples:

"O CRAS é o lugar do governo mais perto de você para
pedir ajuda. É de graça e não precisa de encaminhamento."

Serviços:
- Fazer CadÚnico (porta de entrada para benefícios)
- Atendimento familiar (conversa com assistente social)
- Grupos de convivência (crianças, jovens, idosos)
- Encaminhar para benefícios (Bolsa Família, BPC, etc.)
- Orientar sobre moradia, trabalho, documentos
- Encaminhar para CREAS se necessário
```

### CREAS
```
"O CREAS ajuda pessoas que tiveram seus direitos
desrespeitados: violência, abandono, abuso, exploração."

Serviços:
- Atendimento a vítimas de violência (doméstica, sexual)
- Proteção de crianças e adolescentes
- Proteção de idosos vítimas de maus-tratos
- Atendimento a pessoas com deficiência violentadas
- Acompanhamento de adolescentes em medida socioeducativa
- Abordagem social (pessoas em situação de rua)
```

### Centro POP
```
"O Centro POP é para quem está na rua. Lá tem banho,
comida, lugar pra descansar e ajuda pra conseguir
documentos e benefícios."

Serviços:
- Higiene pessoal (banho, lavanderia)
- Alimentação
- Ajuda com documentos (RG, CPF)
- Encaminhamento para saúde
- Cadastro no CadÚnico
- Encaminhamento para abrigo
```

## Busca de Equipamentos

### API Expandida
```python
# backend/app/routers/nearby.py
@router.get("/api/v1/nearby/suas")
async def buscar_equipamento_suas(
    lat: float,
    lng: float,
    tipo: str = "cras",  # cras, creas, centro_pop, abrigo
    limit: int = 5,
) -> list[EquipamentoSUAS]:
    """Busca equipamentos SUAS por proximidade."""
    resultados_local = await db_buscar(tipo, lat, lng, limit)
    if len(resultados_local) < limit:
        resultados_google = await google_places_buscar(tipo, lat, lng)
        resultados_local.extend(resultados_google)
    return resultados_local[:limit]
```

### Fontes de Dados
```python
FONTES_EQUIPAMENTOS = {
    "cras": {
        "censo_suas": "https://aplicacoes.mds.gov.br/snas/vigilancia/index2.php",
        "google_places": "CRAS Centro de Referência de Assistência Social",
        "campos": ["endereco", "telefone", "horario", "coordenador"],
    },
    "creas": {
        "censo_suas": "mesma base, filtro diferente",
        "google_places": "CREAS Centro de Referência Especializado",
    },
    "centro_pop": {
        "google_places": "Centro POP população de rua",
    },
    "caps": {
        "cnes_datasus": "http://cnes.datasus.gov.br/",
        "google_places": "CAPS Centro de Atenção Psicossocial",
    },
}
```

## Fluxo de Decisão no Agente
```python
# backend/app/agent/tools/classificar_necessidade_suas.py
async def classificar_e_encaminhar(mensagem: str, perfil: dict) -> dict:
    """Classifica a necessidade e encaminha para equipamento correto."""

    classificacao = await classificar_com_ia(mensagem)

    encaminhamentos = {
        "beneficio": {"equipamento": "CRAS", "servico": "CadÚnico / Benefícios"},
        "violencia": {"equipamento": "CREAS", "servico": "PAEFI", "urgente": True},
        "situacao_rua": {"equipamento": "Centro POP", "servico": "Acolhimento"},
        "saude_mental": {"equipamento": "CAPS", "servico": "Acolhimento"},
        "crianca_risco": {"equipamento": "Conselho Tutelar", "urgente": True},
        "documento": {"equipamento": "CRAS", "servico": "Encaminhamento"},
        "trabalho": {"equipamento": "CRAS", "servico": "Inclusão Produtiva"},
        "idoso_risco": {"equipamento": "CREAS", "servico": "PAEFI", "urgente": True},
    }

    enc = encaminhamentos.get(classificacao["tipo"], encaminhamentos["beneficio"])

    if perfil.get("latitude") and perfil.get("longitude"):
        unidade = await buscar_equipamento_suas(
            lat=perfil["latitude"],
            lng=perfil["longitude"],
            tipo=enc["equipamento"].lower().replace(" ", "_"),
        )
        enc["unidade"] = unidade[0] if unidade else None

    return enc
```

## Arquivos Relacionados
- `backend/app/routers/nearby.py` - API de busca por proximidade
- `backend/app/agent/tools/buscar_cras.py` - Busca CRAS (existente)
- `backend/app/agent/tools/classificar_necessidade_suas.py` - Classificador
- `backend/app/models/equipamento_suas.py` - Modelo de dados

## Fontes de Dados Oficiais
- Censo SUAS: https://aplicacoes.mds.gov.br/snas/vigilancia/
- CNES/DataSUS (CAPS): http://cnes.datasus.gov.br/
- Mapa SUAS: https://mapas.mds.gov.br/
- NOB-SUAS: https://www.gov.br/mds/pt-br/acoes-e-programas/suas
