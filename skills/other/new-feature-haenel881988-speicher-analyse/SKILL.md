---
name: new-feature
description: Scaffolding für ein neues Feature in der Tauri v2 App. Erstellt Rust-Command in commands/, typisierte API-Funktion in tauri-api.ts und React-View in src/views/. Nutze diesen Skill wenn ein komplett neues Feature von Grund auf implementiert werden soll (Backend + Frontend). Aufruf mit /new-feature [feature-name] [beschreibung].
---

# Neues Feature scaffolden

Du erstellst das Grundgerüst für ein neues Feature in der Speicher Analyse Tauri-App.

## Argumente

- `$ARGUMENTS[0]` = Feature-Name (kebab-case, z.B. `disk-health`)
- `$ARGUMENTS[1]` = Kurzbeschreibung des Features (optional)

## Voranalyse

1. Lies die bestehende Architektur:
   - `src-tauri/src/commands/` - Wie Commands definiert werden (8 Module)
   - `src-tauri/src/lib.rs` - Wie Commands registriert werden
   - `src/api/tauri-api.ts` - Wie API-Funktionen typisiert werden
   - `src/App.tsx` - App Shell
   - `src/components/TabRouter.tsx` - Wie Views lazy-loaded werden
   - `src/components/Sidebar.tsx` - Wie Sidebar-Tabs definiert sind
2. Prüfe ob ein ähnliches Feature bereits existiert

## Dateien erstellen/ändern

### 1. Rust-Command: `src-tauri/src/commands/cmd_*.rs`

```rust
#[tauri::command]
pub async fn feature_action(param: String) -> Result<serde_json::Value, String> {
    let safe_param = param.replace("'", "''");
    let script = format!(r#"
        $result = Get-Something '{}'
        $result | ConvertTo-Json -Depth 3
    "#, safe_param);
    crate::ps::run_ps_json(&script).await
}
```

### 2. Registrierung: `src-tauri/src/lib.rs` + `commands/mod.rs`

### 3. API-Bridge: `src/api/tauri-api.ts`

```typescript
export const featureAction = (param: string) =>
  invoke<ReturnType>('feature_action', { param });
```

### 4. React-View: `src/views/FeatureNameView.tsx`

```tsx
import { useState, useCallback, useEffect } from 'react';
import * as api from '../api/tauri-api';
import { useAppContext } from '../context/AppContext';

export default function FeatureNameView() {
  const { showToast } = useAppContext();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [loaded, setLoaded] = useState(false);

  const loadData = useCallback(async () => {
    if (loading) return;
    setLoading(true);
    try {
      const result = await api.featureAction();
      setData(result);
      setLoaded(true);
    } catch (err: any) {
      showToast('Fehler: ' + err.message, 'error');
    } finally {
      setLoading(false);
    }
  }, [loading, showToast]);

  useEffect(() => {
    if (!loaded) loadData();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className="feature-page">
      <div className="feature-header"><h2>Feature-Titel</h2></div>
      {loading && <div className="loading-state">Lade Daten...</div>}
      {!loading && loaded && data && (
        <div className="feature-content">{/* Inhalt */}</div>
      )}
      {!loading && !loaded && (
        <div className="tool-placeholder">Noch keine Daten geladen.</div>
      )}
    </div>
  );
}
```

**React-Konventionen:**
- Funktionale Komponente mit `export default`
- State via `useState`, Side-Effects via `useEffect` mit Cleanup-Return
- API über `import * as api from '../api/tauri-api'`
- Context über `useAppContext()` (showToast, scanId, drives)
- JSX escaped automatisch — KEIN `dangerouslySetInnerHTML`
- Alle UI-Texte auf Deutsch mit korrekten Umlauten

### 5. TabRouter: `src/components/TabRouter.tsx`

```tsx
const FeatureNameView = lazy(() => import('../views/FeatureNameView'));
```

### 6. Sidebar: `src/components/Sidebar.tsx`

Button in die passende Gruppe einfügen.

## Mensch-Checkliste (PFLICHT — Lesson #95)

**Ein Feature ist NICHT fertig wenn es technisch funktioniert. Es ist fertig wenn ein Mensch es intuitiv bedienen kann.**

Vor dem Commit MUSS jeder Punkt geprüft und umgesetzt werden:

### Tastaturkürzel
- [ ] Strg+Z/Y (Undo/Redo) wo Aktionen rückgängig gemacht werden können?
- [ ] Strg+S (Speichern) wo Daten gespeichert werden?
- [ ] Strg+P (Drucken) wo Inhalte gedruckt werden können?
- [ ] Escape (Abbrechen/Zurücksetzen) für modale Dialoge und Werkzeuge?
- [ ] Entf/Delete für Löschen von ausgewählten Elementen?
- [ ] Navigation-Shortcuts (Bild↑/↓, Pos1/Ende) bei langen Listen/Seiten?
- [ ] Welche Shortcuts kennt der User von ähnlichen Windows-Programmen?

### Undo/Redo
- [ ] Kann der User seine letzten Aktionen rückgängig machen?
- [ ] Gibt es sichtbare Undo/Redo-Buttons im Toolbar?

### Auswahl und Interaktion
- [ ] Kann der User Elemente auswählen (Klick)?
- [ ] Kann der User ausgewählte Elemente bearbeiten/löschen?
- [ ] Gibt es visuelles Feedback welches Element ausgewählt ist?
- [ ] Kann der User Text markieren und kopieren wo es Sinn macht?

### Navigation
- [ ] Gibt es eine Positionsanzeige (z.B. "Seite X von Y", "Element X von Y")?
- [ ] Kann der User zu einer bestimmten Position springen?
- [ ] Scrollt die Ansicht bei Keyboard-Navigation mit?

### Visuelles Feedback
- [ ] Ungespeicherte Änderungen sichtbar (z.B. * im Titel)?
- [ ] Lade-Zustände bei async Operationen?
- [ ] Erfolgs-/Fehler-Toast bei Aktionen?
- [ ] Aktives/ausgewähltes Element hervorgehoben?

### Denkfrage (VOR dem Coding)
> "Wenn ich dieses Feature als normaler Windows-User zum ersten Mal öffne — was erwarte ich? Was würde mich frustrieren wenn es fehlt?"

## Security-Checkliste (PFLICHT vor Commit)

- [ ] Alle PowerShell-Parameter escaped?
- [ ] Pfade vom Frontend validiert?
- [ ] Kein `dangerouslySetInnerHTML`?
- [ ] `useEffect` Cleanup für Timer/Listener/Observer?

## Verwandte Skills

- `/add-tauri-command` - Nur Command ohne View
- `/add-sidebar-tab` - Nur Sidebar-Tab ohne Backend
- `/powershell-cmd` - PowerShell-Befehle
- `/changelog` - Nach Fertigstellung
