---
name: find-overfull
description: Find pages with overfull boxes (content that doesn't fit) in LaTeX presentations. Use when checking for layout issues or content overflow.
argument-hint: <file.tex>
allowed-tools: Bash, Read
---

# Find Overfull Boxes Tool

Use `tools/find_overfull.py` to find overfull hbox/vbox warnings in LaTeX log files.

## Usage

**Basic usage (parses .log file for a .tex file):**
```bash
python tools/find_overfull.py $ARGUMENTS[0]
```

**Filter by box type:**
```bash
python tools/find_overfull.py <file>.tex --vbox-only  # vertical overflow (too tall)
python tools/find_overfull.py <file>.tex --hbox-only  # horizontal overflow (too wide)
```

**Filter by severity:**
```bash
python tools/find_overfull.py <file>.tex --min-badness 10  # only boxes > 10pt overfull
```

**Output formats:**
```bash
python tools/find_overfull.py <file>.tex --pages-only  # just page numbers, one per line
python tools/find_overfull.py <file>.tex --json        # JSON format
```

## Output

The tool reports:
- Page number where overflow occurs
- Type (hbox = too wide, vbox = too tall)
- How much it overflows (in pt)
- Source line number in .tex file
- Context (problematic content)

## Notes

- Requires the .log file to exist (run pdflatex first)
- Looks in `build/` directory for log files by default
