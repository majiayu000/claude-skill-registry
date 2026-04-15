---
name: operations-and-lean
description: Operations management and lean production techniques for turning inputs into outputs under variability. Covers the Toyota Production System, seven wastes, just-in-time, kanban, jidoka, single-minute die exchange, 5 Whys, value stream mapping, bottleneck theory, and the distinction between mass production and flexible production. Use when diagnosing operational waste, designing production flows, setting up quality systems, or comparing batch-and-queue to one-piece flow.
type: skill
category: business
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/business/operations-and-lean/SKILL.md
superseded_by: null
---
# Operations and Lean

Operations is the function that transforms inputs into outputs at acceptable cost, quality, and timing. Lean is the body of thought — rooted in the Toyota Production System (TPS) — that treats waste elimination as the primary operational lever, and flexibility as the route to scale that mass production cannot match. This skill catalogs the core TPS techniques with worked examples, contrasts lean against Ford's mass-production template, and gives decision guidance for when each applies.

**Agent affinity:** ohno (TPS and waste elimination), ford (mass production and assembly-line history)

**Concept IDs:** bus-business-structures, bus-cost-benefit-analysis, bus-break-even-analysis

## The Operations Toolbox at a Glance

| # | Technique | Best for | Key signal |
|---|---|---|---|
| 1 | Seven wastes (muda) | Diagnosing operational drag | Productivity has plateaued despite effort |
| 2 | Just-in-time (JIT) | Reducing inventory and lead time | Warehouses full but stockouts still happen |
| 3 | Kanban | Pull-based production signaling | Upstream produces more than downstream consumes |
| 4 | Jidoka (autonomation) | Quality at the source | Defects detected late in the process |
| 5 | SMED (single-minute exchange) | High-variety, small-batch production | Changeovers dominate the schedule |
| 6 | 5 Whys | Root-cause analysis for recurring problems | Fixes repeatedly fail to hold |
| 7 | Value stream mapping | End-to-end flow diagnosis | Nobody sees the whole process |
| 8 | Theory of Constraints | Bottleneck-focused improvement | Local optimizations do not improve throughput |
| 9 | Standard work | Baseline for improvement | Variation prevents meaningful measurement |
| 10 | Mass production (Ford) | Extreme economies of scale on one product | Demand is uniform and predictable |

## Technique 1 — The Seven Wastes (Muda)

**Pattern:** Taiichi Ohno classified waste into seven categories, each a specific form of activity that consumes resources without producing value the customer pays for. Eliminating waste is cheaper than increasing throughput of waste.

**The seven wastes.**

| # | Waste | Example |
|---|---|---|
| 1 | Overproduction | Building parts before the next station needs them |
| 2 | Waiting | Workers or machines idle between steps |
| 3 | Transport | Moving work between stations without transforming it |
| 4 | Over-processing | Adding features or precision the customer does not value |
| 5 | Inventory | Buffer stock hiding production imbalance |
| 6 | Motion | Workers walking, reaching, searching |
| 7 | Defects | Rework, scrap, warranty returns |

**Ohno's emphasis.** Of the seven, overproduction is the most dangerous because it causes or hides the other six. Overproduction generates inventory, which requires transport, which creates motion and waiting, and allows defects to accumulate before detection. Eliminate overproduction and the other wastes become visible and attackable.

**Worked example.** An electronics assembly line produces 1000 units per shift. The downstream test station can only process 800 per shift. The 200-unit gap accumulates as WIP inventory, occupies floor space, hides defects (because problems are detected long after their cause), and creates overtime panic when test falls further behind. The lean fix is not "speed up test" but "slow down assembly to match test, then improve test until assembly can run full speed." Stopping overproduction is the first move.

## Technique 2 — Just-in-Time (JIT)

**Pattern:** Produce only what the next process needs, in the quantity it needs, at the time it needs it. Inventory is a liability because it ties up capital, occupies space, and obscures production problems by providing a buffer that masks variability.

**Historical basis.** Ohno developed JIT at Toyota starting in the 1950s, partly as a response to Japan's capital scarcity (inventory was unaffordable) and partly as a philosophical inversion of the American push-production model. By the 1980s JIT had become the default for global manufacturing, though imperfectly understood — many firms copied the inventory reduction without the accompanying discipline.

**Worked example.** A supplier delivers parts in hourly batches matched to the customer's production rate. The customer has no receiving dock, no warehouse, no forklifts for the incoming stream — parts are carried directly to the line. If the supplier is late by 30 minutes, the customer's line stops. That pressure forces both parties to solve the underlying variability rather than cover it with buffer.

**When NOT to use.** JIT requires reliable suppliers, stable demand, and geographic proximity. A firm pursuing JIT with unreliable suppliers or long supply chains will experience recurring stockouts. The 2020-2021 pandemic exposed firms that had adopted the inventory reduction without the reliability prerequisites.

## Technique 3 — Kanban

**Pattern:** A visual signal (card, bin, or electronic token) authorizes the upstream process to produce the quantity the downstream process just consumed. No kanban signal, no production. This implements JIT as a pull system rather than a push system.

**Worked example.** A paint shop consumes paint from a bin holding 5 gallons. When the bin is empty, it is sent upstream as a kanban card. The paint-mixing station mixes 5 gallons, attaches the card to the new bin, and returns it. No mixing happens without a returned bin. The number of bins in circulation (the kanban quantity) caps the maximum inventory.

**Critical discipline.** Kanban quantity must be tight enough to force improvement but loose enough not to starve the line. The standard practice is to start with a safe quantity, then progressively remove bins from circulation and see which problems surface. Each problem, once fixed, allows another bin to be removed.

## Technique 4 — Jidoka (Autonomation)

**Pattern:** Build quality into the process rather than inspecting it in afterward. Machines are equipped to stop automatically when a defect is detected; workers are empowered to stop the line (the *andon* cord) when they see a problem. Production does not restart until the cause is understood.

**Historical basis.** The word *jidoka* dates to Sakichi Toyoda's automatic loom (1902), which stopped on thread breakage. Ohno generalized it from weaving to all production. The philosophical point is that producing known defects at full speed is worse than stopping the line; every defect produced downstream of a detected problem adds to the cost of the fix.

**Worked example.** A torque wrench on an automotive line reports every fastening to a central system. When three consecutive fastenings fall below the spec, the line stops. The team convenes at the station, runs a 5 Whys investigation, and resumes only when the cause is identified and contained. A manager's instinct is "this is expensive, stop stopping the line." The lean response is "the line is only expensive because we have not finished solving the problems that make it stop."

## Technique 5 — SMED (Single-Minute Exchange of Die)

**Pattern:** Reduce the time to change a production line from one product to another, so that small-batch production becomes economically competitive with large-batch. The name "single-minute" means "under ten minutes" — changeovers that used to take hours.

**Historical basis.** Shigeo Shingo (working with Toyota) developed SMED in the 1950s-60s. The core insight is to separate changeover steps into "internal" (must happen while the machine is stopped) and "external" (can happen while the machine is running), then convert as many internal steps as possible to external, then streamline the remaining internal steps.

**Worked example.** A stamping press changeover takes 4 hours. Analysis reveals that 3 of those hours are internal but could be external (pre-heating dies, pre-positioning fixtures) and only 1 hour genuinely requires the press to be stopped. A kit-and-stage process moves 3 hours to external. Further refinement of the internal hour (quick-release clamps, color-coded alignment marks) reduces it to 15 minutes. The press's economic batch size drops by an order of magnitude, enabling JIT.

**Strategic consequence.** SMED is the technique that made flexible production economically competitive with mass production. Without SMED, Ford's model dominates because changeover cost forces large batches. With SMED, variety becomes cheap.

## Technique 6 — 5 Whys

**Pattern:** When a problem occurs, ask "why" five times, following the causal chain from symptom to root cause. Stop only when further "why" no longer produces new information or when the remaining cause is outside the problem's solvable scope.

**Worked example.** *The robot stopped.*

1. Why did the robot stop? The circuit overloaded and the fuse blew.
2. Why did the circuit overload? The bearing was dry and seized.
3. Why was the bearing dry? The lubrication pump was not circulating enough oil.
4. Why was it not circulating enough? The pump intake was clogged with shavings.
5. Why was the intake clogged? The filter is missing.

**Fix:** Add a filter. If the team had stopped at "the fuse blew," they would have replaced the fuse and experienced the same failure in a week. 5 Whys produces root-cause fixes that hold.

**When it stalls.** If the fifth "why" leads to "because that is how it has always been" or "because the supplier decided to do it that way," the root cause is policy, not physics. Policy can be changed but requires a different conversation.

## Technique 7 — Value Stream Mapping

**Pattern:** Draw the end-to-end flow of material and information from customer order to customer delivery, noting at each step the processing time, waiting time, inventory, and information flow. The map reveals where value is actually created and where time is spent not creating value.

**Typical finding.** In most non-lean operations, value-added time (time the customer would pay for) is under 5 percent of the total lead time. The other 95 percent is waiting, transport, inspection, rework, and queue. This fact is usually invisible until the value stream is mapped, because no individual actor sees the whole flow.

**Worked example.** An order-to-cash process has a 45-day lead time. The map reveals 16 hours of actual work spread across 45 days, with the rest being queue between departments. The fix is not to speed up the work (the work is already fast) but to reduce queue by reducing batch sizes and eliminating approval bottlenecks. Lead time drops to 4 days with no change in the 16 hours of work.

## Technique 8 — Theory of Constraints

**Pattern:** In any process, one step is the constraint — the step whose capacity determines total throughput. Improvements to non-constraint steps do not improve total throughput; they only increase inventory and waste. Improvements must be targeted at the constraint until a new constraint emerges.

**Historical basis.** Eliyahu Goldratt codified this in *The Goal* (1984). The principle is compatible with lean thinking but emphasizes throughput over waste elimination as the primary lever.

**Five focusing steps.**

1. Identify the constraint.
2. Exploit the constraint (use it fully — no idle time, no low-value work).
3. Subordinate everything else to the constraint (other steps run at the constraint's pace).
4. Elevate the constraint (invest to increase its capacity).
5. Repeat — the constraint will have moved.

**When to use.** When local optimizations have failed to improve total throughput. The theory of constraints explains why: optimizing a non-constraint is wasted effort.

## Technique 9 — Standard Work

**Pattern:** Define the current best-known way to perform each task, document it, and train to it. Standard work is not a permanent prescription but a baseline: improvements modify the standard; unauthorized variation obscures whether improvements work.

**Ohno's framing.** "Where there is no standard, there can be no *kaizen*." Improvement requires a baseline. A process that is done differently every time cannot be improved, only randomized.

**Worked example.** Three workers assemble the same component with three different motion sequences. Observed defect rates differ: 2 percent, 5 percent, 8 percent. Making the 2-percent worker's method the standard drops the other two to 2 percent within a week. The standard then becomes the baseline for the next round of improvement.

## Technique 10 — Mass Production (Ford)

**Pattern:** Standardize the product, standardize the process, drive the largest possible volume through the smallest possible variety. Achieved economies of scale that reduced the Model T's price from $850 (1908) to $260 (1925) while wages rose. The historical template for 20th-century industrial production.

**Mechanisms.**

- **Interchangeable parts** — parts precise enough to fit any unit without fitting
- **Moving assembly line** — work comes to the stationary worker, not the reverse
- **Vertical integration** — Ford owned rubber plantations, iron mines, steel mills, and ships
- **Labor specialization** — each worker performs one task at high repetition
- **Continuous flow** — no stops, no batching between stations

**Trade-offs.** Ford's approach delivered extreme cost advantage on one product. It failed when demand diversified. By 1927 GM offered "a car for every purse and purpose" while Ford still made the Model T in black; Ford had to retool the entire River Rouge plant to build the Model A, at enormous cost. Mass production is the right answer only when variety can be suppressed.

**Labor note.** Ford paid above-market wages (the $5 day, 1914) to reduce turnover on work that was brutally repetitive, but the production model depended on worker compliance and produced recurring labor conflict. The historical record includes both the genuine achievement and the costs paid by workers, and the lean successors (Toyota) explicitly designed around worker judgment rather than worker compliance.

## Mass Production vs Lean

| Dimension | Mass Production (Ford) | Lean Production (Toyota) |
|---|---|---|
| Optimization target | Volume on one variant | Flexible variety |
| Inventory | Large buffers | Minimal, pull-based |
| Worker role | Execute specified motion | Detect problems, improve standards |
| Changeover cost | High | Low (SMED) |
| Quality strategy | Inspect finished goods | Build quality in at source |
| Response to variability | Larger buffers | Eliminate the source |
| Best when | Demand is uniform and predictable | Demand is varied or uncertain |

## Decision Guidance

1. **Is the problem visible drag despite hard work?** Seven wastes diagnostic.
2. **Is inventory rising faster than sales?** JIT + kanban to cap it.
3. **Are defects surfacing late?** Jidoka — detect at the station that causes them.
4. **Is variety killing you on changeover?** SMED.
5. **Are fixes not holding?** 5 Whys until you reach a cause you can actually change.
6. **Is end-to-end lead time long but per-step work short?** Value stream map.
7. **Are local improvements not improving total throughput?** Theory of Constraints.
8. **Is work done differently every time?** Standard work.
9. **Is demand truly uniform and cost the only variable?** Consider mass production.

## References

- Ohno, T. (1988). *Toyota Production System: Beyond Large-Scale Production*. Productivity Press.
- Womack, J. P., Jones, D. T., & Roos, D. (1990). *The Machine That Changed the World*. Rawson Associates.
- Womack, J. P., & Jones, D. T. (1996). *Lean Thinking*. Simon & Schuster.
- Shingo, S. (1985). *A Revolution in Manufacturing: The SMED System*. Productivity Press.
- Goldratt, E. M. (1984). *The Goal: A Process of Ongoing Improvement*. North River Press.
- Ford, H. (1926). *Today and Tomorrow*. Doubleday.
- Liker, J. (2004). *The Toyota Way*. McGraw-Hill.
