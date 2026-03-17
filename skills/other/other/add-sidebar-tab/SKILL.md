---
name: add-sidebar-tab
description: Fügt einen neuen Sidebar-Tab mit React-View hinzu. Erstellt View-Komponente in src/views/, TabRouter-Eintrag und Sidebar-Button. Backend-Commands werden über /add-tauri-command hinzugefügt. Aufruf mit /add-sidebar-tab [tab-name] [sidebar-gruppe] [beschreibung].
---

# Neuen Sidebar-Tab hinzufügen

Du fügst einen neuen Tab in die Sidebar der Speicher Analyse Tauri-App ein, inklusive React-View und App-Integration.

## Argumente

- `$ARGUMENTS[0]` = Tab-Name (kebab-case, z.B. `disk-health`)
- `$ARGUMENTS[1]` = Sidebar-Gruppe: `start`, `analyse`, `bereinigung`, `system`, `sicherheit`, `extras`
- `$ARGUMENTS[2]` = Kurzbeschreibung (optional)

## Voranalyse

**Pflicht — lies diese Dateien zuerst:**

1. `src/components/Sidebar.tsx` - Bestehende Sidebar-Struktur und Gruppen
2. `src/components/TabRouter.tsx` - Wie Views lazy-loaded werden
3. `src/style.css` - Bestehende View-Styles als Referenz
4. Eine bestehende View als Referenz (z.B. `src/views/PrivacyView.tsx`)

## 3 Dateien ändern/erstellen

### 1. `src/views/<TabName>View.tsx` — React-View

```tsx
import { useState, useCallback, useEffect } from 'react';
import * as api from '../api/tauri-api';
import { useAppContext } from '../context/AppContext';

export default function TabNameView() {
  const { showToast } = useAppContext();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [loaded, setLoaded] = useState(false);

  const loadData = useCallback(async () => {
    if (loading) return;
    setLoading(true);
    try {
      const result = await api.tabNameAction();
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
    <div className="tab-name-page">
      <div className="tab-name-header"><h2>Anzeigename</h2></div>
      {loading && <div className="loading-state">Lade Daten...</div>}
      {!loading && loaded && data && (
        <div className="tab-name-content">{/* Inhalt */}</div>
      )}
      {!loading && !loaded && (
        <div className="tool-placeholder">Noch keine Daten geladen.</div>
      )}
    </div>
  );
}
```

**Konventionen:**
- `export default` Funktionale Komponente
- `useEffect` mit Cleanup-Return für Timer/Listener/Observer
- API über `import * as api from '../api/tauri-api'`
- JSX escaped automatisch — KEIN `dangerouslySetInnerHTML`
- Alle UI-Texte auf Deutsch mit korrekten Umlauten

### 2. `src/components/TabRouter.tsx` — Lazy-Import + Route

```tsx
const TabNameView = lazy(() => import('../views/TabNameView'));

// Im switch/map:
case 'tab-name':
  return <Suspense fallback={<div className="loading-state">Laden...</div>}><TabNameView /></Suspense>;
```

### 3. `src/components/Sidebar.tsx` — Button hinzufügen

Button in die passende Gruppe einfügen.

## Sidebar-Gruppen Referenz

| Gruppe | Inhalt |
|--------|--------|
| `start` | Dashboard, Explorer |
| `analyse` | Dateitypen, Verzeichnisbaum, Treemap, Top 100, Duplikate, Alte Dateien |
| `bereinigung` | Bereinigung, Autostart, Dienste |
| `system` | Optimierung, Updates, S.M.A.R.T., System-Profil, PC-Diagnose |
| `sicherheit` | Privacy, Netzwerk, Software-Audit, Sicherheits-Check |
| `extras` | PDF-Editor, Terminal, Einstellungen |

## Security-Checkliste (PFLICHT vor Commit)

- [ ] Kein `dangerouslySetInnerHTML`?
- [ ] `useEffect` Cleanup für Timer/Listener/Observer?
- [ ] Loading/Error States korrekt gehandelt?

## Ausgabe

- Welche Dateien erstellt/geändert wurden
- Sidebar-Gruppe und Position
- Ob Backend-Commands noch benötigt werden (→ `/add-tauri-command`)
