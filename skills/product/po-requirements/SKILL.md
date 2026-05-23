---
description: Product Owner requirements gathering and story creation for [PROJECT_NAME]
globs: []
alwaysApply: false
---

# PO Requirements Skill

> Project: [PROJECT_NAME]
> Generated: [DATE]
> Purpose: Guide for gathering requirements and creating user stories

## When to Use

This skill guides you when:
- Creating new user stories with `/create-spec`
- Adding stories with `/add-story`
- Adding quick tasks with `/add-todo`
- Creating bug stories with `/add-bug`

## Quick Reference

### User Story Format
```gherkin
Feature: [Feature Name]
  Als [User Role]
  möchte ich [Action],
  damit [Benefit].
```

### Acceptance Criteria (Gherkin)
- **Ein Verhalten pro Szenario**: Fokussiert und testbar
- **Konkrete Werte**: "100€" nicht "einen Betrag"
- **Nutzer-Perspektive**: WAS passiert, nicht WIE
- **Max 2-3 "And" Steps**: Pro Given/When/Then

### Requirements Dialog Questions

**Story Context:**
1. Was soll erreicht werden?
2. Wer braucht das? (User Role)
3. Warum ist das wichtig? (Business Value)

**Story Details:**
4. Was sind die Akzeptanzkriterien? (2-5 Szenarien)
5. Welche Edge Cases gibt es?
6. Gibt es Abhängigkeiten zu anderen Stories?

**Prioritization:**
7. Wie kritisch ist das? (Critical/High/Medium/Low)
8. Welcher User-Type profitiert am meisten?

---

## Detailed Guidance

### Gherkin Best Practices

**Good Example:**
```gherkin
Scenario: Erfolgreiche Registrierung mit valider Email
  Given ich bin auf der Registrierungsseite
  And kein Account existiert mit email@example.com
  When ich email@example.com und ein Passwort eingebe
  And ich auf "Registrieren" klicke
  Then wird mein Account erstellt
  And ich erhalte eine Bestätigungsemail
  And ich werde zum Dashboard weitergeleitet
```

**Bad Example (avoid):**
```gherkin
# ❌ Zu technisch, mehrere Verhaltensweisen
Scenario: Registrierung und Login
  Given ich navigiere zu /register.html
  When ich das Formular ausfülle und submitiere
  Then wird ein POST zu /api/users gemacht
  And die Datenbank enthält einen neuen Eintrag
  And ich kann mich einloggen
```

### Story Sizing

**XS (1 SP):** Single file, < 50 LOC
- Beispiel: "Add loading spinner to button"

**S (2-3 SP):** 2-3 files, < 200 LOC
- Beispiel: "User can edit profile name"

**M (5 SP):** 4-5 files, < 400 LOC
- Beispiel: "User registration with email verification"

**Too Large:**
- If > 5 files or > 400 LOC: Split into multiple stories
- If multiple features: Create separate stories

### Priority Guidelines

**Critical:**
- System doesn't work without it
- Blocker for other work
- Security issue

**High:**
- Important for release
- High user value
- Frequently requested

**Medium:**
- Nice to have
- Improves UX
- Optional feature

**Low:**
- Future enhancement
- Edge case
- Rarely used

### Dependency Types

**Technical Dependency:**
- Story A must be done before Story B can start
- Example: "API endpoint" before "Frontend integration"

**No Dependency:**
- Stories can be done in any order
- Parallel execution possible

---

## Common Patterns

### New Feature Story
```gherkin
Feature: Export User Data
  Als angemeldeter User
  möchte ich meine Daten als PDF exportieren,
  damit ich eine Kopie für meine Unterlagen habe.

Scenario: Erfolgreicher Export
  Given ich bin angemeldet
  And ich habe Daten in meinem Account
  When ich auf "Daten exportieren" klicke
  Then wird eine PDF-Datei generiert
  And die PDF enthält alle meine Daten
  And die PDF wird heruntergeladen
```

### Enhancement Story
```gherkin
Feature: Bulk User Selection
  Als Administrator
  möchte ich mehrere User auf einmal auswählen,
  damit ich Aktionen effizienter durchführen kann.

Scenario: Auswahl mehrerer User mit Checkbox
  Given ich bin auf der User-Liste
  When ich die Checkboxen von 3 Usern anklicke
  Then sind 3 User ausgewählt
  And ich sehe "3 User ausgewählt"
  And Bulk-Aktionen sind verfügbar
```

### Bug Fix Story
```gherkin
Feature: Fix Login Error Message
  Als User
  möchte ich eine hilfreiche Fehlermeldung sehen,
  damit ich verstehe warum Login fehlschlägt.

Scenario: Falsches Passwort zeigt klare Meldung
  Given ich habe einen Account mit user@example.com
  When ich user@example.com mit falschem Passwort eingebe
  Then sehe ich "Email oder Passwort ist falsch"
  And NICHT "Error 401"
```

---

## Anti-Patterns to Avoid

❌ **Vage Beschreibungen**
- "Als User möchte ich die App nutzen"
- Better: "Als Administrator möchte ich User deaktivieren"

❌ **Technische Details im Feature**
- "Als Developer möchte ich einen API Endpoint bauen"
- Better: "Als User möchte ich mein Profil bearbeiten"

❌ **Zu groß**
- "Als User möchte ich das komplette Profil-System nutzen"
- Better: Split in: Profil ansehen, Profil bearbeiten, Avatar hochladen

❌ **Mehrere Features in einer Story**
- "Als User möchte ich registrieren, einloggen, und Passwort zurücksetzen"
- Better: 3 separate Stories

---

## Checklist for Good Stories

When creating a story, verify:
- [ ] Clear user role (wer?)
- [ ] Specific action (was?)
- [ ] Clear benefit (warum?)
- [ ] 2-5 concrete acceptance criteria
- [ ] Appropriate size (XS/S/M)
- [ ] No technical implementation details
- [ ] Testable scenarios
- [ ] Dependencies identified

---

## Project-Specific Patterns

[PROJECT_SPECIFIC_PATTERNS]
