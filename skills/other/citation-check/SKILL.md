---
name: citation-check
description: Audit citation existence and fabrication risk, in-text/reference parity, DOIs, claim support, and style.
---

# Citation Integrity Auditor

## Heritage and scope

This is an original Open Science Skills workflow adapted for experimental social science. It remixes general citation-check and source-verification ideas from Cheng-I Wu's *Academic Research Skills for Claude Code* (CC BY-NC 4.0), especially the separation between citation formatting, existence checks, DOI checks, and uncertainty reporting. Do not copy ARS prose into reports; apply the workflow below.

## Instructions

### 1. Orient before checking

Identify the inputs and constraints:

- Manuscript source: LaTeX, Markdown, Word export, PDF text, or pasted prose.
- Bibliography source: `.bib`, CSL JSON, Zotero export, reference section, footnotes, or mixed.
- Target style: default to APA 7 unless the user names a journal or style.
- Scope: whole manuscript, one section, bibliography only, or DOI-only pass.
- Tool availability: if web lookup, Crossref, DataCite, DOI.org, Semantic Scholar, or OpenAlex are unavailable, mark verification status as `NOT CHECKED` rather than guessing.
- For LaTeX/BibTeX, drive the audit off the keys actually `\cite`d in the manuscript (follow `\input`/`\include`), not every entry in a master `.bib`. Only cited keys reach the printed reference list, which is what readers and critics actually check.
- Note the bibliography style. Many common styles (`apalike`, `plain`, `unsrt`) do not render the `doi` field, so a wrong or dead DOI is invisible in the compiled PDF and ranks as source-hygiene unless the style prints it. Author, year, title, volume, issue, and pages do render — prioritize those for any artifact that is already public.

### 2. Build the citation inventory

Create two inventories before judging errors:

- **In-text inventory:** every author-year, parenthetical, narrative, footnote, or numeric citation appearing in the manuscript.
- **Reference inventory:** every bibliography entry, including entry key if present, authors, year, title, outlet, DOI/URL, publication status, and notes.

Normalize cautiously:

- Treat spelling variants, diacritics, hyphenated surnames, particles (`de`, `van`, `von`), and organizational authors as possible matches until checked.
- For multiple works by the same author-year, verify `a/b/c` suffixes are assigned consistently.
- For BibTeX, preserve the entry key and report it with every finding.

### 3. Run structural checks

Report:

- Cited in text but missing from references.
- In references but never cited.
- Author-year mismatch between in-text citation and reference entry.
- Duplicate bibliography entries for the same work.
- Ambiguous citations where two reference entries could satisfy one in-text citation.
- Broken cross-references caused by LaTeX/BibTeX key drift.

Do not "fix" ambiguous cases silently. List the likely match and the evidence.

### 4. Verify source existence and identifiers

This is the highest-stakes check: confirm each cited work actually exists and that its identifier points to *that* work. Hallucinated citations — a real author with a plausible but nonexistent title, or a DOI that resolves to a different paper — are the failure mode that ends careers. Use programmatic indexes first; they are near-deterministic and resist hallucination.

**Concrete lookups (via web fetch):**

- Crossref bibliographic search: `https://api.crossref.org/works?rows=5&query.bibliographic=<URL-encoded "title first-author year">`. Compare returned title/authors/year/DOI. Append `&mailto=<email>` for the polite pool. On HTTP 429, fall back to OpenAlex.
- DOI resolution: `https://api.crossref.org/works/<doi>` (or `https://doi.org/<doi>`). Confirm the resolved title **and** authors match *this* entry. A DOI that resolves to a *different* real work is the single most common LLM-fabrication signature — never treat "DOI resolves" as "DOI correct."
- OpenAlex: `https://api.openalex.org/works?search=<URL-encoded title>` or `?filter=doi:<doi>`. Independent index; use when Crossref is rate-limited or for abstracts.
- Exact-title test: search the title in quotation marks. Zero hits anywhere is a strong fabrication signal.
- Author-corpus cross-check (catches the "fabricated title grafted onto a real author" pattern): query the real author's works (`...query.author=<name>`) and confirm the cited title appears in their corpus. A real author + nonexistent title + invented co-authors/venue is the classic hallucination.

**Tiered fallback by source type:**

- Journal articles → Crossref / OpenAlex / DOI resolution.
- Books and chapters → publisher page, WorldCat, Google Books, OpenAlex. Book DOIs are spotty and frequently 404 even for real books; a dead book DOI is usually source-hygiene, not a missing source.
- Datasets and official statistics → the issuing archive (ISSP, V-Dem, ANES, KGSS, national election studies, government statistical catalogues). Verify the catalogue/series number resolves to the *cited* title — a real catalogue number attached to the wrong title is a fabrication tell.
- Grey literature / government / internal reports → the issuing agency's own site (`site:` search). If untraceable, classify as `NEEDS AUTHOR VERIFICATION`, not fabricated — an insider or co-author may be citing a real internal document.
- News / web items → confirm the named outlet actually ran the piece.
- Preprints / "forthcoming" → SSRN, arXiv, SocArXiv, OSF, author pages/CVs, conference programs. A forthcoming item's year is inherently uncertain; prefer the authors' own current listing.

**Labels:**

- `MISSING DOI`: likely DOI exists but is absent.
- `NO DOI FOUND`: searched, none found; not necessarily an error.
- `DEAD DOI`: the identifier 404s (common for real book DOIs).
- `DOI RESOLVES TO DIFFERENT WORK`: DOI is live but points to another paper — high-signal hallucination tell.
- `METADATA MISMATCH`: real work, wrong year/volume/issue/pages/author names.
- `TITLE DRIFT`: cited title differs materially from the indexed title.
- `STATUS UPDATE`: working paper/preprint now has a journal/book version.
- `NEEDS AUTHOR VERIFICATION`: no programmatic match, but plausibly real grey literature.
- `LIKELY FABRICATED`: no trace after identifier, exact-title, **and** author-corpus searches. Reserve for genuine non-existence, but do not shy away from it when the evidence is clear.

**Do NOT over-flag these as fabricated:**

- Double-blind anonymization placeholders (e.g. `title={Article withheld for review}`, author `{Author}`) — intentional blinding stubs, not citations.
- The author's own work (self-citations) — flag metadata conflicts for the author to reconcile (their CV vs the canonical published record) rather than silently overwriting; the author is the authority on their own paper.

**High-stakes audits (publication or public posting):** run a second, independent verification pass with different framing, defaulting to "fabricated until independently confirmed" for any suspect. A single pass misses real items; independent passes catch each other's gaps. When remediating rather than only reporting, never invent a replacement — substitute only a real, verified source (ideally the one the author intended), confirm any new DOI resolves to the right work before writing it, and re-verify the fix renders as expected.

### 5. Check style and completeness

For APA 7 and most social-science journal styles:

- DOI should be a URL form when available: `https://doi.org/...`.
- Do not add a period after DOI or URL.
- Journal articles need article title, journal title, volume, issue when available, pages or article number, and DOI when available.
- Books need publisher; edited chapters need editors, book title, page range, publisher.
- Reports and datasets need institutional author, date, title, publisher/archive, version if relevant, and URL/DOI.
- Data, code, and materials should be cited as research products, not buried only in availability statements.

When target style is not APA, apply the target style but still keep the integrity checks above.

### 6. Audit evidentiary use

For literature reviews and theory sections, sample the most important citations and classify how they are used:

- **Background:** source establishes context only.
- **Claim support:** source is used as evidence for a substantive claim.
- **Method precedent:** source justifies a design, estimator, measurement strategy, or reporting practice.
- **Contrast:** source is cited as an opposing or incomplete account.

Flag overclaiming when the cited source plausibly cannot support the sentence where it appears. If source text is unavailable, mark `SOURCE TEXT NOT CHECKED`.

## Output

Produce a `Citation Audit Report`:

```
# Citation Audit Report

Scope: <files/sections checked>
Target style: <style or journal>
Verification tools used: <Crossref/DataCite/S2/OpenAlex/Web/manual/none>
Summary: <N blocking, N recommended, N minor, N needs-author-verification>

## Blocking Issues
| Location | Entry/key | Issue | Evidence | Fix |

## Recommended Fixes
| Location | Entry/key | Issue | Evidence | Fix |

## Minor Style Issues
| Location | Entry/key | Issue | Fix |

## DOI and Source-Status Table
| Entry/key | Current DOI/URL | Verification status | Suggested action |

## In-text / Reference Parity
| Type | Citation or key | Location | Suggested action |

## Needs Author Verification
| Entry/key | Why unresolved | What author should check |
```

Severity:

- **Blocking:** missing cited reference, wrong DOI, possibly nonexistent source, citation supports a decisive claim but appears wrong, or broken citation build.
- **Recommended:** missing likely DOI, stale working paper, author-year mismatch that is fixable, uncited important reference, incomplete metadata.
- **Minor:** punctuation, capitalization, inconsistent initials, style-only issues.

## Quality checks

- [ ] In-text inventory and reference inventory were built before findings were listed.
- [ ] For BibTeX, the audit covered the actually-cited keys, not just the easy-to-find entries.
- [ ] Every "DOI resolves" was confirmed to resolve to the *cited* work, not merely to resolve.
- [ ] Suspected fabrications were tested with exact-title and author-corpus searches before labeling.
- [ ] Double-blind placeholders, grey literature, and self-citations were not mislabeled as fabricated.
- [ ] For high-stakes audits, an independent second pass was run, or its absence was noted.
- [ ] Every DOI mismatch was based on resolved metadata, not intuition.
- [ ] Unverified sources are labeled as unresolved, not fabricated.
- [ ] Existing author-year suffixes were checked for consistency.
- [ ] Data/code/material citations were included when relevant.
- [ ] The report distinguishes integrity errors from style issues.
- [ ] ARS-derived workflow ideas are attributed when this skill's structure is reused outside this repository.
