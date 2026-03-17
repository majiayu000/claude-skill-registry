---
name: plan
description: Run a planning ritual. Invokes Ada.
argument-hint: "[timescale: daily|weekly|quarterly|yearly]"
---

# Plan

Invoke Ada with action=plan and the specified timescale.

## Usage

- `/plan` or `/plan daily` - plan today
- `/plan weekly` - plan the week
- `/plan quarterly` - plan the quarter
- `/plan yearly` - plan the year

## Process

1. Parse timescale from argument (default: daily)
2. Invoke @ada with: action=plan, timescale={parsed}
