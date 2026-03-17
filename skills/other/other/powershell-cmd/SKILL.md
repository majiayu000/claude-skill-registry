---
name: powershell-cmd
description: Fügt einen neuen PowerShell-Befehl korrekt in die Speicher Analyse Tauri-App ein. Verwendet crate::ps::run_ps() mit korrektem Escaping, UTF-8-Encoding und Fehlerbehandlung. Nutze diesen Skill wenn ein neuer Windows-Systembefehl via PowerShell integriert werden soll. Aufruf mit /powershell-cmd [befehl-name] [beschreibung].
---

# PowerShell-Befehl einbinden (Tauri/Rust)

Du bindest einen neuen PowerShell-Befehl in die Speicher Analyse Tauri-App ein, unter Beachtung aller kritischen Lektionen.

## Argumente

- `$ARGUMENTS[0]` = Command-Name (snake_case, z.B. `get_battery_status`)
- `$ARGUMENTS[1]` = Beschreibung (optional)

## Voranalyse

**Pflicht — lies diese Dateien zuerst:**

1. `src-tauri/src/ps.rs` - Die `run_ps()` und `run_ps_json()` Funktionen verstehen
2. `src-tauri/src/commands/` - Bestehende Commands als Referenz (8 Module: cmd_scan, cmd_files, cmd_network, cmd_privacy, cmd_system, cmd_terminal, cmd_misc)
3. `src-tauri/src/lib.rs` - Command-Registrierung

## KRITISCHE REGELN (aus Lessons Learned)

### 1. IMMER `crate::ps::run_ps()` verwenden

```rust
// RICHTIG:
let output = crate::ps::run_ps(&script).await?;

// Für JSON-Ausgabe:
let json = crate::ps::run_ps_json(&script).await?;

// FALSCH — NIEMALS so (kein UTF-8, kein korrektes Error-Handling):
use std::process::Command;
let output = Command::new("powershell.exe").arg("-Command").arg(script).output()?;
```

### 2. IMMER Parameter escapen (SECURITY-PFLICHT)

```rust
// RICHTIG: Vor format!() escapen
let safe_name = name.replace("'", "''");
let script = format!("Get-Service '{}'", safe_name);

// FALSCH — Command Injection!
let script = format!("Get-Service '{}'", name);  // name könnte "'; Remove-Item -Recurse C:\\" enthalten
```

**Escaping-Regeln:**
- String-Parameter: `.replace("'", "''")`
- IP-Adressen: Regex-Validierung VOR Verwendung
- Dateipfade: Existenz prüfen + innerhalb erlaubter Verzeichnisse
- Enum-Werte: Per `match` auf Whitelist prüfen

### 3. Timeout einbauen

```rust
use tokio::time::{timeout, Duration};

// RICHTIG: Timeout um hängende PS-Prozesse abzufangen
let result = timeout(
    Duration::from_secs(30),
    crate::ps::run_ps(&script)
).await
.map_err(|_| "PowerShell-Timeout nach 30 Sekunden".to_string())?;
```

**Timeout-Richtwerte:**
- Standard-Befehle: 30 Sekunden (PowerShell Cold Start = 5-10s)
- Schwere Befehle (Windows Update, DISM): 120 Sekunden
- Netzwerk-Scans: 60 Sekunden

### 4. KEINE parallelen PowerShell-Prozesse

```rust
// RICHTIG: Sequenziell
let result1 = crate::ps::run_ps(&script1).await?;
let result2 = crate::ps::run_ps(&script2).await?;

// FALSCH: Parallel (können sich gegenseitig aushungern!)
let (r1, r2) = tokio::join!(
    crate::ps::run_ps(&script1),
    crate::ps::run_ps(&script2)
);
```

### 5. Multi-Line Scripts korrekt übergeben

```rust
// RICHTIG: Raw-String mit Newlines
let script = r#"
    $items = Get-ItemProperty HKLM:\SOFTWARE\...
    $items | ForEach-Object {
        [PSCustomObject]@{
            Name = $_.DisplayName
            Version = $_.DisplayVersion
        }
    } | ConvertTo-Json -Depth 3
"#;

// FALSCH: Newlines durch Spaces ersetzen (zerstört Statement-Grenzen!)
let script = multi_line.replace('\n', " ");
```

### 6. JSON-Output für strukturierte Daten

```rust
let script = r#"
    $data = Get-Process | Select-Object Name, Id, WorkingSet64
    $data | ConvertTo-Json -Depth 3
"#;

// run_ps_json() parst direkt zu serde_json::Value
let json = crate::ps::run_ps_json(script).await?;
```

## Template für neuen Command

```rust
// In src-tauri/src/commands/cmd_*.rs (passendes Modul wählen)

#[tauri::command]
pub async fn befehl_name(param: String) -> Result<serde_json::Value, String> {
    // SECURITY: Parameter escapen
    let safe_param = param.replace("'", "''");

    let script = format!(r#"
        $result = Get-Something '{}'
        $result | ConvertTo-Json -Depth 3
    "#, safe_param);

    // Timeout einbauen
    use tokio::time::{timeout, Duration};
    let output = timeout(
        Duration::from_secs(30),
        crate::ps::run_ps(&script)
    ).await
    .map_err(|_| "Timeout nach 30 Sekunden".to_string())??;

    // JSON parsen
    let json: serde_json::Value = serde_json::from_str(&output)
        .map_err(|e| format!("JSON-Fehler: {}", e))?;

    // Array sicherstellen (einzelnes Objekt → Array wrappen)
    if json.is_object() {
        Ok(serde_json::json!([json]))
    } else {
        Ok(json)
    }
}
```

**Danach:**
1. In `src-tauri/src/lib.rs` → `generate_handler![]` eintragen
2. In `src/api/tauri-api.ts` → typisierte Export-Funktion hinzufügen

## Häufige Fallstricke

| Problem | Ursache | Lösung |
|---------|---------|--------|
| Timeout nach 5s | PowerShell Cold Start | `run_ps()` + 30s Timeout |
| Kryptische Zeichen | Kein UTF-8 | `run_ps()` hat UTF-8 Prefix eingebaut |
| Leere Ausgabe | Single Object statt Array | `ConvertTo-Json` + Array-Check |
| Parse-Fehler | PS Warnings in stdout | `-ErrorAction SilentlyContinue` |
| Hängt endlos | Kein Timeout | `tokio::time::timeout()` wrappen |
| Script bricht ab | Newlines ersetzt | Raw-Strings oder `.trim()`, nie `.replace('\n', " ")` |
| Command Injection | Kein Escaping | `.replace("'", "''")` VOR format!() |

## Security-Checkliste (PFLICHT)

- [ ] Parameter mit `.replace("'", "''")` escaped?
- [ ] Pfade validiert (Existenz + erlaubte Verzeichnisse)?
- [ ] Enum-Werte per match/Whitelist geprüft?
- [ ] IP-Adressen per Regex validiert?
- [ ] Timeout mit `tokio::time::timeout()` eingebaut?
- [ ] Keine parallelen PS-Aufrufe?

## Ausgabe

Nach dem Einbinden, gib eine Zusammenfassung:
- Command: Name und Signatur
- PowerShell-Befehl: Was ausgeführt wird
- Escaping: Welche Parameter wie escaped werden
- Timeout: Standard (30s) oder angepasst
- Registrierung: In lib.rs + tauri-api.ts eingetragen
