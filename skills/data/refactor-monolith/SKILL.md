---
name: Refactor-Monolith
description: Skill para decomposição segura de arquivos monolíticos. Análise estrutural profunda, mapeamento exaustivo de dependências, extração incremental com zero quebra de lógica. Exige entendimento completo do negócio antes de qualquer ação.
---

# 🏗️ REFACTOR-MONOLITH - Decomposição Segura de Monolitos

## 🚨 PRINCÍPIO FUNDAMENTAL

```
╔══════════════════════════════════════════════════════════════════╗
║  NUNCA REFATORAR SEM ENTENDER 100% DA LÓGICA DE NEGÓCIO         ║
║  NUNCA EXTRAIR SEM MAPEAR 100% DAS DEPENDÊNCIAS                 ║
║  NUNCA QUEBRAR O QUE FUNCIONA                                    ║
╚══════════════════════════════════════════════════════════════════╝
```

**Regra de Ouro:** É melhor um monolito funcionando do que módulos quebrados.

---

## 📋 QUANDO USAR ESTA SKILL

### ✅ USAR QUANDO:
- Arquivo com +500 linhas
- Arquivo com +10 funções/métodos
- Arquivo com múltiplas responsabilidades (UI + lógica + dados)
- Arquivo difícil de manter/entender
- Arquivo com funções que poderiam ser reutilizadas
- Arquivo que múltiplos devs precisam mexer simultaneamente

### ❌ NÃO USAR QUANDO:
- Arquivo funciona bem e não causa problemas
- Refatoração apenas por "limpeza estética"
- Prazo apertado sem tempo para testes
- Não há entendimento completo do negócio
- Sistema em produção crítica sem ambiente de teste

---

## 🔬 FASE 0: PRÉ-ANÁLISE (OBRIGATÓRIA)

### 0.1 Perguntas de Negócio (FAZER ANTES DE TUDO)

```markdown
ANTES de olhar o código, entender:

1. PROPÓSITO
   - Qual o objetivo principal deste arquivo?
   - Que problema de negócio ele resolve?
   - Quem são os usuários das funcionalidades?

2. CRITICIDADE
   - Este arquivo é crítico para o sistema?
   - Quebrar aqui impacta faturamento/operação?
   - Há janela segura para mudanças?

3. HISTÓRICO
   - Por que ficou monolítico? (crescimento orgânico? pressa?)
   - Houve tentativas anteriores de refatorar?
   - Quais funcionalidades foram adicionadas recentemente?

4. EXPECTATIVA
   - Qual o resultado esperado da refatoração?
   - Quais módulos idealmente existiriam?
   - Há padrão de modularização já usado no projeto?
```

### 0.2 Checklist de Viabilidade

```markdown
□ Entendi o propósito de negócio do arquivo
□ Sei quem usa cada funcionalidade
□ Tenho acesso ao arquivo completo
□ Posso testar após cada mudança
□ Tenho rollback disponível (git)
□ Não há deploy urgente pendente
□ Stakeholder aprovou a refatoração
```

**Se qualquer item for NÃO → PARAR e resolver antes de continuar.**

---

## 🔍 FASE 1: ANÁLISE ESTRUTURAL PROFUNDA

### 1.1 Radiografia do Arquivo

```bash
# Métricas básicas
wc -l [arquivo]                    # Total de linhas
grep -c "function\|=>" [arquivo]   # Total de funções
grep -c "async" [arquivo]          # Funções assíncronas
grep -c "export\|module.exports" [arquivo]  # Exports

# Complexidade
grep -n "if\|else\|switch\|for\|while" [arquivo] | wc -l  # Branches
grep -n "try\|catch" [arquivo] | wc -l                      # Error handling
grep -n "TODO\|FIXME\|HACK" [arquivo]                       # Débitos técnicos
```

### 1.2 Mapa de Funções (DOCUMENTAR TODAS)

```markdown
## INVENTÁRIO DE FUNÇÕES - [nome-arquivo.js]

| # | Função | Linha | Linhas | Responsabilidade | Dependências Internas | Chamada Por |
|---|--------|-------|--------|------------------|----------------------|-------------|
| 1 | init() | 15 | 45 | Inicialização | config, setupUI | main |
| 2 | fetchData() | 60 | 30 | Busca API | formatResponse | init, refresh |
| 3 | formatResponse() | 90 | 25 | Formata dados | - | fetchData |
| ... | ... | ... | ... | ... | ... | ... |

### Legenda de Responsabilidades:
- CONFIG: Configuração e constantes
- INIT: Inicialização e setup
- UI: Manipulação de DOM/interface
- DATA: Busca e processamento de dados
- CALC: Cálculos e lógica de negócio
- UTIL: Utilitários genéricos
- EVENT: Handlers de eventos
- EXPORT: Exportação/download
- CACHE: Gerenciamento de cache
- VALID: Validações
```

### 1.3 Análise de Responsabilidades

```markdown
## MATRIZ DE RESPONSABILIDADES

┌─────────────────────────────────────────────────────────────┐
│ RESPONSABILIDADE      │ FUNÇÕES           │ LINHAS │ %     │
├───────────────────────┼───────────────────┼────────┼───────┤
│ Configuração          │ 2                 │ 50     │ 5%    │
│ Inicialização         │ 3                 │ 120    │ 12%   │
│ Interface (UI)        │ 8                 │ 300    │ 30%   │
│ Lógica de Negócio     │ 5                 │ 250    │ 25%   │
│ Comunicação (API)     │ 4                 │ 150    │ 15%   │
│ Utilitários           │ 6                 │ 80     │ 8%    │
│ Event Handlers        │ 4                 │ 50     │ 5%    │
├───────────────────────┼───────────────────┼────────┼───────┤
│ TOTAL                 │ 32                │ 1000   │ 100%  │
└─────────────────────────────────────────────────────────────┘

DIAGNÓSTICO:
- UI (30%) + Lógica (25%) = 55% → Forte candidato a separação
- Utilitários (8%) → Pode virar módulo compartilhado
```

---

## 🕸️ FASE 2: MAPEAMENTO EXAUSTIVO DE DEPENDÊNCIAS

### 2.1 Dependências Internas (Dentro do Arquivo)

```markdown
## GRAFO DE DEPENDÊNCIAS INTERNAS

funcaoA()
├── chama: funcaoB(), funcaoC()
├── usa variável: CONFIG, state
└── modifica: elementoDOM

funcaoB()
├── chama: funcaoD()
├── usa variável: CONFIG
└── retorna para: funcaoA(), funcaoE()

funcaoC()
├── chama: nenhuma
├── usa variável: state
└── retorna para: funcaoA()

## VARIÁVEIS DE ESTADO COMPARTILHADAS
| Variável | Tipo | Escrito por | Lido por | Crítica? |
|----------|------|-------------|----------|----------|
| state | object | init, fetchData | render*, calc* | SIM |
| CONFIG | const | - | todos | NÃO |
| currentPage | let | pagination | render | SIM |
```

### 2.2 Dependências Externas (Fora do Arquivo)

```bash
# Quem importa este arquivo?
grep -r "require.*[nome-arquivo]\|import.*[nome-arquivo]" . --include="*.js"

# Este arquivo importa quem?
grep -n "require\|import" [arquivo]

# Quais IDs/classes DOM são manipulados?
grep -oE "(getElementById|querySelector)\\(['\"][^'\"]+['\"]\\)" [arquivo]

# Quais rotas/endpoints são chamados?
grep -oE "fetch\\(['\"][^'\"]+['\"]" [arquivo]
grep -oE "/api/[^'\" ]+" [arquivo]
```

### 2.3 Matriz de Acoplamento

```markdown
## MATRIZ DE ACOPLAMENTO

                    │ config │ core │ ui │ utils │ EXTERNO
────────────────────┼────────┼──────┼────┼───────┼─────────
config              │   -    │  ←   │ ←  │   ←   │    
core                │   →    │  -   │ ←→ │   ←   │   API
ui                  │   →    │  →←  │ -  │   ←   │   DOM
utils               │   →    │  →   │ →  │   -   │    
────────────────────┼────────┼──────┼────┼───────┼─────────

LEGENDA:
→  = depende de (importa/usa)
←  = é dependido por (exporta para)
←→ = dependência mútua (ALERTA: difícil separar)
```

### 2.4 Identificação de "Costuras Naturais"

```markdown
## COSTURAS PARA CORTE

Uma "costura" é um ponto onde o código pode ser dividido com MÍNIMO impacto.

### COSTURAS IDENTIFICADAS:

1. ✅ COSTURA LIMPA: Funções utilitárias (linhas 800-900)
   - Não dependem de estado
   - Não acessam DOM
   - Funções puras
   - RISCO: Baixo

2. ⚠️ COSTURA MÉDIA: Configuração (linhas 1-50)
   - Constantes globais
   - Precisam ser importadas por todos módulos
   - RISCO: Médio (ordem de carregamento)

3. 🔴 COSTURA DIFÍCIL: UI + Core (linhas 200-600)
   - Dependência mútua
   - Estado compartilhado
   - RISCO: Alto (requer refatoração de estado primeiro)

### ORDEM RECOMENDADA DE EXTRAÇÃO:
1º → Utilitários (risco baixo, ganho rápido)
2º → Configuração (estabiliza imports)
3º → Separar estado em store
4º → UI (após estado isolado)
5º → Core (após UI isolado)
```

---

## ❓ FASE 3: PERGUNTAS DE CLARIFICAÇÃO

### 3.1 Perguntas Obrigatórias ao Stakeholder

```markdown
ANTES de propor estrutura de módulos, PERGUNTAR:

## SOBRE FUNCIONALIDADES

1. "A função [X] ainda é usada ou é código legado?"
   → Identificar dead code antes de extrair

2. "O comportamento de [Y] está correto ou há bugs conhecidos?"
   → Não perpetuar bugs em módulos novos

3. "Existe regra de negócio não documentada em [Z]?"
   → Capturar conhecimento tácito

## SOBRE PRIORIDADES

4. "Quais funções são mais críticas para o negócio?"
   → Priorizar estabilidade das críticas

5. "Quais partes mudam com mais frequência?"
   → Isolar partes voláteis

6. "Há planos de novas features que afetam este arquivo?"
   → Considerar evolução futura

## SOBRE RESTRIÇÕES

7. "Há restrições de performance a considerar?"
   → Evitar overhead de modularização excessiva

8. "Outros sistemas/equipes dependem deste código?"
   → Mapear consumidores externos

9. "Posso renomear funções ou há contratos fixos?"
   → Entender flexibilidade de interface
```

### 3.2 Análise Lógica x Código

```markdown
## CHECKLIST: LÓGICA DE NEGÓCIO

Para CADA função identificada, validar:

□ Entendo O QUE esta função faz (propósito)
□ Entendo POR QUE ela existe (regra de negócio)
□ Entendo QUANDO ela é chamada (fluxo)
□ Entendo QUEM depende do resultado (consumidores)
□ O código reflete corretamente a lógica?
□ Há edge cases tratados que não são óbvios?
□ Há comentários explicando decisões de negócio?

## ALERTAS DE LÓGICA OCULTA

🚨 ATENÇÃO para:
- Números mágicos sem explicação
- Condicionais complexos (if dentro de if)
- Try/catch que engole erros silenciosamente
- Timeouts/delays sem justificativa
- Ordenações específicas de operações
- Validações que parecem redundantes (podem não ser)
```

---

## 📐 FASE 4: PROPOSTA DE ARQUITETURA MODULAR

### 4.1 Template de Estrutura

```markdown
## PROPOSTA DE MODULARIZAÇÃO

### ARQUIVO ORIGINAL:
`[caminho/arquivo-monolito.js]` (XXX linhas)

### ESTRUTURA PROPOSTA:

```
[pasta-modulo]/
├── config.js          # Constantes e configuração
│   └── [XX linhas] - Funções: A, B
│
├── core.js            # Lógica de negócio principal
│   └── [XX linhas] - Funções: C, D, E
│
├── ui.js              # Manipulação de interface
│   └── [XX linhas] - Funções: F, G, H
│
├── api.js             # Comunicação com backend
│   └── [XX linhas] - Funções: I, J
│
├── utils.js           # Utilitários
│   └── [XX linhas] - Funções: K, L, M
│
├── events.js          # Event handlers
│   └── [XX linhas] - Funções: N, O
│
└── index.js           # Orquestrador (entry point)
    └── [XX linhas] - init, bindEvents
```

### DIAGRAMA DE DEPENDÊNCIAS:

```
                    ┌──────────┐
                    │  index   │ (entry point)
                    └────┬─────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    ┌────────┐      ┌────────┐      ┌────────┐
    │  core  │◄────►│   ui   │      │ events │
    └───┬────┘      └───┬────┘      └───┬────┘
        │               │               │
        ▼               ▼               │
    ┌────────┐      ┌────────┐          │
    │  api   │      │ config │◄─────────┘
    └───┬────┘      └────────┘
        │
        ▼
    ┌────────┐
    │ utils  │ (sem dependências internas)
    └────────┘
```

### REGRAS DE IMPORTAÇÃO:

1. `utils` → Não importa nenhum módulo interno
2. `config` → Não importa nenhum módulo interno  
3. `api` → Importa apenas `utils`, `config`
4. `core` → Importa `api`, `utils`, `config`
5. `ui` → Importa `core`, `utils`, `config`
6. `events` → Importa `ui`, `core`, `config`
7. `index` → Importa todos, orquestra
```

### 4.2 Validação da Proposta

```markdown
## CHECKLIST DE VALIDAÇÃO DA ARQUITETURA

### Princípios
□ Cada módulo tem UMA responsabilidade clara
□ Dependências fluem em uma direção (sem ciclos)
□ Módulos podem ser testados isoladamente
□ Nenhuma lógica de negócio duplicada
□ Estado centralizado ou claramente distribuído

### Compatibilidade
□ API pública (exports) permanece compatível
□ Ordem de inicialização preservada
□ Event listeners funcionam igual
□ Performance não degradada

### Praticidade
□ Estrutura segue padrão já usado no projeto
□ Nomenclatura consistente
□ Tamanho dos módulos equilibrado (não criar micro-módulos)
```

---

## 🔧 FASE 5: EXTRAÇÃO INCREMENTAL SEGURA

### 5.1 Princípio da Extração Atômica

```markdown
╔══════════════════════════════════════════════════════════════════╗
║  UMA FUNÇÃO POR VEZ                                              ║
║  UM COMMIT POR EXTRAÇÃO                                          ║
║  UM TESTE APÓS CADA MUDANÇA                                      ║
╚══════════════════════════════════════════════════════════════════╝
```

### 5.2 Protocolo de Extração

```markdown
## SEQUÊNCIA DE EXTRAÇÃO (para cada função)

### PASSO 1: Preparar
```bash
# Criar branch
git checkout -b refactor/extract-[nome-funcao]

# Backup
cp [arquivo-original].js [arquivo-original].js.backup
```

### PASSO 2: Criar Módulo Destino (se não existir)
```javascript
// [pasta]/[modulo-destino].js

// Imports necessários (identificados na análise)
// ...

// Função extraída virá aqui

// Export
module.exports = { /* funções */ };
```

### PASSO 3: Copiar Função (NÃO recortar ainda)
```javascript
// [pasta]/[modulo-destino].js

function funcaoExtraida() {
  // Código COPIADO do original
  // Ainda não modificou o original
}

module.exports = { funcaoExtraida };
```

### PASSO 4: Testar Módulo Isolado
```bash
# Verificar syntax
node --check [modulo-destino].js

# Teste unitário se possível
node -e "const m = require('./[modulo-destino]'); console.log(m.funcaoExtraida);"
```

### PASSO 5: Atualizar Original para Usar Módulo
```javascript
// [arquivo-original].js

// ADICIONAR import no topo
const { funcaoExtraida } = require('./[pasta]/[modulo-destino]');

// MANTER função original COMENTADA (não deletar ainda)
/*
function funcaoExtraida() {
  // código antigo
}
*/

// Código que chamava funcaoExtraida() continua funcionando
// porque agora vem do import
```

### PASSO 6: Testar Sistema Completo
```bash
# Testar funcionalidade no browser/app
# Verificar console por erros
# Testar casos de uso principais
```

### PASSO 7: Commit Atômico
```bash
git add [modulo-destino].js [arquivo-original].js
git commit -m "refactor: extract funcaoExtraida to [modulo]

- Moved funcaoExtraida from monolith to dedicated module
- Original function kept commented for safety
- All tests passing"
```

### PASSO 8: Só Depois de Validado, Remover Código Comentado
```bash
# Após 1-2 dias sem problemas em produção
# Remover função comentada do original
git commit -m "chore: remove commented legacy funcaoExtraida"
```
```

### 5.3 Ordem de Extração Recomendada

```markdown
## ORDEM SEGURA DE EXTRAÇÃO

NÍVEL 1 - RISCO ZERO (fazer primeiro)
├── Constantes e configuração
├── Funções utilitárias puras
└── Funções sem dependências internas

NÍVEL 2 - RISCO BAIXO
├── Funções de formatação
├── Funções de validação
└── Helpers de cálculo

NÍVEL 3 - RISCO MÉDIO
├── Funções de API/fetch
├── Funções de cache
└── Event handlers simples

NÍVEL 4 - RISCO ALTO (fazer por último)
├── Funções de UI que manipulam estado
├── Funções de inicialização
└── Orquestradores/controllers

NÍVEL 5 - NUNCA EXTRAIR SOZINHO
├── Funções com dependência circular
├── Funções que modificam estado global
└── Funções com efeitos colaterais ocultos
→ Requer refatoração prévia do estado
```

---

## ✅ FASE 6: VALIDAÇÃO E TESTES

### 6.1 Testes de Regressão

```markdown
## CHECKLIST DE REGRESSÃO (após cada extração)

### Funcional
□ Feature principal funciona
□ Features secundárias funcionam
□ Edge cases funcionam
□ Erros são tratados corretamente

### Performance
□ Tempo de carregamento similar
□ Sem memory leaks novos
□ Sem requests duplicados

### Compatibilidade
□ Funciona no Chrome
□ Funciona no Firefox
□ Funciona no Safari
□ Funciona no mobile

### Multi-tenant (se aplicável)
□ Dados isolados por liga_id
□ Sem vazamento entre tenants
```

### 6.2 Smoke Test Rápido

```javascript
// Script de smoke test
async function smokeTest() {
  const checks = [];
  
  // 1. Módulos carregam sem erro
  try {
    const config = require('./config');
    const core = require('./core');
    const ui = require('./ui');
    checks.push({ name: 'Modules load', status: '✅' });
  } catch (e) {
    checks.push({ name: 'Modules load', status: '❌', error: e.message });
  }
  
  // 2. Funções existem
  const requiredFunctions = ['init', 'render', 'fetchData'];
  requiredFunctions.forEach(fn => {
    const exists = typeof core[fn] === 'function';
    checks.push({ name: `Function ${fn}`, status: exists ? '✅' : '❌' });
  });
  
  // 3. Exports corretos
  // ...
  
  console.table(checks);
  return checks.every(c => c.status === '✅');
}
```

---

## 🚨 FASE 7: ROLLBACK E RECUPERAÇÃO

### 7.1 Plano de Rollback

```markdown
## ROLLBACK PLAN

### Cenário 1: Bug detectado imediatamente
```bash
# Reverter último commit
git revert HEAD
```

### Cenário 2: Bug detectado após múltiplas extrações
```bash
# Voltar para estado antes da refatoração
git log --oneline  # Encontrar commit anterior
git checkout [hash-commit-seguro] -- [arquivo-original].js
```

### Cenário 3: Rollback completo
```bash
# Voltar branch inteira
git checkout main
git branch -D refactor/[nome]

# Restaurar backup
cp [arquivo].js.backup [arquivo].js
```

### Cenário 4: Produção quebrou
```bash
# Deploy emergencial do backup
# 1. Reverter no git
# 2. Rebuild
# 3. Deploy
# 4. Investigar em ambiente de dev
```
```

### 7.2 Pontos de Verificação

```markdown
## CHECKPOINTS DE SEGURANÇA

Criar checkpoint ANTES de:
□ Extrair primeira função
□ Extrair função crítica
□ Modificar estrutura de estado
□ Alterar ordem de inicialização
□ Remover código comentado

Checkpoint = commit + tag
```bash
git commit -m "checkpoint: before extracting [funcao]"
git tag checkpoint-[nome]-[data]
```
```

---

## 📋 TEMPLATES E CHECKLISTS

### Template: Documento de Refatoração

```markdown
# REFATORAÇÃO: [Nome do Arquivo]

## Metadata
- **Arquivo:** [caminho/arquivo.js]
- **Linhas:** [XXX]
- **Data início:** [data]
- **Responsável:** [nome]
- **Status:** [Em análise | Em andamento | Concluído | Pausado]

## Motivação
[Por que refatorar este arquivo?]

## Análise
- Funções identificadas: [X]
- Responsabilidades: [lista]
- Dependências externas: [lista]
- Riscos identificados: [lista]

## Estrutura Proposta
[Diagrama de módulos]

## Plano de Execução
| # | Extração | Risco | Status | Data |
|---|----------|-------|--------|------|
| 1 | utils.js | Baixo | ✅ | [data] |
| 2 | config.js | Baixo | ⏳ | |
| ... | ... | ... | ... | |

## Validações
- [ ] Testes funcionais
- [ ] Testes de regressão
- [ ] Review de código
- [ ] Aprovação stakeholder

## Rollback
[Instruções de rollback]

## Lições Aprendidas
[Preencher ao final]
```

### Checklist Master

```markdown
## CHECKLIST COMPLETO - REFATORAÇÃO DE MONOLITO

### PRÉ-REFATORAÇÃO
□ Entendi 100% da lógica de negócio
□ Mapeei 100% das dependências
□ Identifiquei costuras naturais
□ Proposta aprovada pelo stakeholder
□ Tenho ambiente de teste
□ Tenho plano de rollback
□ Branch criada
□ Backup feito

### DURANTE REFATORAÇÃO
□ Extraindo uma função por vez
□ Commitando após cada extração
□ Testando após cada commit
□ Mantendo código antigo comentado
□ Documentando decisões

### PÓS-REFATORAÇÃO
□ Todos testes passando
□ Performance validada
□ Multi-tenant validado
□ Code review feito
□ Documentação atualizada
□ Código comentado removido
□ Branch mergeada
□ Tag de versão criada

### MONITORAMENTO (1 semana após)
□ Sem bugs reportados
□ Sem degradação de performance
□ Equipe consegue manter novos módulos
□ Lições aprendidas documentadas
```

---

## 🚫 ANTI-PATTERNS (NUNCA FAZER)

### ❌ Big Bang Refactor
```
ERRADO: Refatorar tudo de uma vez, commitar no final
CERTO: Uma extração por vez, um commit por extração
```

### ❌ Refatorar Sem Entender
```
ERRADO: "Vou separar em módulos porque está grande"
CERTO: "Entendi que X faz Y por causa de Z, posso extrair"
```

### ❌ Deletar Código Imediatamente
```
ERRADO: Recortar função do original para o módulo
CERTO: Copiar, testar, só depois comentar, só depois deletar
```

### ❌ Criar Micro-Módulos
```
ERRADO: Um arquivo por função (50 arquivos de 20 linhas)
CERTO: Agrupar por responsabilidade (5-8 arquivos coesos)
```

### ❌ Ignorar Dependências Circulares
```
ERRADO: Extrair A que depende de B que depende de A
CERTO: Resolver ciclo primeiro (extrair dependência comum C)
```

### ❌ Refatorar e Adicionar Feature
```
ERRADO: "Já que estou mexendo, vou melhorar X também"
CERTO: Refatoração pura, sem mudança de comportamento
```

---

## 🎯 COMANDOS DE ATIVAÇÃO

### Iniciar Análise
```
@Refactor-Monolith analisar [caminho/arquivo.js]
```

### Continuar de Fase Específica
```
@Refactor-Monolith fase-2 [caminho/arquivo.js]  # Mapeamento
@Refactor-Monolith fase-4 [caminho/arquivo.js]  # Proposta
@Refactor-Monolith fase-5 [caminho/arquivo.js]  # Extração
```

### Extrair Função Específica
```
@Refactor-Monolith extrair [funcao] de [origem] para [destino]
```

---

## 📚 REFERÊNCIAS

### Princípios Aplicados
- S.A.I.S (Solicitar → Analisar → Identificar → Alterar)
- S.D.A (Sistema de Dependências Arquiteturais)
- Antipattern (Preservar intenção original)
- Preservação da Lógica (Nunca quebrar funcionalidade)

### Integração com Workflow
```
/pesquisa → identifica monolito problemático
/Refactor-Monolith → planeja decomposição
/spec → detalha mudanças cirúrgicas
/code → implementa extrações
```

---

**STATUS:** 🏗️ REFACTOR-MONOLITH - SURGICAL DECOMPOSITION PROTOCOL

**Versão:** 1.0

**Última atualização:** 2026-01-17