---
name: skills-from-expertise
description: Turns expertise from talks, books and interviews into a method an agent
  can follow, extracting decisions and criteria instead of merely restating the source
  material.
license: MIT
metadata:
  version: 6.1.0
---
# Designing a methodology

## What this is and what is not here

**The official specification answers "how to shape it".** Frontmatter, file length, progressive
disclosure, description, testing, scripts: all of that lives there and does not need repeating.

**Here is the question "what to put inside".** It is harder, and covered almost nowhere.
A model knows the format natively. What it does not know is what separates a method from
a collection of useful notes.

**The check for why this matters at all.** A skill written perfectly to format is useless
if there is no deciding procedure inside. It will load correctly, organise knowledge neatly,
and change not a single action.

## How to use this

**What not to do:**

- Don't turn assembly into a questionnaire. Most of this file covers hard cases, not
  a mandatory procedure.
- Don't start assembling before the digest is written.
- Don't argue with the author of the source inside the skill. A limitation is recorded
  as a condition of use, not as a rebuttal.
- Don't pass a guess off as an inference, especially when it is shaped as a prohibition
  or as a number.
- Don't publish material from someone else's source without going through the legal framing.

**Order:** digest, then four extraction steps, then mandatory parts, then four checks, then
the format line. In full, see "Order of work" at the end of the file.

**What to ask when data is missing:** the purpose of the result, meaning publication, private
use, or commercial distribution. That is the only thing that does not follow from the request
itself, and both the license and the strictness of the legal framing depend on it. Everything
else is determined from the material. Whose source it is shows in what was sent; whether
a skill is needed at all is covered in "When a skill is not needed".

**When this is the wrong place:** you need format, field limits, and file mechanics, which
belong to the Agent Skills specification; or you need to write the subject text itself rather
than the method underneath it.

---

# What counts as done

**The result of a build is not one file but three things. A skill without the first
and the third does not count as done.**

1. **The digest file**, a separate `.md`, written before assembly of the skill begins.
   What goes into chat is a link to it plus two short sections: **what was said in passing**
   and **what was left out**.
2. **The skill file.**
3. **The format line in the report**, with counted values rather than checkmarks.

⚠️ **This is the composition of the result, not the stages of a procedure, and that difference
decides everything.** A stage can be skipped unnoticed, because it exists only in your memory
of an instruction you read. An incomplete result is visible at the moment of delivery.

⚠️ **The digest is delivered before assembly, not together with the finished skill.** At that
moment the user can still say "the important part here is something else", and that costs far
less than rewriting an assembled file.

**This is the only place where stopping is justified**, and it does not contradict the rule
"don't ask permission to continue" below. The difference is in price. An ordinary question
costs a turn and saves nothing; a remark about the digest cancels an entire wrong assembly.
Having delivered the digest, wait for an answer. In everything else work without stopping.

**Why exactly those two sections go into chat.** A full retelling in chat costs tokens and
time, and nobody is going to reread it. The user can object at exactly two points: where you
judged something secondary, and where you dropped it. The rest they will check in the file
if they want to.

Details: how the digest is built is covered in the "Cross-check against the source" check,
and what goes into the format line is at the end of the file.

# The fast path

**Don't turn building a skill into a questionnaire.** Most of this file covers hard cases,
not a mandatory procedure.

**If everything is clear from the request, work straight away.** Own material, a skill
for yourself, a simple subject: take the four steps from "How to extract a method", run
the four mandatory checks, and deliver.

| Always | Only when the situation calls for it |
|---|---|
| Digest file, four extraction steps, format line | The opening fork, when the source and purpose are not obvious |
| The checks "decision criterion", "presence of refusals", "strip the borrowings", "cross-check against the source" | The other four checks, on large or contested material |
| A "Boundaries" section in the result | Legal framing, only with someone else's source |
| | Judgement domains, boundaries between skills, when the task calls for it |

**The proportionality rule:** the size of the procedure matches the size of the material.
A hundred-line skill from a single conversation does not require what a set of thirty sources
requires.

⚠️ **Proportionality concerns the size of the parts, not whether they exist.** On small
material the digest is short, not absent, and the format line is equally short at any size.
The three-part composition of the result does not shrink. What shrinks is what is inside them.

## How to run the conversation

**Ask questions in a batch, not one at a time.** Five questions in one message cost the user
less than five messages with one question each. Number them so they can be answered as a list.

**Don't ask what you can decide yourself.** If a sensible option is obvious, take it and say
so out loud: "I'm taking this option, tell me if that's wrong." A question belongs where
different answers produce different results.

**Don't ask permission to continue.** Ask only when a choice is needed that you cannot make
for the user. The only planned stop is after delivering the digest, see "What counts as done".

**Work while work is possible.** If part of the material is unclear and part is understood,
assemble what is understood and put the question about the unclear part at the end, rather
than instead of the work.

## What to show at the end

Having handed over the file, say briefly:

- **what came out**, meaning which forks and rules were extracted;
- **where you had to fill gaps**, meaning what was inferred rather than taken from the source;
- **what remained uncovered**, meaning areas where the method did not reconstruct;
- **what was dropped deliberately**, with a reason for each item. Everything from the
  "said in passing" section that did not make it into the skill belongs here;
- **what the user decides**: publication, license, contact with the author of the source;
- **the format line**, with counted values.

**Don't retell the contents in sequence**, but **do show the structure**. The user has
the file. What they cannot do is see it whole in a terminal, because several hundred lines
do not read by scrolling. A map of sections with one line about each solves that in ten lines.

## When you are editing an existing file

⚠️ **A separate requirement, and it is broken almost every time.** During an edit the user
does not see the result. They see only your report, and a report saying "did such and such"
without showing it means there is nothing to check and nothing to object to.

**Show with every edit:**

| What | Why |
|---|---|
| **What you deleted, verbatim or as a list** | A deletion is invisible in a report and unrecoverable in the user's memory |
| **Where what you deleted went** | Otherwise it looks like a loss |
| **The wording you added**, if it carries a rule | The user must be able to argue with the wording, not just with the fact of the edit |
| **What prompted the edit** | Your own observation, their remark, a failed check |

**The rule about deletions:** always show cuts explicitly; additions may be summarised.
The user will see what was added while reading. What was deleted they will never see.

**If there are many edits**, collect them into a table: version, what was done, what prompted
it. A list of fifteen paragraphs does not get read. A fifteen-row table does.

**What not to do:** don't announce a substantive decision as a result ("removed duplicates")
without listing what exactly you judged to be a duplicate. A duplicate is a judgement,
and it can be wrong.

### After an edit, check what else it touched

⚠️ **An edit in one place leaves traces in others, and the file starts contradicting itself.**
This is the main way a file degrades during long refinement: each individual edit is correct,
but together they diverge. And they diverge silently. There is no error, there are two
instructions, and the one encountered first is the one carried out.

**What to check after every substantive edit:**

| Trace | What to look for |
|---|---|
| **Numbers** | "three mandatory checks", "five steps", "six rules": every mention of the quantity of what you changed |
| **Duplicated rules** | The same instruction phrased in another section in different words. Search by meaning, not by string |
| **Summaries and tables** | Fast paths, checklists, contents. They are written once and never reread |
| **References to sections** | "see the section on…", where the section may have been renamed or absorbed |
| **Terms** | If you renamed a concept, the old name survives wherever it is mentioned in passing |

⚠️ **Summaries diverge first.** A rule gets changed in its own section, because that is where
it is being thought about. The line about the same rule in the "always do this" table sits
elsewhere and survives the edit untouched.

**One check after all edits:** take what you changed and find every place in the file where
it is mentioned. By search, not from memory.

---

# The opening fork

**Ask only if it does not follow from the request.** "Make a skill from my experience" means
the source is the user's own and no question is needed. "Break down this video" means
the source is someone else's, and the licensing question is asked only when publishing.

Clarify before assembly:

- **the origin of the material:** the user's own expertise, someone else's public material,
  or mixed;
- **the purpose:** publication for the community, private use, or commercial distribution.

The answers determine the working mode.

| Source | Mode |
|---|---|
| Own | The "Legal framing" section does not apply. Work freely |
| Someone else's, public | Full mode: extraction, testing, and quoting rules |
| Mixed | Full mode, applied to the borrowed parts |

| Purpose | License |
|---|---|
| Publication for the community | MIT or CC BY 4.0. With no license, "all rights reserved" applies and the file cannot be used |
| Commercial distribution | **Don't apply a license by default.** Clarify the distribution model |
| Private use | No license needed |

**Don't apply an open license before establishing the purpose.** It is irreversible for copies
that have already spread.

## The source's license overrides that table

Check **before** choosing a license for the result: what license the source itself carries.
It can remove your choice entirely.

| Source license | What it means |
|---|---|
| **CC BY-SA** | A derivative **must** carry the same license. MIT is not available |
| **CC BY-NC** | Commercial distribution is forbidden. The "commercial" row above drops out |
| **CC BY-ND** | Derivatives are forbidden outright. Extracting the method is fine, distributing a reworking is not |
| **CC BY / MIT / Apache** | Free, with attribution |
| **No license** | "All rights reserved". The method may be extracted, the text may not |

**With several sources, check compatibility.** Material under CC BY-SA and material under
a proprietary license do not combine in one file: the first requires opening the result,
the second forbids it.

**If the source's license is unknown**, treat it as absent and work in "all rights reserved"
mode.

⚠️ **A separate note about videos and talks.** Public availability is not an open license.
A video posted publicly is "all rights reserved" by default: the method may be extracted,
the text may not be carried over.

With a commercial purpose and someone else's sources, say so plainly: the extraction rules
are mandatory, and the share of your own expression has to be the decisive one.

**If the origin cannot be established**, work in full mode. When there are clear signs
of someone else's text (address to an audience, the author's own metaphors, traces of speech),
tell the user and clarify the source before including it in the file.

---

# When a skill is not needed, and what to do instead

⚠️ **This is a fork, not a reason to refuse the work.** Material is almost always good
for something. The question is the form, not whether to do it at all. Hedging with "it all
depends here" instead of working is worse than an imperfect method.

## There is only one case where a method genuinely does not exist

**The decision is made by taste**, and the people who hold the expertise disagree with each
other systematically on the same inputs. Not "sometimes differently" but systematically: two
strong specialists look at the same thing, arrive at opposite answers, and both are right.

Then there is no procedure and nothing to build one from.

**Everything else is not "there is no method" but "the method has not been found", and those
are different conclusions with different actions.**

## The method exists, but not in the author's explanations

Two signs that are easy to mistake for the absence of a method. **Both mean you should dig
further rather than stop.**

**The result is not reproducible**, meaning the same process by the same person gives
a different outcome. This is not the absence of a method but **a hidden variable you have not
found**. Look for what differed in the circumstances: a different client, a different deadline,
a different stage. The difference you find is the missing criterion.

**Success is explained only in hindsight**, meaning the explanations appear after the result
and do not predict the next one. That means **the author's explanations are useless, not that
the procedure is absent**. Stop taking their explanations and watch their actions instead: what
they do the same way every time, and what they change.

**A rule covering both:** an observation about repeatability is a pattern, not a method.
**A pattern becomes a method once the conditions are found** under which it holds. Until
the conditions are found, record it as a pattern with a note, but do not throw it away.

## The method covers only some of the decisions

The most common case of all. The procedure reconstructs for some forks and not for others.

Describe it where it exists, and **mark the zone where it does not**: "here the decision
is made from experience, there is no reproducible criterion". Mixing the two is not allowed,
because an unmarked zone of intuition reads as a procedure.

---

## What to make instead of a skill

A skill is not the only form. Most often the material fits one of these.

| What you ended up with | Form | Why that one |
|---|---|---|
| **One or two rules that must always hold** | Project instructions | They load permanently rather than on a trigger. A skill does not fit: it will not always fire |
| **Knowledge on a topic where a skill already exists** | A section or a separate file of that skill | Creates no competition for triggers and does not multiply references |
| **A catalogue of techniques with no procedure for choosing** | A reference, labelled as a reference | A catalogue is useful. A catalogue passed off as a method is harmful: it creates false confidence in reproducibility |
| **Little material, but a live topic** | An entry in the backlog | Material arrives in portions, and the threshold is reached over several rounds |
| **Genuine matter of taste** | Nothing | The only case where writing nothing is the honest answer |

**How to choose between the first two.** A rule that has to apply to any task in the project
belongs in the instructions. Knowledge needed only in a particular situation belongs in a skill
or in its files. A sign of confusion: a skill that is "needed always" is actually a project
instruction, and it will not fire reliably.

---

## A backlog of skills

**Keep a separate backlog for skills, starting with the first piece of material you set
aside.** Without it, half-assembled work is lost: a month later you will remember neither
the topic nor what was missing.

**What to record for each deferred topic:**

- **the topic**, in one line, phrased by the user's task rather than by the subject;
- **what is already there**: which forks and criteria have been found, and from what source;
- **what is missing**, specifically: how many cases, which questions were not asked, which
  block of material is absent;
- **where to look for what is missing**: a source, a person, a type of material;
- **the threshold**: at what volume the topic becomes a skill.

**Record decisions separately, not just tasks.** "Established this duplicates such and such"
or "decided not to do it, it is a matter of taste" is an entry that saves a repeated round.
A backlog made only of tasks turns into a list of debts within six months; a backlog with
decisions turns into the project's history.

**The closing rule:** **strike closed entries through, with a date and an outcome**, rather
than deleting them. A deleted entry comes back: the same material arrives again and the work
is redone.

⚠️ **Check an entry before adding it.** "We don't have this topic" is worth verifying by
searching for meaning rather than for the name, otherwise the backlog fills with a gap that
does not exist while the topic is already covered under another name.

**When to review:** with every new piece of material on an adjacent topic, and before any
reassembly of the set. A backlog nobody rereads does not work.

---

# The core distinction

> **A set of tips** tells you what exists. **A methodology** tells you what to do in a specific
> situation and on what basis to choose.

| | A set of tips | A methodology |
|---|---|---|
| Answers the question | What is known about this | What do I do now |
| Form | A list of techniques | A sequence with forks |
| How an option is chosen | The reader decides | The criterion is named |
| What happens if a step is skipped | Nothing, the steps are independent | The result breaks |
| Testability | Cannot be tested | You can say whether it worked |

**A practical test.** Take any section of the skill and ask: *"having read this, what action
will I take differently?"* No answer means it is reference material, not a method. Reference
material has its uses, but it does not replace a procedure.

## Signs that there is no method yet

- **Everything is listed, nothing is chosen.** Ten tools with no indication of when to use which.
- **Not a single "don't".** A method that forbids nothing decides nothing.
- **Every point is true on its own.** Truth is not a sign of method; coherence is.
- **You cannot get it wrong.** If the instructions make it impossible to do the wrong thing,
  they prescribe nothing.
- **The order of the points can be changed without loss.** That means there is no sequence.

---

# How to extract a method from expertise

Expertise is almost never laid out as a method. An expert speaks in stories, examples,
and asides, while holding the deciding procedure in their head without being aware of it.

**How you extract depends on whether the holder of the knowledge is available.** That is
the first fork, and it changes the whole procedure.

| Source | Approach | Main section |
|---|---|---|
| A finished text, video, or book, author unavailable | **Reconstruct** the criterion from examples | Steps 1–4 below |
| A live expert you can put questions to | **Draw out** the criterion with questions | "When you can ask the expert" |
| The user's own experience | **Extract from yourself**, the hardest case | "When the expertise is your own" |

## The second axis: the form of the material

The first fork answers **where to take the method from**. The second answers **what you are
physically working with**. They are independent: a book and a spreadsheet can come from
the same unavailable author, and the procedures for taking them apart differ.

| Form | Where the meaning sits | What to do first |
|---|---|---|
| **Linear text**: a book, article, regulation | The order of exposition and the wording | Read it, look for choice points |
| **Speech**: a video, podcast, call | The asides and digressions; the order is accidental | Transcribe it, and **do not carry the order over** |
| **Structure**: a table, matrix, diagram | **The structure itself is the method**: columns are criteria, rows are cases | Read the structure first, the contents second |
| **Spatial**: a board, deck, screenshots | Connections and placement rather than sequence | **Convert to text before analysis** |
| **Traces of decisions**: chat logs, tickets, code | Nothing is stated, only outcomes remain | Look for recurring forks |

**Three rules follow from that table:**

**Structured sources get unfolded, not assembled.** In an ordinary source you assemble
the procedure out of scattered decisions. In a good table it is already there: the columns
are the criteria, and the work runs the other way, unfolding what was compressed and working
out what justifies each column. An empty column, or a column filled identically in every row,
is a signal that the criterion is formal and not needed in the method.

**Convert spatial material to text before analysis, not after.** A diagram cannot be searched
by word or checked against what you have already written. While it stays a picture it takes
no part in the work. Convert it using your own structures: the original diagram cannot be
reproduced, since it is protected separately from the text.

**Take speech apart by its asides, and writing by its assertions.** In speech the boundaries
of a method sit in the digressions; in written text editing has cleaned them out and they have
to be reconstructed.

A catalogue by specific type, covering books, articles, courses, regulations, tables, boards,
forums, research, code, and your own notes, is in `references/source-types.md`.

## Step 1. Find decisions, not topics

Reading the source, look for **the points where the expert chooses**, not the places where
they explain.

Markers of choice in speech: *"here I look at…", "it depends on whether…", "if yours is like
this, then…", "I wouldn't, because…", "first you need to understand…"*.

Every such phrase is a candidate fork in the methodology. Everything else is justification.

## Step 2. Reconstruct the criterion

An expert names the decision but rarely names **what they decided by**. That has to be worked
out and then checked against their other examples.

*An example of reconstruction. The expert says: "for this client I'd suggest an assessment,
for that one a quote straight away." Two decisions are named. The criterion is not. From
the neighbouring examples it becomes visible: an assessment goes to people who don't understand
their own problem, a quote to those who do and are choosing a contractor. The criterion
is the stage of awareness. Now it is a method.*

**If the criterion cannot be reconstructed**, write exactly that: "the expert decides this
intuitively, there is no reproducible criterion." An honest hole beats an invented rule.

## Step 3. Test the criterion against counterexamples

Take the criterion and find a case in the source where it would **not** work. If no limitation
turns up at all, the criterion is phrased too broadly.

A method without boundaries is not a method but a slogan.

## Step 4. Assemble into a sequence

Lay the decisions out in the order they are actually made, and check the dependencies: which
step cannot precede which, and why.

**Order in a methodology carries information.** If the steps can be rearranged freely, this
is a list, and it should honestly be presented as a list rather than posing as a procedure.

---

# When you can ask the expert

Reconstruction is for when the author is unavailable. When they are available, **don't
reconstruct the criterion, draw it out.** That is faster and more accurate, but it takes
the right questions: asked directly how they make a decision, an expert almost always answers
wrongly.

**Why the direct question fails.** Expertise is automated: the decision is made faster than
it is noticed. What the person gives back is not their procedure but a rationalisation of it,
usually what they were taught rather than what they do.

## The technique: two cases with different outcomes

The main instrument.

Find **two similar situations in their practice where they decided differently**. Show both
and ask: **what exactly was different?**

The answer to that question is the criterion. It usually comes out immediately, because
the person is comparing specifics rather than describing an abstraction.

*If two such cases cannot be found, ask for a case where their usual decision did not fit.
It works the same way: the exception exposes the rule.*

## What else to ask

- **"What told you it had to be different here?"** draws out the criterion.
- **"What would have to change for you to decide the opposite?"** draws out the boundary.
- **"Where do you most often get it wrong?"** draws out the zone where the method fails.
- **"What do beginners do that you don't?"** draws out the negative rules, which the expert
  never states because to them they are obvious.
- **"What do you check first?"** draws out the order.

## What not to do

**Don't offer the expert a ready formulation to confirm.** They will agree: it sounds
reasonable and there is nothing to push back on. Agreement verifies nothing. Ask about cases
and draw the conclusion yourself.

**Don't accept "it depends on a lot of things" as an answer.** That is a signal the question
was asked abstractly. Go back to specific cases.

**Don't argue with the expert about their own practice.** Your job is to record how they
decide, not how it ought to be done. If you think they are wrong, see "When the expert
is wrong".

---

# When the expertise is your own

The hardest case, and usually underestimated. Your own method is less visible to you than
someone else's, because it is automated, and automated things cannot be seen from inside.

**The main trap:** instead of their own procedure, a person writes down what they read
elsewhere. The result restates the industry consensus rather than their own method, when
their own method was the one thing that was unique.

## The procedure for extracting from yourself

1. **Take the five most recent real cases**, not a typical scenario. A typical scenario
   is already a generalisation, and generalising yourself comes after, not before.
2. **For each, write down what was done**, in the order it actually happened. Not how it
   should have gone: how it went.
3. **Find where the cases diverged.** The point of divergence is a fork in the method.
4. **For each divergence, answer: what in the situation made you go the other way.** That
   is the criterion.
5. **Test on a sixth case** that was not in the sample. If the criterion predicted
   the decision, the method is there.

## Questions to put to yourself

- **What do I do that others in this role don't?** That is yours, not borrowed.
- **What do people correct me on most often, where I don't agree?** There sits a position
  rather than a habit.
- **What do I refuse to do that everyone else does?** Negative rules, the strongest part
  of a method and the one least often written down.
- **What question do I ask first when someone comes to me?** The entry point of the procedure.
- **Where do I regularly get it wrong myself?** The boundary of the method.

## What to do with what you could not explain

Mark it, don't invent it. "Here I decide from experience and cannot name what I go by" is a working
entry: it shows the reader that this point needs a person, not an instruction.

**An invented explanation is worse than a gap.** It creates confidence where there should
be none, and it breaks the first time it is carried into someone else's context.

---

# A rule and its mechanism

## Why a rule ends up looking obvious

The most common damage when knowledge is carried over: the rule arrives without the explanation
of **why** it works, and turns into a platitude.

> "Write about the client, not about yourself" is a platitude.
>
> "Write about the client, because nobody chooses in a vacuum. They are comparing you against
> three others, and the one who wins is the one in whose text they recognised their own
> situation" is a rule with a mechanism.

**The second gets applied, the first does not.** Not because the first is wrong, but because
nothing follows from it about what to do when you meet an exception.

## The rule: every prescription carries its mechanism

The formula: **what to do, why it works, when it stops working.**

The third part is not decoration. It is what makes the rule applicable in a situation
the author never anticipated.

**If the mechanism is unknown**, say so plainly: "the rule reproduces in practice,
the explanation is unknown." That beats inventing a plausible cause, because an invented
mechanism creates confidence in exactly the cases where the transfer fails.

## How to tell a rule from an observation

| | Observation | Rule |
|---|---|---|
| "It worked this way for me" | yes | no |
| Tested on several cases | sometimes | required |
| Conditions for reproducing are named | no | yes |
| What to do with it | take into account | carry out |

Observations are useful and worth keeping, but **mark them as observations**. An observation
presented as a rule breaks in the first unfamiliar context, and the method takes the blame.

---

# Negative rules

**The most valuable and least accessible part of any expertise.** The expert does not state
them: to them they are obvious, and the obvious goes unsaid.

**Why they are stronger than prescriptions.** A prescription describes one path out of many.
A prohibition cuts off a whole class of paths at once, which is why it transfers to situations
the author never foresaw. A method built from ten "do this" is weaker than one built from five
"do this" and three "never do that".

## Where to look for them

| Where | What to look for |
|---|---|
| **In beginners' mistakes** | What every newcomer does that the expert never does |
| **In refusals** | Which jobs, tasks, and clients they turn down, and on what grounds |
| **In irritation** | What sets them off in someone else's work. Irritation is a prohibition in compressed form |
| **In corrections** | What they fix first when taking over someone else's work |
| **In arguments with colleagues** | What they disagree with in the accepted view. That is a position, not a habit |

**The question that draws them out of a live expert:** *"what do you refuse to do that plenty
of people do, and why?"* It works better than a direct "what shouldn't be done", because
it rests on specific observable behaviour.

## Telling a real prohibition from a matter of taste

A real prohibition carries **a mechanism of damage**: it is clear what breaks and why.
"I don't do that, I don't like it" is taste, and it enters the method only as a marked
preference.

**The check:** can the expert name a case where breaking this prohibition led to specific
harm? If yes, it is a prohibition. If not, it is a preference.

## A prohibition needs grounds in the source

⚠️ **A separate rule, because an invented prohibition costs more than an invented explanation.**
An explanation simply fails to help. A prohibition **takes away an option that might have
worked**.

**What counts as grounds:** a counterexample in the source, a caveat from the author,
a described case of failure, or damage that is named outright. **What does not count:**
the prohibition looking reasonable.

**What to do when there are no grounds.** Don't ask the user, who usually knows no more than
you do, especially with someone else's material. **Rephrase it as a recommendation about order,
or leave it out.**

| Unproven prohibition | What to write instead |
|---|---|
| "These options don't combine, pick one" | "Start with one, the cheapest" |
| "You can't do it that way" | "People usually start elsewhere, because…" |
| "It only works under this condition" | "Tested under this condition, beyond it unknown" |

The right-hand column carries the same practical instruction and takes nothing away.

**Tell an inference from a guess.** They look alike from outside.

| | What was done | Does it follow from the source? |
|---|---|---|
| **Inference** | The author gave four conditions with a counterexample for each, so all four are needed, so there is a decision criterion | **Yes**, the counterexamples prove it |
| **Guess** | The author gave three techniques, and you decided they cannot be combined | **No**, nothing implies it |

Inferences cannot be forbidden, since extracting a method is itself an act of filling gaps.
What is forbidden is **passing a guess off as an inference**, and above all when the guess
is shaped as a prohibition.

### A numeric threshold is the same error, but more dangerous

⚠️ **A number that is not in the source does not go into the file as a threshold.** "Fewer
than several tens of thousands of people", "longer than three months", "cheaper than fifteen
percent": if the author never named those quantities, they are invented, however reasonable
they look.

**Why it is worse than a prohibition.** A prohibition reads as a judgement and can be
disagreed with. A figure reads as the result of a measurement. There is nothing to compare
it against, nothing to refute it with, and it starts cutting off decisions immediately.

**What to write instead:** a qualitative condition with a mechanism, such as "the audience
is too small for the algorithm to gather enough volume to learn from". The instruction
survives, the false precision disappears.

**If a number really is needed**, mark it as an estimate inside the file itself, not only
in the report to the user. The report gets read by a person once; the file gets read
by the model every time.

## How to write them

**A prohibition without an explanation does not get followed.** The formula is the same
as for a rule: **what not to do, what breaks if you do, whether there are exceptions.**

The third part is required. Absolute prohibitions are rare, and one presented as absolute
where exceptions exist will be abandoned wholesale at the first encounter with an exception.

---

# Level of abstraction

Two opposite errors, both of which make a method useless. The work sits between them.

| Too narrow | Too broad |
|---|---|
| The rule works only on the author's example | The rule applies to everything and therefore to nothing |
| "For online shoe shops with turnover under five million" | "Take your audience's specifics into account" |
| Sign: transferring to a neighbouring case requires rewriting | Sign: you cannot name a situation where it is wrong |

## How to calibrate

**Climb until the rule starts lying. Then come down one step.**

1. State the rule at the level it is given at in the source.
2. Widen it: remove one condition and check whether it still holds.
3. Repeat until you find the condition without which the rule breaks.
4. **Put that condition back.** That is the right level.

*A worked example. "Publish on Tuesdays" is narrow, tied to one platform and one audience.
Remove the day: "publish regularly at the same time" still holds. Remove the regularity:
"publish" has lost its meaning. So regularity is the condition that matters, and the day
of the week is the author's particular. The rule: publish on a predictable rhythm, with
the exact time chosen for the audience.*

**The sign you have hit the right level:** the rule transfers to neighbouring cases without
rewriting, and yet you can still name a case where it is wrong.

---

# When there is little material

One conversation, half an article, three cases from practice. This comes up more often than
a full body of material.

**Working is fine. Lying about completeness is not.**

| What you can do on thin material | What you cannot |
|---|---|
| Describe the procedure that is visible | Claim it is complete |
| Name the criteria that were stated | Fill in the missing ones by plausibility |
| Record one or two cases as examples | Present them as a tested regularity |
| Mark where the data ran out | Hide the gaps for the sake of looking finished |

**What to do explicitly:** mark the zones built on a single case inside the file itself.
"Based on a single observation, needs verification" is a working entry, not an admission
of weakness.

**What not to do:** fill the gaps with industry commonplaces. A skill where half is the
author's own method and half is industry consensus with nothing marking the difference
is worse than an honestly incomplete one, because the user cannot tell them apart.

**When it is better to wait for material:** if not a single fork reconstructs from what
you have, there is nothing to assemble. Say so plainly and propose what to gather: more cases,
a conversation with the person who holds the knowledge, a specific missing piece.

---

# What goes in the "Boundaries" section

**A required part of any methodology.** The absence of boundaries is not a sign
of universality but a sign that nothing has been tested.

What to describe:

**Where the method does not work.** Direct counterexamples, not hedges of the "it's all
individual" kind.

**Under what condition the conclusions change.** *For example: a set of rules derived
for a stagnating market, where half of them are unnecessary in a growing one.*

**What is time-bound.** Mark separately any knowledge tied to:
- legislation and jurisdiction;
- specific services, platforms, companies;
- prices, rates, market shares;
- the political situation.

⚠️ **A regulation ages differently from a practice.** A practice goes out of date gradually
and invisibly, which is why the advice for it is "check again". A regulation changes on
a specific day: before it the old wording is entirely correct, after it entirely wrong,
and there is no "roughly correct" in between.

**What follows from this:** for knowledge that rests on a regulation, standard,
or specification, the file records **the revision and the date the method is correct as of**.
Without that the reader cannot tell whether the file is out of date, and the text itself never
shows it. A phrase along the lines of "as of such a date, revision such and such" goes next
to the rule itself, not only at the end of the file.

**A technique for generalising:** take out the mechanics and leave the specifics
as illustration. Mechanics do not date; a list of platforms dates within a year. Instead
of naming a service, name the function: "a search engine", "a platform with restricted
access", "a classifieds aggregator".

**The scale the method was tested at.** Rules taken from a company of a hundred people do not
transfer to a solo worker automatically, or the other way round. Name the scale of the source.

---

# Contradictions in the material

## When sources contradict each other

⚠️ **First establish whether the sources have a hierarchy.** Everything after that depends
on it, and the order here is the reverse of the usual one: not "whose arguments are stronger"
but "whose source ranks higher".

| | No hierarchy | Hierarchy exists |
|---|---|---|
| Where | Practices, schools, approaches: marketing, management, teaching | Subjects with a governing rule: accounting, law, workplace safety, medical protocols, standards and specifications |
| What a contradiction means | Both may be right under different conditions | One source is **wrong or out of date** |
| What to do | Find the frame for each, see below | Establish rank and follow the higher one |

**The order of rank in subjects with a governing rule:** the rule itself, then official guidance
on it, then established practice, then the opinion of an individual specialist. A later revision
outranks an earlier one.

⚠️ **Here "leave the contradiction open" is harmful advice.** The reader has to get a single
answer and a statement of what backs it. An open fork will lead them into a violation. If rank
cannot be established, that is not a reason to describe both options. It is a reason to write
that the question needs professional verification, and to name where that verification comes
from.

**What follows is only for subjects without a hierarchy.**

**Don't pick a winner silently.** This is the most expensive error in compilation: the reader
gets one claim and has no idea a well-founded opposite exists.

**What to do:**

1. Set out both claims.
2. Find **the frame in which each is true**. Usually the contradiction dissolves in a difference
   of context: a different business size, a different product type, a different sales cycle.
3. Give the rule for choosing: under these conditions the first works, under these the second.

**If no frame can be found**, leave the contradiction open and say that it is open. False
consistency is worse than an honest "opinions differ here".

## When the author contradicts themselves

This happens more often than disagreement between authors, and it usually signals not an error
but **a position refined over time** or **different implied contexts**.

Handle it the same way: both claims, the frames, the rule for choosing. Don't smooth it over
in favour of the later statement, because later is not necessarily more accurate.

## When the expert is wrong

It happens. The signs:

- the claim contradicts verifiable data;
- a mechanism is named but does not survive checking;
- a generalisation is built on a single case;
- the conclusion follows from the author's personal situation rather than from the mechanics.

**What to do:** keep the claim, add the limitation, and state what the limitation rests on.
Don't throw it out silently, because the next time the same source is worked through
the material will come back and the work will repeat.

**What not to do:** don't argue with the author inside the skill. A skill is an instruction,
not a review. The limitation is phrased as a condition of use, not as a rebuttal.

## What not to take at all

- **the source's self-promotion**: descriptions of services, invitations, case studies used
  as proof;
- **the author's own success figures**, except those that carry mechanics such as orders
  of magnitude, ratios, or team size relative to workload;
- **personal stories with no mechanics**, except those that explain a rule;
- **repetitions**: a claim repeated three times in a talk appears once in the method;
- **forecasts**, which date instantly. If a forecast matters, put it in its own section
  and label it as a forecast.

---

# Legal framing

**Method is not protected, expression is.** A sequence of actions, criteria for choosing,
and principles can be freely restated in your own words. What is protected is the specific
text, the order of exposition, the examples, the metaphors, and the author's wording.

⚠️ **The whole procedure for someone else's material follows from that:** you extract
the method, write it anew, and generate your own examples. This is not over-caution but
the normal way to assemble, and the one that gives the better result methodologically.

**The "strip the borrowings" test.** Mentally delete from the file everything taken verbatim
from the source. If a working methodology remains, the file is clean. If what remains
is a skeleton with no content, it is a restatement and cannot be published.

⚠️ **A license is a field plus a file.** If the skill is being distributed, a `LICENSE` file
with the full license text goes next to `SKILL.md`. The field alone in the frontmatter is
a note of intent and carries no legal weight. If the purpose has not been established, leave
the field out too: empty is less ambiguous than wrong.

⚠️ **Open `references/legal.md` when:** the material contains personal data, a direct quote
is needed, the source is under NDA or carries a licensing clause, or the result is leaving
your own disk. The pre-publication checklist is there as well.

# Judgement domains and procedure domains

**How strict to be is chosen by domain, not by taste.**

| | Procedure domain | Judgement domain |
|---|---|---|
| Examples | A database migration, a legal checklist, safety procedure | Positioning, negotiation, choosing a strategy, editing |
| What determines success | Precision of execution | Quality of the decision in context |
| Form in the skill | An exact sequence, deviation forbidden | Criteria, forks, questions for gathering data |
| The author's error | Giving freedom where it does harm | **Giving an algorithm where judgement is needed** |

**The second error is more common and more damaging.** An algorithm in a judgement domain
produces confidently wrong answers: the person follows the steps and gets a result that does
not fit the situation but looks correct.

**The sign of a judgement domain:** asked "what if mine is different", the expert answers
"it depends on…". That means what goes into the skill is not the answer but **the list
of what it depends on**, and what to do with each option.

**How to write a judgement domain so it doesn't turn to mush:**

- name the variables the decision depends on;
- give the values and consequences for each;
- give the questions for gathering the missing data;
- give the prohibitions, which work better than prescriptions in a judgement domain.

---

# Mandatory parts of a skill

Four things without which a method, even correctly extracted, will not fire.

**Requirements for frontmatter fields are in the Agent Skills specification.** The length
limits come from there too: they are checked by the validator at packaging time rather than
at load time, so exceeding one is a debt against publication, not a breakage.

## 1. The "How to use this" block

**It goes immediately after the title and the opening paragraph. Without it the skill
is not ready.**

The reason: the rest of the file describes subject knowledge. This block is the only place
that says **what to do when a request arrives**. Without it the model outputs the contents
whole instead of acting.

```markdown
## How to use this

**What not to do:**
- [the most expensive mistakes in this subject, in the imperative]

**Order:**
1. **A verb in the imperative.** One line of explanation.
   [five or six points, no more]

**What to ask when data is missing:** [separated by ·]

**When this is the wrong place:** [routing to the right skill]
```

**What each part is for:**

- **"What not to do"** comes first because it gets read first, and it prevents the standard
  mistake before it happens.
- **"Order"** turns knowledge into a sequence. Without it everything gets output at once.
- **"What to ask"** stops the model answering into a void when the data is missing.
- **"When this is the wrong place"** saves the user from working on the wrong thing.

## 2. The name of the skill

⚠️ **The title of a source is not evidence of what is inside it.** Material is titled to get
opened, not to make its contents clear: a promised outcome, an intrigue, a loud number.
The subject is established **by reading, not by the title**.

**A worked example from a real case.** The source was called "The technology that brings
in 100M+ a year". Inside was a detailed course on lead magnets: types, selection criteria,
metrics.

| Naming it by the title | What happens |
|---|---|
| By the promised outcome, "revenue growth", "a hundred million" | The skill fires on no lead-magnet request at all, and on revenue requests delivers the wrong thing |
| By the intrigue, "technology", "system" | Says nothing |
| **By the content, "lead magnet"** | **Fires where it is needed** |

**The most expensive mistake here is naming by the promised outcome.** The title promises
money, the contents are a tool; a name built on the promise sends the skill into someone
else's niche of requests while leaving its own empty.

**The rule:** first answer for yourself in one phrase **what this is in substance**: "a course
on lead magnets", "an analysis of price segments", "working with customers who left". The name
is built from that phrase, and the source's title plays no part in the decision at all.

**Then go by the user's task, not by the mechanism.** Even having identified the subject
correctly, it is easy to name the skill after the mechanism the author describes rather than
the situation the person will arrive in.

| Bad | Why |
|---|---|
| The source's title or promise | About the source, not about the task |
| The subject area, `marketing`, `content` | A set will contain ten of those |
| The name of the mechanism instead of the task | The user is looking for a solution to their situation, not for a term |
| The author's name for their method | Not yours, plus a trademark question |
| Something generic, `helper`, `utils`, `tools` | Says nothing |

**A one-phrase check:** a person sees only the name in a list of thirty. Can they say when
to call this skill? If not, the name does not work.

**A second check, for a set:** read the neighbours' names in a row. Two names differing by one
word break navigation the same way identical section titles break it inside a file.

**What the name carries and what the description carries.** Both take part in selection,
but differently. Specifics and the user's own phrasing belong in the description; the name
works for the person scanning a set with their eyes. So the name is short and clear rather
than long and precise.

**Technical requirements:** lowercase Latin letters, digits, and hyphens, **up to 64
characters**. The folder name matches the name in the frontmatter.

## 3. The description the skill is found by

**The description is the main selection mechanism.** Nothing else in the file matters
if the skill never fired.

**What gets cut first if the description has to shrink.** The user's own phrasing, meaning
the typical wordings of a request. Routing to neighbours ("for such and such, see
the neighbouring skill") stays: without it skills start competing for the same requests,
and the cause is invisible.

**If it doesn't fit**, shorten the user phrasings rather than the routing: ten wordings
instead of twenty. Keep the references to neighbours.

**What has to be inside:**

1. **What this is**, in one phrase, in substance.
2. **When to use it**: situations rather than topics, such as "when content goes out
   and no enquiries come in".
3. **The user's own phrasing**: ten to twenty phrases in quotes, the way they will actually
   say it, conversationally, without terminology, sometimes with mistakes.
4. **Who it fits**: the area, the size, the type of case.
5. **Where to go instead**: neighbours, with what makes them different.

**The main rule:** write the phrases **a person says, not the ones a specialist knows**.
"They don't subscribe" is right. "Low subscription conversion" is wrong, because that is how
someone already fluent phrases it, and they would manage without the skill anyway.

**Add a loading condition if the skill is needed beyond a direct request.** For example:
a skill about restrictions in a regulated area should load for any sales text in that area,
even when the request was simply "write me a post".

**Check for overlaps with neighbours.** The same phrase in two descriptions is a guaranteed
selection error.

## 4. The mode block, when the subject touches the model's own actions

**Needed when the skill is about work the model can do itself:** writing, editing, fact
checking, working with models, research.

Without it you get an instruction for a human that a model happens to be reading, and asked
to do the work the model explains how to order the work instead.

```markdown
## How to read this skill

⚠️ **You are the one loading this skill. Some of the rules here are about your own output.**

| Mode | When | What to do |
|---|---|---|
| **You are doing the work** | [a request for a result] | Apply the rules silently, to your own output |
| **The user is setting up a process** | [a request for methodology] | Deliver it as methodology |
```

**The rule of the first mode:** if a result was asked for, don't explain how to ask for it.

---

# What goes in the main file and what goes in a separate one

The official specification describes the **mechanics** of progressive disclosure. Here is
the criterion for deciding what goes where.

**The criterion is not length but frequency of access.** The main file loads in full every time
the skill fires. So there is one question: **is this piece needed every time?**

| Into the main file | Into a separate file |
|---|---|
| Needed on any request about the subject | Needed in one case out of several |
| Determines the order of work and the forks | Catalogues, tables, industry particulars |
| Decisions taken every time | Depth for a rare case |

**It follows that length by itself decides nothing.** A thousand-line file where every line
is needed on every request is built correctly. A two-hundred-line file where a hundred and
fifty lines are needed once in ten runs is not.

### The second criterion: what breaks if the file never gets opened

⚠️ **What gets moved out stops being carried out.** A separate file is opened when someone
decides it is needed, and that decision is made by circumstance and often not made at all.
Anything moved out turns from mandatory into available on demand.

**Hence the rule: a mandatory action does not go into a separate file, even if it is rarely
needed.** What goes out is what people consult for detail: catalogues, extended analyses,
particular cases, longer explanations.

| Can be moved out | Cannot be moved out |
|---|---|
| Lists and catalogues to choose from | An action that has to happen |
| Extended analysis of a rule already stated | The rule itself |
| Particulars applying to one case in ten | A check before delivering the result |

**The sign that something was moved out wrongly:** after the move, the result started coming
out without what used to get done. Look for it not in the text of the reference file, which
stayed correct, but in what stopped happening.

**What to do with the rare but mandatory:** leave one line of the action itself in the body
and move the explanations and particulars into the file. The line gets carried out,
the explanations get opened when needed.

## What to cut first when the file has grown

1. **Catalogues and lists**: types, formats, industry inventories. Needed when choosing,
   not always.
2. **Extended particulars**: rare cases, longer analyses.
3. **Reference tables** consulted at specific moments.

**What never to cut:** the order of work, the forks, the criteria for choosing,
the prohibitions. Without them the main file stops being an instruction and becomes a table
of contents.

## The sign of a wrong split

**The model reads a separate file on every run**, which means it belongs in the main one.

**The model never opens a separate file**, which means either it is not needed or the pointer
from the main file is poor. Check the wording of the pointer: it should name the situation
in which the file is needed, not only its contents.

---

# When there are many skills

**The main criterion for splitting is a different class of request, not a different topic.**
Two skills are needed when a person arrives with different questions and gets different
procedures. One topic cut in half by volume gives two skills that always load together,
which is one skill split needlessly.

⚠️ **A reference to a neighbour has to carry content, not just a name.** "Layer-by-layer
analysis, see the neighbouring skill" breaks when the neighbour was never downloaded.
"Layer-by-layer analysis: start at the top, then each one below until you find the first
broken layer. More in the neighbouring skill" works on its own.

⚠️ **Sitting in the same folder does not make something part of the set.** Before referring
to an existing skill, make sure it belongs to the same set rather than merely lying nearby.
Skills from different topics and different sources end up in one folder easily, and
a reference to such a neighbour ties a foreign file into the set: it will not travel when
the set is handed out, and the reference will be left dangling.

**Signs that it is foreign:** a different subject area, a different author of the material,
a different purpose, such as a working skill for yourself against one meant for publication.
When in doubt, don't add the reference. State what is needed in place instead: one line
of content is more reliable than a reference that may not resolve.

⚠️ **Open `references/skill-sets.md` when:** there are more than three skills and they refer
to each other, or you are deciding whether to hand out the set whole or in parts, or
an existing skill needs updating with new material.

# How a skill degrades during refinement

Every failure below appears **not while writing but while refining**, and none of them
is visible from inside a single edit. Each is found only by walking the whole file.

## Friction accumulates one rule at a time

Nobody adds unnecessary requirements on purpose. They get added one by one, and each
is justified: clarify the source, check the purpose, run a check. **The sum is a five-question
questionnaire and a twelve-step conveyor before the first useful action.**

**The sign:** count how many actions are needed before the first result. More than three
means the file has begun serving itself.

**What to do:** don't delete requirements. Separate the mandatory from the situational
and move the mandatory to the top as a short block.

## Duplicates appear between sessions, not within one

You cannot duplicate within one session: you can see what you are writing. You duplicate
a week later, adding a section without remembering that the same thought is already stated
above.

**The sign:** one thought lives in "common failures", in the checks, and in the body
of a section. Three places is normal for a file that has grown.

**What to do:** read the file end to end periodically. Duplicates show up only that way,
because in pieces each one
of them looks appropriate.

## Section names drift together

Sections about adjacent things naturally end up with similar names. A real example from this
file: there were "Boundaries of applicability" and "Boundaries between skills", "Working with
sources" and "Working with someone else's source". The contents were completely different:
one pair covered conditions of use and splitting a set, the other covered disagreements
in the material and the law.

**What breaks is not the content but the navigation.** The wrong section gets opened.

**What to do:** name sections by the task, not by the subject. Those same four became "What
goes in the Boundaries section", "When there are many skills", "Contradictions in the
material", and "Legal framing", and no name is confusable with any other now.

## Someone else's recommendation turns into your own rule

"Keep the file under so many lines for optimal performance", read once, becomes a hard limit
nobody ever set within a couple of sessions, and starts dictating decisions about content.

**The sign:** a limit whose source is not named, justified with something like "that's how
it's done".

**What to do:** remember for every limit where it came from and how binding it is.
A recommendation taken for a rule cuts content for no reason.

## A skill about the model's actions gets written as an instruction for a human

A category error, invisible from inside: the text is correct, it is simply addressed to
the wrong reader. It appears whenever the subject of the skill is work the model can do
itself: writing, fact checking, editing, working with models.

**The sign:** the file contains prompts and advice to "ask the model to do such and such",
when the file is being read by the model.

**What to do:** a mode block at the top, see "Mandatory parts of a skill".

## The author stops seeing the file as a whole

The shared cause of all five. After several sessions the edits go piece by piece, the whole
is never reread, and the failures above live unnoticed for months.

**What to do:** every few edits, read the file straight through from start to finish. It takes
minutes and finds what no piecewise check will.

---

# Checking the quality of the methodology

Run before publication.

**Falsifiability.** Can you name a situation in which the method gives a wrong result?
If not, the method is phrased too generally.

**Presence of refusals.** Is there a single "don't"? A method with no prohibitions does not
narrow the space of decisions, and so does not help.

**Decision criterion.** For every fork: is it stated what the choice is made on? "Judge by
the situation" is not a criterion.

**Transfer.** Take a case that was not in the source. Does the method give an answer for it?
If it works only on the author's examples, it is a retelling of examples.

**The reverse check for obviousness.** Read each rule and ask: would a non-specialist do
the same thing from common sense? If yes, either the rule is redundant or it has lost
the mechanism that made it non-trivial. Usually the second: look for the missing "why" before
deleting anything.

⚠️ **The checks judge the text, not the work.** The first seven test the internal coherence
of the file: whether the claims connect, whether criteria exist, whether it falls apart
without quotes. **None of them shows whether the method works on a live task.** A coherent
and useless method passes all of them.

The only real check is **to apply it**. Build something with this method on material that was
not present during assembly, and watch three things: where you had to invent beyond what
is written, where what is written got in the way, where you silently ignored it. All three
are defects of the method, not of your discipline.

If there is nothing to apply it to yet, say so in the report to the user.

⚠️ **Don't confuse this with the caveat about a regulated area.** That one is mandatory and
never prohibited: it states that the skill does not replace professional advice, and it refers
to the subject. What is prohibited are caveats about **the file itself**, about how far it can
be trusted.

⚠️ **Don't put general reliability caveats in the file:** "not tested in practice",
"inaccuracies possible", "needs verification". They are true of any freshly assembled skill
and therefore carry no information. A model reading the file can do nothing with them except
hedge for no reason.

The notes that genuinely change behaviour are about **a specific place, not the file as
a whole**, and they are already described where they belong: a missing criterion in step 2
of extraction and in "The method covers only some of the decisions", conditions of use
in "What goes in the Boundaries section".

**Order.** Swap two steps. Did it get worse? Good, the order carries meaning. Did nothing
change? Then it is a list, so present it as a list.

**Strip the borrowings.** Mentally delete every verbatim fragment of the source from the file.
If the instruction stays usable, the method was extracted. If the file falls apart, text was
carried over, and it needs rewriting from the procedure.

This test sits in the quality checks rather than in the legal section, and that is not
an accident: **it tests the same thing from two sides.** A compilation of someone else's
wordings fails both as a method and as a legal construction, because in both cases it means
the same thing: the deciding procedure was not extracted, the text was copied.

A practical consequence follows: **if the file passes the earlier checks, it almost always
passes this one.** A method phrased as directives with criteria and boundaries physically
cannot consist of someone else's wordings. Failing this test is a signal to go back
to the first.

**Cross-check against the source.** The only check that catches **losses during extraction**.
The other seven judge the finished text: it can be flawless and still be missing a third
of the material, and nothing in it shows that.

⚠️ **Rereading the source "more carefully" does not work.** Reading it after assembly, you
recognise what you already extracted and confirm your own work. What was missed does not stand
out precisely because there is nothing to remember about it.

### The digest is written before the skill and stays a separate file

**The order:**

1. **Write the digest of the source as a separate file**, before any extraction of the method
   and before assembling the skill. Into chat go a link to the file plus the sections "said
   in passing" and "what was left out".
2. **Assemble the skill**, working from the digest.
3. **Cross-check the finished skill against the digest**, marking each item as: included,
   deliberately dropped with a reason, or **lost**. The third category has to be empty.

⚠️ **The digest and the skill are two different documents with different jobs.** The digest
**records the source**; the skill **builds a method from it**. As long as both jobs are done
in one pass they compete, and recording always loses, because building requires active
attention and recording does not.

**What the digest has that a list of bullet points does not.** The line "technique: set a role"
does not contain "imagine you're explaining this to a mate in the kitchen at four in
the morning". It contains a pointer to it. Assembling from a pointer means going back
to the source for the wording, and going back is exactly where things get lost. The digest
carries **the content itself**, and you can assemble straight from it.

**The structure of a digest:**

- the contents of the source by its own sections, **with the author's wordings preserved**
  wherever the wording is the value;
- ⚠️ **a separate heading for what was said in passing**, which is what gets lost first;
- **"What was left out"**, with a reason for each item;
- **"Added by me"**, everything that was not in the source.

The last two sections remove separate work later: the marking of what was inferred and
the list of deliberate refusals both come out immediately rather than being reconstructed
from memory.

⚠️ **Every item in the "said in passing" section is closed at assembly in one of two ways:**
it entered the skill, or it is named in the report as dropped, with a reason. There is no third
outcome.

**Why this section needs a rule of its own.** The rest of the digest is large, and skipping
part of it is noticeable. What was said in passing was separated out precisely because at
assembly it becomes invisible again, now against the background of the file you have built.
The list catches the loss on the way in, and **it does not by itself carry the finding
forward**: without closing each item it stays an observation that obliges nothing.

⚠️ **The cross-check runs against the source, not against the digest.** The digest is not
written automatically either, and whatever fell out at that step cannot be caught anywhere
further down the chain. The loss becomes invisible, because every subsequent check will agree.

**The digest is not published with the skill.** It is a working document: it keeps quotes,
the author's name, and pieces of the source that must not go into a published file.

### A term is lost separately from its mechanism

⚠️ **The mechanism can reach the skill intact while the name the author gives it disappears.**
This has to be checked separately: the "included, dropped, lost" cross-check runs by content
and misses this kind of loss, because the content is there.

**Why it matters:** with a description and no name, the method cannot be found, discussed,
or matched against anyone else's material. The reader of the skill is left with a paraphrase
where the author had a term.

**The rule: if a mechanism has a name in the source, it goes into the skill together with
the mechanism**, even when the name is someone else's and well known. Being well known
is no reason to drop it. On the contrary, a familiar term connects the skill to what
the reader already knows.

### Splitting rules leaves traces

When the source has six rules and the skill ends up with seven or five, **reread the whole
file for mentions of the quantity**, following the traces from "After an edit, walk
the traces of what changed". Here the trace appears at assembly rather than during
refinement: the number from the source reaches the "How to use this" block and the description
before the rules get split.

### What to follow when building the list

**The author's own transition markers**, not your own sense of the structure:

| Type of source | Markers |
|---|---|
| Speech | "second idea", "step three", "also worth mentioning", "and now", "by the way" |
| Text | headings, subheadings, numbering |
| Structured | whole rows and columns |

**Every marker opens an item on the list.** Even if only one sentence follows it.

### Why the things that get lost are the ones that do

⚠️ **Losses correlate not with importance but with how much time the author spent on it.**

The author talks for five minutes about a mechanism and gives one sentence to a technique.
Extracting, you reproduce their emphases, and what was said in passing drops out entirely.
Yet the value of the passing remark is often higher: to the author it is obvious and therefore
brief, while to the reader it is new.

**A practical rule: on the list, one sentence weighs the same as a five-minute block.**
Volume in the source does not carry over to the list.

**What gets lost most often:**

- **lists of techniques and formats**, which run past as a quick enumeration and read like
  "examples of the above";
- **mechanisms named in a single phrase**, meaning how exactly something is done when
  the author did not expand on it;
- **side remarks in parentheses**: "by the way", "incidentally", "one more thing".

Going through the list, come back separately to every enumeration in the source and to
everything that took less than two sentences.

---

**Before publishing**, run the gate checklist, which is in `references/legal.md`.

# When the user asks you to break a rule

Requests like "just copy that chapter", "leave it as is, nobody will notice", "drop
the caveats, they spoil the look" are ordinary, and usually there is no bad intent behind
them, only haste.

**What to do:**

1. **Say briefly what the risk is**, without a lecture. One or two sentences.
2. **Offer what gives the same result lawfully.** There almost always is one: extract
   the method instead of copying the text, take a quote by the rules instead of moving
   a paragraph across, link instead of reproducing.
3. **Don't refuse the whole task.** The task is usually lawful; the problem is the method.

**What not to do:** don't moralise, don't repeat the warning twice, don't block the work over
a debatable trifle. If the user insists and the risk is not critical, do it, having stated
your reservation once.

**Where refusal is mandatory and not up for discussion:** direct reproduction of protected
text passed off as your own, removing attribution from someone else's method, circumventing
the terms of restricted access. Offer an alternative there and stop.

---

# Common failures

Four that the checks above do not catch.

**An archive instead of a tool.** The material is set out precisely, with structure and
quotes, and contains not a single action. It appears when sources come in a stream: the work
drifts imperceptibly from "writing an instruction" to "restating the source". The checks miss
it, because each section looks sensible on its own. The cure is a question put to each one:
**what action does this change?**

**Attribution instead of content.** "The author notes", "the source phrases it this way".
The author's name is needed once, in the header. After that it takes up space and turns
an instruction into lecture notes.

**Terminology renamed for clarity.** Behind an author's term sits a distinction, and renaming
loses it. Explaining, yes. Replacing, no.

**A description by topic rather than by situation.** A description like "about content
marketing" instead of "when content goes out and no enquiries come in". The skill will never
be selected, and no quality of content compensates for that.

---

# Order of work

**The core is six steps plus a zeroth. Everything else connects as the situation requires.**

0. **Write the digest of the source** as a separate file, following the author's transition
   markers, before any extraction of the method. The skill gets assembled from it afterwards
   and the cross-check runs against it. It only works if done now: the same pass that does
   the assembly cannot replace it.
1. **Write out the choice points**, the places where the expert decides rather than explains.
2. **Reconstruct the criterion** for each. If it does not reconstruct, mark it as intuitive.
3. **Assemble into a sequence** and check the dependencies between steps.
4. **Work out the mechanism** for every rule: why it works and when it stops.
5. **Describe the boundaries**: where it fails, what is time-bound, at what scale it was
   tested.

**Plus one step worth doing almost every time:**

6. **Collect the negative rules.** They will not be sitting ready in the source, and without
   them the method is half as strong.

**Connects when there is a reason:**

| Step | When it is needed |
|---|---|
| Establish the mode from the entrance fork | The source or purpose is not obvious |
| Calibrate the level of abstraction | The rule works only on the author's example, or applies to everything |
| Test criteria against counterexamples | The material is large or the criterion looks too broad |
| Work through contradictions | There are several sources, or the author disagrees with themselves |
| Determine the domain | It is unclear whether to give an algorithm or criteria |
| Mark the zones on thin material | Some conclusions rest on one or two cases |
| Decide what to move into a separate file | The main file is overloaded with rarely needed material |
| Separate from neighbouring skills | There are neighbours on the topic |
| **Pass the gate before publication** | **The result is leaving your own disk** |

**Checks before delivery:** four are mandatory, namely decision criterion, presence
of refusals, strip the borrowings, and **cross-check against the source**. The other four
are for large or contested material.

## Format: the line that always ships

⚠️ **The report to the user about a finished skill must contain this line.** Not "checked",
not ticks, but **counted values**:

```
Format: description N/1024 · name N/64 · license: <value or "no field">
```

⚠️ **A number cannot be written without counting. A tick can be placed without looking.**
That is the whole difference, and it has been verified: the checklist version failed on four
builds in a row, including ones where the rule had been read and discussed.

**A broader conclusion follows, beyond format: a rule whose execution is not counted does not
get executed.** Knowing a rule and following it are unconnected. If a requirement has
a numeric form, demand the number rather than a confirmation.

**What counts as a violation in each field:**

| Field | Norm | If violated |
|---|---|---|
| `description` | ≤ 1024 | Exceeding it is a debt against publication, not a breakage. Cut when publishing: the user's own phrasing goes, the routing stays |
| `name` | ≤ 64, lowercase Latin, digits and hyphens | The folder name has to match |
| `license` | an identifier (`MIT`, `CC-BY-4.0`) **or no field at all** | A pointer to a section of the file will not do, remove the field |

**Run it always, even when the file is not being published.** The frontmatter is read
by the loader rather than by a person, and exceeding a limit breaks the skill regardless
of who is using it.
