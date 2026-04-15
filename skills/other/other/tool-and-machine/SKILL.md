---
name: tool-and-machine
description: Tools and machines as the leverage-amplification layer of the trades — how hand tools, powered tools, and programmable machines differ in what they amplify, what they constrain, and what skill they demand. Covers the tool-to-machine progression, the Nasmyth steam-hammer lineage of precision power, the block-making machinery at Portsmouth as the first mass-production machine shop, and the modern CNC/robotics layer. Use when selecting tools for a job, justifying a tool purchase, or teaching a learner why tools are organized the way they are.
type: skill
category: trades
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/trades/tool-and-machine/SKILL.md
superseded_by: null
---
# Tools and Machines

A tool extends the body. A machine replaces a portion of the body with a controlled mechanism. This is not a merely semantic distinction — the shift from tool to machine is the shift from human judgment at every step to human judgment only at the setup, and it has deep consequences for what the operator needs to know, what errors are possible, and what kinds of work are economically viable. This skill maps the tool-to-machine progression across trades, the historical lineage from hand tools to programmable machines, and the criteria for choosing the right layer for a given job.

**Agent affinity:** nasmyth (precision power, machine-shop foundation), brunel-tr (block-making machinery, first mass-production shop), edison (workshop invention tools)

**Concept IDs:** trades-tool-progression, trades-precision-power, trades-machine-setup

## The Tool–Machine Spectrum

Think of a five-layer progression:

| Layer | Example | Human contribution | Replaced by next layer |
|---|---|---|---|
| 1. Hand tool | chisel, file, handsaw | every motion, every direction, every force | repeated motions |
| 2. Powered hand tool | circular saw, drill, angle grinder | direction and force; motor handles speed | guided direction |
| 3. Stationary powered tool | table saw, drill press, milling machine | position of workpiece, feed rate | clamping and feeding |
| 4. NC/CNC machine | CNC mill, CNC lathe, waterjet | the program, the setup | program generation |
| 5. Programmed/robotic | robotic cell, 3D printer, automated line | cell design, maintenance | — |

Each layer is a different tradeoff between human judgment and machine consistency. Hand tools give the maximum flexibility and the maximum demand on skill. Programmed machines give the minimum flexibility (for any given setup) and the maximum consistency. The layers coexist in almost every serious shop because different jobs belong to different layers.

### The Nasmyth precision lesson

James Nasmyth's 1839 steam hammer was a breakthrough in precision power. Before the steam hammer, a blacksmith could strike a hot workpiece with whatever force a human arm could deliver — maybe thirty pounds of hammer, maybe fifty on a big forge. Nasmyth's hammer could deliver tons of force, but crucially it could also be controlled to stop an inch above the anvil or to lightly crack a walnut shell. Power without control is useless; control without power is limited. The steam hammer solved both at once, and it became the archetype for "precision power" — the idea that a machine's value is not in its maximum force but in the range of force it can deliver on demand.

The same principle applies all the way up the stack. A CNC mill is valuable because it can move a cutter across ten feet of travel with one-thousandth-of-an-inch repeatability. A plasma cutter is valuable because it can pierce inch-thick steel and also trace a curve as delicate as a pencil line. The tool's range is the figure of merit, not its maximum.

## The Block-Making Machines at Portsmouth

Between 1802 and 1805, Marc Brunel and Henry Maudslay designed and built a set of 45 machines for the Portsmouth Block Mills that collectively produced ship's pulley blocks faster and more consistently than any hand-operated shop of the era. This was the first fully mechanized mass-production line in the world, and every principle that later mass-production shops used was visible in it:

- **Dedicated single-purpose machines.** Each of the 45 machines did one step of the block-making process. The workpiece moved between machines in sequence. Setup cost was paid once per machine per shift, not once per block.
- **Interchangeable parts.** The blocks were made to specification so that any pulley block of a given size could replace any other. This was revolutionary for its time — hand-made blocks had to be matched to their specific pulley wheel.
- **Deskilled operation, skilled design.** Each machine could be operated by an unskilled worker after a short training, but the design of each machine required the top craftsman-engineers of the era.
- **Capital for labor.** Ten unskilled workers on the Brunel machines replaced 110 skilled craftsmen. This was the economic breakthrough that made industrial production viable.

The Portsmouth machines are the Rosetta Stone for understanding the tool-to-machine transition. Every subsequent automation wave — Ford's assembly line, Taylor's time-study, modern CNC, robotic welding — is a continuation of the pattern that Brunel and Maudslay established. Understanding Portsmouth is understanding how industrial production came to be possible at all.

### The Portsmouth tradeoff

Portsmouth also made visible the tradeoff that has accompanied every mechanization wave since: skill moves from the operator to the designer of the machine. The worker on a Portsmouth machine knew less than the craftsman they replaced. The engineer who designed the Portsmouth machine knew more — because designing a machine requires understanding the operation well enough to reduce it to a single repeatable mechanism. This redistribution of skill is the central fact that makes industrial mechanization economically and politically consequential.

## Hand Tools — Layer 1

Hand tools are the most flexible layer. A single chisel can do rough bulk removal, fine paring, mortise cutting, and scraping, depending entirely on how it is held and struck. A single file can shape metal to any contour within its reach. A handsaw can cut any straight or curved line the user can guide.

### What hand tools demand

Hand tools demand skill in proportion to the flexibility they offer. A beginner with a chisel produces work that is measurably worse than a beginner with a hand-router jig that mechanically constrains the same operation. The skill is the investment that replaces the constraint. This is why traditional trades pedagogy begins with hand tools — the learner has to develop the judgment that mechanized tools hide, and hand tools expose every gap in that judgment immediately.

### When hand tools are still the right choice

Despite the availability of power tools, hand tools remain the right choice for:

- **Final fitting and finishing.** Power tools remove material in quantities that exceed the final fitting tolerance. A hand plane takes off a half-thousandth per pass; a power planer takes off twenty thousandths minimum.
- **One-off work where setup would dominate cycle time.** Setting up a machine for a single cut may take longer than doing the cut by hand.
- **Work in awkward positions or locations.** Tools have to fit the space; power tools are often larger and less maneuverable.
- **Quiet work.** Hand tools are silent. In restoration work, in occupied buildings, and in contexts where noise is socially costly, hand tools are not a nostalgia choice but a requirement.
- **Work where the feel of the material is part of the craft.** A hand plane lets the user feel wood grain changing under the blade. A power planer does not. Some crafts depend on this feedback loop.

## Powered Hand Tools — Layer 2

Powered hand tools give up a small amount of flexibility for a large amount of speed. A circular saw cuts a straight line faster than a hand saw but only cuts straight lines. A drill drills a hole faster than a brace but cannot be used as a lever the way a brace can. A power plane removes material faster than a hand plane but cannot take off the half-thousandth that final fitting demands.

The rule is that powered hand tools are for roughing and bulk work, not for fitting and finishing, unless the tool is specifically designed for the finishing operation. A random-orbit sander is a finishing tool; a belt sander is not.

## Stationary Machines — Layer 3

Stationary machines invert the relationship: the workpiece moves through the tool rather than the tool moving over the workpiece. This inversion gives much greater precision because the tool's position relative to the shop is fixed and can be measured, while the workpiece can be held against reference surfaces that the machine provides.

### Setup as the unit of cost

A stationary machine's cost is dominated by setup time, not cycle time. Setting up a drill press for a specific hole pattern takes minutes; drilling the hole takes seconds. This cost structure means stationary machines favor repetition — ten identical holes cost almost the same as one hole because the setup is paid once. A shop's use of stationary machines is a direct indicator of whether its work is repetitive enough to justify them.

## CNC and Programmable Machines — Layer 4

CNC shifts the skill from setup to programming. A competent CNC machinist is a programmer who also happens to know metalworking. The program is the artifact that represents the operator's judgment; the machine executes it without interpretation. This is power at industrial scale, but it also means the programmer's errors are executed faithfully — a program that cuts too deep will cut too deep every time, with perfect consistency.

### What CNC is good at

- Repetitive work with tight tolerances
- Complex geometries that hand-guided tools cannot execute
- Jobs where consistency matters more than individual judgment
- Integration into automated production

### What CNC is bad at

- One-off work where programming cost dominates
- Work that requires in-process judgment (material that varies, unexpected grain, debris)
- Small shops where the capital cost cannot be amortized
- Work where the human skill is the point (fine handmade furniture, restoration, repair)

## Tool Selection Heuristics

For a given job, the right tool is the simplest tool that will do the job to the required tolerance. "Simplest" here means lowest on the layer stack that still achieves the tolerance, because lower layers require more skill but give more flexibility and lower capital cost. Specifically:

1. **If the tolerance can be hit by hand, use a hand tool.** This is almost always cheaper per piece for small quantities.
2. **If hand tools will be slower than a powered tool, and speed matters, move up one layer.**
3. **Move up only when the tolerance, speed, or volume makes the current layer impractical.**
4. **Do not skip layers for jobs that do not need them.** A CNC mill used for a job that a drill press would handle is expensive theater.
5. **Do not stop at a layer that cannot hit the tolerance.** A drill press used for a job that needs a mill produces unacceptable work regardless of how much time is spent.

Skilled tradespeople have this heuristic automatically. Apprentices learn it by watching.

## Maintenance and the Tool as Asset

Every tool in the shop is a depreciating asset. Maintenance slows the depreciation. Neglect accelerates it. A shop that treats tools as consumables ends up buying tools constantly. A shop that treats tools as investments gets decades out of them. The difference in cost over a career is enormous.

The maintenance discipline belongs to the workshop-practice skill, but the tool selection discipline belongs here: choosing a tool that the shop can actually maintain is part of choosing a tool. A tool that requires specialist maintenance not available locally is a tool that will fail early in the shop's life. This is why traditional trades favor tools that are field-serviceable over tools that are more powerful but more fragile.

## References

- James Nasmyth, *Autobiography* (1883) — the steam hammer and precision power
- Carolyn Cooper, *Shaping Invention* (1991) — Portsmouth Block Mills as mass-production archetype
- K. R. Gilbert, *The Portsmouth Block-Making Machinery* (1965) — engineering details
- David Pye, *The Nature and Art of Workmanship* (1968) — workmanship of risk vs certainty
