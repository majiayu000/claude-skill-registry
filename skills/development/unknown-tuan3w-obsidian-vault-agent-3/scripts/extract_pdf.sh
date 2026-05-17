#!/bin/bash
set -euo pipefail

# extract_pdf.sh — Extract text from a PDF, split into per-page files,
# and write quality metadata.
#
# Usage: extract_pdf.sh <pdf_path> <output_dir>

# ── Arguments ──────────────────────────────────────────────────────────
PDF_PATH="${1:-}"
OUTPUT_DIR="${2:-}"

if [[ -z "$PDF_PATH" || -z "$OUTPUT_DIR" ]]; then
    echo "Usage: extract_pdf.sh <pdf_path> <output_dir>" >&2
    exit 1
fi

# ── Dependency check ──────────────────────────────────────────────────
if ! command -v pdftotext &> /dev/null; then
    echo "Error: pdftotext not found." >&2
    echo "Install it with:" >&2
    echo "  macOS:  brew install poppler" >&2
    echo "  Ubuntu: sudo apt-get install poppler-utils" >&2
    exit 1
fi

# ── Input validation ─────────────────────────────────────────────────
if [[ ! -f "$PDF_PATH" ]]; then
    echo "Error: File not found: $PDF_PATH" >&2
    exit 1
fi

# ── Setup output directories ─────────────────────────────────────────
mkdir -p "$OUTPUT_DIR/pages"

# ── Extract full text ─────────────────────────────────────────────────
pdftotext -layout "$PDF_PATH" "$OUTPUT_DIR/full_text.txt"

# ── Get page count ────────────────────────────────────────────────────
TOTAL_PAGES=0
if command -v pdfinfo &> /dev/null; then
    TOTAL_PAGES=$(pdfinfo "$PDF_PATH" 2>/dev/null | awk '/^Pages:/ { print $2 }')
fi

# Fallback: count form feed characters + 1 (last page has no trailing FF)
if [[ "$TOTAL_PAGES" -eq 0 || -z "$TOTAL_PAGES" ]]; then
    FF_COUNT=$(tr -cd '\f' < "$OUTPUT_DIR/full_text.txt" | wc -c | tr -d ' ')
    if [[ "$FF_COUNT" -gt 0 ]]; then
        TOTAL_PAGES=$((FF_COUNT + 1))
    else
        TOTAL_PAGES=1
    fi
fi

# ── Quality metrics ───────────────────────────────────────────────────
FULL_TEXT="$OUTPUT_DIR/full_text.txt"

# Total characters and printable characters (letters, digits, punctuation, space)
TOTAL_CHARS=$(wc -c < "$FULL_TEXT" | tr -d ' ')
if [[ "$TOTAL_CHARS" -gt 0 ]]; then
    PRINTABLE_CHARS=$(tr -cd '[:print:]\n\t' < "$FULL_TEXT" | wc -c | tr -d ' ')
    # Use awk for floating-point division
    PRINTABLE_RATIO=$(awk "BEGIN { printf \"%.2f\", $PRINTABLE_CHARS / $TOTAL_CHARS }")
else
    PRINTABLE_RATIO="0.00"
fi

# Word count and words per page
WORD_COUNT=$(wc -w < "$FULL_TEXT" | tr -d ' ')
if [[ "$TOTAL_PAGES" -gt 0 ]]; then
    WORDS_PER_PAGE=$(awk "BEGIN { printf \"%d\", $WORD_COUNT / $TOTAL_PAGES }")
else
    WORDS_PER_PAGE=0
fi

# ── Determine fallback need ──────────────────────────────────────────
NEEDS_FALLBACK=false
if awk "BEGIN { exit ($PRINTABLE_RATIO < 0.5) ? 0 : 1 }"; then
    NEEDS_FALLBACK=true
fi
if [[ "$WORDS_PER_PAGE" -lt 20 ]]; then
    NEEDS_FALLBACK=true
fi

# ── Split into per-page files ────────────────────────────────────────
# Use awk to split on form feed (ASCII 12) characters
awk -v outdir="$OUTPUT_DIR/pages" '
BEGIN { page = 1; file = sprintf("%s/page_%03d.txt", outdir, page) }
{
    # Split the line on form feeds
    n = split($0, parts, "\f")
    for (i = 1; i <= n; i++) {
        if (i > 1) {
            close(file)
            page++
            file = sprintf("%s/page_%03d.txt", outdir, page)
        }
        print parts[i] > file
    }
}
END { close(file) }
' "$FULL_TEXT"

# ── Title from filename ──────────────────────────────────────────────
BASENAME=$(basename "$PDF_PATH")
TITLE="${BASENAME%.pdf}"
TITLE="${TITLE%.PDF}"

# ── Write metadata.json ──────────────────────────────────────────────
cat > "$OUTPUT_DIR/metadata.json" <<EOF
{
  "title": "$TITLE",
  "format": "pdf",
  "total_pages": $TOTAL_PAGES,
  "words_per_page": $WORDS_PER_PAGE,
  "printable_ratio": $PRINTABLE_RATIO,
  "needs_fallback": $NEEDS_FALLBACK,
  "extraction_tool": "pdftotext"
}
EOF

echo "Extraction complete: $TOTAL_PAGES pages → $OUTPUT_DIR"
echo "  Words/page: $WORDS_PER_PAGE | Printable ratio: $PRINTABLE_RATIO | Needs fallback: $NEEDS_FALLBACK"
