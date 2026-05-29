---
name: economia-solidaria
description: Diretório de cooperativas e economia solidária
---

Catálogo de cooperativas, feiras solidárias, bancos comunitários e moedas sociais digitais.

## Contexto

- SENAES (Secretaria Nacional de Economia Solidária) reativada pelo governo atual
- Liga Coop tem 10.000+ motoristas cooperados em 20 cidades
- E-dinheiro opera moedas sociais digitais em comunidades
- Cooperativas são alternativa real à "uberização" do trabalho
- OIT aprovou regulamentação do trabalho em plataformas em 2025

## Categorias

### Tipos de Empreendimentos Solidários
```
├── Cooperativas de Trabalho
│   ├── Transporte (Liga Coop, Femob)
│   ├── Entregas (Senoritas Courier, PedaLá)
│   ├── Limpeza e serviços
│   └── Artesanato e produção
│
├── Cooperativas de Produção
│   ├── Agricultura familiar
│   ├── Pesca artesanal
│   ├── Costura e confecção
│   └── Reciclagem (catadores)
│
├── Bancos Comunitários
│   ├── Banco Palmas (CE)
│   ├── Banco Maré (RJ)
│   └── Rede de bancos comunitários
│
├── Moedas Sociais Digitais
│   ├── E-dinheiro (plataforma nacional)
│   ├── Palmas (Fortaleza)
│   ├── Mumbuca (Maricá/RJ)
│   └── Outras moedas locais
│
├── Feiras e Mercados
│   ├── Feiras orgânicas
│   ├── Feiras de agricultura familiar
│   └── Mercados solidários
│
└── Incubadoras e Apoio
    ├── ITCP (Incubadoras universitárias)
    ├── SENAES/MTE
    └── Fórum Brasileiro de Economia Solidária
```

## Implementação

### Busca de Cooperativas
```python
# backend/app/agent/tools/economia_solidaria.py
async def buscar_cooperativas(
    lat: float,
    lng: float,
    tipo: str = None,      # transporte, producao, servicos, catadores
    raio_km: float = 10,
) -> list[dict]:
    """Busca cooperativas e empreendimentos solidários próximos."""
    resultados = []

    # Base local (cadastradas)
    local = await db_buscar_cooperativas(lat, lng, raio_km, tipo)
    resultados.extend(local)

    # Google Places (complementar)
    termos = {
        "transporte": "cooperativa transporte",
        "producao": "cooperativa produção feira orgânica",
        "catadores": "cooperativa reciclagem catadores",
        "servicos": "cooperativa serviços",
    }
    termo = termos.get(tipo, "cooperativa economia solidária")
    google = await google_places_buscar(termo, lat, lng, raio_km * 1000)
    resultados.extend(google)

    return resultados

async def buscar_feiras(
    municipio_ibge: str = None,
    dia_semana: str = None,    # segunda, terca, ...
) -> list[dict]:
    """Busca feiras solidárias e de agricultura familiar."""
    return await db_buscar_feiras(municipio_ibge, dia_semana)
```

### Guia de Formalização de Cooperativa
```python
PASSOS_CRIAR_COOPERATIVA = [
    {
        "passo": 1,
        "titulo": "Reunir pessoas",
        "descricao": "Junte pelo menos 7 pessoas que querem trabalhar juntas no mesmo ramo.",
        "dica": "Todos precisam ter CPF e ser maiores de 16 anos.",
    },
    {
        "passo": 2,
        "titulo": "Definir o que a cooperativa vai fazer",
        "descricao": "Escolham a atividade principal: transporte, produção, serviços, etc.",
        "dica": "Pensem no que vocês já sabem fazer bem.",
    },
    {
        "passo": 3,
        "titulo": "Fazer a assembleia de fundação",
        "descricao": "Reunião oficial para criar a cooperativa. Todos votam e assinam a ata.",
        "documentos": ["Ata de assembleia", "Estatuto social", "Lista de presença"],
    },
    {
        "passo": 4,
        "titulo": "Registrar na Junta Comercial",
        "descricao": "Levar os documentos na Junta Comercial do seu estado.",
        "custo": "Varia por estado (geralmente R$100-300)",
    },
    {
        "passo": 5,
        "titulo": "Tirar CNPJ",
        "descricao": "Cadastrar na Receita Federal pelo site gov.br.",
        "custo": "Gratuito",
    },
    {
        "passo": 6,
        "titulo": "Buscar apoio",
        "descricao": "Procure a ITCP (incubadora) da universidade mais perto ou o SENAES.",
        "dica": "O apoio da incubadora é GRATUITO e ajuda muito.",
    },
]
```

### Integração com Moedas Sociais
```python
async def buscar_moeda_social(municipio: str) -> dict | None:
    """Verifica se existe moeda social digital no município."""
    moedas = {
        "FORTALEZA": {"nome": "Palmas", "banco": "Banco Palmas", "plataforma": "E-dinheiro"},
        "MARICA": {"nome": "Mumbuca", "banco": "Banco Mumbuca", "plataforma": "Mumbuca Digital"},
        "SAO PAULO": {"nome": "Sampa", "banco": "Banco Comunitário União Sampaio", "plataforma": "E-dinheiro"},
    }
    return moedas.get(municipio.upper())
```

## Programas de Fomento
```
📋 PAA (Programa de Aquisição de Alimentos)
  - Governo compra da agricultura familiar
  - Valor: até R$12.000/ano por produtor
  - Onde: CONAB ou Prefeitura

📋 PNAE (Merenda Escolar)
  - 30% da merenda deve vir da agricultura familiar
  - Onde: Secretaria de Educação do município

📋 PRONAF (Crédito Rural)
  - Crédito para cooperativas rurais
  - Juros reduzidos
  - Onde: Banco do Brasil, Banco do Nordeste

📋 Programa Nacional de Economia Solidária
  - Capacitação e assistência técnica
  - Onde: SENAES/MTE ou Fórum de Economia Solidária
```

## Mensagens (Linguagem Simples)

### Cooperativa Encontrada
```
Achei cooperativas perto de você:

🤝 {{nome}}
📍 {{endereco}} ({{distancia}} km)
📞 {{telefone}}
💼 Trabalha com: {{atividade}}

Cooperativa é um grupo de pessoas que trabalham juntas
e dividem os ganhos de forma justa. Diferente de empresa,
todo mundo tem o mesmo poder de decisão.

Quer saber como participar?
```

## Arquivos Relacionados
- `backend/app/agent/tools/economia_solidaria.py` - Tool do agente
- `backend/app/models/cooperativa.py` - Modelo de dados
- `backend/app/jobs/dados_abertos/cooperativas.py` - Ingestão de dados

## Referências
- SENAES: https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/economia-solidaria
- SIES (Sistema de Informações): https://sies.ecosol.org.br
- E-dinheiro: https://www.yoururl.com.br/edinheiro
- Fórum Brasileiro de Economia Solidária: https://fbes.org.br
- Liga Coop: https://www.ligacoop.com.br
