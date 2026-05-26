---
name: "cep-v8"
description: "Cross-model context handoff via expert council. 40% token reduction, 9.5/10 recall, 97% cross-domain preservation."
---

# CEP v8

## Execute

1. **S2A Filter:** Remove noise, keep signal
2. **Council (4 phases):** Load KB per phase, ARQ wrap (confidence≥0.9)
   - P1: `EXPERTS-MEMORY_ARCHITECT.md` → preservation list
   - P2: `EXPERTS-CROSS-DOMAIN_ANALYST.md` → edge map (xd flags)
   - P3: `EXPERTS-COMPRESSION_SPECIALIST.md` → CoD 5-iter (target 0.15)
   - P4: `EXPERTS-RESTORATION_ENGINEER.md` → cold-start validate
3. **Techniques:** `CASCADE.md` for integration
4. **Gates:** density≥0.15, xd≥97%, cold-start pass, trust(5), YAML valid
5. **Output:** Packet ID `$MM$DD$YYYY-XXX-LN-domain-topic-context` + preamble + YAML

## Schema

`PROTOCOL.md` for full YAML structure.

PDL Layers: L1:knowledge, L2:relational, L3:contextual, L4:metacognitive

## References

- `CASCADE.md` - Techniques
- `PROTOCOL.md` - Full spec
- `MIRAS.md` - Future positioning
- `EXPERTS-*.md` - Council KBs

## Holistic Check

Packet ID: WHEN/WHO/HOW HARD/WHAT/DOMAIN

---

*CEP v8 | ktg.one*
```

