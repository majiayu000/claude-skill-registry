---
name: pdf
description: Generate a PDF from a markdown note file via pandoc + xelatex with mermaid diagram support.
---

When the user asks to generate a PDF from a markdown note file, follow this workflow:

1. **Determine the input file**: The user will provide a path or dendron note name. Resolve it to a filename relative to `notes/` (e.g., `swanki.processing.pdf_processor.md`).

2. **Determine the output filename**: Strip the `.md` extension from the input filename to use as the output name (e.g., `swanki.processing.pdf_processor`).

3. **Run the PDF generation script**:

   ```bash
   bash notes/assets/publish/scripts/bib_tex_pdf.sh <input_filename> . <output_filename>
   ```

   - First arg: markdown filename (relative to `notes/`)
   - Second arg: always `.` (output dir, relative to `notes/` after the script's internal `cd ./notes`)
   - Third arg: output PDF name without extension

4. **Verify the output**: Check that `notes/assets/pdf-output/<output_filename>.pdf` exists.

5. **Report the result**: Tell the user the path to the generated PDF and note any warnings (e.g., missing citations).

## Important Notes

- The script uses `SCRIPT_DIR` to derive `NOTES_DIR`, so all paths are resolved automatically
- The script uses `mermaid-filter` for diagram rendering -- if mermaid diagrams produce empty PNGs, the env vars `MERMAID_FILTER_LOC`, `MERMAID_FILTER_SCALE`, `MERMAID_FILTER_WIDTH` may need to be set (the script handles this)
- Unicode emojis will cause xelatex to fail -- if the PDF build fails, check for emojis and replace with plain text alternatives before retrying
- Use a 120s timeout for the bash command since PDF generation can be slow

## Example Invocations

- "/pdf notes/swanki.processing.pdf_processor.md"
- "/pdf swanki.processing.pdf_processor.md"
- "generate pdf for the processing module note"
