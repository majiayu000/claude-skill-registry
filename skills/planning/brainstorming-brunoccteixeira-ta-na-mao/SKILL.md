---
name: brainstorming
description: Design de features e brainstorming
---

Metodologia estruturada para projetar novas funcionalidades.

## Processo de Design

### 1. PROBLEMA: Definir Claramente
```markdown
## Problema
[Descrição em 1-2 frases]

## Quem é afetado?
[Usuário específico]

## Qual a dor?
[O que incomoda/falta]

## Como sabemos que é um problema?
[Evidência: feedback, dados, observação]
```

### 2. EXPLORAR: Gerar Opções
```markdown
## Opções

### Opção A: [Nome]
- Como funciona: [descrição]
- Prós: [vantagens]
- Contras: [desvantagens]

### Opção B: [Nome]
- Como funciona: [descrição]
- Prós: [vantagens]
- Contras: [desvantagens]

### Opção C: [Nome]
- Como funciona: [descrição]
- Prós: [vantagens]
- Contras: [desvantagens]
```

### 3. DECIDIR: Escolher Abordagem
```markdown
## Decisão: [Opção escolhida]

### Justificativa
[Por que essa opção?]

### Trade-offs aceitos
[O que estamos abrindo mão?]
```

### 4. ESPECIFICAR: Detalhar Solução
```markdown
## Especificação

### User Stories
- Como [usuário], quero [ação] para [benefício]

### Critérios de Aceite
- [ ] Critério 1
- [ ] Critério 2
- [ ] Critério 3

### Fluxo do Usuário
1. Usuário faz X
2. Sistema responde Y
3. Usuário vê Z

### Casos de Borda
- E se [cenário incomum]?
- E se [erro acontecer]?
```

## Templates

### Nova Feature do Agente
```markdown
# Feature: [Nome]

## Problema
Usuários não conseguem [ação] pelo chat.

## Solução
Adicionar ferramenta que [faz X].

## Implementação

### Nova Tool
- Arquivo: `backend/app/agent/tools/nova_tool.py`
- Função: `async def executar_acao(param: str) -> dict`
- Retorno: `{"resultado": "...", "sucesso": True}`

### Prompt do Agente
Adicionar em `agent.py`:
"Quando o usuário pedir [X], use a ferramenta [Y]"

### Testes
- `backend/tests/test_nova_tool.py`
```

### Nova Página do Frontend
```markdown
# Feature: Página de [Nome]

## Problema
Usuários precisam [ver/fazer X] e não tem lugar no app.

## Solução
Nova rota `/caminho` com [descrição].

## Implementação

### Componentes
- `src/pages/NovaPagina.tsx` - Página principal
- `src/components/NovoComponente.tsx` - Componente auxiliar

### Rota
Em `App.tsx`:
```jsx
<Route path="/caminho" element={<NovaPagina />} />
```

### API (se necessário)
- Endpoint: `GET /api/v1/recurso`
- Response: `{dados: [...]}`
```

## Checklist de Design

- [ ] O problema está claro?
- [ ] Consideramos múltiplas opções?
- [ ] A solução é a mais simples possível?
- [ ] Pensamos nos casos de erro?
- [ ] Usuário de baixa escolaridade vai entender?
- [ ] Sabemos como medir sucesso?

## Princípios do Tá na Mão

1. **Simplicidade** - Menos é mais
2. **Acessibilidade** - Linguagem de 5ª série
3. **Mobile-first** - Maioria acessa pelo celular
4. **Offline-friendly** - Conexão ruim é comum
5. **Inclusivo** - Funciona para todos
