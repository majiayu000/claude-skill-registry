---
name: add-tauri-command
description: Fügt einen neuen Tauri-Command hinzu mit Einträgen in commands/, lib.rs und tauri-api.ts. Stellt konsistente Benennung, Parameter-Escaping und Fehlerbehandlung sicher. Nutze diesen Skill wenn eine neue Backend-Funktion vom Frontend aus aufgerufen werden soll. Aufruf mit /add-tauri-command [command-name] [beschreibung].
---

# Tauri-Command hinzufügen

Du fügst einen neuen Tauri-Command zur Speicher Analyse App hinzu.

## Argumente

- `$ARGUMENTS[0]` = Command-Name in snake_case (z.B. `get_disk_health`)
- `$ARGUMENTS[1]` = Beschreibung (optional)

## Voranalyse

1. Lies `src-tauri/src/commands/` — das passende Modul (cmd_scan, cmd_files, cmd_network, cmd_privacy, cmd_system, cmd_terminal, cmd_misc) identifizieren
2. Lies `src-tauri/src/commands/mod.rs` um die Re-Export-Struktur zu verstehen
3. Lies `src-tauri/src/lib.rs` um die Command-Registrierung im `generate_handler![]` zu sehen
4. Lies `src/api/tauri-api.ts` um die typisierte API-Bridge zu verstehen
5. Prüfe ob ein ähnlicher Command bereits existiert

## 3 Dateien ändern

### 1. `src-tauri/src/commands/cmd_*.rs` — Command-Funktion

Im passenden Modul hinzufügen:

```rust
#[tauri::command]
pub async fn command_name(param: String) -> Result<serde_json::Value, String> {
    // SECURITY: Parameter für PowerShell escapen
    let safe_param = param.replace("'", "''");

    let script = format!("Get-Something '{}'", safe_param);
    let output = crate::ps::run_ps(&script).await?;

    let json: serde_json::Value = serde_json::from_str(&output)
        .map_err(|e| format!("JSON-Parse-Fehler: {}", e))?;
    Ok(json)
}
```

**Security-Regeln (PFLICHT bei JEDEM Command):**
- **PowerShell-Escaping:** Alle String-Parameter die in `format!()` für PowerShell verwendet werden MÜSSEN mit `.replace("'", "''")` escaped werden
- **Pfad-Validierung:** Pfade vom Frontend validieren (existiert? innerhalb erlaubter Verzeichnisse?)
- **Enum-Whitelist:** Parameter mit festen Werten per `match` auf erlaubte Werte prüfen
- **IP-Validierung:** IP-Adressen mit Regex validieren

**Konventionen:**
- `snake_case` für Funktionsnamen
- `#[tauri::command]` Attribut
- `Result<serde_json::Value, String>` Rückgabetyp
- Async für I/O-Operationen
- PowerShell über `crate::ps::run_ps()` oder `crate::ps::run_ps_json()`

### 2. `src-tauri/src/lib.rs` — Command registrieren

```rust
.invoke_handler(tauri::generate_handler![
    // ... bestehende Commands ...
    commands::command_name,  // NEU
])
```

### 3. `src/api/tauri-api.ts` — Typisierte Export-Funktion

```typescript
export const commandName = (param: string) =>
  invoke<ReturnType>('command_name', { param });
```

**Benennungs-Konvention:**
- Rust-Command: `snake_case` (z.B. `get_disk_health`)
- TypeScript-Funktion: `camelCase` (z.B. `getDiskHealth`)
- Frontend-Import: `import { getDiskHealth } from '../api/tauri-api'`

## Frontend-Aufruf (optional)

```typescript
// In src/views/SomeView.tsx
import { commandName } from '../api/tauri-api';
import { useAppContext } from '../context/AppContext';

const { showToast } = useAppContext();
try {
    const result = await commandName(arg);
} catch (err: any) {
    showToast('Fehler: ' + err.message, 'error');
}
```

## Security-Checkliste (PFLICHT vor Commit)

- [ ] Alle String-Parameter für PowerShell mit `.replace("'", "''")` escaped?
- [ ] Pfade vom Frontend validiert?
- [ ] Enum-Parameter per Whitelist/match geprüft?
- [ ] IP-Adressen per Regex validiert?
- [ ] Keine `format!()` mit unescaptem User-Input?

## Häufige Fehler vermeiden

- Command in `cmd_*.rs` definiert aber NICHT in `mod.rs` re-exportiert → Compile-Fehler
- Command NICHT in `lib.rs` registriert → "unknown command"
- `camelCase` in Rust → muss `snake_case` sein
- TypeScript-Funktion mit falschem invoke-Namen → stille Fehler
- Parameter in `format!()` ohne Escaping → Command Injection

## Ausgabe

- Rust-Command: `commands::command_name` (in welchem cmd_*.rs Modul)
- TypeScript-Funktion: `commandName()` in `src/api/tauri-api.ts`
- Parameter: Typen und Escaping-Status
- Registrierung: In `lib.rs` + `mod.rs` eingetragen
