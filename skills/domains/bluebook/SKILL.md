---
name: bluebook
description: This skill should be used when the user asks to "cite a case", "format a citation", "check Bluebook format", "cite a statute", "use id. or supra", "format footnotes", "cite a law review article", or needs Bluebook 21st Edition citation guidance. Covers cases, statutes, secondary sources, signals, and short forms.
---

# Bluebook 21st Edition Citation

Citation formatting for law reviews and legal scholarship per *The Bluebook: A Uniform System of Citation* (21st ed. 2020).

**Announce:** "I'm using the bluebook skill for citation formatting."

## When to Use

Invoke this skill for:
- Formatting case citations (federal, state, foreign)
- Statutory and regulatory citations
- Secondary sources (books, articles, treatises)
- Short form citations (id., supra, hereinafter)
- Introductory signals and parentheticals
- Citation sentences vs. citation clauses

**For legal writing style**: Use `/writing-legal` skill (Volokh)
**For general writing**: Use `/writing` skill (Strunk & White)

<EXTREMELY-IMPORTANT>
## IRON LAW #1: NO CITATION WITHOUT VERIFICATION

**If you haven't verified EVERY element of a citation, DO NOT write it.**

Before writing ANY citation:
1. Verify case name spelling and procedural posture
2. Verify reporter volume and page numbers
3. Verify court and year
4. Verify pinpoint page exists

**Guessing reporter volumes or page numbers is LYING. Period.**
</EXTREMELY-IMPORTANT>

<EXTREMELY-IMPORTANT>
## IRON LAW #2: NO SHORT FORMS WITHOUT FULL CITATION FIRST

**Id., supra, and hereinafter REQUIRE a preceding full citation.**

Before using ANY short form:
1. Locate the full citation in the document
2. Verify no intervening citations (for id.)
3. Verify the supra reference is unambiguous

**Using id. after intervening citations creates ambiguity. Delete and cite in full.**
</EXTREMELY-IMPORTANT>

<EXTREMELY-IMPORTANT>
## IRON LAW #3: FOOTNOTE VS. TEXT CITATION FORMAT

**Law review citations use footnote format (Rule 1). Court documents use text format (Bluepages).**

```
FOOTNOTE (law reviews):    Smith v. Jones, 500 U.S. 1, 5 (1991).
TEXT (court documents):    Smith v. Jones, 500 U.S. 1, 5 (1991)

FOOTNOTE (statutes):       18 U.S.C. § 1001 (2018).
TEXT (statutes):           18 U.S.C. § 1001 (2018)
```

**If writing for a law review and using text format conventions, DELETE and reformat.**
</EXTREMELY-IMPORTANT>

## The Gate Function

Before writing ANY citation:

```
1. IDENTIFY → What type of source? (case, statute, article, book)
2. LOCATE   → Find the correct rule in Bluebook
3. VERIFY   → Confirm ALL elements (volume, page, court, year)
4. FORMAT   → Apply correct typeface and punctuation
5. CHECK    → Does this match examples in the rule?
6. WRITE    → Only after steps 1-5
```

**Skipping any step produces unreliable citations.**

## Rationalization Table - STOP If You Think:

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "I'm pretty sure that's the volume" | Pretty sure = wrong | VERIFY with actual source |
| "Id. is close enough" | Intervening cite breaks id. | Use full short form |
| "This signal seems right" | Wrong signals mislead readers | CHECK rule 1.2 examples |
| "The parenthetical isn't needed" | Parentheticals explain relevance | ADD what the source says |
| "I'll fix the pinpoint later" | Pinpoints prove claims | ADD pinpoint NOW |
| "Small caps isn't that important" | Typeface is mandatory | APPLY correct typeface |
| "This abbreviation is obvious" | Wrong abbreviations fail | CHECK tables T6, T10, T12 |

## Red Flags - STOP Immediately If:

- "Let me guess the reporter volume" → NO. Verify the actual cite.
- "Id. probably works here" → NO. Check for intervening citations.
- "Supra will point them back" → NO. Verify the full citation exists.
- "I'll use the common abbreviation" → NO. Use Bluebook tables.
- "Close enough on the page number" → NO. Exact pinpoints required.

## Quick Reference: Common Citation Forms

### Cases (Rule 10)

```
Full citation:
Brown v. Board of Education, 347 U.S. 483, 495 (1954).

Short form (same footnote or five footnotes with no intervening):
Id. at 496.

Short form (different footnote, no intervening):
Brown, 347 U.S. at 497.

Short form (intervening citations):
Brown v. Board of Education, 347 U.S. at 498.
```

### Statutes (Rule 12)

```
Full citation:
42 U.S.C. § 1983 (2018).

Multiple sections:
42 U.S.C. §§ 1983-1985 (2018).

Short form:
§ 1983 or id. § 1984
```

### Law Review Articles (Rule 16)

```
Full citation:
Cass R. Sunstein, *On the Expressive Function of Law*, 144 U. Pa. L. Rev. 2021, 2030 (1996).

Short form:
Sunstein, supra note 12, at 2035.
```

### Books (Rule 15)

```
Full citation:
Richard A. Posner, Economic Analysis of Law 45 (9th ed. 2014).

Short form:
Posner, supra note 5, at 52.
```

## Typeface Rules (Rule 2)

| Source Type | Law Review Format |
|-------------|-------------------|
| Case names | Italics: *Brown v. Board* |
| Book titles | Small caps: ECONOMIC ANALYSIS OF LAW |
| Article titles | Italics: *On the Expressive Function* |
| Journal names | Small caps: U. PA. L. REV. |
| Periodical names (non-consecutively paginated) | Italics: *N.Y. Times* |
| Statutes | Roman: 42 U.S.C. § 1983 |

## Introductory Signals (Rule 1.2)

| Signal | Meaning | Use When |
|--------|---------|----------|
| [no signal] | Direct support | Source directly states proposition |
| *See* | Implicit support | Source supports but doesn't directly state |
| *See, e.g.,* | One of several | Multiple sources support; citing representative |
| *Cf.* | Analogous support | Source supports by analogy |
| *Compare* ... *with* | Comparison | Sources illustrate through contrast |
| *See generally* | Background | Source provides helpful background |
| *But see* | Contradiction | Source contradicts proposition |
| *Contra* | Direct contradiction | Source directly contradicts |

### Signal Order (Rule 1.3)

Within a single citation sentence, signals appear in this order:
1. [no signal]
2. *E.g.,*
3. *Accord*
4. *See*
5. *See also*
6. *Cf.*
7. *Compare*
8. *Contra*
9. *But see*
10. *But cf.*
11. *See generally*

## Common Errors Checklist

### Case Citations

- [ ] Party names shortened properly (omit "Inc.", "Ltd." unless only identifier)
- [ ] "United States" abbreviated to "U.S." (as party, not "United States of America")
- [ ] Reporter abbreviation matches T1
- [ ] Court identifier included unless obvious from reporter
- [ ] Year is decision year, not argument year
- [ ] Pinpoint included for specific propositions

### Statutory Citations

- [ ] Current official code used (not session laws for current statutes)
- [ ] Section symbol (§) used, not "Section"
- [ ] Space between § and number
- [ ] Year is code edition year, not enactment year
- [ ] Supplements cited when applicable

### Short Forms

- [ ] Full citation appears earlier in same document
- [ ] Id. used only when no intervening citation
- [ ] Supra refers to footnote number where full cite appears
- [ ] Hereinafter defined in first full citation

## Progressive Disclosure

For detailed rules, consult:

### Reference Files

- **`references/cases.md`** - Complete case citation rules (R. 10)
- **`references/statutes.md`** - Statutory and regulatory citations (R. 12-14)
- **`references/secondary-sources.md`** - Books, articles, treatises (R. 15-17)
- **`references/short-forms.md`** - Id., supra, hereinafter rules (R. 4)
- **`references/signals-parentheticals.md`** - Signals, parentheticals, order (R. 1)

### When to Load References

Load the specific reference when:
- Formatting an unfamiliar source type
- Encountering edge cases (unpublished cases, foreign sources)
- Checking state-specific reporter requirements
- Working with complex statutory schemes
- Formatting international materials

## Integration

Use with `/writing-legal` for complete legal scholarship workflow:
1. `/bluebook` formats citations correctly
2. `/writing-legal` ensures argument structure and evidence handling
3. `/ai-anti-patterns` catches AI writing indicators before submission

## Delete & Restart Pattern

**When to delete and restart:**

1. **Citation uses guessed page numbers** → Delete, verify source, cite with real numbers
2. **Id. follows intervening citation** → Delete id., use full short form
3. **Wrong signal used** → Delete, reread Rule 1.2, apply correct signal
4. **Typeface incorrect** → Delete, apply Rule 2 typeface
5. **Abbreviation doesn't match Bluebook tables** → Delete, use table abbreviation

**How to restart:**

```
Old: See Smith v. Jones, 500 U.S. at 15. Id. at 20. [intervening cite] Id. at 25.
New: See Smith v. Jones, 500 U.S. at 15. Id. at 20. [intervening cite] Smith, 500 U.S. at 25.
```

The third cite cannot use id. after an intervening citation.
