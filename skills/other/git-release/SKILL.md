---
name: git-release
description: Erstellt ein vollständiges Release mit Versionsbump in Cargo.toml + tauri.conf.json, Änderungsprotokoll-Update, Git-Tag und Push. Nutze diesen Skill wenn eine neue Version veröffentlicht werden soll. Aufruf mit /git-release [version oder major|minor|patch] [release-beschreibung].
---

# Release erstellen

Du erstellst ein vollständiges Release für die Speicher Analyse Tauri-App.

## Argumente

- `$ARGUMENTS[0]` = Neue Version (z.B. `2.1.0`) ODER Bump-Typ: `major`, `minor`, `patch`
- `$ARGUMENTS[1]` = Release-Beschreibung (optional, wird aus Änderungsprotokoll abgeleitet falls leer)

## Ablauf

### 1. Aktuelle Version ermitteln

Lies `src-tauri/Cargo.toml` → `[package] version = "..."`.

**Versionierung (SemVer):**
- `major` = Breaking Changes (z.B. 2.0.0 → 3.0.0)
- `minor` = Neue Features (z.B. 2.0.0 → 2.1.0)
- `patch` = Bug-Fixes (z.B. 2.0.1 → 2.0.2)

Falls ein Bump-Typ statt expliziter Version angegeben wurde, berechne die nächste Version.

### 2. Prüfungen

1. **Git-Status sauber?** `git status` — keine uncommitteten Änderungen
2. **Auf main Branch?** `git branch --show-current` — muss `main` sein
3. **Remote aktuell?** `git fetch && git status` — kein Behind/Ahead

Falls Prüfungen fehlschlagen → dem User mitteilen und abbrechen.

### 3. Version bumpen

Version an **allen 3 Stellen** gleichzeitig aktualisieren:

1. **`src-tauri/Cargo.toml`** → `[package] version = "<neue-version>"`
2. **`src-tauri/tauri.conf.json`** → `"version": "<neue-version>"`
3. **`src/components/Toolbar.tsx`** → `.toolbar-version` Text (falls vorhanden)

**WICHTIG:** Alle 3 Stellen MÜSSEN identische Version haben.

### 4. Änderungsprotokoll prüfen

Lies `docs/protokoll/aenderungsprotokoll.md`:
- Sammle alle Einträge seit der letzten Version
- Diese bilden die Release-Notes

Falls keine Einträge vorhanden → User warnen.

### 5. Git Commit + Tag + Push

```bash
git add .
git commit -m "release: v<neue-version> - <Release-Beschreibung>"
git tag -a v<neue-version> -m "<Release-Beschreibung>"
git push && git push --tags
```

**Tag-Format:** `v<version>` (z.B. `v2.1.0`)

### 6. Zusammenfassung

```markdown
## Release v<version>

### Version
- Vorherige: v<alte-version>
- Neue: v<neue-version>
- Typ: <major|minor|patch>

### Änderungen seit letztem Release
- <Eintrag 1 aus Änderungsprotokoll>
- <Eintrag 2>
- ...

### Git
- Commit: <hash>
- Tag: v<neue-version>
- Push: Erfolgreich
```

## Wichtige Hinweise

- **Niemals** `--force` verwenden
- **Immer** prüfen dass der Working Tree sauber ist
- **Tag-Nachricht** sollte die wichtigsten Änderungen zusammenfassen
- **Version:** IMMER aus `src-tauri/Cargo.toml` lesen (Hauptquelle), nicht `package.json`
- **3 Stellen:** Cargo.toml + tauri.conf.json + Toolbar.tsx — alle gleichzeitig aktualisieren
- Falls der User keine Version angibt, schlage basierend auf den Änderungen einen Bump-Typ vor
