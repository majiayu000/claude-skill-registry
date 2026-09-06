---
name: fastopt
description: 'Use when optimizing suspected hot paths without waiting for benchmarks. Not for estimated-floor optimization: use fastopt-extreme. Not for measured-floor rebuild campaigns: use extremely-optimize.'
---

# Fastopt

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User wants to optimize suspected hot paths without waiting for benchmarks, labeling claims as hypotheses. |
| Authority | Read-only. No file, VCS, credential, paid, published, deployed, or remote mutation. |
| Side effect | Chat output only: hypotheses and benchmark designs before any mutation or performance claim. |
| Done | Hypotheses and benchmark designs for suspected hot paths are emitted; no mutation or speed claim made. |

## Inputs

Required: one or more suspected hot paths named by the user (file, function, or call site) and the workload or input shape that makes each path hot.

Optional: prior measurements, profiling traces, or environment constraints the user supplies. Absent measurements are treated as unmeasured, not as evidence of slowness.

## Procedure

1. For each named hot path, read the source and surrounding call graph read-only; record the inputs, allocations, loops, and branches that plausibly dominate cost. Done when: every named path is read and its cost-plausible elements recorded.
2. Label every cost observation a hypothesis, not a finding: state the assumed workload, the assumed dominant operation, and the assumed magnitude rank, with no speed claim. Done when: every observation carries its hypothesis label with workload, dominant operation, and magnitude rank.
3. For each hypothesis, design a benchmark that would confirm or refute it: name the metric, the baseline, the variant, the workload generator, the warm-up, the repetition count, and the noise controls. Done when: every hypothesis has a benchmark design with all seven elements named.
4. Bound the change scope implied by each hypothesis to the named path; do not propose edits outside it or assume a fix is correct. Done when: every hypothesis's implied change scope is bounded to its named path.
5. If a hypothesis cannot be tested without mutating code, state the minimal mutation needed to measure it and stop before performing it. Done when: the blocking reason and minimal mutation are stated, or the hypothesis is testable read-only.
6. Emit the hypotheses and benchmark designs as chat output. Make no mutation and no speed claim. Done when: the chat report is emitted with no mutation and no speed claim.

## Failure and recovery
- Unmeasured path: mark the hypothesis unmeasured; do not infer slowness from absence of data.
- Ambiguous hot path: ask the user to name the path and workload; stop rather than guess.
- Benchmark infeasible in read-only scope: state the blocking reason and the minimal mutation that would unblock measurement; do not perform it.
- No recovery widens authority: this skill never mutates files, VCS, credentials, or remote state. A blocked result is emitted as blocked, not as success.

## Output
A chat report containing, per suspected hot path: one labeled hypothesis (workload, dominant operation, magnitude rank, no speed claim) and one benchmark design (metric, baseline, variant, workload generator, warm-up, repetitions, noise controls). Blocked paths are reported as blocked with the reason.
