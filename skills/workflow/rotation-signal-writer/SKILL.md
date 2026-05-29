---
name: Rotation Signal Writer
description: Convert Structure/Flows JSON into concrete rotation actions with size, stop, invalidation under the Crypto Rotation Playbook v2. Use after structure or flows outputs are available.
allowed-tools: Read, Grep, Glob
---

# Rotation Signal Writer

## Instructions
1) Read the newest files in out/structure/*.json and out/flows/*.json.
2) Apply rules:
   - ≤2% account risk per leg; ≤4% daily.
   - Keep ≥20–30% PAXG core until daily HL+HH confirms.
   - Stage BTC: probe 10–15% on 4H CoC↑ + 1H VWAP hold; add 10–15% after successful retest.
   - Alts only when correlation gates pass AND ETHBTC slope ≥0 (ETH before SOL/ADA).
3) Produce out/rotation_signals.md with:
   - Portfolio Health, Signals, Action Plan (exact %), Stops/Invalidations, Trader Checklist.
4) End with a trader brief (<200 words).
