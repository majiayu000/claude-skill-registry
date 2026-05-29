---
name: mermaid-reverse-attempt
description: Mermaid URL codec - encodes/decodes #base64: (amp CLI) and #pako: (mermaid.live) formats
---

# Mermaid Reverse Attempt

Encode diagrams to shareable URLs, decode URLs back to source.

## Formats Discovered

| Prefix | Source | Method |
|--------|--------|--------|
| `#base64:` | amp CLI | `JSON.stringify({code}) → base64` |
| `#pako:` | mermaid.live | `pako.deflate(JSON.stringify({code})) → base64` |

## Usage

```bash
# Encode diagram to pako URL (compressed)
node scripts/codec.js encode-pako < diagram.mmd

# Encode to base64 URL (amp style)
node scripts/codec.js encode-base64 < diagram.mmd

# Decode URL to diagram
node scripts/codec.js decode "https://mermaid.live/edit#pako:..."
```

## Quick Reference

```javascript
// Decode
const hash = url.split('#')[1];
if (hash.startsWith('pako:')) {
  return JSON.parse(pako.inflate(Buffer.from(hash.slice(5), 'base64'), {to:'string'})).code;
}
if (hash.startsWith('base64:')) {
  return JSON.parse(Buffer.from(hash.slice(7), 'base64').toString()).code;
}

// Encode pako
`https://mermaid.live/edit#pako:${Buffer.from(pako.deflate(JSON.stringify({code:diagram}))).toString('base64')}`
```

## GF(3)

- Trit: 0 (ERGODIC)
- decode ∘ encode = id
