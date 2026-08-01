---
name: project-phase-planner
description: 'name: project-phase-planner'
---

﻿---
name: project-phase-planner
description: Erstelle und pflege den phasenbasierten Projektplan fuer ATS CV Scorer; verwenden, wenn der Gesamtplan, Phasen oder Aufgaben aktualisiert werden muessen.
---

# Skill: project-phase-planner

## Zweck
Erzeuge und aktualisiere den phasenbasierten Projektplan inklusive Rollen, Aufgaben, Artefakten und Abschlusskriterien.

## Wann anwenden
- Wenn neue Phasen, Aufgaben oder Rollen benoetigt werden.
- Wenn der Plan an den aktuellen Project Snapshot angepasst werden muss.

## Vorgehen (Schritt-fuer-Schritt)
1) Lies den neuesten Project Snapshot unter `docs/project_state/`.
2) Leite Phasen, Aufgaben und Status aus dem Snapshot ab.
3) Aktualisiere den Phasenplan in `docs/codex_skills/PHASE_PLAN.md`.
4) Stelle sicher, dass Phase 0 explizit als erledigt markiert ist.

## Lernperspektive
- Warum so? Ein phasenbasierter Plan macht Fortschritt messbar und auditierbar.
- Alternativen: lose To-do-Listen ohne Status und Rollen.
- Warum nicht hier? Ohne Phasenstruktur fehlen Lern- und Entscheidungsnachweise.

## Repo-Referenzen
- `docs/project_state/`
- `docs/codex_skills/PHASE_PLAN.md`
- `docs/00_overview/PROJECT_STATE.md`

## Qualitaetscheck
- Alle Phasen haben Ziele, Rollen, Aufgaben, Outputs und Abschlusskriterien.
- Status basiert auf dem Project Snapshot.
- Keine nicht belegten Annahmen.

## Phasenbezug
| Phase | Aufgabe | Status |
|-------|---------|--------|
| Phase 1 | Phasenplan aus Snapshot ableiten | offen |