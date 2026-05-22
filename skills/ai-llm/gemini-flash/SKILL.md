---
name: gemini-flash
description: "Use Gemini Flash for quick tasks: reading PDFs, processing images, analyzing screenshots, summarizing documents. Fast, cheap, 1M+ token context."
allowed-tools: Bash, Read
---

# Gemini Flash (via ocw)

Fast model. Best for: PDFs, images, summaries, quick analysis.
**No edit/write permissions** - read-only analysis.

## Create Session

```bash
ocw new flash
```

Returns 6-char hash. Save it for all interactions.

## Chat

```bash
ocw chat <hash> << 'EOF'
your prompt
EOF
```

## Chat with File

```bash
ocw chat <hash> -f /path/to/file.pdf << 'EOF'
analyze this
EOF
```

## List Sessions

```bash
ocw list
```
