---
name: re-bridge
description: Use when working on historical compiler path, RE-derived code, morph designer bridge, type 2/3 branches, sanitized handoffs, stage byte layout, passthrough sentinel, trust tiers, or any code in trench-forge/src/historical.rs or contracts/
---

Before writing any code, read these files:
- `docs/context/re-findings.md` — proven compiler facts, type branches, byte layout, sentinel values
- `docs/context/trust-hierarchy.md` — which artifacts are safe to implement from
- `docs/context/identity.md` — TRENCH is a stress simulator, not an emulation

Key constraints:
- Data flows one way: DIRTY → sanitized → CLEAN. Never reverse.
- Only Tier 1 and Tier 2 artifacts are implementation-ready. Tier 3 = orientation only. Tier 4 = do not implement.
- MorphDesigner is NOT the fix for forge quality — it's a small deterministic compiler, same ceiling as RBJ.
- No ROM dumps, binary blobs, or address-derived artifacts in shipping code.
- No heritage branding (E-mu, Morpheus, Z-Plane) in anything that ships.
