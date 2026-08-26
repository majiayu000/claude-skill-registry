# Legal framing

Applies in full when the source belongs to someone else. For the user's own expertise
the section is not needed.

**Expression is protected, the idea is not.** A method, a criterion, a procedure are free
in any jurisdiction (Berne; US §102(b); EU InfoSoc). Wording, examples, metaphors, and
the structure of exposition are protected.

**Extract the deciding procedure and state it as a directive.** Don't retell a paragraph
of the source as a paragraph of the skill.

**Don't carry over the author's examples, cases, or metaphors.** Generate your own for
the same procedure.

**Don't reproduce the source's order of exposition.** Order in a skill is set by the sequence
of application, not by the structure of a talk.

**Use the names of the author's frameworks as references**, don't appropriate them.

**Diagrams, tables, and screenshots are protected separately from text.** Rebuild them with
your own means, don't paste the originals.

**Working from a transcript, the source's phrasings seep into your output unnoticed.** After
assembling a section, reread your own text for the source's characteristic turns of phrase
and rewrite from the procedure.

**Don't include fragments of the transcript in the file**, not in the body, not
in appendices, not as "sources".

## Personal data

Don't carry over names, companies, or identifying details from the source's cases. Replace
them with a generalisation or an invented example: **the specifics of a case are not part
of the method.**

The rule applies to the user's own material as well, whenever third parties appear in it.

## Quoting

Quote **only when the criterion cannot be reconstructed without the exact wording**.
A disguised paraphrase is worse than an honest quote.

The conditions follow the stricter variant (the EU and Russian right of quotation), which also
passes under fair use:

- the minimum volume needed for the criterion;
- the author and source are named;
- it is visually set apart;
- it is surrounded by your own directives and is not an instruction in itself.

```markdown
The criterion, in the author's words: "[quote]".
— [Name, source](link)
```

Doesn't pass? Rephrase.

**Don't quote instead of formulating.** Don't assemble the file as a chain of quotes with
connective tissue.

## Into the output file

**The license** follows the purpose table in "The opening fork".

**Where to put it.** The `license` field in the frontmatter is legitimate and appears
in the list of allowed properties. But **the value has to be an identifier**, not a pointer:

| Like this | Not like this |
|---|---|
| `license: MIT` | `license: see the section at the end of the file` |
| `license: CC-BY-4.0` | `license: to be confirmed` |
| No field at all | A field that does not state the license |

**If the purpose has not been established, leave the field out.** The absence of a field reads
unambiguously: there is no license, so "all rights reserved". A placeholder instead
of an identifier is worse than nothing, because it looks like an answer without being one.

**For skills that get distributed**, a `LICENSE` file with the full license text goes next
to `SKILL.md` alongside the field. The field alone is enough as a note, not as legal weight.

**A sources section when material was borrowed:** links to authors and materials, phrased
as "based on public materials", **not** "contains materials".

**Regulated areas.** If the methodology concerns medicine, law, finance, or psychotherapy,
include a note on the area of application and on the fact that the skill does not replace
professional advice.

⚠️ **Code carries its own license, and it outranks yours.** Copyleft licenses (GPL and its
relatives) require the derivative to be distributed on the same terms, so a single inserted
fragment redefines the license of the entire skill. Carry over the mechanism rather than
the text of the program. The absence of a license file in a repository means "all rights
reserved", not "free to use".

⚠️ **Official documents are the exception to the ban on carrying text over.** Statutes, court
decisions, and government documentation are not objects of copyright, and **paraphrasing them
does harm**: the exact wording of the rule is the content, and your own words produce
an interpretation instead. Quote the rule verbatim, separate it from your interpretation,
and state the revision.

**The exception does not extend** to commentaries and textbooks on legislation, to standards
distributed for a fee, or to translations. All three have authors of their own.

## Boundaries of this section

**Does not apply to:** facts, statistics, commonly known methods, or the user's own expertise.

**Stops working when the source is under a separate agreement:** a paid course, an NDA,
a closed community. Contractual restrictions outrank the general rule about ideas, and
extracting the method can be forbidden by contract.

**Attribution removes the question of appropriation, not of reproduction.** Don't use it
as a substitute for rewriting.

---

# Jurisdiction: whose law applies

The section above names Berne, US §102(b), and EU InfoSoc, which is the general frame and
works almost everywhere. The specifics resolve differently.

**The law of the country where the use takes place applies**, not the country of the author
and not the country named in the source. Published to an open repository, the use takes place
everywhere it was downloaded.

**What follows practically:**

- **The right of quotation differs.** In Russia and the EU it is stricter: a closed list
  of purposes, mandatory attribution, a volume justified by the purpose. American fair use
  is more flexible but less predictable, decided by a court on four factors after the fact.
- **Aim at the stricter regime.** Material that passes under the Russian or EU right
  of quotation also passes under fair use. The reverse is not true.
- **The term of protection differs**, usually seventy years after the author's death, though
  not everywhere. For contemporary material the question does not arise.

**For a skill this means one rule:** write so that the volume of borrowing is justified
in the strictest jurisdiction it might land in.

---

# Trademarks are a separate regime from copyright

The two cannot be conflated: **copyright protects the text, a trademark protects the mark.**
Material can be entirely rewritten in your own words and still infringe rights in a mark.

## What is protected as a mark

Names of companies, products, and services, and also **the names of methods and frameworks**
when registered. The last one bears directly on working with someone else's methods.

## What you can and cannot do

| You can | You cannot |
|---|---|
| Mention the name of a method as a reference: "the method is called such and such, by so and so" | Take someone else's name into the name of your skill or product |
| Compare: "unlike such and such an approach" | Present it as though it were your own development |
| Describe the content of the method in your own words | Create the impression that the mark's owner had a hand in your material |

**The practical criterion:** a reference describes something else's, use appropriates it.
The question that settles it: **could a reader think this was released by the owner
of the mark?**

## The common error when working with frameworks

The author of a method gives it a name. The name enters the skill naturally, because renaming
an author's terms is not allowed, and that is correct for **terms inside the method**. But
**the name of the framework** in the skill's title or in its name is a different matter.

**The working solution:** keep the terms inside; make the name of the skill your own,
descriptive, built on the user's task. It works better for triggering, too.

---

# Platform terms and transcription

A question separate from copyright, settled by **your agreement with the platform** rather
than by copyright law.

**What that means.** A publicly available video is a question of copyright in the content.
Downloading it and transcribing it automatically is a question of the platform's terms
of service, where such actions are often restricted separately.

**The practical frame:**

- a transcript is **working material**, not a product. It does not get published, attached
  to the skill, or placed in the repository;
- what goes into the output file is the extracted method, not the transcription;
- a link to the original in the sources section is fine and useful: it sends the reader
  to the author rather than replacing them.

**What never to do:** publish transcripts of someone else's material as part of a pack,
even in a utility folder of the repository.

---

# Co-authorship and contributions from several people

Comes up when the method was assembled from a conversation, joint work, or an interview.

**An interview taken specifically for this.** The expert's answers are their contribution.
Agree the terms of use **before publication**: whether their name can be used, whether they
can be quoted, whether it can be distributed commercially. A verbal agreement is enough
for trust but not for a dispute.

**Joint development of a method.** If the methodology grew out of two people's work, rights
are shared by default and neither can dispose of them alone. Record the agreement in writing
before, not after.

**Material created by an employee.** A work made for hire belongs to the employer by default,
but the terms differ, and a company's internal documents usually contain trade secrets
as well.

---

# Liability for harm

Separate from copyright. It arises when a decision was made on the methodology and caused
a loss.

**Open licenses contain a disclaimer of warranties.** MIT states outright that the material
is provided "as is", without warranty of any kind. That is standard and sufficient protection
for most cases, and one more reason to apply a license rather than leave the file without one.

**Regulated areas require more.** Medicine, law, finance, psychotherapy, safety: besides
a license you need an explicit note in the file itself, covering the area of application
and the fact that the material does not replace professional advice.

**What increases the risk and therefore calls for care:**

- promising a specific outcome in the description;
- wording that reads as a personal recommendation;
- the absence of boundaries of applicability, which makes any incorrect application look
  like a defect of the method.

**Boundaries of applicability work here too.** A method that honestly describes where it fails
is better protected than one claiming universality, and that is the same criterion of quality.

---

# What to do if a claim arrives

**Don't delete silently and don't argue publicly.** Both moves worsen your position.

**The order:**

1. **Record what exactly is being claimed:** reproduction of text, use of a name,
   appropriation of authorship, breach of access terms. These are different claims with
   different remedies.
2. **Check by your own procedure:** run the "strip the borrowings" test. If the file falls
   apart, the claim has grounds, and the fix is rewriting.
3. **Answer on the substance, and quickly.** Most claims close with attribution, a rewrite
   of the disputed fragment, or dropping a name.
4. **For commercial distribution or an unsettled dispute, go to a lawyer** rather than into
   correspondence.

**What helps in advance:** a preserved working archive of digests with sources and dates.
It shows the method was extracted rather than copied, and it reconstructs the history
of every decision.

---

# The gate before publication

The legal rules are spread through the file because they apply at different moments.
**Here they are collected into one pass.** Run it before the result goes anywhere beyond
your own disk.

⚠️ **Open publication is irreversible.** Copies that have spread cannot be recalled, and
a license does not change retroactively for those who already downloaded it. This gate
is the last point where everything is still cheap.

**The pass:**

- [ ] **The "strip the borrowings" test passes**, the file does not fall apart without
      verbatim fragments
- [ ] **The source's license has been checked**, it is not CC BY-SA, NC, or ND, or the
      restrictions have been accounted for
- [ ] **Examples and metaphors are your own**, not carried over
- [ ] **The structure is your own**, it does not reproduce the source's contents page
- [ ] **Diagrams have been rebuilt**, no original images pasted in
- [ ] **Personal data removed**: names, companies, sums from cases
- [ ] **Names of other people's frameworks** appear only as references, not in the skill's
      name
- [ ] **No transcript fragments in the file**, in the body or in appendices
- [ ] **The result's license is set** and matches the purpose
- [ ] **Sources are credited** with the phrasing "based on public materials"
- [ ] **For regulated areas**, the note on application is in the file

**If even one item fails, publication waits.** Fixing it before release costs an hour;
after release it costs a dispute.

**What to tell the user at this step.** Name what has been checked and what is left to their
decision: whether to contact the author of the source, which license to apply, whether
to publish at all. **The decision to publish is theirs.** Your job is to make sure it is taken
with knowledge of the risks rather than blind.

---
