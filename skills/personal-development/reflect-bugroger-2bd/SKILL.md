---
name: reflect
description: Run a reflection ritual. Invokes Ada.
argument-hint: "[timescale: daily|weekly|quarterly|yearly]"
---

# Reflect

Invoke Ada with action=reflect and the specified timescale.

## Usage

- `/reflect` or `/reflect daily` - reflect on today
- `/reflect weekly` - reflect on the week
- `/reflect quarterly` - reflect on the quarter
- `/reflect yearly` - reflect on the year

## Process

1. Parse timescale from argument (default: daily)
2. Invoke @ada with: action=reflect, timescale={parsed}
