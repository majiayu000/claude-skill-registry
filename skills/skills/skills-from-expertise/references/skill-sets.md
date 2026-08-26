# Architecture of a set

## The main criterion: a separate skill or part of a neighbour

> **A separate skill is needed if a request exists that should load this one rather than
> a neighbour.** With no such request, it is a section or a separate file of the neighbour,
> not a skill.

The same explains why sets fill up with skills that cannot stand alone: **the boundary was
drawn by the logic of the subject area rather than by the type of request.**

Subject logic says: "diagnosis, strategy, and production are parts of one domain."
The user's task says: "mine isn't working" is one request, "I need to plan the year"
is a completely different one. The second dictates the boundary.

**A badly drawn boundary breaks not the content but the selection:** the wrong skill fires,
and the user gets half the knowledge without suspecting it.

**Criteria for a separate skill, all three required:**

1. **The triggers do not overlap** with existing ones. Verified by comparing descriptions,
   not by eye.
2. **There is enough material for a standalone document.**
3. **The topic cannot be nested** inside an existing skill without distorting its boundaries.

**When adding a new skill, fix the neighbours immediately:** remove from their descriptions
the phrases that now belong to the new one, and add mutual "when this is the wrong place"
references.

## Three architectures for a set

| Architecture | When it works | The cost |
|---|---|---|
| **A flat set of independents** | Tools unrelated to each other | Impossible in a connected domain: the connections will appear anyway and stay unwritten |
| **Core and periphery** | A domain with shared mechanics and specific applications | The periphery does not work without the core and cannot be handed out separately |
| **A strict hierarchy** | Almost never | Fragile: changing one node breaks the whole branch under it |

**Core and periphery is what almost any connected set grows into**, regardless of intent.
A few skills turn out to be foundational: everything refers to them and they refer to almost
nothing. The rest apply the foundational mechanics to specific cases.

**How to tell what you have ended up with:** count the references. Many incoming and few
outgoing means a core. The reverse means periphery, or a router. Few of either means the skill
is isolated and can be handed out on its own.

**A separate note on routers.** A skill that decides nothing itself and only determines where
to go is a legitimate and useful type. Its sign: many outgoing references at small size.
**There should not be two routers in one set**, since they compete for the same requests;
if there are two, one of them has actually become a full skill and its description needs
narrowing.

## A reference has to name the content, not the name

**The cheapest change that makes a set usable when handed out in parts.**

| Breaks without the neighbour | Works alone as well |
|---|---|
| "Layer-by-layer analysis, see the neighbouring skill" | "Layer-by-layer analysis: start at the top, then each one below until you find the first broken layer. More in the neighbouring skill" |

A user who downloaded one skill gets the substance even without the neighbouring file. A user
with the whole set gets both the substance and the pointer.

**The rule:** every reference carries one line about what is there, not only about where to go.

## How to hand them out

| Method | Requirement | When to choose it |
|---|---|---|
| **One at a time** | Every skill is self-sufficient, references name content | A set of loosely connected tools |
| **As a bundle** | Internal coherence, a shared entry point | A connected domain where the periphery is meaningless without the core |
| **Core separately, add-ons separately** | The core is self-sufficient, the add-ons declare their dependency | A large set where everyone uses the core and only some use the periphery |

**What to account for when handing out a bundle:** the metadata of every skill loads at start.
Thirty descriptions occupy context regardless of whether they are needed today. That is
the price of coherence and it is real: a set of thirty skills should not consist of thirty
two-hundred-line skills if half of them can be merged.

**Different layers are handed out separately.** Skills about a subject area and skills about
how to work with skills themselves are different packs: they have different audiences and zero
shared references.

## Fewer skills, more structure inside

**Choosing between "add a neighbouring skill" and "add a section", default to the section.**

The reasons:
- **fewer references**, and every reference is a place where the connection can break;
- **more context**, since the model sees adjacent material at once rather than through
  a pointer;
- **the skill stays complete**, so it can be used without wondering what else to install;
- **cheaper metadata**, one description instead of two.

**Add a separate skill only when the main criterion above is clearly met.** Doubt resolves
in favour of the section.

---

# Updating an existing method

A separate operation, matching neither creation nor simple addition. It comes up when a skill
on the topic already exists and new material has arrived.

**The first question: does the new material add, refine, or refute?**

| What happened | What to do |
|---|---|
| **Adds**: a new case, a new tool, one more branch | Write it in. Check that it does not break the existing order |
| **Refines**: the old rule turned out to be a special case | Rewrite the rule more broadly, keeping the old one as a special case with its condition |
| **Refutes**: the new contradicts what is written | **Don't overwrite.** Handle it as a contradiction: both versions, the frames, the rule for choosing |
| **Duplicates**: the same thing in different words | Do nothing. Check that what is already recorded is the fuller version |

**The most common error in updating is silently replacing the old with the new.** A month
later nobody, including you, will remember that a different claim was there and why it was
dropped. The next time the same source is worked through it will come back, and the work will
repeat.

**Check for a duplicate before writing.** Search by meaning rather than by string: the same
method may be recorded under a different name. A match in topic without a match in wording
is entirely normal.

**If new material showed the method was wrong**, don't delete it, mark it: what was believed
before, what turned out to be the case, and what the new version rests on. The history
of an error is more useful than its absence, because it prevents a repeat round.

---
