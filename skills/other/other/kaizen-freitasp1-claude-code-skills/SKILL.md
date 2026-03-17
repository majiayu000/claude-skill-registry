---
name: kaizen
description: Manufacturing-fokussierter Continuous Improvement Skill fuer fabrikIQ. Implementiert Lean Manufacturing Prinzipien (5 Whys, Ishikawa, PDCA) fuer systematische Problemloesung und Qualitaetsverbesserung. Aktivieren bei Bug-Analyse, Refactoring, Code Review, Production Incidents.
triggers:
  - /why
  - /cause-and-effect
  - /plan-do-check-act
  - /kaizen
---

# Kaizen - Continuous Improvement Skill

Dieser Skill bringt bewaehrte Lean Manufacturing Methoden in die Softwareentwicklung. Entwickelt fuer fabrikIQ, anwendbar auf jedes TypeScript/React Projekt.

## Die 4 Saeulen des Kaizen

### 1. Continuous Improvement (Kaizen)
Kleine, inkrementelle Aenderungen statt Big Bang Refactoring.

**Prinzip**: Jeder Commit sollte den Code minimal besser hinterlassen als vorgefunden.

```typescript
// VORHER: Grosses Refactoring geplant
// "Ich refactore mal schnell die ganze Auth-Logik"

// KAIZEN: Kleine Schritte
// Commit 1: Extrahiere validateToken() aus auth.ts
// Commit 2: Fuege Typen fuer TokenPayload hinzu
// Commit 3: Ersetze any mit unknown + Type Guard
// Commit 4: Schreibe Unit Test fuer validateToken()
```

### 2. Poka-Yoke (Error Proofing)
Fehler durch Design verhindern, nicht durch Disziplin.

**TypeScript Constraints**:
```typescript
// FALSCH: Runtime Check (Fehler moeglich)
function processOrder(status: string) {
  if (status !== 'pending' && status !== 'approved') {
    throw new Error('Invalid status');
  }
}

// POKA-YOKE: Compile-Time Constraint (Fehler unmoeglich)
type OrderStatus = 'pending' | 'approved' | 'shipped' | 'cancelled';

function processOrder(status: OrderStatus) {
  // TypeScript verhindert ungueltige Werte
}
```

**Fail-Fast Pattern**:
```typescript
// FALSCH: Spaete Fehlererkennung
async function analyzeData(file: File) {
  const data = await parseFile(file);  // 10 Sekunden
  const result = await geminiAnalyze(data);  // 30 Sekunden
  if (!data.hasRequiredColumns()) {  // Fehler erst nach 40 Sekunden!
    throw new Error('Missing columns');
  }
}

// POKA-YOKE: Fail-Fast (fruehe Validierung)
async function analyzeData(file: File) {
  // Validierung ZUERST (< 1ms)
  const preview = await parseFilePreview(file, 10);
  if (!preview.hasRequiredColumns()) {
    throw new Error('Missing columns');  // Sofort!
  }

  // Teure Operationen NUR wenn valide
  const data = await parseFile(file);
  const result = await geminiAnalyze(data);
}
```

### 3. Standardized Work
Konsistente Patterns reduzieren kognitive Last und Fehler.

**API Response Pattern (fabrikIQ Standard)**:
```typescript
// Standard Response Format
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: unknown;
  };
  meta?: {
    timestamp: string;
    duration_ms: number;
    region: 'fra1';  // DSGVO
  };
}

// Alle Endpoints nutzen dieses Format
export async function handler(req: Request): Promise<Response> {
  const start = Date.now();
  try {
    const result = await processRequest(req);
    return Response.json({
      success: true,
      data: result,
      meta: {
        timestamp: new Date().toISOString(),
        duration_ms: Date.now() - start,
        region: 'fra1'
      }
    });
  } catch (error) {
    return Response.json({
      success: false,
      error: {
        code: error.code ?? 'UNKNOWN_ERROR',
        message: error.message
      }
    }, { status: error.status ?? 500 });
  }
}
```

### 4. Just-In-Time (YAGNI)
Implementiere nur was JETZT gebraucht wird.

```typescript
// FALSCH: "Vielleicht brauchen wir das spaeter"
interface User {
  id: string;
  email: string;
  name: string;
  // "Fuer spaeter"
  avatar?: string;
  preferences?: UserPreferences;
  notifications?: NotificationSettings;
  integrations?: ExternalIntegrations;
  analytics?: UserAnalytics;
}

// YAGNI: Nur aktuelle Requirements
interface User {
  id: string;
  email: string;
  name: string;
}

// Erweitern wenn tatsaechlich benoetigt (mit eigenem Commit)
```

---

## Befehle

### /why - 5-Whys Root Cause Analysis

**Trigger**: `/why`, `5 whys`, `root cause`, `warum passiert`

**Anwendung**: Bei Bugs, Production Incidents, wiederkehrenden Problemen

**Workflow**:

1. **Problem definieren** (konkret, messbar)
   ```
   Problem: API Timeout bei SECOM-Dataset (504 nach 60s)
   ```

2. **5x "Warum?" fragen**
   ```
   Why 1: Warum Timeout?
   → Gemini API braucht >60s fuer Antwort

   Why 2: Warum >60s?
   → Prompt enthaelt 590 Spalten x 1567 Zeilen

   Why 3: Warum so viele Daten?
   → Kein Column Sampling implementiert

   Why 4: Warum kein Sampling?
   → Urspruenglich nur kleine CSVs erwartet

   Why 5: Warum nicht angepasst?
   → Keine automatischen Performance-Tests mit grossen Dateien
   ```

3. **Root Cause identifizieren**
   ```
   Root Cause: Fehlende Performance-Testabdeckung fuer grosse Datasets
   ```

4. **Countermeasure definieren**
   ```
   Massnahme 1: Column Sampling (MAX_COLUMNS = 50) implementieren
   Massnahme 2: Performance-Test mit SECOM in CI/CD hinzufuegen
   Massnahme 3: Timeout-Monitoring mit Alerting einrichten
   ```

**Output-Format**:
```markdown
## 5-Whys Analyse

**Problem**: [Konkrete Beschreibung]
**Datum**: [ISO-8601]
**Betroffene Komponente**: [Datei/Service]

### Analyse

| Level | Frage | Antwort |
|-------|-------|---------|
| Why 1 | Warum [Symptom]? | [Antwort] |
| Why 2 | Warum [Antwort 1]? | [Antwort] |
| Why 3 | Warum [Antwort 2]? | [Antwort] |
| Why 4 | Warum [Antwort 3]? | [Antwort] |
| Why 5 | Warum [Antwort 4]? | [Antwort] |

### Root Cause
[Kernursache in einem Satz]

### Countermeasures
1. **Sofort** (< 1 Tag): [Quick Fix]
2. **Kurzfristig** (< 1 Woche): [Strukturelle Loesung]
3. **Langfristig** (< 1 Monat): [Praevention]
```

---

### /cause-and-effect - Ishikawa Diagram

**Trigger**: `/cause-and-effect`, `/ishikawa`, `/fishbone`, `ursache-wirkung`

**Anwendung**: Bei komplexen Problemen mit mehreren moeglichen Ursachen

**Die 6 M-Kategorien (Manufacturing)**:

1. **Mensch** (People): Skills, Training, Kommunikation
2. **Maschine** (Machine): Hardware, Tools, Infrastructure
3. **Material** (Material): Input-Daten, Dependencies
4. **Methode** (Method): Prozesse, Workflows, Patterns
5. **Messung** (Measurement): Monitoring, Tests, Metriken
6. **Milieu** (Environment): Production, Staging, Local

**Workflow**:

1. **Effekt definieren** (rechts)
   ```
   Effekt: Login schlaegt intermittierend fehl
   ```

2. **Ursachen nach Kategorie sammeln**
   ```
   MENSCH:
   ├── Nutzer loescht Cookies manuell
   └── Admin aendert Session-TTL ohne Kommunikation

   MASCHINE:
   ├── Vercel Cold Start > Session Check
   └── KV Storage Latenz-Spikes

   MATERIAL:
   ├── JWT Secret Rotation nicht synchron
   └── OAuth Token abgelaufen

   METHODE:
   ├── Kein Retry bei Session-Validierung
   └── Keine Graceful Degradation

   MESSUNG:
   ├── Keine Login-Erfolgsrate-Metrik
   └── Kein Alerting bei Auth-Fehlern

   MILIEU:
   ├── Production vs Preview unterschiedliche KV
   └── Lokale Entwicklung ohne echte Auth
   ```

3. **Wahrscheinlichste Ursachen priorisieren**

4. **Validierung planen** (Hypothesen testen)

**Output-Format**:
```
                    ┌─────────────────────────────────────────────────────┐
                    │                                                     │
    ┌───────────┐   │   ┌───────────┐       ┌───────────┐                │
    │  MENSCH   │───┼───│  MASCHINE │       │  MATERIAL │────────────────┤
    └───────────┘   │   └───────────┘       └───────────┘                │
         │          │        │                   │                       │
    ┌────┴────┐     │   ┌────┴────┐         ┌────┴────┐                  │
    │ Cookies │     │   │ Cold    │         │ JWT     │                  ▼
    │ geloescht│    │   │ Start   │         │ Rotation│          ┌──────────────┐
    └─────────┘     │   └─────────┘         └─────────┘          │    LOGIN     │
                    │                                             │    FEHLER    │
    ┌───────────┐   │   ┌───────────┐       ┌───────────┐        └──────────────┘
    │  METHODE  │───┼───│  MESSUNG  │       │   MILIEU  │────────────────┤
    └───────────┘   │   └───────────┘       └───────────┘                │
         │          │        │                   │                       │
    ┌────┴────┐     │   ┌────┴────┐         ┌────┴────┐                  │
    │ Kein    │     │   │ Keine   │         │ Prod vs │                  │
    │ Retry   │     │   │ Alerting│         │ Preview │                  │
    └─────────┘     │   └─────────┘         └─────────┘                  │
                    │                                                     │
                    └─────────────────────────────────────────────────────┘

## Priorisierte Hypothesen

| # | Kategorie | Ursache | Wahrscheinlichkeit | Validierung |
|---|-----------|---------|-------------------|-------------|
| 1 | Maschine  | Cold Start | Hoch | Logs auf "first request" pruefen |
| 2 | Material  | JWT Rotation | Mittel | Secret-Aenderungshistorie pruefen |
| 3 | Methode   | Kein Retry | Mittel | Retry-Logik implementieren, messen |
```

---

### /plan-do-check-act - PDCA Zyklus

**Trigger**: `/pdca`, `/plan-do-check-act`, `deming cycle`, `verbesserungszyklus`

**Anwendung**: Bei Feature-Implementierung, Refactoring, Process Improvement

**Workflow**:

```
    ┌─────────────────────┐
    │                     │
    │   ┌─────┐ ───────► ┌─────┐
    │   │PLAN │          │ DO  │
    │   └─────┘ ◄─────── └─────┘
    │      ▲                │
    │      │                ▼
    │   ┌─────┐          ┌─────┐
    │   │ ACT │ ◄─────── │CHECK│
    │   └─────┘          └─────┘
    │                     │
    └─────────────────────┘
         (Iterate)
```

**Phase 1: PLAN**
- Ziel definieren (SMART: Specific, Measurable, Achievable, Relevant, Time-bound)
- Hypothese formulieren
- Erfolgskriterien festlegen
- Risiken identifizieren

```markdown
## PLAN

**Ziel**: API Response Time < 10s fuer 95% der Requests (aktuell: 30s)
**Deadline**: 2025-01-15
**Hypothese**: Column Sampling auf 50 Spalten reduziert Tokens um 80%

**Erfolgskriterien**:
- [ ] P95 Latency < 10s
- [ ] Keine Qualitaetsverlust in Analyse-Output
- [ ] SECOM-Dataset funktioniert ohne Timeout

**Risiken**:
- Sampling koennte wichtige Spalten ausschliessen
- Nutzer erwarten alle Spalten in Analyse
```

**Phase 2: DO**
- Implementierung in kleinen Schritten
- Dokumentation waehrend der Umsetzung
- Isolierte Aenderungen (Feature Branch)

```markdown
## DO

**Branch**: feature/column-sampling
**Commits**:
1. `feat: add MAX_COLUMNS constant (50)`
2. `feat: implement column sampling in fileParser`
3. `test: add SECOM sampling test`
4. `docs: update AGENTS.md with sampling details`

**Notizen**:
- Erste 50 Spalten genommen (alphabetisch)
- TODO: Smarter Algorithmus (Varianz-basiert)
```

**Phase 3: CHECK**
- Ergebnisse messen vs. Erfolgskriterien
- Unerwartete Nebenwirkungen dokumentieren
- Lessons Learned sammeln

```markdown
## CHECK

**Messungen**:
| Metrik | Ziel | Ist | Status |
|--------|------|-----|--------|
| P95 Latency | < 10s | 8.2s | OK |
| SECOM Timeout | 0 | 0 | OK |
| Analyse-Qualitaet | Keine Regression | Minor | WARNUNG |

**Beobachtungen**:
- Qualitaet leicht gesunken (fehlende Korrelationen)
- Erste 50 Spalten nicht optimal (viele NaN-Spalten)

**Lessons Learned**:
- Alphabetische Auswahl ist suboptimal
- Varianz-basierte Auswahl wuerde bessere Spalten finden
```

**Phase 4: ACT**
- Entscheiden: Standardisieren oder Iterieren?
- Prozess anpassen basierend auf Learnings
- Naechsten PDCA-Zyklus planen

```markdown
## ACT

**Entscheidung**: ITERIEREN (nicht standardisieren)

**Verbesserungen fuer naechsten Zyklus**:
1. Varianz-basierte Spaltenauswahl implementieren
2. Nutzer-Feedback zu Analyse-Qualitaet einholen
3. A/B-Test: 50 vs 75 Spalten

**Naechster PDCA-Zyklus**:
- Start: 2025-01-16
- Fokus: Smart Column Selection Algorithm
```

---

## Integration mit fabrikIQ

### Wann welchen Befehl nutzen?

| Situation | Befehl | Begruendung |
|-----------|--------|-------------|
| Production Bug | `/why` | Schnelle Root Cause Analyse |
| Komplexer Bug mit vielen Faktoren | `/cause-and-effect` | Strukturierte Ursachensammlung |
| Neues Feature planen | `/plan-do-check-act` | Iterative Implementierung |
| Refactoring | `/plan-do-check-act` | Messbare Verbesserung |
| Wiederkehrender Fehler | `/why` dann `/cause-and-effect` | Kombinierte Analyse |

### Automatische Trigger

Dieser Skill aktiviert sich automatisch bei:
- `git log` mit Muster "fix:" oder "hotfix:"
- Vercel Deployment Failures
- Test-Failures in CI/CD
- Keywords: "bug", "fehler", "timeout", "crash", "regression"

### Quality Gate Integration

Nach jedem PDCA-Zyklus:
```bash
npx tsc --noEmit      # TypeScript Check
npm run build         # Build
npm run test          # Unit Tests
npm run test:e2e      # E2E (optional)
```

---

## Checkliste vor Code-Aenderungen

- [ ] **Continuous Improvement**: Ist die Aenderung inkrementell? (Max 1 Feature pro Commit)
- [ ] **Poka-Yoke**: Sind Fehler durch Typen verhindert? (Keine Runtime-Validierung wo Compile-Time moeglich)
- [ ] **Standardized Work**: Folgt der Code etablierten Patterns? (API Response Format, Error Handling)
- [ ] **Just-In-Time**: Wird nur das implementiert was JETZT gebraucht wird? (Kein "fuer spaeter")

## Dokumentation

Nach jeder Analyse:
1. Ergebnis in `docs/kaizen/` ablegen
2. Commit Message mit Kaizen-Referenz: `fix: resolve timeout (5-Whys #12)`
3. Lessons Learned in CHANGELOG.md

---

## Ressourcen

- [Toyota Production System](https://www.toyota-global.com/company/vision_philosophy/toyota_production_system/)
- [Lean Manufacturing Principles](https://www.lean.org/explore-lean/what-is-lean/)
- [The Toyota Way - Jeffrey Liker](https://www.mheducation.com/highered/product/toyota-way-liker/M9780071392310.html)

---

*Entwickelt fuer fabrikIQ - Manufacturing Intelligence Platform*
*DSGVO-konform | Region fra1 | Dresden AI Insights*
