---
name: tdd-strict
description: Erzwingt striktes Test-Driven Development mit Red-Green-Refactor Zyklus. Blockiert Code-Generierung ohne vorherige Tests. Dokumentiert 13 ungueltige Rationalisierungen. Aktivieren bei neuen Features, Bug Fixes, Refactoring.
---

# Striktes Test-Driven Development

Dieser Skill erzwingt TDD-Praktiken basierend auf dem Kernprinzip:

> **"If you didn't watch the test fail, you don't know if it tests the right thing."**

## Wann aktivieren

- Bei jeder neuen Feature-Implementierung
- Bei Bug Fixes (erst Test der Bug reproduziert, dann Fix)
- Bei Refactoring (Tests muessen vor UND nach Aenderung bestehen)
- Bei API-Erweiterungen
- Bei jeder exportierten Funktion

## Der Red-Green-Refactor Zyklus

### 1. RED: Test schreiben der fehlschlaegt

```typescript
// ZUERST: Test schreiben
describe('calculateOEE', () => {
  it('should return 0 when availability is 0', () => {
    const result = calculateOEE({ availability: 0, performance: 100, quality: 100 });
    expect(result).toBe(0);
  });
});

// Test MUSS fehlschlagen:
// Error: calculateOEE is not defined
// ODER
// Error: Expected 0 but received undefined
```

**Wichtig**: Der Test MUSS aus dem richtigen Grund fehlschlagen:
- Funktion existiert nicht
- Funktion gibt falsches Ergebnis zurueck
- NICHT: Syntaxfehler im Test selbst

### 2. GREEN: Minimaler Code der Test besteht

```typescript
// DANACH: Minimaler Code
export function calculateOEE(params: OEEParams): number {
  if (params.availability === 0) return 0;
  // Weitere Logik kommt spaeter durch weitere Tests
  return 0;
}
```

**Regel**: Schreibe den EINFACHSTEN Code der den Test besteht.
- Keine Optimierungen
- Keine zusaetzlichen Features
- Keine "offensichtlichen" Erweiterungen

### 3. REFACTOR: Bereinigen ohne neues Verhalten

```typescript
// Nach mehreren gruenen Tests: Refactoring erlaubt
export function calculateOEE({ availability, performance, quality }: OEEParams): number {
  return (availability * performance * quality) / 10000;
}
```

**Regeln fuer Refactoring**:
- Alle bestehenden Tests MUESSEN bestehen bleiben
- KEIN neues Verhalten hinzufuegen
- Nur Code-Struktur verbessern
- Nach jedem Refactoring-Schritt: Tests laufen lassen

## Die 13 ungueltigen Rationalisierungen

Diese Ausreden sind NIEMALS akzeptabel:

### 1. "Zu einfach zum Testen"
**Realitaet**: Einfacher Code braucht einfache Tests. 1 Zeile Test ist okay.
```typescript
it('should add two numbers', () => {
  expect(add(2, 3)).toBe(5);
});
```

### 2. "Ich teste spaeter"
**Realitaet**: "Spaeter" bedeutet "nie". TDD bedeutet Test ZUERST.

### 3. "Bereits manuell getestet"
**Realitaet**: Manuelle Tests sind nicht reproduzierbar und skalieren nicht.

### 4. "Zeitdruck erlaubt keine Tests"
**Realitaet**: Tests sparen Zeit bei Debugging und verhindern Regressionen.

### 5. "Private Methoden muss man nicht testen"
**Realitaet**: Teste das Verhalten durch Public APIs. Wenn nicht testbar: Refactor.

### 6. "UI-Code kann man nicht testen"
**Realitaet**: React Testing Library, Playwright, Storybook existieren genau dafuer.

### 7. "Die Logik ist trivial"
**Realitaet**: Triviale Logik aendert sich. Tests dokumentieren erwartetes Verhalten.

### 8. "Wir haben einen QA-Prozess"
**Realitaet**: QA findet Bugs spaeter und teurer. TDD verhindert Bugs von Anfang an.

### 9. "Der Code ist nur temporaer"
**Realitaet**: Temporaerer Code lebt oft Jahre. Tests sichern auch temporaeren Code ab.

### 10. "Tests verlangsamen die Entwicklung"
**Realitaet**: TDD beschleunigt langfristig durch weniger Debugging und Regressionen.

### 11. "Legacy Code hat keine Tests"
**Realitaet**: Charakterisierungstests vor Aenderungen schreiben. Schrittweise verbessern.

### 12. "Das Framework/die Library testet das schon"
**Realitaet**: Teste DEINE Nutzung des Frameworks, nicht das Framework selbst.

### 13. "Mocking ist zu aufwaendig"
**Realitaet**: Wenn Mocking zu komplex ist, ist das Design zu komplex. Refactor.

## Verification Checklist

Vor jedem Commit MUSS gelten:

- [ ] Jede exportierte Funktion hat mindestens einen Test
- [ ] Jeder Test ist VOR der Implementation fehlgeschlagen (RED beobachtet)
- [ ] Jeder Test prueft genau EINE Sache (Single Assertion Principle)
- [ ] Minimaler Code pro Test (kein Over-Engineering)
- [ ] Edge Cases abgedeckt:
  - [ ] Null/Undefined Inputs
  - [ ] Leere Arrays/Strings
  - [ ] Grenzwerte (0, MAX_INT, negative Zahlen)
  - [ ] Fehlerhafte Inputs (TypeError erwartet)
- [ ] Test-Namen beschreiben Verhalten: `should [erwartetes Ergebnis] when [Bedingung]`
- [ ] Keine `skip` oder `only` Tests im Commit
- [ ] Coverage mindestens 80% fuer neuen Code

## TDD-Workflow in der Praxis

### Schritt 1: Test-Datei erstellen

```bash
# Fuer neue Funktion in src/utils/oee.ts
touch src/utils/oee.test.ts
```

### Schritt 2: Minimaler fehlschlagender Test

```typescript
// src/utils/oee.test.ts
import { describe, it, expect } from 'vitest';
import { calculateOEE } from './oee';

describe('calculateOEE', () => {
  it('should return 85 for sample manufacturing data', () => {
    const result = calculateOEE({
      availability: 90,
      performance: 95,
      quality: 99
    });
    expect(result).toBeCloseTo(84.645, 2);
  });
});
```

### Schritt 3: Test laufen lassen (MUSS fehlschlagen)

```bash
npm run test -- --run src/utils/oee.test.ts

# Erwartete Ausgabe:
# Error: Cannot find module './oee'
# ODER nach Stub:
# Error: Expected 84.645 but received undefined
```

### Schritt 4: Minimale Implementation

```typescript
// src/utils/oee.ts
export interface OEEParams {
  availability: number;
  performance: number;
  quality: number;
}

export function calculateOEE(params: OEEParams): number {
  return (params.availability * params.performance * params.quality) / 10000;
}
```

### Schritt 5: Test laufen lassen (MUSS bestehen)

```bash
npm run test -- --run src/utils/oee.test.ts

# Erwartete Ausgabe:
# PASS src/utils/oee.test.ts
```

### Schritt 6: Naechster Test fuer Edge Case

```typescript
it('should throw when values exceed 100', () => {
  expect(() => calculateOEE({
    availability: 101,
    performance: 100,
    quality: 100
  })).toThrow('Values must be between 0 and 100');
});
```

Zurueck zu Schritt 3 (RED) -> Schritt 4 (GREEN) -> Repeat.

## Anti-Patterns erkennen

### VERBOTEN: Test nach Code

```typescript
// FALSCH: Code zuerst geschrieben
function add(a: number, b: number): number {
  return a + b;
}

// Dann erst Test geschrieben - UNGUELTIG!
// Du weisst nicht ob der Test das richtige testet
```

### VERBOTEN: Zu viel Code auf einmal

```typescript
// FALSCH: Komplette Klasse ohne Tests implementiert
class UserService {
  async create(user: User) { ... }
  async update(id: string, data: Partial<User>) { ... }
  async delete(id: string) { ... }
  async findById(id: string) { ... }
  async findAll(filters: FilterOptions) { ... }
}

// RICHTIG: Eine Methode nach der anderen mit TDD
```

### VERBOTEN: Tests anpassen damit sie bestehen

```typescript
// FALSCH: Test geaendert weil Implementation anders ist
// Vorher: expect(result).toBe(100);
// Nachher: expect(result).toBe(99.5); // "Weil die Formel das so ausgibt"

// RICHTIG: Implementation korrigieren ODER Anforderungen klaeren
```

## Framework-spezifische Patterns

### React Components (Vitest + Testing Library)

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('LoginButton', () => {
  it('should show loading spinner when clicked', async () => {
    render(<LoginButton onLogin={vi.fn()} />);

    await userEvent.click(screen.getByRole('button', { name: /login/i }));

    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });
});
```

### API Endpoints (Supertest)

```typescript
import request from 'supertest';
import { app } from '../app';

describe('POST /api/analyze', () => {
  it('should return 401 without authentication', async () => {
    const response = await request(app)
      .post('/api/analyze')
      .send({ data: 'test' });

    expect(response.status).toBe(401);
    expect(response.body.error).toBe('Unauthorized');
  });
});
```

### Async Code

```typescript
describe('fetchUserData', () => {
  it('should retry 3 times on network failure', async () => {
    const mockFetch = vi.fn()
      .mockRejectedValueOnce(new Error('Network'))
      .mockRejectedValueOnce(new Error('Network'))
      .mockResolvedValueOnce({ id: 1, name: 'Test' });

    const result = await fetchUserData(1, { fetch: mockFetch });

    expect(mockFetch).toHaveBeenCalledTimes(3);
    expect(result.name).toBe('Test');
  });
});
```

## Bei Verstoß gegen TDD

1. **STOPP**: Keine weitere Code-Generierung ohne Test
2. **WARNUNG**: "TDD-Verstoß erkannt: [Beschreibung]"
3. **ANLEITUNG**: Zeige den korrekten TDD-Workflow
4. **FRAGE**: "Soll ich zuerst den Test schreiben?"

## Metriken zur Erfolgsmessung

- **Test-to-Code Ratio**: Mindestens 1:1 (Test-LOC zu Code-LOC)
- **Coverage**: Minimum 80% fuer neuen Code
- **Red-Green Time**: Kurze Zyklen (5-10 Minuten pro Feature)
- **Test Execution Time**: Unit Tests unter 10 Sekunden

## Kommandos

```bash
# Einzelnen Test laufen lassen (RED pruefen)
npm run test -- --run path/to/file.test.ts

# Alle Tests (vor Commit)
npm run test

# Coverage Report
npm run test:coverage

# Watch Mode (waehrend Entwicklung)
npm run test -- --watch
```

## Integration mit anderen Skills

- **code-quality-gate**: TDD Tests sind Teil von Gate 1 (Pre-Commit)
- **strict-typescript-mode**: Tests muessen auch Type-safe sein
- **supervisor**: Pruefer-Agent verifiziert TDD-Einhaltung

## Quellen und Weiterfuehrende Literatur

- Kent Beck: "Test-Driven Development: By Example"
- Robert C. Martin: "Clean Code" (Kapitel 9: Unit Tests)
- Martin Fowler: "Refactoring" (Test-Sicherheit bei Refactoring)
