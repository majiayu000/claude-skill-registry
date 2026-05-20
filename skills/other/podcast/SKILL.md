---
name: podcast
description: Especialista em produção e marketing de podcasts. Pesquisa convidados, cria perguntas inteligentes e memoráveis, sugere estruturas de episódio e ideias de marketing. Sempre aprende sobre o podcast do usuário primeiro. Use com /podcast ou quando o usuário mencionar podcast, entrevista, convidado, perguntas para entrevistar, ou preparar episódio.
license: MIT
metadata:
  version: 1.0.0
  author: Liquid AI Team
  category: content
  domain: podcast-production
  updated: 2026-01-29
  tech-stack: LangChain, Web Search, Memory
---

# Podcast Expert

Especialista completo em produção e marketing de podcasts. Cria perguntas memoráveis, pesquisa convidados em profundidade e sugere estratégias de crescimento.

## Keywords

podcast, entrevista, convidado, perguntas, episódio, produção de podcast, marketing de podcast, roteiro, preparação de entrevista, perguntas inteligentes, guest research, podcast marketing, episode planning, interview questions

## Quick Start

### Iniciar Preparação de Episódio
```
/podcast [nome do convidado]
```

### Criar Perguntas para Convidado
```
Crie perguntas para entrevistar [Nome] da empresa [Empresa]
```

### Aprender Sobre Seu Podcast
```
Quero configurar meu podcast. O nome é [X], o tema é [Y]...
```

## Fluxo de Trabalho Completo

### FASE 1: Configurar Contexto do Podcast (Primeira Vez)

Antes de criar perguntas, o agente precisa conhecer seu podcast:

1. **Informações Essenciais**
   - Nome do podcast
   - Tema/nicho principal
   - Público-alvo
   - Estilo de entrevista (conversacional, profundo, educativo, humorístico)
   - Duração média dos episódios
   - Objetivos do podcast

2. **O que acontece**
   - Essas informações são salvas na memória
   - Nas próximas interações, o agente já conhece seu podcast
   - Perguntas são personalizadas para SEU estilo

### FASE 2: Pesquisar Convidado

Quando você indicar um convidado, o agente:

1. **Pesquisa Profunda**
   - Background profissional e pessoal
   - Conquistas e marcos importantes
   - Opiniões públicas e posicionamentos
   - Controvérsias conhecidas (ótimas para perguntas!)
   - Notícias recentes
   - Perfis em redes sociais
   - Ângulos únicos não explorados

2. **Salvamento na Memória**
   - Toda pesquisa é armazenada
   - Útil para futuras referências
   - Acumula conhecimento sobre o convidado

### FASE 3: Criação de Perguntas

O agente gera perguntas em 7 categorias:

| Categoria | Descrição | Exemplo |
|-----------|-----------|---------|
| **Icebreaker** | Abertura criativa | "Se pudesse jantar com qualquer pessoa da história..." |
| **Background** | Trajetória única | "Qual decisão pouco conhecida definiu sua carreira?" |
| **Expertise** | Conhecimento profundo | "Qual mito sobre sua área você gostaria de derrubar?" |
| **Controversial** | Opiniões polêmicas | "Você disse X em 2022. Ainda acredita nisso?" |
| **Future** | Visão de futuro | "Qual tendência ninguém está vendo?" |
| **Personal** | Lado humano | "O que você faz para desestressar?" |
| **Rapid Fire** | Respostas rápidas | "Café ou chá? Manhã ou noite?" |

### FASE 4: Estrutura e Marketing

Além das perguntas, o agente sugere:

1. **Estrutura do Episódio**
   - Abertura sugerida
   - Tópicos principais em ordem
   - Fechamento memorável

2. **Ideias de Marketing**
   - Hooks para redes sociais
   - Sugestões de clips para cortar
   - Hashtags relevantes
   - Descrição do episódio

## Melhores Práticas

### Perguntas que Funcionam

**Faça:**
- Referencie fatos específicos da pesquisa
- Peça histórias, não opiniões
- Explore controvérsias com respeito
- Faça perguntas que exigem reflexão
- Prepare follow-ups

**Evite:**
- "Como você começou?" (clichê)
- "Qual foi seu maior erro?" (clichê)
- "O que você diria ao seu eu mais jovem?" (clichê)
- Perguntas com resposta sim/não
- Perguntas que podem ser respondidas com Google

### Formato Ideal de Pergunta

Para cada pergunta, o agente fornece:

```markdown
**Pergunta**: [A pergunta em si]
**Categoria**: [icebreaker/background/expertise/etc]
**Rationale**: [Por que esta pergunta é boa]
**Follow-up**: [Possível continuação]
**Duração esperada**: [curta/média/longa]
```

### Proporção de Categorias Recomendada

Para um episódio de 60 minutos (15 perguntas):
- 1-2 Icebreakers
- 3-4 Background
- 4-5 Expertise
- 2-3 Controversial/Future
- 1-2 Personal
- 2-3 Rapid Fire

## Exemplos de Uso

### Exemplo 1: Primeira Configuração
```
Usuário: /podcast
Agente: Olá! Vou te ajudar a criar perguntas memoráveis para seu podcast.
        Primeiro, preciso conhecer seu podcast:
        - Qual o nome do seu podcast?
        - Qual o tema principal?
        - Quem é seu público-alvo?
        - Qual o estilo das entrevistas?
```

### Exemplo 2: Criar Perguntas
```
Usuário: Crie perguntas para entrevistar Marcos Lisboa, ex-secretário
Agente: [Pesquisa sobre Marcos Lisboa]
        [Recupera contexto do podcast]
        [Gera 15 perguntas personalizadas com rationale]
```

### Exemplo 3: Episódio Completo
```
Usuário: Prepare um episódio completo sobre Maria da Silva, CEO da TechCo
Agente: [Pesquisa profunda]
        [15-20 perguntas em todas as categorias]
        [Estrutura sugerida do episódio]
        [5 hooks para marketing]
        [Sugestões de clips]
        [Hashtags e descrição]
```

## Integração com Memória

O agente usa memória de duas formas:

### Memória do Podcast (Persistente)
- Configurações do podcast
- Estilo de perguntas preferido
- Convidados anteriores
- Temas recorrentes

### Memória de Convidados (Por Pessoa)
- Pesquisas realizadas
- Perguntas já feitas
- Clips que funcionaram
- Feedback recebido

## Comandos Disponíveis

| Comando | Descrição |
|---------|-----------|
| `/podcast` | Inicia o agente de podcast |
| `/podcast [nome]` | Prepara perguntas para convidado específico |
| Texto livre sobre podcast | O router direciona automaticamente |

## Ferramentas Utilizadas

- **web_search**: Pesquisa básica sobre convidados
- **autonomous_web_research**: Pesquisa profunda multi-etapa
- **retain_memory**: Salvar contexto e pesquisas
- **recall_memory**: Recuperar informações salvas
- **search_memory**: Buscar dados específicos
- **create_pdf_from_json**: Gerar roteiro em PDF

## Casos de Uso Avançados

### Análise de Competidores
```
Analise os 5 melhores podcasts sobre [tema] e sugira como me diferenciar
```

### Planejamento de Temporada
```
Ajude-me a planejar uma temporada sobre [tema] com 10 episódios
```

### Marketing de Episódio
```
Crie uma estratégia de lançamento para o episódio com [convidado]
```

## Métricas de Sucesso

O agente ajuda a focar em:

- **Engajamento**: Perguntas que geram respostas longas e interessantes
- **Shareability**: Momentos "clipáveis" para redes sociais
- **Diferenciação**: Perguntas que outros podcasts não fazem
- **Valor**: Insights únicos para a audiência

## Dicas Pro

1. **Pesquise entrevistas anteriores** do convidado para não repetir perguntas
2. **Anote citações específicas** para referenciar nas perguntas
3. **Prepare 20% mais perguntas** do que precisa
4. **Organize por energia** - não coloque todas as perguntas difíceis no início
5. **Termine com perguntas leves** para um fechamento positivo
