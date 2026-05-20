---
name: confetti
description: Trigger a two-step confetti celebration by opening the Raycast confetti URL and speaking a phrase with the Alex voice. Use when the user asks to run confetti, celebrate, or trigger the confetti sequence.
---

# Confetti

## Overview
Run a fixed two-command celebration sequence.

## Quick Start

```bash
scripts/run_confetti.sh
```

Optional control flags:

```bash
scripts/run_confetti.sh --wait
scripts/run_confetti.sh --async
```

Default behavior is optimized for performance:
- Interactive terminal (`TTY`): waits for speech to finish.
- Non-interactive automation: starts speech in background and returns immediately.

## Tasks

### Run confetti
- Execute `scripts/run_confetti.sh` to open Raycast confetti and speak the phrase.

## Resources

### scripts/
- `run_confetti.sh`: Triggers confetti and speaks the phrase, with async fast path for automation.
