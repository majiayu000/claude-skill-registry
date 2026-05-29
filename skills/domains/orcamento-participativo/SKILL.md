---
name: orcamento-participativo
description: Orçamento participativo digital
---

Módulo para conectar cidadãos a processos de orçamento participativo municipal, estadual e federal.

## Contexto

- Governo Federal lançou ferramenta nacional de Orçamento Participativo em jan/2026 (400 municípios)
- Piauí opera OPA com R$80M em investimentos decididos por votação popular
- São Paulo tem "Orçamento Cidadão" com votação online
- Maranhão aceita votos pelo WhatsApp
- Brasil Participativo tem 1,5 milhão de usuários registrados

## Funcionalidades

### 1. Descobrir Consultas Abertas
```python
# backend/app/agent/tools/orcamento_participativo.py
async def buscar_consultas_abertas(
    municipio_ibge: str = None,
    uf: str = None,
) -> list[dict]:
    """Busca consultas/votações abertas no município ou estado."""
    consultas = []

    # Federal - Brasil Participativo
    federal = await buscar_brasil_participativo()
    consultas.extend(federal)

    # Estadual
    if uf:
        estadual = await buscar_consultas_estaduais(uf)
        consultas.extend(estadual)

    # Municipal
    if municipio_ibge:
        municipal = await buscar_consultas_municipais(municipio_ibge)
        consultas.extend(municipal)

    # Filtrar apenas abertas
    agora = datetime.now()
    abertas = [c for c in consultas if c["data_inicio"] <= agora <= c["data_fim"]]

    return abertas
```

### 2. Explicar Propostas em Linguagem Simples
```python
async def explicar_proposta(proposta: dict) -> dict:
    """Traduz proposta orçamentária para linguagem de 5ª série."""
    prompt = f"""
    Explique esta proposta de orçamento participativo em linguagem
    muito simples (para pessoa com escolaridade de 5ª série):

    Título: {proposta['titulo']}
    Descrição: {proposta['descricao']}
    Valor: R$ {proposta['valor']:,.2f}
    Área: {proposta['area']}

    Responda com:
    1. O que é isso? (1 frase simples)
    2. Como vai me ajudar? (1 frase)
    3. Quanto custa? (valor em contexto, ex: "dá pra construir 2 creches")
    """
    return await agent.analyze(prompt)
```

### 3. Notificações de Período de Votação
```python
# backend/app/jobs/notificacoes_orcamento.py
async def verificar_e_notificar():
    """Notifica usuários sobre períodos de votação."""
    usuarios = await get_usuarios_com_municipio()

    for usuario in usuarios:
        consultas = await buscar_consultas_abertas(
            municipio_ibge=usuario.municipio_ibge,
            uf=usuario.uf,
        )

        novas = [c for c in consultas if c["id"] not in usuario.consultas_notificadas]

        for consulta in novas:
            await enviar_notificacao(
                usuario=usuario,
                mensagem=f"Tem votação aberta na sua cidade! "
                         f"{consulta['titulo']}. "
                         f"Você pode votar até {consulta['data_fim'].strftime('%d/%m')}.",
                canal=usuario.canal_preferido,  # app, whatsapp, sms
            )
```

### 4. Guia de Como Votar
```python
GUIA_VOTACAO = {
    "brasil_participativo": {
        "passos": [
            "Entre no site brasilparticipativo.presidencia.gov.br",
            "Faça login com sua conta Gov.br",
            "Escolha a consulta da sua cidade",
            "Leia as propostas (ou peça pra gente explicar!)",
            "Vote nas que você acha mais importante",
        ],
        "requisitos": "Conta Gov.br (qualquer nível)",
        "prazo": "Varia por consulta",
    },
    "presencial": {
        "passos": [
            "Vá ao local de votação (geralmente escola ou centro comunitário)",
            "Leve RG e CPF",
            "Escolha as propostas no papel ou urna eletrônica",
        ],
        "requisitos": "Documento com foto",
    },
    "whatsapp": {
        "passos": [
            "Salve o número oficial do orçamento participativo",
            "Mande OI para iniciar",
            "Escolha a proposta pelo número",
            "Confirme seu voto",
        ],
        "requisitos": "WhatsApp ativo",
    },
}
```

## Modelo de Dados
```python
# backend/app/models/consulta_participativa.py
class ConsultaParticipativa(Base):
    __tablename__ = "consultas_participativas"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str]
    descricao: Mapped[str]
    esfera: Mapped[str]          # federal, estadual, municipal
    municipio_ibge: Mapped[str | None]
    uf: Mapped[str | None]
    data_inicio: Mapped[datetime]
    data_fim: Mapped[datetime]
    url_votacao: Mapped[str]
    canal_votacao: Mapped[list]   # ["web", "presencial", "whatsapp"]
    valor_total: Mapped[float | None]
    status: Mapped[str]          # aberta, encerrada, em_apuracao, concluida
    fonte: Mapped[str]           # brasil_participativo, prefeitura, governo_estado
```

## Mensagens (Linguagem Simples)

### Consulta Aberta
```
Tem votação aberta na sua cidade!

📋 {{titulo}}
💰 Valor: R$ {{valor}}
📅 Você pode votar até {{data_fim}}
🗳️ Como votar: {{canais}}

Quer que eu explique as propostas uma por uma?
Manda SIM.
```

### Explicação de Proposta
```
Proposta: {{titulo}}

O que é: {{explicacao_simples}}
Como te ajuda: {{impacto_pessoal}}
Quanto custa: {{valor_em_contexto}}

Quer votar nessa? Acesse: {{url}}
```

## Arquivos Relacionados
- `backend/app/agent/tools/orcamento_participativo.py` - Tool do agente
- `backend/app/models/consulta_participativa.py` - Modelo de dados
- `backend/app/jobs/notificacoes_orcamento.py` - Job de notificações

## Referências
- Brasil Participativo: https://brasilparticipativo.presidencia.gov.br
- OPA Piauí: https://opa.seplan.pi.gov.br
- São Paulo Orçamento Cidadão: https://www.prefeitura.sp.gov.br/cidade/secretarias/governo/participacao_social/orcamento_cidadao
