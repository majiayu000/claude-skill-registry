---
name: artifact
description: Add non-text files to a person's artifacts folder. Use when saving images, documents, or other files related to someone. Trigger words: artifact, save image, add photo, attach file, store document.
---

# Person Artifact Storage

Add images, documents, or other non-text files to a person's artifacts folder.

## Process

1. **Parse the input**: Extract person name and file path
   - `/artifact lucy ~/Downloads/chess-game.png` → name: "lucy", file: "~/Downloads/chess-game.png"
   - `/artifact e ~/Desktop/project-notes.pdf` → name: "e", file: "~/Desktop/project-notes.pdf"

2. **Verify person exists**:
   ```bash
   ls ~/.claude-mind/memory/people/{name}/
   ```
   If not, ask whether to create them first.

3. **Ensure artifacts directory exists**:
   ```bash
   mkdir -p ~/.claude-mind/memory/people/{name}/artifacts
   ```

4. **Copy the file**:
   ```bash
   cp "{source_path}" ~/.claude-mind/memory/people/{name}/artifacts/
   ```
   Preserve the original filename unless there's a conflict.

5. **Optionally add context note**: Ask if the user wants to add a note about this artifact to the profile
   - What is this file?
   - Why is it significant?
   - When was it from?

6. **Confirm**: Report success and the artifact's new location

## Guidelines

- **Preserve filenames**: Keep original names when possible
- **Handle conflicts**: If filename exists, ask before overwriting or suggest renaming
- **Add context**: A file without context loses meaning over time
- **Supported types**: Images, PDFs, documents, screenshots - anything meaningful

## Examples

**Simple storage:**
```
/artifact cal ~/Downloads/system-diagram.png
```
→ Copies to `memory/people/cal/artifacts/system-diagram.png`

**With context:**
```
/artifact e ~/Pictures/beach-sunset.jpg
```
→ Copies file, then asks "Want to add a note about this photo?"

**Natural trigger:**
```
"Save this screenshot to Dawn's folder"
```
→ Copies screenshot, prompts for context
