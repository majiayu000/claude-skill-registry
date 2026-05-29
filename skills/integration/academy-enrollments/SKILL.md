---
name: academy-enrollments
description: Manage academy enrollments by appending rows to a Google Sheet (used by Zapier/n8n to grant LearnWorlds access).
---

# Academy enrollments (Sheets → Zapier/n8n → LearnWorlds)

LearnWorlds API is not available on the current plan, so enrollment actions are triggered by writing rows into a Google Sheet that Zapier/n8n watches.

## Sheet

- Configure defaults in `~/.config/skills/config.json` under `academy_enrollments`:
  - `account`: Google account for Sheets access
  - `sheet_id`: Spreadsheet ID

Example:
```json
{
  "academy_enrollments": {
    "account": "you@example.com",
    "sheet_id": "spreadsheet_id_here"
  }
}
```

Tabs (actual names in the sheet):
- `Dar acceso` (append rows to grant access)
- `Quitar acceso`
- `Añadir tag`
- `Eliminar tag`

`Dar acceso` columns (A:E):
- `email`, `nombre`, `apellidos`, `producto`, `precio`

## Helpers

- Natural-language helper (best effort parser):
  - `scripts/enroll-nl "Enroll Nombre Apellidos (email@dom.com) in AI Expert precio 997"`

- Low-level helper (explicit args):
  - `scripts/enroll-grant-access.sh --email ... --nombre ... --apellidos ... --formacion "AI Expert" --precio 997`
  - If not configured, pass `--account` and `--sheet-id` explicitly.

- List known product IDs seen in the sheet:
  - `scripts/enroll-list-products.sh`
  - If not configured, pass `--account` and `--sheet-id` explicitly.

## Agent behavior

When the user asks in natural language to enroll someone:
1) Parse `email`, full name, course name (e.g. "AI Expert"), optional price.
2) Confirm parsed fields before appending the row (ask for explicit OK if any field is ambiguous).
3) Append a row to `Dar acceso` via the helper.
4) Reply with a short confirmation.

Avoid posting any sensitive data beyond the minimum necessary (email + course). Do not paste full sheet contents in chat.
