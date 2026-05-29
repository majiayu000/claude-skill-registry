---
name: localStorage-patterns
scope: domain
target: organizador-base-conhecimento
description: |
  Comprehensive guide to localStorage patterns for the Ultrathink educational platform. This skill covers schema design, error handling strategies, quota management, and synchronization patterns essential for building resilient web applications with client-side persistence.

  Learn how to handle common localStorage errors (QuotaExceededError, SecurityError, DOMException), implement graceful degradation, manage storage quotas (5-10MB browser limits, 50KB per note), and sync localStorage with React state. The skill emphasizes defensive programming, user-friendly error messages, and fallback strategies.

  Real-world examples are taken directly from the project codebase, including CNotesView, BashNotesView, and auto-save patterns used across 5 learning systems. Each pattern is demonstrated with production code showing how localStorage is used to persist 227 educational modules' progress and user notes.

  Key topics include try/catch patterns for all localStorage operations, QuotaExceededError handling (clear old data, warn user), SecurityError handling (private browsing detection), schema design for JSON storage, versioning strategies, migration patterns, and testing localStorage in different browser contexts.

  This skill is essential for implementing US-041 (localStorage error handling), US-042 (persist module progress), refactoring auto-save logic into custom hooks (useAutoSaveNotes), and maintaining data integrity across the educational platform. Includes troubleshooting guides for common issues encountered in production.

keywords: |
  localStorage, storage, persistence, error-handling, QuotaExceededError,
  SecurityError, quota-management, auto-save, state-sync, schema-design,
  try-catch, fallback, data-migration, browser-storage

allowed-tools: |
  Read, Write, Edit, Grep, Glob, Bash
---

# localStorage Patterns

> **Padrões de Persistência Client-Side para Sistema Educacional Corporativo**
>
> **Versão:** 1.0.0
> **Última Atualização:** 2025-11-19
> **Target:** localStorage API (Web Storage API)
> **Projeto:** Organizador de Base de Conhecimento Enterprise

---

## 📋 Índice

1. [Overview](#-overview)
2. [Quando Usar Esta Skill](#-quando-usar-esta-skill)
3. [Conceitos Fundamentais](#-conceitos-fundamentais)
4. [Padrões de Error Handling](#-padrões-de-error-handling)
5. [Quota Management](#-quota-management)
6. [Schema Design](#-schema-design)
7. [Exemplos Práticos do Projeto](#-exemplos-práticos-do-projeto)
8. [Antipadrões a Evitar](#-antipadrões-a-evitar)
9. [Troubleshooting](#-troubleshooting)
10. [Referências](#-referências)

---

## 🎯 Overview

Esta skill documenta todos os padrões de uso do **localStorage** no **Organizador de Base de Conhecimento Enterprise**, um sistema educacional que persiste notas de usuários e progresso de 227 módulos educacionais usando apenas client-side storage.

**O que você vai aprender:**
- Como tratar erros de localStorage de forma robusta (QuotaExceededError, SecurityError)
- Quando usar localStorage vs. sessionStorage vs. IndexedDB
- Padrões de schema design para JSON storage
- Estratégias de quota management (5-10MB limites)
- Sincronização localStorage ↔ React state
- Testes de localStorage em diferentes browsers
- Migração e versionamento de dados

**Por que esta skill é importante:**
- ✅ **Resiliência:** Previne perda de dados do usuário (notas, progresso)
- ✅ **UX:** Feedback claro quando storage está cheio ou bloqueado
- ✅ **Manutenibilidade:** Schema design facilita evolução
- ✅ **Testabilidade:** Padrões permitem mocks e testes
- ✅ **Performance:** Leitura/escrita otimizada (batching, debouncing)

**Débito Técnico Atual (2025-11-19):**
- ❌ Nenhum try/catch em operações localStorage (5 componentes NotesView)
- ❌ Sem tratamento de QuotaExceededError (usuário perde notas!)
- ❌ Sem limite de 50KB por nota (pode crashar)
- ❌ Sem fallback para sessionStorage ou memória
- ❌ Sem testes unitários de localStorage

**Esta skill resolve:** US-041, US-042, facilita US-043 (refatoração hooks)

---

## 📋 Quando Usar Esta Skill

### Cenário 1: Implementando Auto-Save de Notas

**Situação:** Você precisa salvar notas do usuário automaticamente em `<textarea>` (CNotesView, BashNotesView, etc.)

**Use esta skill para:**
- Decidir quando salvar (onChange, onBlur, debounce?)
- Implementar try/catch robusto
- Tratar QuotaExceededError (storage cheio)
- Mostrar feedback ao usuário (salvando, salvo, erro)
- Sincronizar localStorage → React state

**Exemplo de aplicação:**
```jsx
// ✅ Seguindo padrões da skill
function CNotesView({ courseId }) {
  const [notes, setNotes, saveStatus] = useAutoSaveNotes(courseId);

  return (
    <div>
      <textarea
        value={notes}
        onChange={(e) => setNotes(e.target.value)}
        placeholder="Suas anotações..."
      />
      {saveStatus === 'saving' && <span>💾 Salvando...</span>}
      {saveStatus === 'saved' && <span>✅ Salvo</span>}
      {saveStatus === 'error' && <span>⚠️ Erro ao salvar</span>}
    </div>
  );
}
```

---

### Cenário 2: Persistindo Progresso de Aulas

**Situação:** Você precisa salvar quais aulas o usuário completou (US-042)

**Use esta skill para:**
- Definir schema JSON (array de IDs vs. objeto com timestamps)
- Implementar operações CRUD (adicionar, remover, consultar)
- Tratar erros de leitura/escrita
- Migrar schema antigo → novo (versionamento)
- Sincronizar com UI (progresso visual)

**Exemplo de aplicação:**
```jsx
// ✅ Usando hook customizado
function CLearningSystem() {
  const [completedLessons, markComplete, progress] = useModuleProgress('c', 50);

  const handleComplete = (lessonId) => {
    try {
      markComplete(lessonId);
    } catch (error) {
      if (error.name === 'QuotaExceededError') {
        alert('Storage cheio! Limpe dados antigos.');
      }
    }
  };

  return (
    <div>
      <ProgressBar completed={progress.completed} total={progress.total} />
      <LessonList completedIds={completedLessons} onComplete={handleComplete} />
    </div>
  );
}
```

---

### Cenário 3: Debugging Storage Issues

**Situação:** Usuário reporta "notas não salvam" ou "progresso desaparece ao recarregar"

**Use esta skill para:**
- Diagnosticar se localStorage está disponível (private browsing?)
- Verificar quota disponível (Storage API)
- Inspecionar dados salvos (DevTools Application tab)
- Reproduzir bugs (simular quota excedida)
- Implementar logging de erros

**Exemplo de debug:**
```javascript
// ✅ Diagnóstico completo
function diagnoseLocalStorage() {
  // 1. Testar disponibilidade
  if (typeof Storage === 'undefined') {
    console.error('localStorage não suportado!');
    return;
  }

  // 2. Testar leitura/escrita
  try {
    localStorage.setItem('test', 'value');
    localStorage.removeItem('test');
    console.log('✅ localStorage funcional');
  } catch (e) {
    console.error('❌ localStorage bloqueado:', e.name);
  }

  // 3. Verificar quota (Chrome 110+)
  if (navigator.storage && navigator.storage.estimate) {
    navigator.storage.estimate().then(estimate => {
      const usedMB = (estimate.usage / 1024 / 1024).toFixed(2);
      const quotaMB = (estimate.quota / 1024 / 1024).toFixed(2);
      console.log(`Usando ${usedMB} MB de ${quotaMB} MB (${(estimate.usage / estimate.quota * 100).toFixed(1)}%)`);
    });
  }

  // 4. Listar keys do Ultrathink
  const keys = Object.keys(localStorage).filter(k => k.startsWith('ultrathink_'));
  console.log('Keys Ultrathink:', keys);
  keys.forEach(key => {
    const size = new Blob([localStorage.getItem(key)]).size;
    console.log(`- ${key}: ${(size / 1024).toFixed(2)} KB`);
  });
}
```

---

## 💡 Conceitos Fundamentais

### 1. localStorage vs. Outras Opções

**Comparação:**

| Feature | localStorage | sessionStorage | IndexedDB | Cookies |
|---------|-------------|----------------|-----------|---------|
| **Tamanho** | 5-10 MB | 5-10 MB | 50+ MB | 4 KB |
| **Persistência** | Permanente | Sessão | Permanente | Configurável |
| **API** | Síncrona | Síncrona | Assíncrona | Document.cookie |
| **Performance** | Rápida | Rápida | Rápida (indexed) | Lenta (HTTP) |
| **Escopo** | Origem | Tab/Window | Origem | Domínio |
| **Uso** | Preferências, notas | Estado temporário | DB client-side | Auth tokens |

**Quando usar localStorage (nosso caso):**
- ✅ Dados pequenos (<5MB total)
- ✅ Acesso síncrono (simplicidade)
- ✅ Persistência entre sessões
- ✅ Leitura/escrita frequente
- ✅ Sem necessidade de índices/queries complexas

**Quando NÃO usar localStorage:**
- ❌ Dados sensíveis (não é criptografado!)
- ❌ Dados >5MB (use IndexedDB)
- ❌ Queries complexas (use IndexedDB)
- ❌ Performance crítica para grandes datasets

---

### 2. Limites e Quotas

**Limites por Browser (2025):**

```
Chrome/Edge:   10 MB por origem
Firefox:       10 MB por origem
Safari:        5 MB por origem (mais restritivo!)
Opera:         10 MB por origem
```

**Cálculo aproximado:**
- 1 caractere = ~2 bytes (UTF-16)
- 10 MB = ~5.000.000 caracteres
- Nota de 50KB = ~25.000 caracteres (10 páginas A4)

**Limites do Projeto Ultrathink:**
- 📝 **Máximo 50KB por nota** (25.000 caracteres)
- 📊 **5 sistemas × 50KB = 250KB** (notas)
- 📈 **227 módulos × 100 bytes = 22KB** (progresso)
- 🎯 **Total estimado: ~300KB** (3% da quota)

**Buffer de segurança:** Alertar usuário ao atingir 80% da quota (8MB)

---

### 3. Erros Comuns

#### QuotaExceededError

**Quando ocorre:**
- Storage atingiu limite de 5-10MB
- Tentando salvar dado grande (>50KB)
- Safari em modo privado (quota 0!)

**Como tratar:**
```javascript
try {
  localStorage.setItem('ultrathink_notes_c', longText);
} catch (error) {
  if (error.name === 'QuotaExceededError') {
    // Estratégias:
    // 1. Limpar dados antigos
    clearOldData();

    // 2. Tentar salvar em sessionStorage (fallback)
    sessionStorage.setItem('ultrathink_notes_c_temp', longText);

    // 3. Avisar usuário
    showToast('⚠️ Storage cheio! Dados salvos temporariamente.', 'warning');

    // 4. Oferecer download de backup
    downloadBackup(longText, 'c-notes-backup.txt');
  }
}
```

---

#### SecurityError

**Quando ocorre:**
- Navegação privada (Safari, Firefox)
- Configuração de segurança bloqueou storage
- Iframe cross-origin sem permissão

**Como tratar:**
```javascript
function isLocalStorageAvailable() {
  try {
    const test = '__localStorage_test__';
    localStorage.setItem(test, test);
    localStorage.removeItem(test);
    return true;
  } catch (error) {
    if (error.name === 'SecurityError') {
      console.warn('localStorage bloqueado (private browsing?)');
      return false;
    }
    throw error;
  }
}

// Uso
if (!isLocalStorageAvailable()) {
  // Fallback: usar memória (não persiste)
  const inMemoryStorage = {};
  // ... implementar API similar
}
```

---

#### DOMException

**Quando ocorre:**
- Tentar acessar localStorage em contexto inválido
- Worker thread (não tem acesso a localStorage)
- Browser muito antigo

**Como tratar:**
```javascript
function safeGetItem(key, defaultValue = null) {
  try {
    return localStorage.getItem(key) ?? defaultValue;
  } catch (error) {
    if (error instanceof DOMException) {
      console.error('DOMException ao acessar localStorage:', error);
      return defaultValue;
    }
    throw error;
  }
}
```

---

## 🛡️ Padrões de Error Handling

### Padrão 1: Try/Catch em Todas Operações

**Princípio:** Nunca assumir que localStorage está disponível.

**Implementação:**
```javascript
// ✅ SEMPRE fazer
function saveNotes(courseId, notes) {
  const key = `ultrathink_notes_${courseId}`;

  try {
    localStorage.setItem(key, notes);
    return { success: true, error: null };
  } catch (error) {
    console.error(`Erro ao salvar notas (${key}):`, error);

    // Classificar erro
    if (error.name === 'QuotaExceededError') {
      return { success: false, error: 'quota_exceeded' };
    } else if (error.name === 'SecurityError') {
      return { success: false, error: 'security_blocked' };
    } else {
      return { success: false, error: 'unknown' };
    }
  }
}

// ❌ NUNCA fazer
function saveNotesUnsafe(courseId, notes) {
  localStorage.setItem(`ultrathink_notes_${courseId}`, notes); // Pode crashar!
}
```

---

### Padrão 2: Graceful Degradation

**Princípio:** Sistema continua funcionando mesmo se localStorage falhar.

**Implementação:**
```javascript
// Hook com fallback para memória
function useAutoSaveNotes(courseId) {
  const [notes, setNotes] = useState('');
  const [saveStatus, setSaveStatus] = useState('idle');
  const [storageAvailable, setStorageAvailable] = useState(true);

  // Carregar ao montar
  useEffect(() => {
    try {
      const saved = localStorage.getItem(`ultrathink_notes_${courseId}`);
      if (saved) setNotes(saved);
    } catch (error) {
      console.warn('localStorage indisponível, usando memória');
      setStorageAvailable(false);
    }
  }, [courseId]);

  // Auto-save debounced
  useEffect(() => {
    if (!storageAvailable) return; // Skip se bloqueado

    const timer = setTimeout(() => {
      setSaveStatus('saving');

      try {
        localStorage.setItem(`ultrathink_notes_${courseId}`, notes);
        setSaveStatus('saved');
      } catch (error) {
        console.error('Erro ao salvar:', error);
        setSaveStatus('error');

        if (error.name === 'QuotaExceededError') {
          // Fallback: sessionStorage
          sessionStorage.setItem(`ultrathink_notes_${courseId}_temp`, notes);
        }
      }
    }, 1000); // Debounce 1s

    return () => clearTimeout(timer);
  }, [notes, courseId, storageAvailable]);

  return [notes, setNotes, saveStatus];
}
```

---

### Padrão 3: User-Friendly Error Messages

**Princípio:** Usuário entende o problema e sabe como resolver.

**Implementação:**
```javascript
function showStorageErrorToast(errorType) {
  const messages = {
    quota_exceeded: {
      title: '⚠️ Armazenamento Cheio',
      message: 'Suas notas estão muito grandes. Limite: 50KB por curso.',
      action: 'Limpar Dados Antigos'
    },
    security_blocked: {
      title: '🔒 Modo Privado Detectado',
      message: 'Dados salvos apenas durante esta sessão.',
      action: 'Entendi'
    },
    unknown: {
      title: '❌ Erro ao Salvar',
      message: 'Tente recarregar a página.',
      action: 'Recarregar'
    }
  };

  const config = messages[errorType] || messages.unknown;

  // Usando biblioteca de toast (ex: react-hot-toast)
  toast.error(
    <div>
      <strong>{config.title}</strong>
      <p>{config.message}</p>
      <button onClick={() => handleAction(errorType)}>
        {config.action}
      </button>
    </div>,
    { duration: 8000 }
  );
}
```

---

## 📊 Quota Management

### Padrão 1: Verificar Quota Disponível

**API Moderna (Chrome 110+, Firefox 115+):**
```javascript
async function getStorageInfo() {
  if (!navigator.storage || !navigator.storage.estimate) {
    return { supported: false };
  }

  const estimate = await navigator.storage.estimate();

  return {
    supported: true,
    usedBytes: estimate.usage,
    quotaBytes: estimate.quota,
    usedMB: (estimate.usage / 1024 / 1024).toFixed(2),
    quotaMB: (estimate.quota / 1024 / 1024).toFixed(2),
    percentUsed: ((estimate.usage / estimate.quota) * 100).toFixed(1)
  };
}

// Uso
const info = await getStorageInfo();
console.log(`Usando ${info.usedMB} MB de ${info.quotaMB} MB (${info.percentUsed}%)`);

if (parseFloat(info.percentUsed) > 80) {
  alert('⚠️ Storage quase cheio! Considere limpar dados antigos.');
}
```

---

### Padrão 2: Limitar Tamanho de Notas

**Implementação:**
```javascript
const MAX_NOTE_SIZE_BYTES = 50 * 1024; // 50KB

function validateNoteSize(text) {
  const sizeBytes = new Blob([text]).size;
  const sizeKB = (sizeBytes / 1024).toFixed(2);

  if (sizeBytes > MAX_NOTE_SIZE_BYTES) {
    return {
      valid: false,
      size: sizeKB,
      limit: '50.00',
      message: `Nota muito grande (${sizeKB} KB). Limite: 50 KB.`
    };
  }

  return { valid: true, size: sizeKB };
}

// Uso no componente
function CNotesView({ courseId }) {
  const [notes, setNotes] = useState('');
  const [sizeWarning, setSizeWarning] = useState(null);

  const handleChange = (e) => {
    const newText = e.target.value;
    const validation = validateNoteSize(newText);

    if (!validation.valid) {
      setSizeWarning(validation.message);
      return; // Bloquear input adicional
    }

    setSizeWarning(null);
    setNotes(newText);
  };

  return (
    <div>
      <textarea value={notes} onChange={handleChange} maxLength={25000} />
      {sizeWarning && <p className="text-red-600">{sizeWarning}</p>}
      <p className="text-sm text-gray-500">
        Tamanho: {(new Blob([notes]).size / 1024).toFixed(2)} KB / 50 KB
      </p>
    </div>
  );
}
```

---

### Padrão 3: Limpar Dados Antigos

**Estratégia:** Remover dados não acessados por 90+ dias.

**Implementação:**
```javascript
function clearOldData(daysThreshold = 90) {
  const now = Date.now();
  const keys = Object.keys(localStorage);
  let freedBytes = 0;

  keys.forEach(key => {
    if (!key.startsWith('ultrathink_')) return;

    try {
      const data = JSON.parse(localStorage.getItem(key));

      // Schema com timestamp
      if (data && data.lastUpdated) {
        const ageInDays = (now - data.lastUpdated) / (1000 * 60 * 60 * 24);

        if (ageInDays > daysThreshold) {
          const size = new Blob([localStorage.getItem(key)]).size;
          localStorage.removeItem(key);
          freedBytes += size;
          console.log(`Removido: ${key} (${ageInDays.toFixed(0)} dias)`);
        }
      }
    } catch (error) {
      console.warn(`Erro ao processar ${key}:`, error);
    }
  });

  const freedKB = (freedBytes / 1024).toFixed(2);
  console.log(`Liberados ${freedKB} KB de armazenamento`);

  return freedKB;
}
```

---

## 🗂️ Schema Design

### Padrão 1: Versionamento de Schema

**Princípio:** Schemas evoluem, dados antigos devem migrar.

**Implementação:**
```javascript
// Schema v1 (antigo)
{
  "notes": "Texto das notas...",
  "lastSaved": 1700000000000
}

// Schema v2 (novo - com versão)
{
  "version": 2,
  "notes": "Texto das notas...",
  "metadata": {
    "lastSaved": 1700000000000,
    "lastUpdated": 1700000000000,
    "wordCount": 150,
    "characterCount": 850
  }
}

// Função de migração
function migrateNotesSchema(key) {
  const raw = localStorage.getItem(key);
  if (!raw) return null;

  try {
    const data = JSON.parse(raw);

    // Detectar versão
    if (!data.version) {
      // Migrar v1 → v2
      const migrated = {
        version: 2,
        notes: data.notes || '',
        metadata: {
          lastSaved: data.lastSaved || Date.now(),
          lastUpdated: Date.now(),
          wordCount: (data.notes || '').split(/\s+/).length,
          characterCount: (data.notes || '').length
        }
      };

      localStorage.setItem(key, JSON.stringify(migrated));
      console.log(`Migrado ${key} para v2`);
      return migrated;
    }

    return data; // Já está na versão atual
  } catch (error) {
    console.error(`Erro ao migrar ${key}:`, error);
    return null;
  }
}
```

---

### Padrão 2: Namespace de Keys

**Princípio:** Prefixar todas as keys para evitar conflitos.

**Convenção do Projeto:**
```javascript
// Namespace: ultrathink_<tipo>_<identificador>

// Notas por curso
'ultrathink_notes_bash'
'ultrathink_notes_c'
'ultrathink_notes_rust'

// Progresso por curso
'ultrathink_progress_bash'
'ultrathink_progress_c'
'ultrathink_progress_rust'

// Configurações globais
'ultrathink_settings_theme'
'ultrathink_settings_language'

// Sessão temporária
'ultrathink_session_current_view'

// Função helper
function getKey(type, identifier) {
  return `ultrathink_${type}_${identifier}`;
}

// Uso
const key = getKey('notes', 'bash'); // 'ultrathink_notes_bash'
```

---

### Padrão 3: JSON Schema para Progresso

**Estrutura recomendada:**
```javascript
// Schema para progresso de módulos
{
  "version": 1,
  "courseId": "c",
  "totalModules": 50,
  "completedModules": [
    { "id": "1.1", "completedAt": 1700000000000 },
    { "id": "1.2", "completedAt": 1700000100000 },
    { "id": "2.1", "completedAt": 1700000200000 }
  ],
  "progress": {
    "percentage": 6, // 3/50 * 100
    "lastUpdated": 1700000200000
  }
}

// Operações CRUD
class CourseProgress {
  constructor(courseId, totalModules) {
    this.key = `ultrathink_progress_${courseId}`;
    this.courseId = courseId;
    this.totalModules = totalModules;
  }

  load() {
    try {
      const raw = localStorage.getItem(this.key);
      return raw ? JSON.parse(raw) : this.getDefaultSchema();
    } catch (error) {
      console.error('Erro ao carregar progresso:', error);
      return this.getDefaultSchema();
    }
  }

  getDefaultSchema() {
    return {
      version: 1,
      courseId: this.courseId,
      totalModules: this.totalModules,
      completedModules: [],
      progress: { percentage: 0, lastUpdated: Date.now() }
    };
  }

  markComplete(moduleId) {
    const data = this.load();

    // Evitar duplicatas
    if (data.completedModules.some(m => m.id === moduleId)) {
      return data;
    }

    data.completedModules.push({
      id: moduleId,
      completedAt: Date.now()
    });

    data.progress.percentage = Math.round(
      (data.completedModules.length / this.totalModules) * 100
    );
    data.progress.lastUpdated = Date.now();

    try {
      localStorage.setItem(this.key, JSON.stringify(data));
    } catch (error) {
      if (error.name === 'QuotaExceededError') {
        alert('Storage cheio! Não foi possível salvar progresso.');
      }
      throw error;
    }

    return data;
  }

  isCompleted(moduleId) {
    const data = this.load();
    return data.completedModules.some(m => m.id === moduleId);
  }

  reset() {
    localStorage.removeItem(this.key);
  }
}

// Uso
const cProgress = new CourseProgress('c', 50);
cProgress.markComplete('1.1');
console.log(cProgress.isCompleted('1.1')); // true
```

---

## 🔧 Exemplos Práticos do Projeto

### Exemplo 1: CNotesView (Atual - SEM Error Handling)

**Localização:** `src/components/CNotesView.jsx`

**Código Atual (ANTES - ❌ Problemático):**
```jsx
function CNotesView({ onBack }) {
  const [notes, setNotes] = useState('');

  useEffect(() => {
    // ❌ Sem try/catch!
    const savedNotes = localStorage.getItem('c-learning-notes');
    if (savedNotes) {
      setNotes(savedNotes);
    }
  }, []);

  useEffect(() => {
    // ❌ Sem try/catch!
    // ❌ Sem debounce (salva a cada keystroke!)
    localStorage.setItem('c-learning-notes', notes);
  }, [notes]);

  return (
    <textarea
      value={notes}
      onChange={(e) => setNotes(e.target.value)}
      placeholder="Minhas anotações sobre C..."
    />
  );
}
```

**Problemas:**
1. ❌ Sem try/catch (pode crashar em modo privado)
2. ❌ Sem debounce (performance ruim com 1000+ keystrokes)
3. ❌ Sem tratamento de QuotaExceededError
4. ❌ Sem feedback ao usuário (salvando? erro?)
5. ❌ Sem limite de tamanho (pode exceder quota)

---

**Código Refatorado (DEPOIS - ✅ Robusto):**
```jsx
function CNotesView({ onBack }) {
  const [notes, setNotes, saveStatus] = useAutoSaveNotes('c');
  const [sizeInfo, setSizeInfo] = useState({ size: 0, percentage: 0 });

  useEffect(() => {
    const sizeBytes = new Blob([notes]).size;
    const sizeKB = sizeBytes / 1024;
    const percentage = (sizeBytes / (50 * 1024)) * 100;

    setSizeInfo({ size: sizeKB.toFixed(2), percentage: percentage.toFixed(1) });
  }, [notes]);

  return (
    <div className="notes-container">
      <div className="notes-header">
        <button onClick={onBack}>← Voltar</button>

        <div className="save-status">
          {saveStatus === 'saving' && <span>💾 Salvando...</span>}
          {saveStatus === 'saved' && <span>✅ Salvo automaticamente</span>}
          {saveStatus === 'error' && (
            <span className="text-red-600">⚠️ Erro ao salvar</span>
          )}
        </div>
      </div>

      <textarea
        value={notes}
        onChange={(e) => setNotes(e.target.value)}
        placeholder="Minhas anotações sobre C..."
        className="w-full h-96 p-4 border rounded"
      />

      <div className="notes-footer text-sm text-gray-500">
        <span>Tamanho: {sizeInfo.size} KB / 50 KB ({sizeInfo.percentage}%)</span>
        {parseFloat(sizeInfo.percentage) > 80 && (
          <span className="text-yellow-600 ml-4">
            ⚠️ Nota grande, considere dividir em arquivos menores
          </span>
        )}
      </div>
    </div>
  );
}
```

**Arquivo real:** `src/components/CNotesView.jsx:1-80`

---

### Exemplo 2: Hook useAutoSaveNotes (Novo - Para US-041)

**Localização:** `src/hooks/useAutoSaveNotes.js` (criar)

**Implementação Completa:**
```javascript
import { useState, useEffect, useRef } from 'react';

/**
 * Hook para auto-save de notas com error handling robusto
 *
 * @param {string} courseId - ID do curso ('c', 'bash', 'rust', etc.)
 * @param {number} debounceMs - Delay para auto-save (padrão: 1000ms)
 * @returns {[string, function, string]} [notes, setNotes, saveStatus]
 */
export function useAutoSaveNotes(courseId, debounceMs = 1000) {
  const [notes, setNotes] = useState('');
  const [saveStatus, setSaveStatus] = useState('idle'); // idle, saving, saved, error
  const [storageAvailable, setStorageAvailable] = useState(true);
  const timerRef = useRef(null);

  const key = `ultrathink_notes_${courseId}`;

  // Carregar notas ao montar
  useEffect(() => {
    try {
      const saved = localStorage.getItem(key);
      if (saved) {
        setNotes(saved);
        setSaveStatus('saved');
      }
    } catch (error) {
      console.error('Erro ao carregar notas:', error);

      if (error.name === 'SecurityError') {
        setStorageAvailable(false);
        setSaveStatus('error');
      }
    }
  }, [key]);

  // Auto-save com debounce
  useEffect(() => {
    if (!storageAvailable) return;

    // Limpar timer anterior
    if (timerRef.current) {
      clearTimeout(timerRef.current);
    }

    setSaveStatus('saving');

    timerRef.current = setTimeout(() => {
      try {
        // Validar tamanho
        const sizeBytes = new Blob([notes]).size;
        const MAX_SIZE = 50 * 1024; // 50KB

        if (sizeBytes > MAX_SIZE) {
          console.warn(`Nota muito grande: ${(sizeBytes / 1024).toFixed(2)} KB`);
          setSaveStatus('error');

          // Tentar comprimir (remover espaços extras)
          const compressed = notes.replace(/\s+/g, ' ').trim();
          const compressedSize = new Blob([compressed]).size;

          if (compressedSize <= MAX_SIZE) {
            localStorage.setItem(key, compressed);
            setSaveStatus('saved');
            console.log('Nota comprimida e salva');
          } else {
            alert('⚠️ Nota muito grande! Limite: 50KB');
          }
          return;
        }

        localStorage.setItem(key, notes);
        setSaveStatus('saved');

      } catch (error) {
        console.error('Erro ao salvar notas:', error);
        setSaveStatus('error');

        if (error.name === 'QuotaExceededError') {
          // Fallback: sessionStorage
          try {
            sessionStorage.setItem(`${key}_temp`, notes);
            alert('⚠️ Storage cheio! Nota salva temporariamente.');
          } catch (e) {
            alert('❌ Não foi possível salvar a nota.');
          }
        } else if (error.name === 'SecurityError') {
          setStorageAvailable(false);
          alert('🔒 Modo privado detectado. Notas não serão persistidas.');
        }
      }
    }, debounceMs);

    return () => {
      if (timerRef.current) {
        clearTimeout(timerRef.current);
      }
    };
  }, [notes, key, debounceMs, storageAvailable]);

  return [notes, setNotes, saveStatus];
}
```

**Arquivo real:** `src/hooks/useAutoSaveNotes.js:1-95` (criar para US-041)

---

### Exemplo 3: Hook useModuleProgress (Novo - Para US-042)

**Localização:** `src/hooks/useModuleProgress.js` (criar)

**Implementação Completa:**
```javascript
import { useState, useEffect, useCallback } from 'react';

/**
 * Hook para gerenciar progresso de módulos
 *
 * @param {string} courseId - ID do curso
 * @param {number} totalModules - Total de módulos no curso
 * @returns {[string[], function, object]} [completedIds, markComplete, progressInfo]
 */
export function useModuleProgress(courseId, totalModules) {
  const [completed, setCompleted] = useState([]);
  const key = `ultrathink_progress_${courseId}`;

  // Carregar progresso ao montar
  useEffect(() => {
    try {
      const raw = localStorage.getItem(key);
      if (raw) {
        const data = JSON.parse(raw);
        setCompleted(data.completedModules.map(m => m.id));
      }
    } catch (error) {
      console.error('Erro ao carregar progresso:', error);
    }
  }, [key]);

  // Marcar módulo como completo
  const markComplete = useCallback((moduleId) => {
    if (completed.includes(moduleId)) {
      console.log(`Módulo ${moduleId} já completo`);
      return;
    }

    const newCompleted = [...completed, moduleId];
    setCompleted(newCompleted);

    const data = {
      version: 1,
      courseId,
      totalModules,
      completedModules: newCompleted.map(id => ({
        id,
        completedAt: Date.now()
      })),
      progress: {
        percentage: Math.round((newCompleted.length / totalModules) * 100),
        lastUpdated: Date.now()
      }
    };

    try {
      localStorage.setItem(key, JSON.stringify(data));
    } catch (error) {
      console.error('Erro ao salvar progresso:', error);

      if (error.name === 'QuotaExceededError') {
        alert('⚠️ Storage cheio! Progresso não salvo.');
      }
    }
  }, [completed, courseId, totalModules, key]);

  // Resetar progresso
  const reset = useCallback(() => {
    setCompleted([]);
    try {
      localStorage.removeItem(key);
    } catch (error) {
      console.error('Erro ao resetar progresso:', error);
    }
  }, [key]);

  // Info de progresso
  const progressInfo = {
    completed: completed.length,
    total: totalModules,
    percentage: Math.round((completed.length / totalModules) * 100),
    remaining: totalModules - completed.length
  };

  return [completed, markComplete, progressInfo, reset];
}
```

**Arquivo real:** `src/hooks/useModuleProgress.js:1-80` (criar para US-042)

---

## ❌ Antipadrões a Evitar

### 1. Operações Síncronas Sem Try/Catch

**❌ Não fazer:**
```javascript
// Pode crashar a aplicação!
const notes = localStorage.getItem('notes');
localStorage.setItem('notes', newNotes);
```

**✅ Fazer:**
```javascript
try {
  const notes = localStorage.getItem('notes');
  localStorage.setItem('notes', newNotes);
} catch (error) {
  console.error('Erro localStorage:', error);
  // Fallback
}
```

---

### 2. Salvar a Cada Keystroke (Sem Debounce)

**❌ Não fazer:**
```javascript
// 1000 keystrokes = 1000 escritas no localStorage!
<textarea onChange={(e) => {
  localStorage.setItem('notes', e.target.value);
}} />
```

**✅ Fazer:**
```javascript
// Debounce de 1 segundo
useEffect(() => {
  const timer = setTimeout(() => {
    localStorage.setItem('notes', notes);
  }, 1000);

  return () => clearTimeout(timer);
}, [notes]);
```

---

### 3. Salvar Dados Sensíveis

**❌ Não fazer:**
```javascript
// localStorage NÃO é criptografado!
localStorage.setItem('user_password', password);
localStorage.setItem('credit_card', cardNumber);
```

**✅ Fazer:**
```javascript
// Dados sensíveis: usar backend + HTTPS
await fetch('/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password })
});
```

---

### 4. Usar localStorage em Loops

**❌ Não fazer:**
```javascript
// 1000 iterações = 1000 escritas!
for (let i = 0; i < 1000; i++) {
  localStorage.setItem(`item_${i}`, data[i]);
}
```

**✅ Fazer:**
```javascript
// Batch: salvar tudo de uma vez
const batch = data.map((item, i) => ({ id: i, data: item }));
localStorage.setItem('items_batch', JSON.stringify(batch));
```

---

### 5. Não Versionar Schema

**❌ Não fazer:**
```javascript
// Mudou a estrutura? Dados antigos quebram!
localStorage.setItem('progress', JSON.stringify({ ids: [1, 2, 3] }));
// 6 meses depois...
localStorage.setItem('progress', JSON.stringify({ modules: [{id: 1}] }));
```

**✅ Fazer:**
```javascript
// Sempre incluir versão
const data = {
  version: 2,
  modules: [{ id: 1, completedAt: Date.now() }]
};

// Migrar ao carregar
function load() {
  const raw = localStorage.getItem('progress');
  const data = JSON.parse(raw);

  if (data.version === 1) {
    return migrateV1toV2(data);
  }

  return data;
}
```

---

## 🚨 Troubleshooting

### Problema 1: "Notas não salvam em modo privado"

**Sintoma:**
- Usuário em Safari/Firefox modo privado
- Console: `SecurityError: The operation is insecure`

**Diagnóstico:**
```javascript
function isPrivateMode() {
  try {
    localStorage.setItem('test', 'test');
    localStorage.removeItem('test');
    return false;
  } catch (e) {
    return e.name === 'SecurityError';
  }
}

if (isPrivateMode()) {
  console.log('Modo privado detectado!');
}
```

**Solução:**
```javascript
// Fallback para sessionStorage
function safeSetItem(key, value) {
  try {
    localStorage.setItem(key, value);
  } catch (error) {
    if (error.name === 'SecurityError') {
      // Tentar sessionStorage
      sessionStorage.setItem(key, value);
      console.warn('Usando sessionStorage (modo privado)');
    }
  }
}
```

---

### Problema 2: "Storage cheio (QuotaExceededError)"

**Sintoma:**
- Console: `QuotaExceededError: Failed to execute 'setItem'`
- Usuário com notas muito grandes

**Diagnóstico:**
```javascript
// Calcular tamanho usado
function calculateTotalSize() {
  let total = 0;
  Object.keys(localStorage).forEach(key => {
    total += new Blob([localStorage.getItem(key)]).size;
  });
  return (total / 1024 / 1024).toFixed(2); // MB
}

console.log(`Total usado: ${calculateTotalSize()} MB`);
```

**Solução:**
```javascript
// Limpar dados antigos
function clearOldData() {
  const keys = Object.keys(localStorage);
  keys.forEach(key => {
    if (!key.startsWith('ultrathink_')) return;

    try {
      const data = JSON.parse(localStorage.getItem(key));
      if (data.lastUpdated && Date.now() - data.lastUpdated > 90 * 24 * 60 * 60 * 1000) {
        localStorage.removeItem(key);
        console.log(`Removido: ${key}`);
      }
    } catch (e) {
      // Ignorar dados inválidos
    }
  });
}

// Chamar antes de salvar
try {
  localStorage.setItem('key', 'value');
} catch (error) {
  if (error.name === 'QuotaExceededError') {
    clearOldData();
    // Tentar novamente
    localStorage.setItem('key', 'value');
  }
}
```

---

### Problema 3: "Dados corruptos (JSON.parse falha)"

**Sintoma:**
- Console: `SyntaxError: Unexpected token in JSON`
- Dados não carregam

**Diagnóstico:**
```javascript
function validateLocalStorageData() {
  const keys = Object.keys(localStorage).filter(k => k.startsWith('ultrathink_'));

  keys.forEach(key => {
    try {
      JSON.parse(localStorage.getItem(key));
      console.log(`✅ ${key} válido`);
    } catch (error) {
      console.error(`❌ ${key} corrompido:`, error);
      localStorage.removeItem(key);
    }
  });
}
```

**Solução:**
```javascript
function safeGetItem(key, defaultValue = null) {
  try {
    const raw = localStorage.getItem(key);
    if (!raw) return defaultValue;

    return JSON.parse(raw);
  } catch (error) {
    console.error(`Erro ao parsear ${key}:`, error);

    // Remover dado corrompido
    localStorage.removeItem(key);
    return defaultValue;
  }
}

// Uso
const notes = safeGetItem('ultrathink_notes_c', '');
```

---

### Problema 4: "Progresso desaparece ao recarregar"

**Sintoma:**
- Progresso salvo mas não aparece após F5
- localStorage vazio

**Diagnóstico:**
```javascript
// Verificar se key está correta
console.log('Keys Ultrathink:', Object.keys(localStorage).filter(k => k.startsWith('ultrathink_')));

// Verificar em outra tab (mesmo domínio)
// localStorage é compartilhado entre tabs da mesma origem
```

**Causas comuns:**
1. Key incorreta (`ultrathink_notes_c` vs `c-learning-notes`)
2. Limpar storage ao desmontar (erro de código)
3. Browser limpa localStorage (configuração)

**Solução:**
```javascript
// Usar constantes para keys
const STORAGE_KEYS = {
  notes: (courseId) => `ultrathink_notes_${courseId}`,
  progress: (courseId) => `ultrathink_progress_${courseId}`
};

// Nunca limpar ao desmontar
useEffect(() => {
  // ✅ Carregar
  const notes = localStorage.getItem(STORAGE_KEYS.notes('c'));

  // ❌ NÃO fazer cleanup de localStorage!
  return () => {
    // localStorage.removeItem(...); // ❌ Errado!
  };
}, []);
```

---

### Problema 5: "Performance ruim com muitas escritas"

**Sintoma:**
- UI trava ao digitar
- Muitas operações localStorage/segundo

**Diagnóstico:**
```javascript
// Contar operações
let writeCount = 0;
const originalSetItem = localStorage.setItem;
localStorage.setItem = function(...args) {
  writeCount++;
  return originalSetItem.apply(this, args);
};

setInterval(() => {
  console.log(`Escritas/segundo: ${writeCount}`);
  writeCount = 0;
}, 1000);
```

**Solução:**
```javascript
// Debounce obrigatório
function useDebouncedLocalStorage(key, value, delay = 1000) {
  useEffect(() => {
    const timer = setTimeout(() => {
      localStorage.setItem(key, value);
    }, delay);

    return () => clearTimeout(timer);
  }, [key, value, delay]);
}
```

---

## 📚 Referências

### Skills Relacionadas

- **[react-components-patterns](../react-components-patterns/SKILL.md)** - Hooks customizados (useAutoSaveNotes)
- **[ultrathink-arch](../ultrathink-arch/SKILL.md)** - Arquitetura e localStorage keys
- **[system-state-management](../system-state-management/SKILL.md)** - Sincronização localStorage ↔ React

### Documentação Técnica

- **[docs/tecnico/storage/](../../docs/tecnico/storage/)** - Documentação completa de storage (criar)
- **[ROADMAP.md](../../docs/backlog/ROADMAP.md)** - US-041, US-042 (user stories)

### Código Real do Projeto

**Componentes com localStorage (ANTES da refatoração):**
- `src/components/CNotesView.jsx:45-60` - Notas de C (sem error handling)
- `src/components/BashNotesView.jsx:45-60` - Notas de Bash (duplicado)
- `src/components/RustNotesView.jsx:45-60` - Notas de Rust (duplicado)
- `src/components/VSCodeNotesView.jsx:45-60` - Notas de VSCode (duplicado)
- `src/components/ClaudeCodeNotesView.jsx:45-60` - Notas de Claude Code (duplicado)

**Hooks Customizados (DEPOIS da refatoração - US-041, US-042):**
- `src/hooks/useAutoSaveNotes.js` - Auto-save com error handling
- `src/hooks/useModuleProgress.js` - Gerenciamento de progresso

### Recursos Externos

- **[MDN - Web Storage API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API)**
- **[MDN - Storage API](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API)** - Quota management
- **[Can I Use - localStorage](https://caniuse.com/namevalue-storage)** - Suporte por browser
- **[Web.dev - Storage Limits](https://web.dev/storage-for-the-web/)** - Limites detalhados

---

## 📝 Arquivos Auxiliares

Esta skill possui 3 arquivos auxiliares detalhados:

1. **[error-handling.md](./auxiliary/error-handling.md)** - Guia completo de tratamento de erros
2. **[quota-management.md](./auxiliary/quota-management.md)** - Estratégias de gerenciamento de quota
3. **[troubleshooting.md](./auxiliary/troubleshooting.md)** - Diagnósticos e soluções para problemas comuns

---

**📍 Você está em:** `.claude/skills/localStorage-patterns/SKILL.md`
**📅 Criado em:** 2025-11-19
**👤 Mantido por:** João Pelegrino + Claude Code
**🎯 Uso:** Referência para implementar localStorage no projeto (US-041, US-042)
**🔄 Última auditoria:** 2025-11-19
**📊 Auto-discovery score:** TBD (testar após criação)
**🚀 Desbloqueia:** US-041 (error handling), US-042 (persist progress), L0-04 (treinamento)
