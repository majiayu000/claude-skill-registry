---
name: pesquisa-campo
description: Pesquisa de campo digital com questionários e análise
---

Templates de questionários, coleta offline e análise qualitativa para entender necessidades reais dos usuários.

## Contexto

- Decisões de produto devem ser baseadas em dados do público real
- Público-alvo tem baixa escolaridade — questionários precisam ser simples
- Coleta pode ser presencial (CRAS, mutirões) ou via WhatsApp
- Análise qualitativa com IA categoriza respostas abertas

## Templates de Questionário

### 1. Satisfação do Usuário (NPS Adaptado)
```json
{
  "titulo": "O que você achou do Tá na Mão?",
  "perguntas": [
    {
      "id": "q1",
      "texto": "O Tá na Mão te ajudou a descobrir algum benefício?",
      "tipo": "escolha_unica",
      "opcoes": ["Sim, descobri benefícios novos", "Sim, mas eu já sabia", "Não me ajudou"]
    },
    {
      "id": "q2",
      "texto": "Foi fácil de usar?",
      "tipo": "escala",
      "opcoes": ["Muito difícil", "Difícil", "Normal", "Fácil", "Muito fácil"],
      "emoji": ["😫", "😕", "😐", "🙂", "😊"]
    },
    {
      "id": "q3",
      "texto": "Você indicaria o Tá na Mão pra alguém?",
      "tipo": "escala",
      "opcoes": ["Com certeza não", "Acho que não", "Talvez", "Acho que sim", "Com certeza sim"]
    },
    {
      "id": "q4",
      "texto": "O que mais te ajudou?",
      "tipo": "multipla_escolha",
      "opcoes": ["Ver meus benefícios", "Lista de documentos", "Achar o CRAS", "Dinheiro esquecido", "Farmácia Popular"]
    },
    {
      "id": "q5",
      "texto": "O que você gostaria que tivesse no app?",
      "tipo": "texto_livre",
      "placeholder": "Fale o que quiser..."
    }
  ]
}
```

### 2. Necessidades do Cidadão (Discovery)
```json
{
  "titulo": "Queremos te conhecer melhor",
  "perguntas": [
    {
      "id": "n1",
      "texto": "Qual a sua maior dificuldade pra conseguir benefícios?",
      "tipo": "multipla_escolha",
      "opcoes": [
        "Não sei quais tenho direito",
        "Não sei onde ir",
        "Falta de documentos",
        "Fila muito grande no CRAS",
        "Não entendo a linguagem",
        "Não tenho internet"
      ]
    },
    {
      "id": "n2",
      "texto": "Como você ficou sabendo dos seus benefícios?",
      "tipo": "multipla_escolha",
      "opcoes": ["Vizinho/amigo", "CRAS", "Igreja/comunidade", "Internet", "TV/rádio", "Não sabia"]
    },
    {
      "id": "n3",
      "texto": "Você usa celular pra quê?",
      "tipo": "multipla_escolha",
      "opcoes": ["WhatsApp", "Facebook", "YouTube", "Caixa Tem", "Nada disso"]
    },
    {
      "id": "n4",
      "texto": "Alguém te ajuda a mexer no celular?",
      "tipo": "escolha_unica",
      "opcoes": ["Faço sozinho(a)", "Filho(a) me ajuda", "Vizinho/amigo ajuda", "Não mexo no celular"]
    }
  ]
}
```

### 3. Avaliação de Atendimento (CRAS)
```json
{
  "titulo": "Como foi seu atendimento no CRAS?",
  "perguntas": [
    {
      "id": "a1",
      "texto": "Quanto tempo esperou na fila?",
      "tipo": "escolha_unica",
      "opcoes": ["Menos de 30 min", "30 min a 1 hora", "1 a 2 horas", "Mais de 2 horas", "Não consegui ser atendido"]
    },
    {
      "id": "a2",
      "texto": "A pessoa que te atendeu explicou tudo direitinho?",
      "tipo": "escala",
      "opcoes": ["Não explicou nada", "Explicou pouco", "Explicou bem", "Explicou muito bem"]
    },
    {
      "id": "a3",
      "texto": "Resolveu o que você precisava?",
      "tipo": "escolha_unica",
      "opcoes": ["Sim, tudo", "Sim, em parte", "Não, preciso voltar", "Não resolveu nada"]
    }
  ]
}
```

## Coleta de Dados

### Via App/Web
```python
# backend/app/routers/pesquisa.py
@router.post("/api/v1/pesquisa/{questionario_id}/resposta")
async def registrar_resposta(
    questionario_id: str,
    resposta: RespostaQuestionario,
):
    """Registra resposta de questionário (anonimizada)."""
    # NÃO armazenar dados identificáveis
    registro = {
        "questionario_id": questionario_id,
        "respostas": resposta.respostas,
        "metadata": {
            "canal": resposta.canal,  # app, web, whatsapp, presencial
            "municipio_ibge": resposta.municipio_ibge,  # opcional
            "timestamp": datetime.utcnow(),
        },
        # SEM: cpf, nome, telefone, endereço
    }
    await db.pesquisas.insert_one(registro)
    return {"mensagem": "Obrigado por responder!"}
```

### Via WhatsApp
```python
# Fluxo de pesquisa via WhatsApp
FLUXO_PESQUISA_WHATSAPP = {
    "inicio": {
        "mensagem": "Oi! Podemos te fazer 3 perguntas rápidas pra melhorar o Tá na Mão? É anônimo.",
        "botoes": ["Sim, pode perguntar", "Agora não"],
    },
    "pergunta_1": {
        "mensagem": "O Tá na Mão te ajudou a descobrir algum benefício?\n\n1️⃣ Sim\n2️⃣ Não\n3️⃣ Ainda não usei direito",
        "espera": "numero",
    },
    # ...
}
```

### Offline (Presencial)
```typescript
// frontend/src/services/pesquisa-offline.ts
export class PesquisaOfflineService {
  async salvarRespostaLocal(questionarioId: string, respostas: Record<string, any>) {
    // Salvar no IndexedDB quando sem internet
    await db.formulariosPendentes.add({
      tipo: 'pesquisa',
      endpoint: `/api/v1/pesquisa/${questionarioId}/resposta`,
      dados: { respostas, canal: 'presencial' },
      timestamp: Date.now(),
      sincronizado: 0,
    });
  }
}
```

## Análise com IA

### Categorização de Respostas Abertas
```python
# backend/app/services/analise_pesquisa.py
async def categorizar_respostas_abertas(
    respostas: list[str],
    contexto: str,
) -> dict:
    """Usa IA para categorizar respostas de texto livre."""
    prompt = f"""
    Categorize estas respostas de uma pesquisa com cidadãos de baixa renda
    sobre o app Tá na Mão ({contexto}):

    Respostas:
    {chr(10).join(f'- {r}' for r in respostas)}

    Retorne em JSON:
    1. categorias: lista de categorias identificadas com contagem
    2. sentimento_geral: positivo, neutro ou negativo
    3. insights_principais: top 3 descobertas
    4. sugestoes_acao: o que fazer com essas informações
    """
    return await agent.analyze(prompt)
```

### Relatório de Pesquisa
```python
async def gerar_relatorio_pesquisa(questionario_id: str) -> dict:
    """Gera relatório consolidado de um questionário."""
    respostas = await buscar_respostas(questionario_id)

    return {
        "questionario_id": questionario_id,
        "total_respostas": len(respostas),
        "periodo": {"inicio": min_data, "fim": max_data},
        "por_canal": contar_por_canal(respostas),
        "resumo_por_pergunta": resumir_por_pergunta(respostas),
        "analise_texto_livre": await categorizar_respostas_abertas(
            [r["q5"] for r in respostas if r.get("q5")],
            contexto="sugestões de melhorias"
        ),
        "nps_score": calcular_nps(respostas),
    }
```

## Arquivos Relacionados
- `backend/app/routers/pesquisa.py` - Endpoints de pesquisa
- `backend/app/services/analise_pesquisa.py` - Análise com IA
- `frontend/src/components/Questionario.tsx` - Componente de formulário
- `frontend/src/services/pesquisa-offline.ts` - Coleta offline

## Ética e Privacidade
- Participação sempre voluntária
- Respostas 100% anônimas (sem CPF, nome, telefone)
- Dados agregados — mínimo 10 respostas para gerar relatório
- Consentimento explícito antes de cada pesquisa
- Direito de desistir a qualquer momento
