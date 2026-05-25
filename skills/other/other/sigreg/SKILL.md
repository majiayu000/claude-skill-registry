---
name: sigreg
description: Sketched Isotropic Gaussian Regularization primitive. Scalar loss matching the embedding distribution to a standard-normal target via Cramér-Wold slicing and the Epps-Pulley empirical characteristic function test. Port of rbalestr-lab/lejepa (MIT). Default-off in v1.49.571.
version: 1.49.571
tier: T1
phase: 729
source_paper: arXiv:2511.08544v3
license_attribution: rbalestr-lab/lejepa (MIT)
---

# SIGReg — Sketched Isotropic Gaussian Regularization

Port of SIGReg from Balestriero & LeCun (2025, *LeJEPA*) arXiv:2511.08544v3. The
primitive computes a scalar loss measuring how far an embedding distribution is
from the standard-normal target, using Cramér-Wold slicing plus the Epps-Pulley
empirical characteristic function test. Linear O(N·M·K) time, naturally
differentiable, multi-GPU friendly (all_reduce over ECF averages).

## Public API

```typescript
import { sigreg } from './src/sigreg/index.js';

const loss = sigreg(embeddings);  // embeddings: number[num_samples][num_dims]
// scalar loss; use as L_total = L_pred + λ · loss
```

For telemetry:

```typescript
import { sigregWithBreakdown } from './src/sigreg/index.js';

const { loss, perSliceStatistic, maxSliceStatistic, runTag } = sigregWithBreakdown(embeddings);
```

## Configuration

Default matches the LeJEPA reference implementation:

```typescript
const LEJEPA_DEFAULT_CONFIG = {
  numSlices: 1024,
  univariateTest: { numPoints: 17, sigma: 1.0 },
};
```

## Feature flag

Default-off. Opt-in via `.claude/gsd-skill-creator.json`:

```json
{
  "heuristics-free-skill-space": {
    "sigreg": { "enabled": true }
  }
}
```

## Attribution

Ported from https://github.com/rbalestr-lab/lejepa under the MIT license.
© Randall Balestriero and LeJEPA Contributors. See `../../license_notices.md`.

## Related modules

- `src/skill-isotropy/` — Skill Space Isotropy Audit (Phase 728) — read-only audit use case
- `src/intrinsic-telemetry/` — Phase 733 — SIGReg-on-embeddings is a candidate signal
