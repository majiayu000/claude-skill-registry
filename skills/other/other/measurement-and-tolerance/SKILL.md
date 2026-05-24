---
name: measurement-and-tolerance
description: Measurement and tolerance for the trades — how dimensions are specified, measured, and verified, and how real parts are allowed to deviate from their specifications. Covers tolerance stacks, reference surfaces and datum chains, the difference between accuracy and precision, measurement tool selection by required resolution, and the discipline of stating tolerance in terms of what the fit actually requires rather than what the tool can read. Use when writing a specification, selecting measurement tools, or diagnosing a fit failure that looks like a measurement error.
type: skill
category: trades
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/trades/measurement-and-tolerance/SKILL.md
superseded_by: null
---
# Measurement and Tolerance

Tolerance is the amount of deviation from a nominal dimension that is acceptable for a part to still function. Measurement is how the actual deviation is determined. The two together form the dimensional backbone of the trades — everything that depends on parts meeting each other depends on somebody having specified, measured, and verified dimensions. This skill covers the conceptual machinery of tolerance, the practical discipline of measurement, and the common failure modes where parts that measure correctly still do not fit.

**Agent affinity:** nasmyth (precision machining tolerances), taylor (time-study and measurement discipline), brunel-tr (interchangeable parts at Portsmouth)

**Concept IDs:** trades-tolerance-stack, trades-datum-reference, trades-measurement-resolution

## Tolerance is Not Slop

The word "tolerance" often suggests sloppiness — a tolerant specification is one that accepts worse work than an intolerant one. This is backwards. A tolerance is a statement of the maximum deviation that the engineering has already accounted for. A tolerance of ±0.001" is not permission to be sloppy; it is a declaration that the designer has verified that the function survives up to 0.001" of deviation and not beyond. Tightening the tolerance beyond what the function requires is waste; loosening it past what the function tolerates is failure.

### The cost curve

The cost of producing a part rises sharply as the tolerance tightens. Rough shop tolerances (±1/64" in wood, ±0.010" in metal) cost almost nothing beyond baseline. Fine shop tolerances (±0.005" in wood, ±0.001" in metal) cost several times more. Machine shop tolerances (±0.0005" in metal) cost an order of magnitude more. Metrology-grade tolerances (±0.0001" and below) cost several orders of magnitude more and require climate-controlled measurement rooms. Specifying a tolerance that is tighter than the function needs is paying this cost without benefit.

### Where tolerance comes from

Tolerances come from the function. A door in a house needs to swing freely; it tolerates a gap of a few sixteenths at the sides. A drawer needs to slide without binding; it tolerates a gap of thirty-seconds. A bearing fit in an engine needs a thousandth of interference; any more and it seizes, any less and it spins on the shaft. A precision optical mount needs a tenth of a thousandth; anything looser and the image is blurred. The tolerance follows from the function, not from the wish.

## Accuracy, Precision, and Resolution

These three terms are often confused. They are distinct.

- **Accuracy** is how close a measurement is to the true value. A scale that reads "50.00 g" when the true weight is 50.00 g is accurate.
- **Precision** is how close repeated measurements are to each other. A scale that consistently reads "49.97 g" on the same object is precise but not accurate (biased by 0.03 g).
- **Resolution** is the smallest increment the measurement tool can display. A digital caliper with 0.01 mm resolution can display 12.34 mm but not 12.345 mm.

All three matter. A high-resolution instrument that is inaccurate produces confident wrong readings. A high-accuracy instrument with poor resolution cannot distinguish values finer than its resolution. A high-precision but biased instrument produces consistent but wrong results. The ideal is all three: high resolution, high accuracy, and high precision.

### Resolution rule of thumb

The measurement tool's resolution should be about one-tenth of the tolerance being measured. Measuring a ±0.001" tolerance with a tool that reads to 0.001" is inadequate — the tool cannot distinguish a passing part from a failing one near the limit. Measuring the same tolerance with a tool that reads to 0.0001" is appropriate. Measuring with a tool that reads to 0.00001" is overkill and usually means the reading is dominated by noise and temperature effects.

## Datum References

A datum is a reference surface or feature from which other measurements are made. Every dimension is measured from something; that something is the datum. In a well-designed drawing, the datums are called out explicitly and all critical dimensions are referenced to the same datums in a consistent way.

### Why datums matter

A part may have multiple surfaces that look equivalent but are not. Measuring "the length of the part" has a different meaning depending on which surfaces you measure from. If the two end surfaces are both square to the sides, the measurements agree. If one end is slightly off-square, the measurements disagree, and the "true" length is ambiguous. Datum references resolve this ambiguity by specifying which surface is authoritative.

### Datum hierarchy

A primary datum is the first reference, usually the surface with the largest area or the most critical function. A secondary datum is the next reference, usually square to the primary. A tertiary datum is the third, orthogonal to the others. Together they define a coordinate system for the part. All dimensions are then referenced to this coordinate system in a consistent order.

### Common datum mistakes

- **Different datums on different drawings.** Part drawing uses corner A as origin; assembly drawing uses corner B. When the part is measured against the assembly, the tolerances accumulate in unexpected ways.
- **Implicit datums.** The drawing shows dimensions but does not specify which surfaces they are measured from. Different machinists pick different surfaces and get different parts.
- **Datum that is not machinable.** A datum defined on a surface that is not flat or not accessible to the measurement tool. The drawing is correct but not manufacturable.

## Tolerance Stacks

A tolerance stack is the accumulation of dimensional errors across multiple parts or features. When three parts each tolerance ±0.002" are assembled in series, the total stack in the worst case is ±0.006". In the statistical case (random errors from different sources), the stack is about ±0.0035". The worst case is guaranteed; the statistical case is typical.

### Worst case vs RSS

- **Worst case** tolerance stack assumes all parts are at the same extreme end of their tolerance. This is pessimistic but safe. Used when the consequence of a bad stack is catastrophic.
- **Root-sum-square (RSS)** tolerance stack assumes errors are random and normally distributed, and combines variances. This is the expected stack in high-volume production. Used when some rework is acceptable.

A design engineer chooses which stack method to use based on the consequences of assembly failure. Medical devices, safety-critical parts, and irreplaceable components use worst case. High-volume commercial products often use RSS with a planned rework rate.

### Designing around stacks

Common techniques for managing tolerance stacks:

- **Reduce the number of parts in the stack.** Fewer parts means fewer errors to accumulate.
- **Hand-fit critical interfaces.** Allow the final fit to be established during assembly rather than specified in advance.
- **Use tight tolerances where they matter and loose where they don't.** The budget spent on tolerance should be proportional to the function's sensitivity.
- **Use adjustable features.** Shims, set screws, adjustment screws, and slotted holes let the final assembly be brought into spec even when individual parts vary.

## Measurement Tools by Layer

Different measurement tools are appropriate for different resolution ranges. Using a tool outside its range is either wasteful (too much tool for the job) or inadequate (not enough tool).

### Rough shop (±1/32" to ±1/16")

- Tape measure (resolution ±1/32", accuracy depends on how the tape is held)
- Combination square (resolution ±1/32")
- Level (±1/16" over several feet)

### Fine shop (±0.005" to ±0.001")

- Dial caliper (resolution 0.001", accuracy ±0.001")
- Dial indicator (resolution 0.001", accuracy better)
- Steel rule with magnifier (resolution 1/64")

### Machine shop (±0.0005" to ±0.0001")

- Micrometer (resolution 0.0001", accuracy ±0.0001")
- Dial indicator on a test stand (resolution 0.0001" with the right indicator)
- Gauge blocks for reference

### Metrology (below ±0.0001")

- Gauge blocks (reference accuracy at the millionths)
- Air gauge, electronic gauge (resolution to 0.00001")
- Coordinate measuring machine (CMM) in climate-controlled room
- Optical interferometry

Each tier builds on the one below. A gauge block set is verified against a primary reference in a national lab. A micrometer is calibrated against gauge blocks. A dial caliper is checked against a micrometer. A tape measure is checked against a caliper. The chain of traceability is what makes measurements meaningful outside the shop that made them.

## Measurement Discipline

Beyond the choice of tool, measurement has a discipline of its own. The discipline is what separates measurements that can be trusted from measurements that merely exist.

### Zero the tool before use

Every measurement tool has some zero offset. Calipers and micrometers are zeroed against themselves (close the jaws, set to zero). Dial indicators are zeroed against a reference surface. Scales are tared against an empty container. A tool that is not zeroed produces a reading that is systematically offset by the zero error, which is often small but cumulative across parts.

### Check against a known reference

A measurement tool should periodically be checked against a known reference — gauge block, certified part, or other calibrated standard. The interval depends on the tool, the environment, and the stakes. A production-shop micrometer checked weekly will catch drift before it produces bad parts. A micrometer that is never checked will eventually drift enough to matter, and the drift will be blamed on other causes.

### Measure the same thing multiple times

A single measurement is subject to single-measurement error — grip force, alignment, temperature, the user's fatigue level. Multiple measurements average out some of these. Experienced machinists measure critical dimensions two or three times and use the consistent value, not the first value. If the measurements disagree, the dimension is remeasured until they agree or until the source of the disagreement is found.

### Record, don't remember

Measurements that are going to be used later should be written down, not remembered. Memory is unreliable for numbers. A shop notebook, a markup on the drawing, a label on the part — any of these beats remembering. A machinist who says "I measured it earlier, it was fine" is making a memory claim, not a measurement claim, and memory claims do not stack as evidence.

## When the Parts Don't Fit

A classic failure mode: the parts measure correctly and do not fit. This is not actually a measurement error; it is usually a specification error, a datum error, or a fit allowance that was not considered.

### Diagnostic questions

1. Are the parts being measured the same way the assembly uses them? The datum in the drawing may not match the datum in assembly.
2. Is there a tolerance stack that the designer did not calculate?
3. Is there a material movement (thermal, moisture) that has changed the part since it was measured?
4. Is the measurement tool accurate at the dimension being measured? (Some tools are accurate at midrange and drift at the extremes.)
5. Is the fit's actual requirement what the drawing said? (Sometimes the drawing is wrong.)

The tradesperson diagnosing this has to be willing to question the drawing, not just the part. A drawing is a specification, but specifications can be wrong.

## References

- David Pye, *The Nature and Art of Workmanship* (1968) — the "workmanship of risk" and approximate-fit discipline
- Stanley J. Wrysinski, *Tolerance Stack Analysis* (technical references) — stack methods
- *Machinery's Handbook* (Industrial Press) — reference for measurement tools, fits, standards
- Carolyn Cooper, *Shaping Invention* (1991) — the history of interchangeable parts
