---
name: Code
description: Fase 3 - Implementation Protocol. Le Spec.md, solicita arquivos originais, aplica mudancas CIRURGICAS linha por linha, valida multi-tenant, testa e documenta. Preserva logica, zero improviso.
---

# FASE 3: IMPLEMENTATION (SURGICAL EXECUTION)

## Objetivo
Executar especificacao tecnica com precisao cirurgica, sem improviso, preservando logica existente.

---

## INPUT OBRIGATORIO

### Carregar Spec
```bash
# Localizar Spec gerado na Fase 2
ls -la .claude/docs/SPEC-*.md

# Ler Spec completo
cat .claude/docs/SPEC-[nome-tarefa].md
```

---

## PROTOCOLO DE IMPLEMENTACAO

### FASE 1: VALIDACAO PRE-EXECUCAO

#### 1.1 Checklist de Seguranca
- [ ] Spec completo e claro
- [ ] Arquivos listados existem
- [ ] Mudancas linha por linha definidas
- [ ] Rollback plan documentado

#### 1.2 Preparar Ambiente
```bash
# Verificar branch atual
git branch --show-current

# Criar branch para feature (se nao existir)
git checkout -b feat/[nome-tarefa]

# Backup de arquivos criticos (se destrutivo)
cp [arquivo-critico].js [arquivo-critico].js.backup
```

### FASE 2: SOLICITAR ARQUIVOS ORIGINAIS

#### 2.1 NUNCA Modificar Sem Ver
```bash
# Para CADA arquivo listado no Spec:
cat [caminho/completo/arquivo.js]

# Ler COMPLETAMENTE, nao apenas a linha alvo
# Entender contexto antes/depois da mudanca
```

#### 2.2 Principio da Preservacao
- Ler arquivo completo
- Identificar logica de negocio
- Preservar fluxo existente
- Mudanca cirurgica APENAS onde especificado

### FASE 3: EXECUTAR MUDANCAS (Ordem do Spec)

#### 3.1 Seguir Ordem Exata
```
1. Models (estrutura de dados)
   |
2. Controllers (logica backend)
   |
3. Routes (endpoints)
   |
4. Services (se houver)
   |
5. Frontend JS (logica cliente)
   |
6. Frontend HTML (UI)
   |
7. Frontend CSS (estilos)
```

#### 3.2 Executar Mudanca Cirurgica
```javascript
// Spec diz: "Linha 45: ADICIONAR"

// PROCEDIMENTO:
// 1. cat arquivo.js (ver arquivo completo)
// 2. Localizar linha 45
// 3. Entender contexto (linhas 40-50)
// 4. Aplicar mudanca EXATA do Spec
// 5. Preservar restante do arquivo
```

#### 3.3 Validar Apos Cada Arquivo
```bash
# Syntax check
node --check [arquivo-modificado].js

# Se frontend:
grep -n "console.log\|debugger" [arquivo].js  # Remover debug

# Verificar imports
grep -n "require\|import" [arquivo].js
```

### FASE 4: VALIDACOES CRITICAS

#### 4.1 Multi-Tenant (OBRIGATORIO)
```bash
# Verificar TODAS as queries
grep -n "\.find\|\.findOne\|\.updateMany" [arquivo].js

# Cada query DEVE ter liga_id:
Model.find({
  liga_id: ligaId,  // OBRIGATORIO
  temporada: temporada
})
```

#### 4.2 Seguranca
```bash
# Rotas protegidas?
grep -n "router\.\(post\|put\|delete\)" routes/[arquivo].js

# Devem ter middleware:
router.post('/endpoint',
  verificarAdmin,      // Protecao
  validarLigaId,       // Multi-tenant
  controller.acao
)
```

#### 4.3 Performance
```bash
# Queries com .lean()?
grep -n "\.find\|\.findOne" [arquivo].js | grep -v "lean"

# Adicionar .lean() em reads:
Model.find({ ... }).lean()  // Economia de memoria
```

### FASE 5: TESTES

#### 5.1 Testes Unitarios (se existirem)
```bash
# Rodar testes do modulo
npm test -- [modulo]

# Se falhar, corrigir antes de continuar
```

#### 5.2 Teste Manual (obrigatorio)
- Seguir casos de teste do Spec
- Validar cenarios positivos
- Validar cenarios negativos
- Testar edge cases

#### 5.3 Validacao Multi-Liga
```bash
# Testar com liga SuperCartola (32 times)
# Testar com liga Sobral (4-6 times)
# Garantir isolamento de dados
```

---

## PADRAO DE COMMITS

### Mensagem Estruturada
```bash
git commit -m "tipo(escopo): descricao curta

- Mudanca 1 especifica
- Mudanca 2 especifica
- Mudanca 3 especifica

Ref: SPEC-[nome].md
"
```

### Tipos de Commit
- `feat`: Nova funcionalidade
- `fix`: Correcao de bug
- `refactor`: Refatoracao sem mudar comportamento
- `perf`: Melhoria de performance
- `style`: Mudancas de formatacao
- `docs`: Apenas documentacao
- `test`: Adicionar/corrigir testes

---

## PROTOCOLO DE TESTES

### Teste 1: Funcionalidade Basica
```javascript
async function testar() {
  const ligaId = '684cb1c8af923da7c7df51de';
  const participanteId = 'test-id';

  const resultado = await controller.novaFuncao(participanteId, ligaId);

  console.assert(resultado.saldoTotal !== undefined, 'Saldo deve existir');
  console.log('Teste 1 passou');
}
```

### Teste 2: Multi-Tenant Isolation
```javascript
async function testarMultiTenant() {
  const liga1 = '684cb1c8af923da7c7df51de';
  const liga2 = '684d821cf1a7ae16d1f89572';

  await Model.create({ liga_id: liga1, dados: 'teste1' });
  const resultado = await Model.find({ liga_id: liga2 });

  console.assert(resultado.length === 0, 'Isolamento multi-tenant OK');
  console.log('Teste Multi-Tenant passou');
}
```

---

## CHECKLIST FINAL

### Codigo
- [ ] Todas mudancas do Spec aplicadas
- [ ] Arquivos originais preservados (logica intacta)
- [ ] Syntax check passou
- [ ] Sem console.log de debug
- [ ] Sem codigo comentado desnecessario

### Seguranca
- [ ] Queries com liga_id
- [ ] Rotas protegidas com middleware
- [ ] Inputs validados
- [ ] Errors tratados

### Performance
- [ ] Queries com .lean() (reads)
- [ ] Indices verificados
- [ ] Sem N+1 queries

### Testes
- [ ] Funcionalidade basica testada
- [ ] Multi-tenant validado
- [ ] Cenarios negativos testados
- [ ] Edge cases cobertos

### Documentacao
- [ ] Commits descritivos
- [ ] README atualizado (se necessario)
- [ ] CHANGELOG atualizado
- [ ] pending-tasks.md marcado como concluido

---

## ANTI-PATTERNS (NAO FAZER)

### Improvisar Mudancas
```javascript
// Spec: "Adicionar linha 45"
// ERRADO: Adicionar na linha 50 porque "parece melhor"

// CORRETO: Adicionar EXATAMENTE na linha 45
// Se achar que Spec esta errado, PARAR e revisar Spec
```

### Modificar Sem Ver Original
```javascript
// ERRADO:
str_replace(old_str: "linha que eu acho que existe")

// CORRETO:
cat arquivo.js  // Ver PRIMEIRO
str_replace(old_str: "linha exata copiada do arquivo")
```

### Quebrar Logica Existente
```javascript
// ERRADO: Remover codigo "que parece nao usar"
// Sem ver quem chama

// CORRETO:
grep -r "funcaoAntiga" .  // Ver quem usa
// So remover se NINGUEM usa
```

### Ignorar Multi-Tenant
```javascript
// ERRADO:
Model.find({})  // Query global

// CORRETO:
Model.find({ liga_id: ligaId })  // SEMPRE filtrar
```

---

## FINALIZACAO

### Marcar Tarefa como Concluida
```markdown
# pending-tasks.md

## Concluidas
- [x] Implementar [nome da funcionalidade]
  - **Concluido:** [data]
  - **Arquivos:** [lista]
  - **Commits:** [hashes]
  - **Branch:** feat/[nome]
  - **Testes:** Passaram
  - **Deploy:** Pendente
```

### Preparar para Review/Merge
```bash
# Atualizar branch com main
git fetch origin
git rebase origin/main

# Push para review
git push origin feat/[nome]

# Ou merge direto (se nao houver PR)
git checkout main
git merge feat/[nome]
git push origin main
```

---

**STATUS:** CODE PROTOCOL - SURGICAL & TESTED
**Versao:** 1.0 (High Senior Edition)
