---
name: plannotator
description: Revisao interativa de planos
---

Metodologia para revisar e validar planos de implementacao antes de executar.

## Quando Usar

- Antes de implementar features complexas
- Quando mudancas afetam multiplos arquivos
- Para tarefas que tocam dados sensiveis (CPF, valores)
- Quando ha duvida sobre a abordagem

## Estrutura de um Plano

```markdown
# Plano: [Nome da Feature/Task]

## Objetivo
[O que vamos fazer em 1-2 frases]

## Contexto
[Por que estamos fazendo isso]

## Arquivos Afetados
- `arquivo1.py` - [o que muda]
- `arquivo2.tsx` - [o que muda]

## Passos de Implementacao
1. [Passo 1]
2. [Passo 2]
3. [Passo 3]

## Riscos e Mitigacoes
| Risco | Mitigacao |
|-------|-----------|
| [risco 1] | [como evitar] |

## Criterios de Verificacao
- [ ] Criterio 1
- [ ] Criterio 2

## Rollback
[Como desfazer se der errado]
```

## Checklist de Revisao

### Clareza
- [ ] O objetivo esta claro?
- [ ] Entendo por que estamos fazendo isso?
- [ ] Os passos estao especificos o suficiente?

### Completude
- [ ] Todos os arquivos afetados estao listados?
- [ ] Considerei os casos de borda?
- [ ] Ha plano de rollback?

### Seguranca
- [ ] Toca em dados sensiveis (CPF, valores)?
- [ ] Ha validacao de entrada?
- [ ] Logs nao expoem dados sensiveis?

### Simplicidade
- [ ] E a solucao mais simples possivel?
- [ ] Estou adicionando features alem do pedido?
- [ ] Posso fazer menos e resolver o problema?

### Verificabilidade
- [ ] Como vou testar que funciona?
- [ ] Testes automatizados cobrem?
- [ ] Criterios de aceite sao verificaveis?

## Perguntas para Validacao

### Sobre o Problema
- "Qual problema exatamente estamos resolvendo?"
- "Para quem e esse problema?"
- "Como sabemos que e um problema?"

### Sobre a Solucao
- "Por que essa abordagem e nao outra?"
- "Qual a solucao mais simples que funciona?"
- "O que pode dar errado?"

### Sobre a Implementacao
- "Quais arquivos vou modificar?"
- "Em que ordem fazer as mudancas?"
- "Como verifico que funcionou?"

## Template de Feedback

```markdown
## Feedback do Plano

### Pontos Positivos
- [o que esta bom]

### Pontos de Atencao
- [o que revisar]

### Bloqueadores
- [o que impede aprovacao]

### Sugestoes
- [melhorias propostas]
```

## Fluxo de Aprovacao

```
1. Criar plano
2. Auto-revisar com checklist
3. Apresentar ao usuario
4. Incorporar feedback
5. Obter aprovacao
6. Executar
```
