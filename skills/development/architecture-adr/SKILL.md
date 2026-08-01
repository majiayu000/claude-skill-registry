---
name: architecture-adr
description: 'name: architecture-adr'
---

﻿---
name: architecture-adr
description: Dokumentiere Architekturentscheidungen (ADRs) und Architektur-Updates; verwenden bei neuen Design-Entscheidungen oder Aenderungen am Architektur- oder Technologie-Stack.
---

# Skill: architecture-adr

## Zweck
Halte Architekturentscheidungen nachvollziehbar fest und verknuepfe sie mit dem Projektkontext.

## Wann anwenden
- Wenn eine neue Architektur- oder Technologieentscheidung getroffen wird.
- Wenn bestehende Entscheidungen angepasst oder revidiert werden.

## Vorgehen (Schritt-fuer-Schritt)
1) Lies bestehende ADRs und den Projektueberblick.
2) Formuliere Kontext, Entscheidung, Alternativen und Konsequenzen.
3) Lege eine neue ADR-Datei an oder aktualisiere eine bestehende.
4) Verlinke relevante Anforderungen oder Module, falls betroffen.

## Lernperspektive
- Warum so? ADRs schaffen Transparenz ueber das Warum hinter Architektur.
- Alternativen: informelle Notizen, Kommentare in Code oder Issues.
- Warum nicht hier? Informelle Spuren gehen verloren und sind schwer nachzuvollziehen.

## Repo-Referenzen
- `docs/02_architecture/ADR/ADR-001-streamlit-mvp.md`
- `docs/02_architecture/ADR/ADR-002-ml-matching.md`
- `docs/00_overview/PROJECT_OVERVIEW.md`

## Qualitaetscheck
- ADR enthaelt Kontext, Entscheidung, Alternativen, Konsequenzen.
- Aussagen verweisen auf Repo-Dateien oder Anforderungen.
- Keine Annahmen ohne Repo-Beleg.
## Phasenbezug
| Phase | Aufgabe | Status |
|-------|---------|--------|
| Phase 2 | ADR-Entscheidungen dokumentieren | erledigt |