---
name: codemap-update
description: >
  Codebase haritasını güncelle. "/codemap-update" komutuyla veya
  her feature implementation sonrasında otomatik çalışır. Claude'un
  codebase'de gezinmesini context harcamadan sağlar.
---

# Codemap Update Workflow

## Amaç
Claude'un codebase'i her seferinde keşfetmek için context harcamaması için
güncel bir harita tut.

## Adımlar

### 1. Mevcut Codemap Kontrol Et
`.claude/codemap.md` dosyası var mı? Yoksa oluştur.

### 2. Proje Yapısını Tara
```bash
find src/ -name "*.ts" -o -name "*.tsx" | sort
```

### 3. Codemap'i Güncelle
`.claude/codemap.md` dosyasına şunu yaz:

```markdown
# Codemap — [tarih]

## Screens
- src/screens/HomeScreen.tsx → Ana ekran, todo listesi
- src/screens/AddTodoScreen.tsx → Yeni todo ekleme formu

## Components
- src/components/TodoItem.tsx → Tekil todo satırı (toggle, delete)
- src/components/TodoList.tsx → Todo listesi (FlatList wrapper)
- src/components/AddTodoInput.tsx → Input + buton

## Hooks
- src/hooks/useTodos.ts → Todo CRUD operasyonları
- src/hooks/useFilter.ts → Filtre state'i

## Store
- src/store/todo.store.ts → Zustand todo store
  - State: todos[], filter, loading
  - Actions: addTodo, toggleTodo, deleteTodo, setFilter

## Services  
- src/services/storage.service.ts → AsyncStorage wrapper
  - saveTodos(), loadTodos(), clearTodos()

## Tests
- src/components/__tests__/TodoItem.test.tsx
- src/hooks/__tests__/useTodos.test.ts
```

### 4. Checkpoint Notu Ekle
Codemap'in sonuna:
```
## Son Güncelleme
- Tarih: [bugün]
- Son eklenen: [son feature adı]
- Test coverage: [son bilinen %]
```

Bu harita sayesinde yeni session'larda Claude tüm dosyaları okumak yerine
bu haritayı okuyarak hızlıca context kurar.
