---
name: padel
description: Check padel court availability and manage bookings via the padel CLI.
metadata: {"moltbot":{"nix":{"plugin":"github:joshp123/padel-cli","systems":["aarch64-darwin","x86_64-linux"]},"config":{"requiredEnv":["PADEL_AUTH_FILE"],"stateDirs":[".config/padel"],"example":"config = { env = { PADEL_AUTH_FILE = \"/run/agenix/padel-auth\"; }; stateDirs = [ \".config/padel\" ]; };"},"cliHelp":"Padel CLI for availability\n\nUsage:\n  padel [command]\n\nAvailable Commands:\n  auth         Manage authentication\n  availability Show availability for a club on a date\n  book         Book a court\n  bookings     Manage bookings history\n  search       Search for available courts\n  venues       Manage saved venues\n\nFlags:\n  -h, --help   help for padel\n  --json       Output JSON\n\nUse \"padel [command] --help\" for more information about a command.\n"}}
---

# Padel Booking Skill

## CLI

```bash
padel  # On PATH (moltbot plugin bundle)
```

## Venues

Use the configured venue list in order of preference. If no venues are configured, ask for a venue name or location.

## Commands

### Check next booking
```bash
padel bookings list 2>&1 | head -3
```

### Search availability
```bash
padel search --venues VENUE1,VENUE2 --date YYYY-MM-DD --time 09:00-12:00
```

## Response guidelines

- Keep responses concise.
- Use 🎾 emoji.
- End with a call to action.

## Authorization

Only the authorized booker can confirm bookings. If the requester is not authorized, ask the authorized user to confirm.
