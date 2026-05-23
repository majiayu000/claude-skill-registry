---
name: response_style_selector
description: Ask the user to pick a response style and persist the preference.
metadata:
  short-description: Response style selection
---

## Purpose
Set the user's preferred response style on first interaction.

## Steps
1. Ask the user to choose: technical or humanized.
2. Record the choice in `.agent-docs/memory/USER_PREFERENCES.md`.
3. Continue execution without further questions unless blocked.
4. Keep responses short and aligned to the chosen style.
5. Allow the user to change the style later.

## Humanized Mode
- Short, plain language with minimal bullets.
- Minimal code details unless requested.
