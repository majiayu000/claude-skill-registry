---
name: iecsat-storage
description: IECsat Storage Skill
trit: 0
color: "#26D826"
catsharp:
  home: Prof
  poly_op: ⊗ (parallel)
  kan_role: Adj
  bicomodule: true
---

# iecsat-storage Skill


> *"69 bytes of mutual awareness per tile. 3 × 23. Triadic by design."*

## Overview

**IECsat Storage** calculates on-chain storage costs for Plus Code tiles with GF(3)-conserved mutual awareness. Each tile maintains exactly 69 bytes of state.

## The 69-Byte Structure

```
69 = 3 × 23 (triadic decomposition)

┌─────────────────────────────────────────────────────────┐
│                   69-BYTE TILE STATE                    │
├─────────────────────────────────────────────────────────┤
│  PLUS (+1)     │  ERGODIC (0)   │  MINUS (-1)          │
│  23 bytes      │  23 bytes      │  23 bytes            │
│  GENERATOR     │  COORDINATOR   │  VALIDATOR           │
├────────────────┼────────────────┼──────────────────────┤
│  state_hash    │  neighbor_refs │  proof_data          │
│  (20 bytes)    │  (20 bytes)    │  (20 bytes)          │
│  trit (1 byte) │  trit (1 byte) │  trit (1 byte)       │
│  flags (2 B)   │  flags (2 B)   │  flags (2 B)         │
└────────────────┴────────────────┴──────────────────────┘

Σ(trit) = +1 + 0 + (-1) = 0 ✓ CONSERVED
```

## Plus Code Precision Levels

| Length | Tiles | Resolution | Example |
|--------|-------|------------|---------|
| 2 | 162 | 2,226 km | Global quadrant |
| 4 | 64,800 | 111 km | Country region |
| 6 | 25.9M | 5.6 km | City district |
| 8 | 10.4B | 278 m | City block |
| 10 | 4.1T | 14 m | Building |
| 11 | 83T | 70 cm | Room |
| 13 | 33Q | 14 cm | Object |
| 15 | 13 quint | 5.6 mm | Component |
| 17 | 5.3 sext | 223 μm | Microstructure |

## Storage Cost Analysis (Aptos Mainnet)

```
Pricing assumptions:
- Storage cost: 0.00001 APT per byte
- APT price: $12 USD
- Bytes per tile: 69

Cost formula:
  APT = tiles × 69 × 0.00001
  USD = APT × 12
```

### Cost Table

| Precision | Tiles | Storage | APT | USD |
|-----------|-------|---------|-----|-----|
| 10-char | 4.15T | 286 TB | 2.86M | $34.3B |
| 11-char | 82.9T | 5.7 PB | 57.2M | $687B |
| 12-char | 1.66Q | 114 PB | 1.14B | $13.7T |
| 13-char | 33.2Q | 2.29 EB | 22.9B | $275T |
| 17-char | 5.31S | 366 ZB | 3.66Q | $44 quint |

## Hierarchical Strategy

```
┌─────────────────────────────────────────────────────────┐
│                  ON-CHAIN (APTOS)                       │
│  10-char root tiles: 4.1T × 69B = 286 TB               │
│  Cost: 2.86M APT ($34B)                                │
│  Contains: Merkle roots for child tiles                │
├─────────────────────────────────────────────────────────┤
│                 OFF-CHAIN (ARWEAVE)                     │
│  11-17 char tiles: Content-addressed                   │
│  Proof: Merkle path from root → leaf                   │
│  Cost: ~$0.005/MB permanent storage                    │
└─────────────────────────────────────────────────────────┘
```

## Denotation

```
IECsat : PlusCode → (TileState × MerkleProof)

where:
  TileState = { plus: 23B, ergodic: 23B, minus: 23B }
  MerkleProof = Path from 10-char root to target tile

Invariant: ∀ tile: Σ(trit) ≡ 0 (mod 3)
```

## Practical Applications

### Battery Cell Tracking (238.8B cells)

```
Cells: 238,800,000,000
Storage: 238.8B × 69B = 16.5 TB
APT: 165M APT
USD: $1.98B

Fraction of APT supply: 16.5%
```

### Global Building Coverage (10-char)

```
All buildings worldwide: ~1 billion
Storage: 1B × 69B = 69 GB
APT: 690K APT
USD: $8.3M
```

## Move Implementation

```move
struct TileState has store, copy, drop {
    // PLUS (+1) - 23 bytes
    generator_hash: vector<u8>,  // 20 bytes
    generator_trit: u8,          // 1 byte
    generator_flags: u16,        // 2 bytes

    // ERGODIC (0) - 23 bytes
    coordinator_refs: vector<u8>, // 20 bytes
    coordinator_trit: u8,         // 1 byte
    coordinator_flags: u16,       // 2 bytes

    // MINUS (-1) - 23 bytes
    validator_proof: vector<u8>,  // 20 bytes
    validator_trit: u8,           // 1 byte
    validator_flags: u16,         // 2 bytes
}

public fun is_gf3_conserved(state: &TileState): bool {
    let sum = (state.generator_trit as i8 - 1) +  // 2 → +1
              (state.coordinator_trit as i8) +     // 0 → 0
              (state.validator_trit as i8 - 1);    // 1 → -1 (adjusted)
    sum == 0
}
```

## Commands

```bash
# Calculate storage for N tiles
python3 -c "
tiles = 4_147_200_000_000  # 10-char
bytes_per_tile = 69
apt_per_byte = 0.00001
apt_price = 12

total_bytes = tiles * bytes_per_tile
total_apt = total_bytes * apt_per_byte
total_usd = total_apt * apt_price

print(f'Tiles: {tiles:,}')
print(f'Storage: {total_bytes/1e12:.2f} TB')
print(f'APT: {total_apt/1e6:.2f}M')
print(f'USD: \${total_usd/1e9:.2f}B')
"
```

## GF(3) Triads

```
iecsat-storage (0) ⊗ aptos-gf3-society (+1) ⊗ merkle-validation (-1) = 0 ✓
iecsat-storage (0) ⊗ plus-codes (+1) ⊗ content-addressing (-1) = 0 ✓
```

---

**Skill Name**: iecsat-storage
**Type**: Storage Cost Estimation / On-Chain Economics
**Trit**: 0 (ERGODIC - COORDINATOR)
**GF(3)**: Mediates between tile generation and validation

## Cat# Integration

This skill maps to Cat# = Comod(P) as a bicomodule in the Prof home:

```
Trit: 0 (ERGODIC)
Home: Prof (profunctors/bimodules)
Poly Op: ⊗ (parallel composition)
Kan Role: Adj (adjunction bridge)
```

### GF(3) Naturality

The skill participates in triads where:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.
