---
name: security-scan
description: Schneller Security-Scan der Speicher Analyse Tauri-App (React + TypeScript Frontend). Prüft Command Injection, XSS, Path Traversal und Tauri-Sicherheitskonfiguration. Aufruf mit /security-scan [datei-oder-modul oder "all"].
---

# Security-Scan

Du führst einen fokussierten Security-Scan der Speicher Analyse Tauri-App durch.

## Argument

`$ARGUMENTS` = Dateipfad, Modulname ODER `all` für vollständigen Scan

## Prüfkategorien

### 1. Command Injection (KRITISCH)

**Rust-Backend (`src-tauri/src/commands/cmd_*.rs`):**

```
SICHER:    let safe = param.replace("'", "''"); let script = format!("... '{}'", safe);
UNSICHER:  let script = format!("... '{}'", param);  // param kommt vom Frontend!
```

**Prüfschritte:**
1. Grep nach `format!(` in allen `cmd_*.rs` Dateien
2. Für jedes Match: Parameter VOR format!() mit `.replace("'", "''")` escaped?
3. Ausnahme: Hardcoded Strings ohne User-Parameter sind OK

### 2. XSS (KRITISCH)

**React-Frontend (`src/views/*.tsx`, `src/components/*.tsx`):**

In React ist XSS deutlich seltener, weil JSX automatisch escaped. Prüfe:

```
UNSICHER:  dangerouslySetInnerHTML={{ __html: userInput }}
SICHER:    {variable} in JSX (automatisch escaped)
SICHER:    dangerouslySetInnerHTML={{ __html: sanitizedStaticHtml }}
```

**Prüfschritte:**
1. Grep nach `dangerouslySetInnerHTML` in allen TSX-Dateien
2. Für jedes Match: Wird der Inhalt sanitisiert oder ist er vertrauenswürdig?
3. Grep nach direkter DOM-Manipulation (`document.getElementById`, `innerHTML`)

### 3. Path Traversal (HOCH)

**Rust-Backend:**
1. Grep nach `tokio::fs::`, `std::fs::`, `Path::new(` in cmd_*.rs
2. Kommt der Pfad aus einem Frontend-Parameter?
3. Wird der Pfad validiert?

### 4. Tauri-Konfiguration (HOCH)

**`src-tauri/tauri.conf.json`:**
1. `security.csp` ist NICHT `null` oder leer
2. `withGlobalTauri` ist `true` (React-App braucht `window.__TAURI__`)
3. Capabilities minimal konfiguriert

**`src-tauri/src/lib.rs`:**
4. `tauri-plugin-single-instance` registriert
5. Alle Commands in `generate_handler![]` auch in commands/ definiert

### 5. Parameter-Validierung (MITTEL)

- IP-Adressen: Per Regex validiert?
- Enum-Werte: Per `match` auf Whitelist?
- Pfade: Auf Existenz geprüft?
- Strings: Für PowerShell escaped?

## Scan-Ablauf

### Ganzes Modul (`/security-scan privacy`)

1. Lies `src-tauri/src/commands/cmd_privacy.rs`
2. Lies `src/views/PrivacyView.tsx`
3. Prüfe Kategorien 1-3, 5

### Vollständiger Scan (`/security-scan all`)

1. **Rust-Backend:** Lies alle `src-tauri/src/commands/cmd_*.rs`
2. **Konfiguration:** Lies `src-tauri/tauri.conf.json`
3. **App-Setup:** Lies `src-tauri/src/lib.rs`
4. **React-Frontend:** Grep alle `src/views/*.tsx` und `src/components/*.tsx` nach `dangerouslySetInnerHTML`, `document.getElementById`, direkte DOM-Manipulation
5. **API-Bridge:** Lies `src/api/tauri-api.ts` (keine unvalidierten Durchreichungen?)
6. **Prüfe ALLE 5 Kategorien**

## Ausgabeformat

```markdown
## Security-Scan: [Datei/Modul/Gesamt]

### Zusammenfassung
- Geprüfte Dateien: X
- Kritische Funde: X
- Hohe Funde: X
- Mittlere Funde: X

### Kritisch (sofort beheben)
| # | Typ | Datei:Zeile | Code-Ausschnitt | Empfehlung |

### Hoch (vor nächstem Release beheben)
| # | Typ | Datei:Zeile | Problem | Empfehlung |

### Sicher
- Was korrekt umgesetzt ist
```

## Typ-Kürzel

| Kürzel | Bedeutung |
|--------|-----------|
| CMD-INJ | Command Injection (PowerShell) |
| XSS | Cross-Site Scripting (dangerouslySetInnerHTML) |
| PATH-TRAV | Path Traversal |
| CFG | Konfigurationsproblem |
| VALID | Fehlende Validierung |
