---
name: docx-processing-openai
description: "Toolkit for comprehensive document reading and creation with visual quality control. Use to work with Word documents (.docx files) for: (1) Reading or extracting content from existing DOCX files, (2) Creating new Word documents with professional formatting, (3) Editing documents requiring precise typography and layout, or any other DOCX reading or generation tasks."
metadata:
  author: OpenAI
  license: Proprietary.
  version: 2025.12.12
---

# DOCX reading, creation, and review guidance

## Reading DOCXs
- Use `soffice -env:UserInstallation=file:///tmp/lo_profile_$$ --headless --convert-to pdf --outdir $OUTDIR $INPUT_DOCX` to convert DOCXs to PDFs.
  - The `-env:UserInstallation=file:///tmp/lo_profile_$$` flag is important. Otherwise, it will time out.
- Then Convert the PDF to page images so you can visually inspect the result:
  - `pdftoppm -png $OUTDIR/$BASENAME.pdf $OUTDIR/$BASENAME`
- Then open the PNGs and read the images.
- Only do python printing as a last resort because you will miss important details with text extraction (e.g. figures, tables, diagrams).

## Primary tooling for creating DOCXs
- Create and edit DOCX files with `python-docx`. Use it to control structure, styles, tables, and lists. Install it with `pip install python-docx` if it's not already installed.
- After **every meaningful batch of edits**—new sections, layout tweaks, styling changes—render the DOCX to PDF:
  - `soffice -env:UserInstallation=file:///tmp/lo_profile_$$ --headless --convert-to pdf --outdir $OUTDIR $INPUT_DOCX`
- Convert the PDF to page images so you can visually inspect the result:
  - `pdftoppm -png $OUTDIR/$BASENAME.pdf $OUTDIR/$BASENAME`
- **Inspect every PNG before moving on.** If you see any defect, fix the DOCX and repeat the render → inspect loop until all pages look perfect.


## Quality expectations
- Aim for a client-ready document: consistent typography, spacing, margins, and layout hierarchy. Heading levels should be obvious, lists aligned, and paragraphs easy to scan.
- Never ship obvious formatting defects such as clipped or overlapping text, default-template styling, broken tables, unreadable characters, or inconsistent bullet styling.
- Charts, tables, and visuals must be legible in the rendered PNGs—no pixelation, misalignment, missing labels, or mismatched colors.
- Never use the U+2011 non-breaking hyphen or other unicode dashes as they will not be rendered correctly. Use ASCII hyphens instead.
- Citations, references, and footnotes must be human-readable and professional. No tool-internal tokens (e.g., `[145036110387964†L158-L160]`), malformed URLs, or placeholder text should be present in the document.
- You must convert all citations into a human-readable format in the document with standard scholarly citation format. No `【【turn1541736113682297662view0†L11-L19】` notations are allowed in the document as the reader cannot interpret them (such citations will be severely penalized).
- Content should be concise, relevant, and free of boilerplate AI phrasing. Ensure each section adds value and flows logically.

## Final checks
- Re-run the DOCX → PDF → PNG loop after your final changes and inspect **every page** at 100% zoom. Look for subtle issues like inconsistent spacing, widows/orphans, or misaligned bullet levels.
- Correct every formatting defect you see in the PNGs, including but not limited to: overlapping text or shapes, clipped text or shapes that are cut off, black squares, broken tables, unreadable characters, etc.
- Only deliver the DOCX once the latest PNG review confirms the document is visually flawless and professionally styled.
- Keep intermediate files organized (or cleaned up) so reviewers can easily locate final outputs.
