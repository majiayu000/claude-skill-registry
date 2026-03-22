---
name: tidal-auth
description: Authenticate with Tidal via OAuth. Use when the user wants to log in to Tidal, start authentication, or when a command fails with an authentication error.
allowed-tools: Bash
---

# Tidal Auth

Launch the Tidal OAuth authentication process to obtain a session token.

## Commands

### auth
- **Usage**: `tidal-cli auth`
- **Arguments**: none
- **Output**: Interactive — displays an OAuth login URL for the user to visit in their browser

## Instructions

1. Check `$ARGUMENTS` — if not empty, inform the user that `/tidal-auth` takes no arguments
2. Run the command:
   ```bash
   tidal-cli auth
   ```
3. Display the OAuth URL shown in the output and instruct the user to open it in their browser to complete the login
4. After the user completes the login, inform them the session has been saved and they can now use the other tidal skills

## Error Handling

- If the command fails with a network error (`"Error: Unable to connect to Tidal"`), inform the user to check their internet connection and try again
- If the user is already authenticated (session token exists), the command may indicate so — relay this confirmation to the user
