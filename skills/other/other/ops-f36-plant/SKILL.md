---
name: ops-f36-plant
description: >
  F-36 plant floor operations namespace. Subcommand router for machine testing,
  disposition, shift management, vendor review, and compliance monitoring.
  Designed for Paul Bevilaqua — gloved hands, standing, noisy environment.
triggers:
  - f36
  - plant floor
  - machine test
  - torque test
  - thermal test
  - ndi test
  - disposition
  - shift handoff
  - vendor review
  - assembly status
provides:
  - ops-f36-plant
composes:
  - batch-quality
  - monitor-drift-sensors
  - quality-audit
  - agent-inbox
  - episodic-archiver
  - ops-sam-gov
  - review-pdf
  - cui-marker
  - data-audit
  - sparta-review
  - task-monitor
persona: paul_bevilaqua
streamdeck:
  buttons_manifest: buttons.yaml
  icons_dir: icons/
---

# F-36 Plant Floor Operations

Namespace skill for Paul Bevilaqua's plant floor workflow. Every `pi f36 <subcommand>`
routes through this skill's `run.sh`.

## Subcommands

### Machine Testing (left-to-right workflow)
```bash
pi f36 test torque --part-id <id>      # Torque test sequence
pi f36 test thermal --part-id <id>     # Thermal cycling test
pi f36 test ndi --part-id <id>         # Non-destructive inspection
pi f36 test inspect --part-id <id>     # Visual inspection checklist
```

### Disposition
```bash
pi f36 disposition pass --part-id <id>   # Mark part as passed (green)
pi f36 disposition fail --part-id <id>   # Mark part as failed (red)
pi f36 escalate --part-id <id> --notify-qa  # Escalate to QA supervisor
```

### Documentation
```bash
pi f36 capture-photo --part-id <id>              # Photo documentation
pi f36 capture-photo --type vendor-material      # Vendor material photo
pi f36 log --part-id <id>                        # Log entry for part
pi f36 scan-barcode                              # Scan part barcode
pi f36 next-part                                 # Advance to next part
```

### Shift Operations
```bash
pi f36 shift-handoff          # End-of-shift handoff report
pi f36 shift-summary          # Shift productivity summary
pi f36 shift-log --today      # Today's shift log
pi f36 assembly-status        # Current assembly line status
pi f36 maintenance-log        # Log maintenance event
```

### Vendor Review
```bash
pi f36 deviation-report       # Flag material spec deviation
pi f36 vendor-reject          # Reject vendor material batch
```

## Architecture

This skill composes from existing Embry-OS skills rather than reimplementing:

| Subcommand | Composes From | What It Adds |
|------------|---------------|--------------|
| `test *` | `/quality-audit`, `/batch-quality` | Part-ID tracking, MIL-STD test sequence |
| `disposition *` | `/batch-quality --approve/--reject` | Part-ID linkage, green/red feedback |
| `escalate` | `/agent-inbox` | QA supervisor notification |
| `capture-photo` | camera capture | Part-ID metadata, EXIF tagging |
| `shift-*` | `/episodic-archiver`, `/analytics` | Shift context, handoff formatting |
| `deviation-report` | `/review-pdf --compare` | Spec comparison with deviation flagging |
| `scan-barcode` | xclip/xdotool | Barcode reader integration |

## HMI Design Principles (MIL-STD-1472 + 5ft-Away)

- **Max 13 buttons per context** (out of 32 XL slots). Empty space = breathing room.
- **UNDO at [31]** (bottom-right corner), every context, never moves. Gloved thumb finds it blind.
- **ESCALATE at [7]** (top-right), every context, never moves. Always-on emergency.
- **Zone layout**: top row = widgets/status, middle = actions (sparse), bottom-left = disposition.
- **Voice drives workflow, deck reflects state.** Paul talks to Embry via PersonaPlex.
- **No page navigation.** Context service pushes the right surface based on voice/barcode/workflow.
- **Two interaction modes**: Standing/gloved (5ft, voice + deck) and lean-in (Tauri app, deck = monitor).
- Error prevention: PASS/FAIL visually distinct (green/red), separated from test buttons
- Glove-friendly: large touch targets, no multi-press required

## Stream Deck Integration

This skill's `buttons.yaml` is the single source of truth for all F-36 Stream Deck buttons.
The streamdeck project's context service reads this file to compose button surfaces.

Contexts defined in `buttons.yaml`:
- `machine_test` — part testing workflow (barcode scan, test sequence, disposition)
- `shift_ops` — shift management (handoff, QA, assembly, maintenance)
- `compliance` — compliance monitoring dashboard (drift, SPARTA, datalake)
- `vendor_review` — supply chain verification (SAM.gov, specs, approve/reject)

Universal buttons (present in all contexts):
- `ESCALATE` at position [7] — emergency QA notification
- `UNDO` at position [31] — undo last action, always reachable
