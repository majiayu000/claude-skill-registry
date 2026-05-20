---
name: craft-methodology
description: Craft methodology for the trades — how skilled work is organized, decomposed, sequenced, and evaluated from first principles through finished artifact. Covers the craft arc (intent, layout, roughing, fitting, finishing, inspection), the distinction between process knowledge and product knowledge, and how craft traditions encode error-correction in their sequencing. Use when designing a new trade process, diagnosing a faltering one, or teaching craft structure to a learner.
type: skill
category: trades
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/trades/craft-methodology/SKILL.md
superseded_by: null
---
# Craft Methodology

Craft is not a residual category of "work that isn't knowledge work." It is its own discipline with its own epistemology — a body of knowledge that lives in hand, eye, and workshop practice as well as in drawings and specifications. This skill catalogs the structural moves that skilled craft practitioners use to take a problem from intent to finished object, and the reasons those moves survive across centuries and trades.

**Agent affinity:** vitruvius (triad of firmness, commodity, delight), crawford (philosophy of manual competence), rose (trades pedagogy)

**Concept IDs:** trades-craft-arc, trades-process-knowledge, trades-error-correction

## The Craft Arc

Every tradition of hand-and-machine work — whether carpentry, masonry, machining, smithing, instrument making, plumbing, tailoring, or electronic prototyping — shares a common arc. The names differ, but the structural moves do not.

| Stage | Purpose | Error cost if skipped | Typical artifacts |
|---|---|---|---|
| 1. Intent | What is being made and why | Rework of everything downstream | Brief, sketch, conversation with client |
| 2. Layout | Translate intent into spatial and dimensional plan | Misfit, wasted stock | Drawing, story pole, full-size plan, template |
| 3. Roughing | Remove bulk material or establish rough form | Tool damage, over-commit to wrong shape | Rough stock, first-pass cuts, blanks |
| 4. Fitting | Bring parts into correct relationship | Final assembly fails | Trial fits, scribe marks, shim experiments |
| 5. Finishing | Bring surfaces to their final condition | Appearance, function, durability loss | Surfaces, edges, coatings, final tolerances |
| 6. Inspection | Verify the work matches the intent | Undetected defects reach the user | Checklist, measurement, client sign-off |

The arc is recursive. Inside "fitting" there is a miniature version of the same arc — intent for the fit, layout of where it goes, rough shaping, trial fitting, final dressing, check. This recursion is part of why craft is hard to teach: the macro arc is visible, the nested micro arcs are not.

## Process Knowledge vs Product Knowledge

A large share of what an experienced tradesperson knows is about the process, not the product. This distinction matters because the two kinds of knowledge are acquired differently and decay differently.

**Product knowledge** is about the finished thing. "A half-blind dovetail has pins that do not show on one face." "A #12 AWG copper conductor is rated for 20 amps in residential circuits." "Portland cement hydrates for 28 days to reach design strength." Product knowledge can be written down, tested, and transmitted through documents. It is what trade-school textbooks contain.

**Process knowledge** is about how to get there. "When the saw starts to drift, ease the pressure and let it track itself before correcting." "If the concrete sets faster than expected, a cooler bucket of gauging water buys you time." "When fitting a dovetail, shave the pins from the inside face because the outside face has to stay square." Process knowledge is hard to write down, harder to transmit through documents alone, and decays when a tradition stops being practiced.

The two interact. Product knowledge tells you what the target is. Process knowledge tells you how to approach the target without destroying the workpiece along the way. A textbook describing "correct dovetail proportions" without process knowledge will produce frustrated learners whose dovetails are correctly proportioned and unacceptably ugly.

## Error-Correction as a Design Property

Craft traditions encode error-correction in their sequencing. The traditional order of operations is not arbitrary — it is the order that allows mistakes to be caught when they are still cheap to fix.

### Rough before fine

Rough operations are done before fine operations because a surface that needs to be rough-cut is also a surface that will have small errors. Fine-finishing a surface before rough-cutting it means those errors propagate into the finish and then have to be redone. Rough work protects fine work.

### Reference surfaces before dependent surfaces

A reference surface is one that all other measurements are made from. It has to be established first because every subsequent measurement will inherit its accuracy. Establish a jointed edge on a board before crosscutting to length. Plaster a wall before setting a door jamb against it. Flatten a mill table before using it to measure anything else.

### Parts that are hard to make come before parts that are easy to make

If a project includes one piece whose success is uncertain — an unusual joint, a marginal bend radius, a workpiece already at the limit of the available stock — that piece is made first. If it fails, the rest of the work has not been invested yet. This is a risk-asymmetry move: the expected cost of going hard-first is lower than going easy-first because a failed hard piece at the end costs everything, while a failed hard piece at the start costs only itself.

### Test fit before commit

Any operation that is expensive or irreversible is preceded by a test fit or trial run. Dry-assemble before glue. Tack-weld before seam-weld. Set out with chalk before saw cut. The cost of the test fit is tiny compared to the cost of undoing an irreversible commitment.

## Intent — What the Work Is For

The first stage of craft is not drawing or measurement. It is understanding what the finished thing is for and for whom. A piece of trim that will be seen from above must have its visible surface oriented upward. A gate that must swing over rough ground needs clearance that a gate over smooth ground does not. A chair sized for a child is not a smaller chair sized for an adult; the proportions change because the human does.

Vitruvius names this stage in the triad firmitas, utilitas, venustas — firmness, commodity, delight. Utilitas, the middle term, asks whether the object serves its human purpose. Without utilitas, a structurally sound and beautiful object is still a failure. Modern craft pedagogy (Rose, Crawford) preserves this framing under different names: "the work has to know its user."

### Intent failures

- **Making the wrong thing.** The brief was misread or the client did not know what they wanted. Often revealed at delivery, sometimes at layout.
- **Making the thing at the wrong time.** The craft is correct but arrives after the need has shifted.
- **Making the thing at the wrong scale.** The proportions are right but the overall size is wrong for the user or the space.
- **Making the thing with the wrong tradeoffs.** A cabinet built for maximum durability when the client wanted maximum beauty, or vice versa.

Intent-failure costs scale with how late they are caught. Caught at intent: conversation. Caught at layout: a redrawn plan. Caught at roughing: lost stock and hours. Caught at inspection: lost project. This is why Vitruvius, Rose, and Crawford all begin their teaching with questions about purpose before they introduce tools.

## Layout — Translating Intent to Space

Layout is the translation of intent into a spatial plan that the craft operations can execute. Layout is where craft becomes measurable, where the dimensions that had been implicit become explicit, and where the first opportunity to catch a mistake arrives.

### Layout techniques by trade

- **Carpentry:** story poles, full-size drawings, setting-out chalk lines, framing squares against the stock
- **Masonry:** string lines, story poles marked with course heights, mortar-joint gauges
- **Machining:** layout dye (Prussian blue, layout fluid) with scribed lines, center-punched origin marks
- **Plumbing:** rough-in drawings, chalk marks on subfloor, dry-fit assemblies
- **Electrical:** panel schedules, one-line diagrams, marking boxes on studs
- **Tailoring:** pattern pieces, chalk marks on cloth, basting stitches as provisional layout

All of these are the same move with different media. The common element is that layout creates a cheap, editable representation of the finished work before the irreversible operations begin. Layout is the craft equivalent of a low-fidelity prototype.

### Story poles and their cousins

A story pole is a stick marked with every critical dimension of a job. Carpenters use them for cabinet runs; masons use them for course heights; timber framers use them for tenon locations. The story pole replaces the tape measure as the authoritative source during the work, because a tape measure reads differently depending on how it is held, while a stick with marks on it is unambiguous.

The deeper principle is that a single physical artifact that encodes all the critical dimensions of a job is less error-prone than repeated measurements from a common reference. This is true in any trade. Machinists call it a master gauge; tailors call it a sloper. Whenever the same dimension is going to be used many times, put it on a physical artifact once.

## Roughing, Fitting, Finishing

The three middle stages all remove material, but their economics are different.

**Roughing** removes the most material in the least time. The tolerance is loose, the tool is robust, and the goal is to get close to final shape without damaging anything that will become a reference surface later. A rough cut that removes ten times the material of a finish cut in one-tenth the time is a win even if the surface is terrible, as long as the surface is going to be removed in a later operation.

**Fitting** is the slowest, most deliberate stage. This is where the parts meet each other, where tolerances start mattering, and where experience shows. Fitting is iterative: place, check, mark, remove, replace, check, mark, remove. A fitting operation that is right on the first try is either extraordinary skill or extraordinary luck; most fitting is negotiated.

**Finishing** brings surfaces to their final condition. The operations are fine, the tools are often hand tools (even in machine trades), and the goal is to remove the marks left by earlier operations without introducing new marks or changing dimensions. Finishing is the stage where craft is most visible to users who do not know trades — the surface quality is what they see.

### The economics of sequencing

Each stage has a distinct labor-intensity profile. Roughing is fast and cheap per unit volume. Fitting is slow and expensive. Finishing is variable — sometimes fast (a sprayed finish) and sometimes slow (hand-scraped surfaces). Skilled tradespeople allocate their attention to the stages where error is most costly to fix, which is usually fitting. A project that goes over time usually overflows in the fitting stage, and the remedy is to slow down further in fitting rather than to speed up.

## Inspection

Inspection is the final stage and the one most often shortchanged under time pressure. It is also the stage that determines whether the work is known to be good or merely hoped to be good.

### What good inspection looks like

Good inspection has three properties. First, it uses the intent as its criterion, not a generic checklist. The question is "does this serve the purpose it was made for," not "does this match a list of items that are usually checked." Second, it treats defects as information rather than as failures — a defect found in inspection is a defect not delivered to a user, which is a success of the inspection process. Third, it has a defined stopping rule. Inspection is not infinite; there is a point at which the work is declared finished and released. The stopping rule is part of the craft discipline.

### Inspection by the maker vs by someone else

Both have value. A maker's self-inspection catches errors the maker already has the vocabulary to see — dimensions, joints, finishes. A second pair of eyes catches errors the maker cannot see because they are too close to the work — orientation mistakes, proportion errors, things that "look wrong" without a specific defect being identifiable. Serious craft traditions use both.

## Craft Traditions as Error-Corrected Knowledge

A final observation. Craft traditions are distilled error-correction. When a tradition insists on an apparently arbitrary practice — "always cut dovetails from the tails first" or "always plumb before you square" — that practice is almost always the residue of many generations of people who did it the other way and discovered, the hard way, why the tradition exists. Deviating from tradition is not forbidden, but the cost of deviation is discovering, yourself, what the tradition already knew. That discovery is expensive.

This is why Crawford and Rose both argue that craft pedagogy has to include respect for tradition even when the tradition is not yet understood. Understanding follows practice; practice cannot wait for full understanding without becoming paralysed.

## References

- Vitruvius, *De Architectura* (c. 15 BCE), Book I — the firmitas/utilitas/venustas triad
- Mike Rose, *The Mind at Work* (2004) — craft cognition and the hidden complexity of trade work
- Matthew Crawford, *Shop Class as Soulcraft* (2009) — philosophy of manual competence
- Peter Korn, *Why We Make Things and Why It Matters* (2013) — craft intent and meaning
