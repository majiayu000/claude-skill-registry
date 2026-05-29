---
description: Domain knowledge and business processes for [PROJECT_NAME]
globs:
  - "src/**/*"
alwaysApply: false
---

# Domain Knowledge: [PROJECT_NAME]

> Project: [PROJECT_NAME]
> Last Updated: [DATE]
> Purpose: Fachliche Dokumentation der Geschäftsprozesse

## Self-Updating Rule

**WICHTIG:** Diese Dokumentation soll IMMER aktuell sein.

Wenn du Code änderst der Geschäftslogik betrifft:

1. **Prüfe** ob die Änderung einen dokumentierten Prozess betrifft
2. **Aktualisiere** das entsprechende Prozess-Dokument wenn nötig
3. **Füge hinzu** neue Prozesse die du implementierst
4. **Markiere als veraltet** Prozesse die nicht mehr existieren

## Business Context

[BUSINESS_CONTEXT_DESCRIPTION]

## Domain Areas

| Area | File | Description | Status |
|------|------|-------------|--------|
<!-- Wird automatisch befüllt durch /add-domain -->

## Glossar

| Begriff | Definition |
|---------|------------|
<!-- Fachbegriffe und ihre Bedeutung -->

---

## How to Add New Domain Areas

Use the `/add-domain` command to add new business areas:

```
/add-domain "User Registration"
/add-domain "Order Processing"
```

This will:
1. Create a new document from the process template
2. Add an entry to the Domain Areas table above
3. Prompt you for the process description
