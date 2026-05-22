---
name: gemini-pro
description: "Use Gemini Pro for deep reasoning: complex analysis, domain expertise, nuanced explanations, research, detailed knowledge."
allowed-tools: Bash, Read
---

# Gemini Pro (via ocw)

Powerful reasoning. Best for: complex analysis, domain expertise, research.
**No edit/write permissions** - read-only analysis.

## Create Session

```bash
ocw new pro
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
ocw chat <hash> -f /path/to/file << 'EOF'
analyze in depth
EOF
```

## List Sessions

```bash
ocw list
```
