---
name: debugging_tools
router_kit: FullStackKit
description: Debugging araçları - console, debugger, network, profiling.
metadata:
  skillport:
    category: quality
    tags: [architecture, automation, best practices, clean code, coding, collaboration, compliance, debugging, debugging tools, design patterns, development, documentation, efficiency, git, optimization, productivity, programming, project management, quality assurance, refactoring, software engineering, standards, testing, utilities, version control, workflow]      - debugging-methodology
---

# 🛠️ Debugging Tools

> Debugging araçları ve teknikleri.

---

## 💻 Console Methods

```typescript
console.log('Value:', value);
console.table(arrayData);
console.group('Section');
console.trace('Stack trace');
console.time('op'); /* ... */ console.timeEnd('op');
```

---

## 🔴 Debugger

```typescript
function process(data) {
  debugger; // Breakpoint
  return transform(data);
}
```

```bash
# Node Inspector
node --inspect src/index.js
# chrome://inspect
```

---

## 🌐 Network

```typescript
// Axios interceptor
axios.interceptors.request.use(config => {
  console.log('Request:', config);
  return config;
});
```

---

## 📊 Logging

```typescript
import pino from 'pino';

const logger = pino({ level: 'info' });
logger.info({ userId }, 'User logged in');
logger.error({ err }, 'Login failed');
```

---

## 🔄 Workflow

> **Kaynak:** [OpenTelemetry Documentation](https://opentelemetry.io/docs/) & [Chrome DevTools Debugging Guide](https://developer.chrome.com/docs/devtools/javascript/)

### Aşama 1: Observation & Reproduction
- [ ] **Logging Audit**: Hata anında yeterli bağlam (Context) sağlayan logların (Pino/Winston) basılıp basılmadığını kontrol et.
- [ ] **Reproduction**: Hatayı lokal ortamda veya `staging` üzerinde tutarlı bir şekilde tekrarlayabilmek için gerekli input'ları belirle.
- [ ] **Network Analysis**: API çağrılarını ve payload'ları Tarayıcı Network Tab veya Proxyman/Charles üzerinden izle.

### Aşama 2: Strategic Debugging
- [ ] **Breakpoints**: `debugger` veya IDE breakpoint'leri kullanarak state'in nerede bozulduğunu adım adım (Step-over/Step-into) takip et.
- [ ] **Binary Search**: Hatalı kod bloğunu bulmak için kodun büyük bölümlerini geçici olarak devre dışı bırak (Divide and Conquer).
- [ ] **Memory Profiling**: Memory leak durumunda Heap Snapshot alarak en çok yer kaplayan objeleri analiz et.

### Aşama 3: Fix & Verification
- [ ] **Root Cause Fix**: Sadece semptomu değil, hatanın kök nedenini (Root Cause) düzelt.
- [ ] **Regression Testing**: Düzeltmenin başka yerleri bozmadığından emin olmak için ilgili testleri çalıştır.
- [ ] **Observability Update**: Benzer hataların gelecekte daha hızlı tespiti için yeni bir alert veya metric ekle.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Hata "silinebilir" loglarla mı (console.log) yoksa kalıcı loglarla mı çözüldü? |
| 2 | Trace ID üzerinden tüm request flow'u (Distributed Tracing) takip edilebiliyor mu? |
| 3 | Hata düzeltmesi için bir test senaryosu eklendi mi? |

---
*Debugging Tools v1.5 - With Workflow*
