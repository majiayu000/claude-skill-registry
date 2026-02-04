---
name: Git-Commit-Push
description: Skill para commits e pushes automatizados no GitHub. Analisa mudanças, gera mensagens descritivas seguindo convenções, valida código e executa git push com segurança. Acionado por "faça um git push" ou "commite tudo". Visão full-stack senior dev.
---

# 🚀 GIT COMMIT & PUSH PROTOCOL

## 🎯 Objetivo
Automatizar commits e pushes com mensagens descritivas, validações de código e boas práticas de versionamento.

---

## ⚡ ATIVAÇÃO AUTOMÁTICA

### Comandos que Acionam a Skill

**Termos Diretos (SEMPRE usar skill):**
- `git push`
- `git commit`
- `push`
- `commit`
- `git e push` ← **IMPORTANTE: variação comum**

**Frases em Português:**
- "faça um git push"
- "faça o push"
- "faz um push"
- "faça git e push"
- "git e push"
- "commite tudo"
- "commit e push"
- "suba as mudanças"
- "subir mudanças"
- "envie para o github"
- "envia pro github"
- "git push das alterações"
- "commit das mudanças"
- "salva no git"
- "salvar no git"
- "versiona isso"
- "versionar"
- "commitar"
- "pushar"

**Variações Curtas:**
- "push isso"
- "commita"
- "manda pro git"
- "atualiza o repo"
- "atualizar repositório"
- "sobe isso"
- "sobe pro git"
- "joga no git"
- "puxa e empurra" (pull + push)

**Após Implementações:**
- "pronto, push"
- "feito, commit"
- "terminei, sobe"
- "ok, git push"
- "antes... git e push"
- "antes, push"
- "só falta o push"

**Variações Implícitas (contexto de finalização):**
- "agora commita"
- "pode commitar"
- "manda ver no git"
- "finaliza no github"
- "fecha com push"

**Regex de Detecção:**
```regex
/^(antes\s*[\.,]?\s*)?(git\s*(e\s*)?)?((push|commit|commita|commitar|pushar|suba|subir|envie?|manda|versiona|sobe))/i
/(push|commit|github|repo|git)\s*(isso|tudo|mudanças|alterações)?$/i
/(só\s*falta|pode|agora|fecha\s*com)\s*(o\s*)?(push|commit)/i
```

### Quando Usar
- Após implementar funcionalidade completa
- Após correções de bugs
- Após refatorações
- Quando solicitado explicitamente

---

## 📋 PROTOCOLO DE EXECUÇÃO

### FASE 1: ANÁLISE DE MUDANÇAS

#### 1.1 Verificar Status do Git
```bash
# Ver branch atual
bash git branch --show-current

# Ver mudanças
bash git status --short

# Ver diff detalhado
bash git diff --stat

# Ver arquivos staged (se houver)
bash git diff --cached --stat
```

#### 1.2 Identificar Tipo de Mudança
```bash
# Analisar arquivos modificados
bash git diff --name-only

# Categorizar mudanças:
# - controllers/ → feat/fix backend
# - models/ → feat/fix database
# - routes/ → feat/fix routing
# - public/js/ → feat/fix frontend
# - public/css/ → style
# - *.md → docs
# - package.json → deps
```

#### 1.3 Mapear Escopo da Mudança
- **Backend:** Controllers, Models, Routes, Services
- **Frontend:** JS modules, HTML, CSS
- **Config:** package.json, .env.example, constants
- **Docs:** README, CHANGELOG, markdown files
- **Infra:** Deployment configs, Docker, scripts

---

### FASE 2: VALIDAÇÕES PRÉ-COMMIT

#### 2.1 Validação de Código

**JavaScript/Node.js:**
```bash
# Syntax check em arquivos modificados
bash for file in $(git diff --name-only --diff-filter=AM | grep "\.js$"); do node --check "$file" 2>&1 || echo "❌ Erro em $file"; done

# Verificar console.log esquecidos
bash git diff | grep -n "console\.log\|debugger" && echo "⚠️ Debug code detectado"

# Verificar TODO/FIXME
bash git diff | grep -n "TODO\|FIXME\|XXX" && echo "📝 Marcadores pendentes"
```

**Multi-Tenant Validation:**
```bash
# Verificar queries sem liga_id
bash git diff | grep -A 5 "\.find\|\.findOne\|\.updateMany" | grep -v "liga_id" && echo "⚠️ Query sem liga_id detectada"
```

**Security Checks:**
```bash
# Verificar rotas desprotegidas
bash git diff routes/ | grep "router\.\(post\|put\|delete\)" | grep -v "verificar" && echo "⚠️ Rota sem middleware"

# Verificar secrets expostos
bash git diff | grep -iE "password|secret|key|token" | grep -v "\.env" && echo "🔒 Possível secret exposto"
```

#### 2.2 Validação de Qualidade

**Code Quality:**
```bash
# Verificar arquivos > 500 linhas
bash for file in $(git diff --name-only --diff-filter=AM | grep "\.js$"); do lines=$(wc -l < "$file" 2>/dev/null); [ "$lines" -gt 500 ] && echo "📏 $file muito grande ($lines linhas)"; done

# Verificar funções muito complexas
bash git diff | grep -c "function\|=>" | awk '{if($1 > 20) print "⚠️ Muitas funções em um diff"}'
```

#### 2.3 Decisão: Continuar ou Abortar
- ❌ **Syntax errors** → ABORTAR, corrigir primeiro
- ⚠️ **Debug code** → AVISAR usuário, continuar se confirmado
- ⚠️ **Security issues** → AVISAR, aguardar confirmação
- ✅ **Tudo OK** → Continuar

---

### FASE 3: GERAÇÃO DE MENSAGEM DE COMMIT

#### 3.1 Formato Conventional Commits
```
<tipo>(<escopo>): <descrição curta>

<corpo detalhado (opcional)>

<footer (opcional)>
```

#### 3.2 Tipos Padronizados
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `refactor`: Refatoração sem mudança de comportamento
- `perf`: Melhoria de performance
- `style`: Formatação, espaçamento (não CSS)
- `docs`: Apenas documentação
- `test`: Adicionar/corrigir testes
- `build`: Mudanças no build/deploy
- `ci`: Mudanças em CI/CD
- `chore`: Manutenção geral

#### 3.3 Escopos do Projeto
- `extrato`: Módulo de extratos financeiros
- `acertos`: Sistema de acertos financeiros
- `rodadas`: Gerenciamento de rodadas
- `mata-mata`: Torneio mata-mata
- `pontos-corridos`: Campeonato por pontos
- `artilheiro`: Sistema de artilheiros/campeões
- `fluxo`: Fluxo financeiro
- `melhor-mes`: Melhor jogador do mês
- `export`: Funcionalidades de exportação
- `pwa`: Progressive Web App
- `auth`: Autenticação
- `api`: Integrações API
- `db`: Database/models
- `ui`: Interface geral

#### 3.4 Algoritmo de Geração de Mensagem

**Analisar arquivos modificados:**
```javascript
const mudancas = {
  controllers: arquivos.filter(f => f.includes('controllers/')),
  models: arquivos.filter(f => f.includes('models/')),
  frontend: arquivos.filter(f => f.includes('public/js/')),
  styles: arquivos.filter(f => f.includes('public/css/')),
  routes: arquivos.filter(f => f.includes('routes/')),
  docs: arquivos.filter(f => f.endsWith('.md'))
};

// Determinar tipo principal
let tipo = 'chore';
if (mudancas.controllers.length > 0 || mudancas.models.length > 0) {
  tipo = 'feat'; // ou 'fix' se contiver "fix", "bug", "erro"
}
if (mudancas.styles.length > 0 && mudancas.frontend.length === 0) {
  tipo = 'style';
}
if (mudancas.docs.length > 0 && Object.values(mudancas).flat().length === mudancas.docs.length) {
  tipo = 'docs';
}

// Determinar escopo (pasta principal modificada)
const escopo = identificarEscopoPrincipal(arquivos);

// Gerar descrição baseada em diffs
const descricao = gerarDescricaoInteligente(git.diff);
```

#### 3.5 Exemplos de Mensagens Geradas

**Exemplo 1: Nova feature**
```bash
# Arquivos: controllers/extratoController.js, public/js/extrato/core.js
# Diff: +calcularSaldoAcertos(), +saldoAcertos

Mensagem gerada:
feat(extrato): adiciona cálculo de saldo de acertos

- Implementa função calcularSaldoAcertos() no controller
- Integra saldo de acertos no extrato do participante
- Atualiza frontend para exibir breakdown de saldos
```

**Exemplo 2: Bug fix**
```bash
# Arquivos: controllers/acertosController.js
# Diff: -bug no cálculo, +correção

Mensagem gerada:
fix(acertos): corrige cálculo de acertos com múltiplas parcelas

- Resolve erro ao calcular acertos com mais de 3 parcelas
- Adiciona validação para valores negativos
```

**Exemplo 3: Refatoração**
```bash
# Arquivos: public/js/extrato/core.js, public/js/extrato/ui.js
# Diff: reorganização de funções

Mensagem gerada:
refactor(extrato): separa lógica de apresentação da UI

- Move funções de cálculo para core.js
- Mantém apenas renderização em ui.js
- Melhora manutenibilidade do código
```

**Exemplo 4: Múltiplos módulos**
```bash
# Arquivos: controllers/mataMataController.js, controllers/acertosController.js
# Diff: mudanças em 2 módulos

Mensagem gerada:
feat(torneio): integra acertos financeiros no mata-mata

- Adiciona cálculo de acertos no ranking do mata-mata
- Sincroniza saldos entre módulos
- Atualiza UI para exibir pendências financeiras
```

---

### FASE 4: EXECUÇÃO DE COMANDOS GIT

#### 4.1 Staging Inteligente

**Estratégia 1: Stage por categoria**
```bash
# Backend primeiro
bash git add controllers/ models/ routes/ services/ 2>/dev/null

# Frontend depois
bash git add public/js/ public/css/ public/participante/ 2>/dev/null

# Config e docs
bash git add package.json *.md config/ 2>/dev/null

# Outros arquivos
bash git add . 2>/dev/null
```

**Estratégia 2: Stage tudo de uma vez (padrão)**
```bash
bash git add .
```

#### 4.2 Commit com Mensagem Gerada
```bash
# Executar commit
bash git commit -m "[mensagem gerada]"

# Verificar se commit foi bem-sucedido
bash git log -1 --oneline
```

#### 4.3 Verificações Pré-Push
```bash
# Ver branch atual
bash git branch --show-current

# Ver remote configurado
bash git remote -v

# Ver commits a serem enviados
bash git log origin/$(git branch --show-current)..HEAD --oneline

# Verificar se há divergências
bash git fetch origin
bash git status | grep "behind\|diverged"
```

#### 4.4 Tratamento de Divergências

**Cenário 1: Local ahead, remote não alterado**
```bash
# Push direto
bash git push origin $(git branch --show-current)
```

**Cenário 2: Remote alterado (behind)**
```bash
# Pull com rebase
bash git pull --rebase origin $(git branch --show-current)

# Resolver conflitos se houver
bash git status | grep "both modified" && echo "⚠️ Conflitos detectados"

# Push após resolver
bash git push origin $(git branch --show-current)
```

**Cenário 3: Divergência crítica**
```bash
# Abortar e avisar usuário
bash git merge --abort 2>/dev/null
bash git rebase --abort 2>/dev/null

echo "🚫 PUSH ABORTADO: Divergência detectada"
echo "Ações necessárias:"
echo "1. git fetch origin"
echo "2. git rebase origin/main (ou merge)"
echo "3. Resolver conflitos"
echo "4. Tentar push novamente"
```

---

### FASE 5: EXECUÇÃO DO PUSH

#### 5.1 Push Padrão
```bash
# Push para branch atual
bash git push origin $(git branch --show-current)

# Verificar sucesso
bash echo $? | grep "0" && echo "✅ Push realizado com sucesso" || echo "❌ Push falhou"
```

#### 5.2 Push com Tags (se aplicável)
```bash
# Se houver tags locais não enviadas
bash git push origin --tags
```

#### 5.3 Confirmação Final
```bash
# Ver último commit no remote
bash git log origin/$(git branch --show-current) -1 --oneline

# Ver status limpo
bash git status
```

---

## 📊 OUTPUT FINAL

### Template de Resposta
```markdown
🚀 **GIT PUSH EXECUTADO**

✅ **Commit:** [hash] - [mensagem]
📂 **Arquivos:** [quantidade] modificados
🌿 **Branch:** [nome da branch]
📡 **Remote:** origin/[branch]

📋 **Resumo das Mudanças:**
- [módulo 1]: [descrição]
- [módulo 2]: [descrição]

🔍 **Validações:**
✅ Syntax check passou
✅ Multi-tenant validado
✅ Security checks OK

🔗 **GitHub:** https://github.com/[repo]/commit/[hash]
```

### Exemplo Real
```markdown
🚀 **GIT PUSH EXECUTADO**

✅ **Commit:** a3f2b91 - feat(extrato): adiciona cálculo de saldo de acertos
📂 **Arquivos:** 3 modificados
🌿 **Branch:** main
📡 **Remote:** origin/main

📋 **Resumo das Mudanças:**
- controllers/extratoController.js: nova função calcularSaldoAcertos()
- public/js/extrato/core.js: integração frontend
- routes/extrato-routes.js: endpoint para buscar acertos

🔍 **Validações:**
✅ Syntax check passou
✅ Multi-tenant validado
✅ Security checks OK

🔗 **GitHub:** https://github.com/paulinett1508-dev/SuperCartolaManagerv5/commit/a3f2b91
```

---

## 🔧 CONFIGURAÇÕES AVANÇADAS

### Commit Hooks (Automatizado)
```bash
# Criar pre-commit hook (opcional)
bash cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Syntax check antes de commitar
for file in $(git diff --cached --name-only --diff-filter=AM | grep "\.js$"); do
  node --check "$file" || exit 1
done
EOF

bash chmod +x .git/hooks/pre-commit
```

### Aliases Úteis
```bash
# Criar aliases git úteis
bash git config alias.last 'log -1 HEAD'
bash git config alias.unstage 'reset HEAD --'
bash git config alias.visual 'log --oneline --graph --decorate'
```

---

## ⚙️ ESTRATÉGIAS POR CONTEXTO

### Contexto 1: Desenvolvimento Solo (padrão)
```bash
# Push direto para main
bash git add .
bash git commit -m "[mensagem]"
bash git push origin main
```

### Contexto 2: Feature Branches
```bash
# Verificar se está em feature branch
branch=$(git branch --show-current)
if [[ $branch != "main" && $branch != "master" ]]; then
  # Push para feature branch
  bash git push origin $branch
  echo "💡 Branch de feature: $branch"
  echo "Para merge: git checkout main && git merge $branch"
fi
```

### Contexto 3: Hotfix Crítico
```bash
# Se mensagem contém "hotfix" ou "urgent"
echo "🚨 HOTFIX DETECTADO"
bash git add .
bash git commit -m "hotfix: [descrição]"
bash git push origin main
bash git tag -a "hotfix-$(date +%Y%m%d-%H%M)" -m "Hotfix crítico"
bash git push origin --tags
```

---

## 🚫 ANTI-PATTERNS (NUNCA FAZER)

### ❌ Commit sem Análise
```bash
# ERRADO:
bash git add . && git commit -m "updates" && git push

# CERTO:
# 1. Analisar mudanças
# 2. Validar código
# 3. Gerar mensagem descritiva
# 4. Executar push
```

### ❌ Mensagens Genéricas
```bash
# ERRADO:
git commit -m "fix"
git commit -m "updates"
git commit -m "changes"

# CERTO:
git commit -m "fix(extrato): corrige cálculo de saldo negativo"
git commit -m "feat(pwa): adiciona botão de instalação"
```

### ❌ Push sem Validação
```bash
# ERRADO:
git push (sem verificar syntax, conflitos, etc)

# CERTO:
# 1. Syntax check
# 2. Verificar divergências
# 3. Pull se necessário
# 4. Push
```

### ❌ Commit de Debug Code
```bash
# ERRADO: Commitar com console.log
console.log("DEBUG: saldo =", saldo);

# CERTO: Remover debug antes de commitar
bash git diff | grep "console\.log" && echo "⚠️ Remova debug code"
```

---

## ✅ CHECKLIST COMPLETO

### Pré-Commit
- [ ] Syntax check em todos arquivos .js
- [ ] Sem console.log ou debugger
- [ ] Queries com liga_id validadas
- [ ] Rotas protegidas com middleware
- [ ] Sem secrets expostos
- [ ] Arquivos > 500 linhas revisados

### Commit
- [ ] Mensagem segue Conventional Commits
- [ ] Tipo correto (feat/fix/refactor/etc)
- [ ] Escopo identificado
- [ ] Descrição clara e concisa
- [ ] Corpo detalhado (se necessário)

### Push
- [ ] Branch verificado
- [ ] Remote correto
- [ ] Sem divergências ou conflitos
- [ ] Push bem-sucedido
- [ ] Status limpo (working tree clean)

---

## 🎯 FLUXO VISUAL

```
📝 SOLICITAÇÃO
   "faça um git push"
          ↓
🔍 FASE 1: ANÁLISE
   git status, git diff
          ↓
✅ FASE 2: VALIDAÇÕES
   syntax, multi-tenant, security
          ↓
   ❌ Falhou? → ABORTAR + avisar usuário
   ✅ Passou? → Continuar
          ↓
💬 FASE 3: MENSAGEM
   Gerar commit message descritiva
          ↓
📦 FASE 4: STAGING
   git add (inteligente ou completo)
          ↓
💾 FASE 5: COMMIT
   git commit -m "[mensagem]"
          ↓
🔄 FASE 6: PRÉ-PUSH
   Verificar divergências
          ↓
   🔀 Divergência? → Pull/Rebase → Resolver
   ✅ Limpo? → Continuar
          ↓
🚀 FASE 7: PUSH
   git push origin [branch]
          ↓
✅ CONCLUSÃO
   Confirmar sucesso + resumo
```

---

## 🎓 CASOS DE USO

### Caso 1: Push Simples
```
USUÁRIO: "faça um git push"

SKILL EXECUTA:
1. git status → 3 arquivos modificados
2. Validações → ✅ Tudo OK
3. Mensagem → "feat(extrato): adiciona exportação PDF"
4. git add .
5. git commit -m "[mensagem]"
6. git push origin main
7. Responde: ✅ Push realizado (commit a3f2b91)
```

### Caso 2: Múltiplas Mudanças
```
USUÁRIO: "commite tudo"

SKILL EXECUTA:
1. git status → 12 arquivos em 3 módulos
2. Identifica: backend (extrato) + frontend (mata-mata)
3. Mensagem → "feat: integra acertos em extrato e mata-mata"
4. Adiciona bullets detalhando cada módulo
5. Executa commit + push
6. Responde: ✅ Push com 12 arquivos
```

### Caso 3: Hotfix Urgente
```
USUÁRIO: "git push urgente do fix"

SKILL EXECUTA:
1. Detecta palavra "urgente"
2. Prioriza validação de security
3. Mensagem → "hotfix: corrige vazamento de dados multi-tenant"
4. Commit + push
5. Cria tag hotfix-YYYYMMDD-HHMM
6. Responde: 🚨 Hotfix enviado + tag criada
```

### Caso 4: Conflitos Detectados
```
USUÁRIO: "faça um push"

SKILL EXECUTA:
1. git fetch → detecta divergência
2. git pull --rebase → conflitos em extrato.js
3. PARA e responde:
   "🚫 Push abortado: conflitos detectados em extrato.js
   
   Resolva manualmente:
   1. Abra extrato.js
   2. Resolva marcações <<< === >>>
   3. Execute: git add extrato.js && git rebase --continue
   4. Solicite novo push"
```

---

## 💡 DECISÕES INTELIGENTES

### Escolher Tipo de Commit Automaticamente
```javascript
const palavrasChave = {
  feat: ['adiciona', 'implementa', 'cria', 'novo', 'nova'],
  fix: ['corrige', 'resolve', 'fix', 'bug', 'erro'],
  refactor: ['refatora', 'reorganiza', 'melhora estrutura'],
  perf: ['otimiza', 'performance', 'melhora velocidade'],
  style: ['formata', 'ajusta estilo', 'spacing'],
  docs: ['documenta', 'atualiza README', 'adiciona comentários']
};

// Analisar commit message e diff para determinar tipo
const tipo = identificarTipoInteligente(diff, palavrasChave);
```

### Detectar Escopo Automaticamente
```javascript
// Arquivos modificados
const arquivos = getArquivosModificados();

// Mapear para escopos do projeto
const mapeamento = {
  'controllers/extratoController.js': 'extrato',
  'controllers/mataMataController.js': 'mata-mata',
  'public/js/fluxo-financeiro/': 'fluxo',
  'models/Rodada.js': 'rodadas'
};

const escopo = determinarEscopoPrincipal(arquivos, mapeamento);
```

---

**STATUS:** 🚀 GIT COMMIT & PUSH PROTOCOL - AUTOMATED & SMART

**Versão:** 1.0 (Senior Full-Stack Edition)

**Última atualização:** 2026-01-23

---

## 🔐 SEGURANÇA E COMPLIANCE

### Regras de Proteção
- ❌ Nunca commitar .env
- ❌ Nunca commitar node_modules/
- ❌ Nunca commitar arquivos > 100MB
- ❌ Nunca commitar secrets/tokens
- ✅ Sempre validar multi-tenant
- ✅ Sempre validar security middleware

### Validação de .gitignore
```bash
# Verificar se .gitignore está configurado
bash test -f .gitignore || echo "⚠️ .gitignore não encontrado"

# Verificar se node_modules está ignorado
bash grep -q "node_modules" .gitignore || echo "⚠️ Adicione node_modules ao .gitignore"
```

---

**ATIVADO E PRONTO PARA USO!** 🎯
