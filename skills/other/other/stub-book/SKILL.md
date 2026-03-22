---
name: stub-book
description: Stub out a new book review file with front matter and template captures. Use when adding a new book to _books/.
---

# Stub Book Skill

Create a new book review stub in `_books/` with full front matter and
standard capture blocks.

## Usage

`/stub-book <title>` --- Create a stub for the given book title.

The user may also provide author, series, book number, or a Wikidata QID.
If not provided, look them up.

## Steps

### 1. Determine Book Details

From the user's input, establish:
- **Title** (required)
- **Author** (required)
- **Series** and **book number** (null if standalone)

If the book is part of a series already reviewed on the site, check an
existing entry in `_books/` for the correct author name, series name, and
series numbering convention.

### 2. Find the Wikidata QID

If the user did not provide a QID, search for one:

```bash
cd _scripts/metadata && uv run fetch_book_metadata.py "Book Title"
```

The script prints numbered search results to stderr and picks the first
match by default. **Read the results carefully.** Look for the entry
described as the original novel/work, not a specific edition or
translation.

- If the top result is wrong (e.g., a 2000 Baen edition instead of the
  1993 original novel), note the correct QID from the list and pass it
  to `--qid` in step 3. There is no need to re-run the search script;
  the QID is all the stub script needs.
- If the results are all wrong or empty, the book has no Wikidata entry.
  Proceed to step 3 without a QID.

### 3. Run the Stub Script

The script at `scripts/stub_book.py` (relative to this skill) assembles
the complete file. Run it from the **project root**:

```bash
uv run .claude/skills/stub-book/scripts/stub_book.py \
    --title "The Honor of the Queen" \
    --author "David Weber" \
    --series "Honor Harrington" \
    --book-number 2 \
    --qid Q3400447 \
    --output _books/the_honor_of_the_queen.md
```

**With a QID:** The script calls `fetch_book_metadata.py` internally to
get `isbn`, `date_published`, and `same_as_urls`.

**Without a QID:** Omit `--qid`. The script produces a stub without
`wikidata_qid`, `isbn`, `date_published`, or `same_as_urls`. These can
be added later if a Wikidata entry is created.

**Without a series:** Omit `--series` and `--book-number`. The script
adjusts the opening paragraph and omits the `this_series` capture.

Use `--output` to write directly to `_books/<snake_case_title>.md`, or
omit it to print to stdout.

### 4. Post-Processing

After the script runs, check for issues that need manual fixes:

#### Refine `date_published`

The Wikidata date may be year-only (e.g., `1993`). Existing entries use
`YYYY-MM` format (e.g., `1993-04`). Search Goodreads or the publisher's
site for a more specific date and update the front matter.

#### Check the ISBN

The script takes the first ISBN it finds. This may be a foreign-language
edition. If so, search the Wikidata edition entities for an
English-language ISBN, or find one on the publisher's site. The ISBN
should be ISBN-13 format (978-...).

#### Verify `same_as_urls`

The work-level Wikidata entity (the original novel, not a specific
edition) will have the richest set of `same_as_urls`. If you had to use
an edition QID instead, the URLs may be sparse. Check whether the work
entity exists separately and use its QID if possible.

### 5. Report

Tell the user what was created and flag remaining manual steps:
- Cover image needs to be added at the `image` path.
- `rating` and `date` need updating after the review is written.
- Any metadata issues found in step 4.
