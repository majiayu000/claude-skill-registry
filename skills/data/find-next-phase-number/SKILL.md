---
name: find-next-phase-number
description: Determine the next sequential phase ID for creating a new phase. Use when planning a new phase.
user-invocable: true
---

# Next Phase Number

## How to Find Next ID

Run this command to determine the next available phase number:

```bash
current=$(ls -1 .ushabti/phases/ 2>/dev/null | sed 's/-.*//' | sort -n | tail -1)
if [ -z "$current" ]; then
  echo "0001 (first phase)"
else
  printf "%04d (after %s)\n" $((10#$current + 1)) "$current"
fi
```

## Phase Numbering Convention

- Phase IDs are 4-digit, zero-padded integers: `0001`, `0002`, `0003`, ...
- Combined with a slug: `0001-initial-setup`, `0002-add-auth`, ...

## Creating the Directory

Once you have the next number and a slug:
```bash
mkdir -p .ushabti/phases/NNNN-your-slug
```

Replace `NNNN` with the next ID and `your-slug` with a short, lowercase, hyphenated description.
