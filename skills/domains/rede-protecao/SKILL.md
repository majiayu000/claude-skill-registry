---
name: rede-protecao
description: Rede de proteção social e encaminhamento de urgência
---

Mapeamento integrado de toda a rede de proteção social brasileira com fluxograma interativo de encaminhamento.

## Contexto

- Cidadão em crise não sabe a quem recorrer
- Rede fragmentada: CRAS, CREAS, Conselho Tutelar, Defensoria, CAPS, UBS
- Cada minuto conta em situação de violência, risco ou emergência
- Linguagem simples é essencial para público vulnerável

## Equipamentos da Rede

### Assistência Social (SUAS)
| Equipamento | Função | Público |
|-------------|--------|---------|
| **CRAS** | Prevenção, cadastros, benefícios | Famílias em vulnerabilidade |
| **CREAS** | Proteção especial, violência, abuso | Pessoas com direitos violados |
| **Centro POP** | Atendimento população de rua | Pessoas em situação de rua |
| **Abrigo/Casa de Passagem** | Acolhimento temporário | Pessoas sem moradia |
| **Casa Lar** | Acolhimento crianças/adolescentes | Crianças afastadas da família |

### Saúde
| Equipamento | Função | Público |
|-------------|--------|---------|
| **UBS** | Saúde básica, vacinas, pré-natal | Toda a população |
| **CAPS** | Saúde mental, álcool, drogas | Pessoas com sofrimento psíquico |
| **CAPS AD** | Álcool e drogas | Dependentes químicos |
| **CAPSi** | Saúde mental infantojuvenil | Crianças e adolescentes |
| **UPA/SAMU** | Emergência | Urgências de saúde |

### Justiça e Direitos
| Equipamento | Função | Público |
|-------------|--------|---------|
| **Defensoria Pública** | Assistência jurídica gratuita | Quem não pode pagar advogado |
| **Conselho Tutelar** | Proteção de crianças | Crianças/adolescentes em risco |
| **Delegacia da Mulher** | Violência contra mulher | Mulheres vítimas de violência |
| **Ministério Público** | Direitos coletivos | Comunidades e grupos |

## Telefones de Emergência
```
EMERGÊNCIAS:
  190 - Polícia Militar
  192 - SAMU (saúde)
  193 - Bombeiros

PROTEÇÃO:
  100 - Disque Direitos Humanos (crianças, idosos, PCD)
  180 - Central de Atendimento à Mulher
  188 - CVV (prevenção ao suicídio)
  181 - Disque Denúncia

SERVIÇOS:
  121 - INSS / Previdência
  111 - CadÚnico / Bolsa Família
  156 - Prefeitura (varia por município)
```

## Fluxograma de Encaminhamento

### "Meu problema é..."
```
├── "Preciso de comida / dinheiro / benefício"
│   └── CRAS (cadastro + benefícios)
│
├── "Sofro violência em casa"
│   ├── Mulher → Ligue 180 + Delegacia da Mulher + CREAS
│   ├── Criança → Ligue 100 + Conselho Tutelar + CREAS
│   └── Idoso → Ligue 100 + CREAS + Delegacia
│
├── "Estou na rua / sem moradia"
│   └── Centro POP + CRAS (cadastro) + Abrigo
│
├── "Problema de saúde mental / drogas"
│   ├── Crise aguda → SAMU 192 + CAPS
│   ├── Tratamento → CAPS / CAPS AD
│   └── Criança → CAPSi
│
├── "Preciso de remédio"
│   ├── Receita médica → Farmácia Popular
│   └── Sem receita → UBS primeiro
│
├── "Problema com documento / justiça"
│   ├── Sem documentos → CRAS (encaminha para 2ª via)
│   ├── Problema trabalhista → Defensoria Pública
│   └── Problema com benefício negado → Defensoria Pública
│
├── "Meu filho está em perigo"
│   └── Conselho Tutelar + Ligue 100
│
├── "Pensando em me machucar"
│   └── CVV 188 (24h) + CAPS
│
└── "Outro problema"
    └── CRAS (porta de entrada da rede)
```

## Implementação no Agente

### Tool de Encaminhamento
```python
# backend/app/agent/tools/rede_protecao.py
from enum import Enum

class TipoNecessidade(str, Enum):
    BENEFICIO = "beneficio"
    VIOLENCIA = "violencia"
    MORADIA = "moradia"
    SAUDE_MENTAL = "saude_mental"
    MEDICAMENTO = "medicamento"
    DOCUMENTOS = "documentos"
    CRIANCA_RISCO = "crianca_risco"
    EMERGENCIA = "emergencia"
    JURIDICO = "juridico"

ENCAMINHAMENTOS = {
    TipoNecessidade.BENEFICIO: {
        "primario": "CRAS",
        "telefone": "111",
        "acao": "Vá ao CRAS mais perto com seus documentos.",
        "documentos": ["CPF", "Comprovante de endereço"],
    },
    TipoNecessidade.VIOLENCIA: {
        "primario": "CREAS",
        "telefones": {"mulher": "180", "crianca": "100", "geral": "190"},
        "acao": "Ligue agora. Você não precisa passar por isso sozinha.",
        "urgente": True,
    },
    TipoNecessidade.MORADIA: {
        "primario": "Centro POP",
        "secundario": "CRAS",
        "acao": "Procure o Centro POP mais perto. Lá tem acolhimento e comida.",
    },
    TipoNecessidade.SAUDE_MENTAL: {
        "primario": "CAPS",
        "telefone_crise": "192",
        "telefone_apoio": "188",
        "acao": "O CVV atende 24 horas pelo 188. Você não está sozinho.",
        "urgente": True,
    },
}

async def encaminhar_rede_protecao(
    necessidade: TipoNecessidade,
    latitude: float = None,
    longitude: float = None,
    detalhes: str = None,
) -> dict:
    """Identifica o serviço correto e fornece encaminhamento."""
    encaminhamento = ENCAMINHAMENTOS[necessidade]

    # Buscar unidade mais próxima se tiver localização
    if latitude and longitude:
        unidade = await buscar_equipamento_proximo(
            tipo=encaminhamento["primario"],
            lat=latitude,
            lng=longitude
        )
        encaminhamento["unidade_proxima"] = unidade

    return encaminhamento
```

### Detecção de Urgência no Chat
```python
# backend/app/agent/tools/detectar_urgencia.py
PALAVRAS_URGENCIA = {
    "alto": ["suicídio", "me matar", "não aguento mais", "acabar com tudo",
             "apanho", "me bate", "abuso", "estupro"],
    "medio": ["violência", "ameaça", "medo", "rua", "fome",
              "desespero", "sem saída", "droga"],
}

async def detectar_urgencia(mensagem: str) -> dict:
    """Detecta sinais de urgência na mensagem do cidadão."""
    mensagem_lower = mensagem.lower()

    for palavra in PALAVRAS_URGENCIA["alto"]:
        if palavra in mensagem_lower:
            return {
                "nivel": "ALTO",
                "acao_imediata": True,
                "servico": "CVV 188 ou SAMU 192",
                "mensagem": "Você está passando por algo muito difícil. "
                           "Ligue agora pro 188 (CVV) - atende 24 horas, "
                           "é de graça e é sigiloso."
            }

    for palavra in PALAVRAS_URGENCIA["medio"]:
        if palavra in mensagem_lower:
            return {
                "nivel": "MEDIO",
                "acao_imediata": False,
                "encaminhamento": "rede_protecao"
            }

    return {"nivel": "NORMAL"}
```

## Mensagens ao Usuário (Linguagem Simples)

### Situação de Violência
```
Você não tem culpa. Ninguém tem o direito de te machucar.

Ligue agora:
  180 - Central da Mulher (24h, gratuito, sigiloso)
  190 - Polícia

O CREAS pode te ajudar com proteção e acompanhamento.
O mais perto de você fica em: [endereço]
```

### Situação de Rua
```
Você tem direitos mesmo sem endereço fixo.

Procure o Centro POP:
  [endereço mais próximo]
  Lá tem: banho, comida, lugar pra dormir e ajuda pra conseguir documentos.

Você pode se cadastrar no CadÚnico mesmo sem endereço.
  O CRAS pode te ajudar com isso.
```

### Saúde Mental
```
Tudo bem não estar bem. Pedir ajuda é um ato de coragem.

CVV - 188 (24 horas, gratuito, sigiloso)
  Você pode ligar, mandar mensagem ou acessar cvv.org.br

O CAPS atende de graça e sem precisar de encaminhamento.
  O mais perto: [endereço]
```

## Arquivos Relacionados
- `backend/app/agent/tools/rede_protecao.py` - Tool de encaminhamento
- `backend/app/agent/tools/detectar_urgencia.py` - Detector de urgência
- `backend/app/agent/tools/buscar_cras.py` - Busca CRAS (existente)
- `backend/app/routers/nearby.py` - Endpoint de busca por proximidade

## Fontes de Dados
- **CRAS/CREAS**: Censo SUAS (MDS) - atualização anual
- **CAPS**: CNES/DataSUS - Cadastro Nacional de Estabelecimentos de Saúde
- **Conselhos Tutelares**: SIPIA/CONANDA
- **Defensorias**: DPU + Defensorias Estaduais
