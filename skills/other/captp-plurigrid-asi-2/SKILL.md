---
name: universal-captp-derivation
description: 'Universal CapTP Derivation Skill'
version: 1.0.0
---

# Universal CapTP Derivation Skill

Traces capability derivation chains through 3×3 expert poset with GF(3) conservation.

## Core Principle

> **A capability IS the (seed, index) tuple. Expertise IS the trit alignment.**

## 3×3 Expert Poset Structure

| Layer | Validator (-1) | Coordinator (0) | Generator (+1) | Domain |
|-------|----------------|-----------------|----------------|--------|
| 1 | Jules Hedges | John Baez | Fabrizio Genovese | categorical-games |
| 2 | David Egolf | Mike Shulman | sarahzrf | sheaf-theory |
| 3 | Betweenness | Mantissa | ModalNoah | neural-categorical |

## Derivation Chains

```
capability(-1) → vat(0) → invoke(+1)     [spawn-lifecycle]
membrane(-1)   → netlayer(0) → lambda(+1) [invoke-path]
handoff(-1)    → syrup(0) → sturdy_ref(+1) [transfer-path]
revoke(-1)     → promise(0) → goblin(+1)   [revoke-path]
```

## Superposition States

Each capability exists in superposition across expert domains:
- **generator-dominant**: Red channel highest (trit=+1)
- **coordinator-dominant**: Green channel highest (trit=0)
- **validator-dominant**: Blue channel highest (trit=-1)
- **superposed**: Balanced RGB

## GF(3) Conservation

```
Term Σ + Expert Σ ≡ 0 (mod 3)
```

Current state: **COHERENT** (residue = 0)

## Commands

```bash
# Trace derivation chains
python3 -c "import duckdb; c=duckdb.connect('culture_evolution.duckdb'); print(c.execute('SELECT * FROM derivation_chains').df())"

# View expert triads
python3 -c "import duckdb; c=duckdb.connect('culture_evolution.duckdb'); print(c.execute('SELECT * FROM expert_triads').df())"

# Query NOW superposition
python3 -c "import duckdb; c=duckdb.connect('culture_evolution.duckdb'); print(c.execute('SELECT * FROM now_superposition').df())"

# Universal skill derivation
python3 -c "import duckdb; c=duckdb.connect('culture_evolution.duckdb'); print(c.execute('SELECT * FROM universal_skill_derivation LIMIT 20').df())"
```

## Integration Points

| Database | Table/View | Purpose |
|----------|------------|---------|
| culture_evolution.duckdb | derivation_chains | CapTP flow traces |
| culture_evolution.duckdb | expert_triads | 3×3 expert poset |
| culture_evolution.duckdb | capability_poset | Lattice structure |
| culture_evolution.duckdb | now_superposition | Current state |
| culture_evolution.duckdb | universal_skill_derivation | Full matrix |
| gh_interactome.duckdb | captp_third_party_contributions | Contributor mapping |

## Key Files

- [lib/culture_alter.rb](../../lib/culture_alter.rb) - Stigmergic evolution
- [lib/color_capability.rb](../../lib/color_capability.rb) - CapTP goblin swarm
- [lib/interactome_open_games.rb](../../lib/interactome_open_games.rb) - Expert triads
- [scripts/culture_games.rb](../../scripts/culture_games.rb) - Culture × Open Games

## Trit Assignments

| Trit | Role | Color Channel | Experts |
|------|------|---------------|---------|
| -1 | Validator | Blue | Hedges, Egolf, Betweenness |
| 0 | Coordinator | Green | Baez, Shulman, Mantissa |
| +1 | Generator | Red | Genovese, sarahzrf, ModalNoah |
