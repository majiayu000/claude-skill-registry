---
name: tdd-development
description: Test-Driven Development - Escreva testes primeiro, sempre
version: 1.0.0
category: workflow
triggers:
  - tdd
  - test
  - teste
  - testing
  - unit test
  - teste unitário
  - red green refactor
  - desenvolvimento guiado por testes
tools: []
author: liquid-ai
based_on: obra/superpowers
---

# Test-Driven Development (TDD)

Esta skill implementa a disciplina de Test-Driven Development. TDD não é opcional — é mandatório para código confiável e manutenível.

## Regra Fundamental

> **Escreva o teste primeiro. Veja-o falhar. Escreva o código mínimo para passar.**

Observar o teste falhar prova que o teste realmente valida algo significativo.

## O Ciclo RED-GREEN-REFACTOR

### 1. RED - Teste Falha
```
┌─────────────────────────────────────────┐
│  1. Escreva um teste MÍNIMO que falha   │
│  2. Execute o teste                      │
│  3. CONFIRME que ele falha              │
│  4. O teste deve falhar pelo motivo     │
│     CORRETO (não por erro de sintaxe)   │
└─────────────────────────────────────────┘
```

### 2. GREEN - Teste Passa
```
┌─────────────────────────────────────────┐
│  1. Escreva o código MÍNIMO necessário  │
│  2. Não adicione funcionalidade extra   │
│  3. Execute o teste                      │
│  4. CONFIRME que ele passa              │
└─────────────────────────────────────────┘
```

### 3. REFACTOR - Melhore o Código
```
┌─────────────────────────────────────────┐
│  1. Melhore a qualidade do código       │
│  2. Remova duplicação                    │
│  3. Melhore nomes e estrutura           │
│  4. Execute os testes novamente         │
│  5. CONFIRME que ainda passam           │
└─────────────────────────────────────────┘
```

## Regras Absolutas (NÃO NEGOCIÁVEIS)

### O Que NUNCA Fazer

| Violação | Por Que é Proibido |
|----------|-------------------|
| Escrever código de produção antes do teste | Você não sabe se o código funciona |
| Pular a fase RED | Você não provou que o teste valida algo |
| Escrever múltiplos testes de uma vez | Perde o feedback rápido do ciclo |
| "Consertar" código que já existe sem teste | Está adivinhando, não verificando |
| Usar código escrito antes do teste | Delete e reescreva com TDD |

### Racionalizações Comuns (e Por Que São Falsas)

**"É só um código simples, não precisa de teste"**
- FALSO: Código simples é o mais fácil de testar. Se não consegue testar, não é simples.

**"Vou testar depois"**
- FALSO: Testes escritos depois são testes de confirmação, não de design. Perdem o valor de TDD.

**"Já testei manualmente"**
- FALSO: Teste manual não é repetível, não documenta comportamento, não previne regressões.

**"O prazo está apertado"**
- FALSO: TDD é mais rápido no médio prazo. Bugs custam mais que testes.

**"Já escrevi o código, seria desperdício deletar"**
- FALSO: Sunk cost fallacy. Código sem teste é liability, não asset.

## Checklist de Verificação

### Antes de Escrever Código

- [ ] Existe um teste que falha para este comportamento?
- [ ] O teste falha pelo motivo correto?
- [ ] O teste é mínimo (testa uma coisa só)?
- [ ] O nome do teste descreve o comportamento esperado?

### Depois de Escrever Código

- [ ] O teste passa agora?
- [ ] Você escreveu o código MÍNIMO necessário?
- [ ] Não adicionou funcionalidade "de brinde"?
- [ ] Todos os testes anteriores ainda passam?

### Na Fase de Refactor

- [ ] O código está mais limpo?
- [ ] Removeu duplicação?
- [ ] Os nomes são claros?
- [ ] TODOS os testes ainda passam?

## Padrões de Teste

### Bom Teste
```typescript
// ✅ CORRETO: Nome descritivo, uma asserção, arrange-act-assert
describe('Calculator', () => {
  it('should add two positive numbers', () => {
    // Arrange
    const calculator = new Calculator();

    // Act
    const result = calculator.add(2, 3);

    // Assert
    expect(result).toBe(5);
  });
});
```

### Teste Problemático
```typescript
// ❌ ERRADO: Múltiplas asserções, nome vago, sem estrutura clara
describe('Calculator', () => {
  it('works', () => {
    const calc = new Calculator();
    expect(calc.add(2, 3)).toBe(5);
    expect(calc.subtract(5, 3)).toBe(2);
    expect(calc.multiply(2, 3)).toBe(6);
    expect(calc.divide(6, 2)).toBe(3);
  });
});
```

## Red Flags - Sinais de Violação TDD

| Sinal | Problema |
|-------|----------|
| "Deixa eu só terminar esse código e depois escrevo o teste" | Violação direta do TDD |
| "Esse teste é óbvio, não precisa ver falhar" | Não provou que o teste funciona |
| "Vou escrever todos os testes primeiro" | Perdeu o ciclo de feedback |
| "O código já estava funcionando, só adicionei o teste" | Teste de confirmação, não TDD |
| "Não sei como testar isso" | Sinal de design acoplado |

## Troubleshooting

| Situação | Solução |
|----------|---------|
| "Não sei que teste escrever" | Comece pelo comportamento mais simples possível |
| "O teste é muito difícil de escrever" | O código está muito acoplado. Simplifique o design |
| "Tenho muitos testes quebrando" | Você mudou muito código de uma vez. Volte atrás e faça mudanças menores |
| "O teste passa mas o comportamento está errado" | O teste não está testando o que deveria. Revise as asserções |
| "Não consigo fazer o teste falhar" | Você escreveu o código antes do teste. Delete o código e recomece |

## Fluxo de Trabalho Recomendado

```
1. Receba um requisito
   ↓
2. Escreva um teste que falha (RED)
   ↓
3. Confirme a falha
   ↓
4. Escreva código mínimo (GREEN)
   ↓
5. Confirme que passa
   ↓
6. Refatore se necessário (REFACTOR)
   ↓
7. Confirme que ainda passa
   ↓
8. Repita para o próximo requisito
```

## Ferramentas Recomendadas

### JavaScript/TypeScript
- Jest
- Vitest
- Mocha + Chai

### Python
- pytest
- unittest

### Comandos Úteis
```bash
# Watch mode - executa testes automaticamente
npm test -- --watch

# Coverage - verifica cobertura
npm test -- --coverage

# Single file
npm test -- path/to/test.spec.ts
```

## Lembre-se

> "Código sem teste é código quebrado que ainda não descobrimos."

> "TDD não é sobre testes. É sobre design. Os testes são um bônus."

> "Se você não viu o teste falhar, você não sabe se ele funciona."

---

**Esta skill deve ser ativada AUTOMATICAMENTE quando:**
- O usuário pede para implementar uma feature
- O usuário pede para corrigir um bug
- O usuário pede para refatorar código
- O usuário menciona testes ou qualidade de código
