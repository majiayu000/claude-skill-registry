---
name: cliente:criar-a-partir-video
scope: domain
target: plataforma-b2b-educational-platform
description: |
  Skill especializada para USUÁRIOS FINAIS (clientes) que desejam criar cursos na
  plataforma Plataforma B2B de treinamento técnico corporativo a partir de vídeos do YouTube. Esta skill utiliza um FLUXO
  DE DIAGNÓSTICO INTERATIVO para adaptar a estrutura às características do conteúdo.

  IMPORTANTE: A estrutura do curso é FLEXÍVEL e determinada pelo diagnóstico inicial.
  Não há número fixo de seções, módulos ou formato predefinido. A skill analisa o
  input do usuário (vídeo único, playlist, série de vídeos) e propõe estrutura adequada.

  O processo é COLABORATIVO: após análise inicial, Claude apresenta proposta de
  estrutura e solicita validação/ajustes do usuário antes de prosseguir. Isso garante
  que cursos curtos (1h) e longos (100h+) sejam tratados apropriadamente.

  Formatos de entrada suportados: vídeo único curto (<1h), vídeo único longo (1-10h),
  playlist do YouTube, múltiplos vídeos avulsos, série de vídeos relacionados,
  webinars gravados, lives arquivadas, tutoriais sequenciais.

  A skill guia desde a extração de transcrições até a geração de código React/JSX,
  adaptando padrões de transformação conforme complexidade identificada no diagnóstico.

keywords: |
  transcricao, video, youtube, curso, criar-curso, transformar-video,
  youtube-transcript, playlist, video-longo, video-curto, serie-videos,
  diagnostico, flexivel, adaptativo, estrutura-dinamica, cliente,
  usuario-final, conteudo-educacional, b2b, webinar, tutorial

allowed-tools: |
  Read, Write, Edit, Bash, Grep, Glob
---

# Skill: Criar Curso a partir de Vídeo

> **Guia Flexível para Usuários Finais**
>
> **Versão:** 2.0.0
> **Última Atualização:** 2025-11-24
> **Público-Alvo:** Clientes/Criadores de Conteúdo
> **Abordagem:** Diagnóstico Interativo + Estrutura Adaptativa

---

## Índice

1. [Filosofia da Skill](#-filosofia-da-skill)
2. [Fluxo de Diagnóstico](#-fluxo-de-diagn%C3%B3stico)
3. [Tipos de Input Suportados](#-tipos-de-input-suportados)
4. [Processo Interativo](#-processo-interativo)
5. [Etapas de Execução](#-etapas-de-execu%C3%A7%C3%A3o)
6. [Padrões de Transformação](#-padr%C3%B5es-de-transforma%C3%A7%C3%A3o)
7. [Exemplos por Cenário](#-exemplos-por-cen%C3%A1rio)
8. [Troubleshooting](#-troubleshooting)
9. [Referências](#-refer%C3%AAncias)

---

## Filosofia da Skill

### Princípios Fundamentais

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ESTRUTURA = f(CONTEÚDO)                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ❌ ERRADO: "Todo curso tem 4 seções e 16 módulos"                  │
│                                                                     │
│  ✅ CORRETO: "A estrutura emerge do diagnóstico do conteúdo"        │
│                                                                     │
│  • Vídeo de 30min → Pode ser 1 módulo único                        │
│  • Playlist de 50 vídeos → Pode ser 5 seções com 10 módulos cada   │
│  • Curso de 100h → Pode precisar de hierarquia adicional           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### O que NÃO é fixo:

- ~~4 seções~~ → Número de seções definido pelo conteúdo
- ~~16 módulos~~ → Número de módulos definido pela análise
- ~~32 horas~~ → Duração real do material
- ~~Flashcards obrigatórios~~ → Opcional conforme necessidade

### O que É consistente:

- Processo de diagnóstico interativo
- Padrões de código React/Tailwind
- Nomenclatura UX (Seção, Aula, Curso)
- Integração com sistema existente

---

## Fluxo de Diagnóstico

### Etapa 0: Coleta de Informações (OBRIGATÓRIA)

Antes de qualquer ação, Claude deve coletar:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DIAGNÓSTICO INICIAL                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. TIPO DE INPUT                                                   │
│     □ Vídeo único (URL)                                            │
│     □ Playlist YouTube (URL)                                        │
│     □ Múltiplos vídeos avulsos (lista de URLs)                     │
│     □ Série/curso existente (descrição)                            │
│                                                                     │
│  2. CARACTERÍSTICAS DO CONTEÚDO                                     │
│     • Duração total estimada: ___                                  │
│     • Quantidade de vídeos: ___                                    │
│     • Tema/assunto principal: ___                                  │
│     • Público-alvo: ___                                            │
│     • Idioma: ___                                                  │
│                                                                     │
│  3. OBJETIVO DO CURSO                                               │
│     □ Introdução/overview rápido                                   │
│     □ Curso completo estruturado                                   │
│     □ Material de referência/consulta                              │
│     □ Treinamento corporativo                                      │
│                                                                     │
│  4. RECURSOS DESEJADOS                                              │
│     □ Navegação por seções                                         │
│     □ Checkboxes de progresso                                      │
│     □ Flashcards                                                   │
│     □ Exercícios práticos                                          │
│     □ Caderno de notas                                             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Perguntas de Diagnóstico (Claude deve fazer)

```markdown
## Diagnóstico: Criação de Curso

Antes de começarmos, preciso entender melhor seu conteúdo:

1. **Qual é o input?**
   - URL de vídeo único?
   - URL de playlist?
   - Lista de vídeos separados?

2. **Qual a duração aproximada do conteúdo total?**
   - Menos de 1 hora
   - 1-5 horas
   - 5-20 horas
   - Mais de 20 horas

3. **Como você imagina a estrutura do curso?**
   - Um módulo único (conteúdo curto)
   - Poucos módulos (2-5)
   - Estrutura completa com seções
   - Ainda não sei, preciso de sugestão

4. **Quais recursos são importantes?**
   - Progresso com checkboxes
   - Flashcards para revisão
   - Apenas navegação simples
```

---

## Tipos de Input Suportados

### Matriz de Formatos

| Tipo de Input | Duração Típica | Estrutura Sugerida | Complexidade |
|---------------|----------------|-------------------|--------------|
| Vídeo curto único | < 1h | 1 módulo, seções opcionais | Baixa |
| Vídeo longo único | 1-5h | 3-8 módulos, 1-2 seções | Média |
| Vídeo muito longo | 5-20h | Múltiplas seções e módulos | Alta |
| Playlist pequena | 5-10 vídeos | 1 seção por tema | Média |
| Playlist grande | 10-50 vídeos | Múltiplas seções agrupadas | Alta |
| Playlist muito grande | 50+ vídeos | Hierarquia multinível | Muito Alta |
| Vídeos avulsos | Variável | Análise caso a caso | Variável |
| Webinar/Live | 1-3h | 1 módulo com timestamps | Baixa |

### Decisões Automáticas vs. Interativas

```
AUTOMÁTICO (Claude decide):
├── Padrão de código (React/Tailwind)
├── Estrutura de arquivos
├── Nomenclatura de componentes
└── Integração técnica

INTERATIVO (Usuário valida):
├── Número de seções
├── Agrupamento de módulos
├── Nomes/títulos
├── Recursos opcionais (flashcards, etc.)
└── Nível de detalhamento
```

---

## Processo Interativo

### Fluxo de Comunicação

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CICLO DE ALINHAMENTO                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  USUÁRIO                          CLAUDE                            │
│     │                                │                              │
│     │──── "Quero criar curso" ──────▶│                              │
│     │                                │                              │
│     │◀─── Perguntas diagnóstico ────│                              │
│     │                                │                              │
│     │──── Respostas ────────────────▶│                              │
│     │                                │                              │
│     │◀─── Proposta de estrutura ────│                              │
│     │     "Baseado no seu input,    │                              │
│     │      sugiro X seções com      │                              │
│     │      Y módulos. Concorda?"    │                              │
│     │                                │                              │
│     │──── Ajustes/Aprovação ────────▶│                              │
│     │                                │                              │
│     │◀─── Execução ─────────────────│                              │
│     │                                │                              │
└─────────────────────────────────────────────────────────────────────┘
```

### Template de Proposta de Estrutura

```markdown
## Proposta de Estrutura

Baseado na análise do seu conteúdo, sugiro:

### Visão Geral
- **Duração total:** [X horas]
- **Formato:** [descrição]

### Estrutura Proposta

**Opção A: [Nome descritivo]**
- [N] seções
- [M] módulos no total
- Recursos: [lista]

**Opção B: [Nome descritivo]**
- [N'] seções
- [M'] módulos no total
- Recursos: [lista]

### Perguntas de Refinamento
1. Qual opção prefere?
2. Algum ajuste nos agrupamentos?
3. Quer adicionar/remover recursos?

Aguardo sua validação antes de prosseguir.
```

---

## Etapas de Execução

### Etapa 1: Extração de Transcrições

**Adaptável conforme input:**

```bash
# Vídeo único
python youtube_transcript.py "URL_VIDEO"

# Playlist (extrair lista primeiro)
# Claude analisa playlist e propõe agrupamentos

# Múltiplos vídeos
python youtube_transcript.py --batch lista_videos.txt
```

### Etapa 2: Análise e Proposta

**Claude analisa e propõe (não executa ainda):**

```markdown
Analisei as transcrições e identifiquei:

- [X] tópicos principais
- [Y] subtópicos
- Duração: [Z] horas

Proposta de organização:
[estrutura sugerida]

Posso prosseguir com essa estrutura?
```

### Etapa 3: Criação de Dados (após aprovação)

**Estrutura adaptativa:**

```javascript
// Exemplo: curso CURTO (1 vídeo, 2h)
export const fases[Nome] = [
  { id: 1, nome: "Conteúdo Completo", ... }
];

export const modulos[Nome] = [
  { id: '1.1', nome: 'Introdução', ... },
  { id: '1.2', nome: 'Conceitos', ... },
  { id: '1.3', nome: 'Prática', ... }
];

// Exemplo: curso EXTENSO (playlist 50 vídeos)
export const fases[Nome] = [
  { id: 1, nome: "Fundamentos", ... },
  { id: 2, nome: "Intermediário", ... },
  { id: 3, nome: "Avançado", ... },
  { id: 4, nome: "Especialização", ... },
  { id: 5, nome: "Projetos", ... }
];

export const modulos[Nome] = [
  // 50 módulos organizados nas 5 seções
];
```

### Etapa 4: Transformação de Conteúdo

**Nível de detalhamento conforme necessidade:**

| Cenário | Detalhamento | Componentes |
|---------|--------------|-------------|
| Curso curto | Mínimo | LearningSystem apenas |
| Curso médio | Padrão | LearningSystem + NotesView básico |
| Curso extenso | Completo | LearningSystem + NotesView detalhado + Flashcards |

### Etapa 5: Integração

**Sempre necessário:**
- Atualizar `studyAreas.js`
- Atualizar `SistemaEducacionalCompleto.jsx`

**Opcional conforme escopo:**
- Criar NotesView para cada módulo
- Criar flashcards
- Criar exercícios

---

## Padrões de Transformação

### Transformação Básica (qualquer curso)

| Elemento | JSX |
|----------|-----|
| Título | `<h2 className="text-2xl font-bold">` |
| Parágrafo | `<p className="text-gray-700">` |
| Lista | `<ul className="list-disc">` |

### Transformação Intermediária (cursos médios+)

| Elemento | JSX |
|----------|-----|
| Código | `<CodeBlock code={...}>` |
| Aviso | `<div className="bg-yellow-50 border">` |
| Destaque | `<div className="bg-[cor]-100 p-4 rounded">` |

### Transformação Avançada (cursos extensos)

| Elemento | JSX |
|----------|-----|
| Timeline | Grid com datas/eventos |
| Comparação | Grid 2 colunas |
| Diagrama | Componente visual customizado |
| Interativo | Estado React + handlers |

---

## Exemplos por Cenário

### Cenário 1: Vídeo Curto (45 min)

```
INPUT: "Tenho um vídeo de 45 min sobre Git básico"

DIAGNÓSTICO:
- Tipo: Vídeo único curto
- Duração: < 1h
- Objetivo: Introdução

PROPOSTA:
- 1 seção única
- 3-4 módulos (Intro, Comandos, Branches, Prática)
- Sem flashcards (opcional)
- Progresso simples

RESULTADO:
├── gitLearningData.js (1 fase, 4 módulos)
└── GitLearningSystem.jsx (componente simples)
```

### Cenário 2: Playlist Média (20 vídeos, 15h)

```
INPUT: "Playlist de Docker com 20 vídeos"

DIAGNÓSTICO:
- Tipo: Playlist média
- Duração: ~15h
- Objetivo: Curso completo

PROPOSTA:
- 4 seções (Básico, Imagens, Compose, Produção)
- 20 módulos (1 por vídeo)
- Flashcards por seção
- Progresso detalhado

RESULTADO:
├── dockerLearningData.js (4 fases, 20 módulos)
├── DockerLearningSystem.jsx
├── DockerNotesView.jsx (4 arquivos, 1 por seção)
└── Flashcards integrados
```

### Cenário 3: Mega-Playlist (100+ vídeos)

```
INPUT: "Curso completo de Python, 150 vídeos"

DIAGNÓSTICO:
- Tipo: Playlist muito grande
- Duração: 80h+
- Objetivo: Formação completa

PROPOSTA INTERATIVA:
"Este é um curso extenso. Sugiro dividir em TRILHAS:

Trilha 1: Python Básico (30 vídeos)
Trilha 2: Python Intermediário (40 vídeos)
Trilha 3: Python Avançado (40 vídeos)
Trilha 4: Projetos (40 vídeos)

Cada trilha seria um 'curso' separado no sistema.
Concorda com essa abordagem?"

RESULTADO (após aprovação):
├── pythonBasicoLearningData.js
├── pythonIntermedLearningData.js
├── pythonAvancadoLearningData.js
├── pythonProjetosLearningData.js
└── Componentes correspondentes
```

---

## Troubleshooting

### Problema: Não sei quantas seções criar

**Solução:** Claude analisa e propõe baseado em:
- Mudanças de tema na transcrição
- Duração relativa dos blocos
- Complexidade do conteúdo

### Problema: Vídeos da playlist são muito heterogêneos

**Solução:** Claude sugere agrupamentos e pede validação:
```
"Identifiquei 3 temas diferentes na playlist:
- Vídeos 1-8: Fundamentos
- Vídeos 9-15: Aplicações
- Vídeos 16-20: Avançado

Posso agrupar assim ou prefere outra organização?"
```

### Problema: Conteúdo muito curto para estrutura completa

**Solução:** Claude sugere estrutura mínima:
```
"Com apenas 30 minutos de conteúdo, sugiro:
- 1 módulo único com 3-4 seções internas
- Sem necessidade de NotesView separado
- Progresso simples (completo/não completo)

Prefere essa abordagem simplificada?"
```

### Problema: Transcrição não disponível

**Solução:** Claude oferece alternativas:
```
"O vídeo não tem transcrição automática. Opções:

1. Transcrever manualmente (você fornece texto)
2. Usar serviço externo de transcrição
3. Criar estrutura baseada em títulos/descrições
4. Assistir e anotar tópicos principais

Qual prefere?"
```

---

## Referências

### Arquivos de Referência

| Arquivo | Descrição |
|---------|-----------|
| `src/data/bashLearningData.js` | Exemplo de curso médio (4 seções, 16 módulos) |
| `src/components/BashNotesView.jsx` | Exemplo de NotesView detalhado |
| `docs/TEMPLATE-CURSO-PADRAO.md` | Template técnico |
| `docs/GUIA-TRANSCRICAO-PARA-CURSO.md` | Guia de transformação |

### Skills Relacionadas

- [platform-architecture](../platform-architecture/SKILL.md) - Arquitetura do sistema
- [learning-path-patterns](../learning-path-patterns/SKILL.md) - Padrões de trilhas
- [component-refactor](../component-refactor/SKILL.md) - Refatoração de componentes

### Agent Relacionado

- [learning-path-architect](../../agents/learning-path-architect.md) - Extração de transcrições

---

## Checklist Adaptativo

### Sempre obrigatório:
- [ ] Diagnóstico inicial realizado
- [ ] Estrutura proposta e aprovada pelo usuário
- [ ] Arquivo de dados criado
- [ ] Integração com sistema principal
- [ ] Build passa sem erros

### Conforme necessidade:
- [ ] NotesView criado (se curso médio+)
- [ ] Flashcards criados (se solicitado)
- [ ] Múltiplas seções (se conteúdo extenso)
- [ ] Trilhas separadas (se mega-curso)

---

## Resumo: Fluxo Completo

```
1. USUÁRIO fornece input (URL, playlist, descrição)
           ↓
2. CLAUDE faz perguntas de diagnóstico
           ↓
3. USUÁRIO responde características
           ↓
4. CLAUDE propõe estrutura adaptada
           ↓
5. USUÁRIO valida/ajusta proposta
           ↓
6. CLAUDE executa criação
           ↓
7. USUÁRIO testa e aprova
```

**Princípio Central:** A estrutura serve o conteúdo, não o contrário.

---

**Você está em:** `.claude/skills/cliente:criar-a-partir-video/SKILL.md`
**Versão:** 2.0.0 (Diagnóstico Interativo)
**Criado em:** 2025-11-24
**Mantido por:** Plataforma B2B de treinamento técnico corporativo Team
**Abordagem:** Flexível, Adaptativa, Colaborativa
