---
name: move-frame
description: Move, reorder, or relocate beamer slides/frames within a .tex file or across files. Use this when asked to move slides, reorder presentations, or move frames to backup.
argument-hint: <file.tex> [--list | --from N --to M]
allowed-tools: Bash, Read
---

# Move Beamer Frame Tool

Use `tools/move_frame.py` to move or reorder beamer frames in LaTeX presentations.

## Usage

**List all frames:**
```bash
python tools/move_frame.py $ARGUMENTS[0] --list
```

**Move a single frame:**
```bash
python tools/move_frame.py <file>.tex --from N --to M
```

**Move a range of frames:**
```bash
python tools/move_frame.py <file>.tex --from N-M --to P
```

**Delete frames:**
```bash
python tools/move_frame.py <file>.tex --from N --delete
python tools/move_frame.py <file>.tex --from N-M --delete
```

**Cross-file moves:**
```bash
python tools/move_frame.py source.tex -o dest.tex --from N --to M
python tools/move_frame.py source.tex -o dest.tex --from N --to M --copy  # keep original
```

## Workflow

1. First use `--list` to see frame numbers and titles
2. Then use `--from N --to M` to move frames

## Important

- Frame numbers are 1-indexed
- ALWAYS use this tool for moving slides - do NOT manually cut/paste frame content
- The tool handles preceding comments and properly parses `\begin{frame}...\end{frame}` blocks
