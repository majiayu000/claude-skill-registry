---
name: i18n-locale-coverage
description: Safely repair locale JSON coverage gaps (missing files, missing keys, untranslated EN strings) using deterministic validation gates.
---

# i18n Locale Coverage Repair (JSON-Safe, Gate-Driven)

## Scope

Use this skill when Brikette locale JSON files have coverage gaps from `check-i18n-coverage`:
- Missing files
- Missing keys
- Untranslated keys (locale value equals EN)

This skill is the execution runbook for i18n remediation work discovered in `/lp-do-fact-find` and implemented via `/lp-do-build`.

## Core Commitments (Non-Negotiable)

- EN is the source of truth for structure. Do not edit EN in this skill.
- Fix order is strict: missing files -> missing keys -> untranslated keys.
- Validate every file immediately after writing with JSON safety gates.
- Preserve placeholders/tokens exactly. Never translate token syntax.
- No "done later" debt. Any broken JSON or malformed structure is fixed immediately.

## Allowed

- Read/write locale JSON under `apps/brikette/src/locales/{locale}/**/*.json`
- Use `pnpm --filter @apps/brikette check-i18n-coverage` for baseline and verification
- Use EN file as structural template for missing files/keys

## Not Allowed

- Editing `apps/brikette/src/locales/en/**` (unless user explicitly asks)
- Reconstructing locale JSON from scratch when EN copy can be used
- Using external translation APIs/providers for locale completion
- Bulk blind find/replace across locale trees
- Changing key names, key casing, or object/array shape to "make it pass"
- Leaving non-EN locales with copied EN text when proper translation is expected

## Inputs

Required:
- Target scope (`all`, locale list, namespace/file list)

Optional:
- Severity lane (`missing-files-only`, `missing-keys`, `untranslated`)
- Target locale subset with `--locales=<csv>`
- Slice tag for traceability (example: `pl-guides-sunriseHike`)

## Workflow

### 1) Baseline Snapshot (Traceable)

Run from repo root and persist baseline:

```bash
pnpm --filter @apps/brikette check-i18n-coverage --format=json --output=i18n-coverage-report.before.json
```

Record totals and targeted workset before edits.

### 2) Missing Files Lane (First)

For each missing locale file:
1. Create parent directory if needed.
2. Copy EN file byte-for-byte.
3. Translate values in place (do not alter key structure).

Safe creation pattern:

```bash
mkdir -p "$(dirname apps/brikette/src/locales/<locale>/<path>.json)"
cp apps/brikette/src/locales/en/<path>.json apps/brikette/src/locales/<locale>/<path>.json
```

### 3) Missing Keys Lane (Second)

For each file with missing keys:
1. Run Gate D in strict mode to surface deterministic missing-path/type issues for that file.
2. Add only missing keys, preserving EN shape and leaf types.
3. Translate newly added string values.

### 4) Untranslated Keys Lane (Third)

For keys still equal to EN:
1. Replace with natural locale translation.
2. Keep semantic meaning and formatting.
3. Keep URLs, slugs, IDs, placeholders, and token syntax unchanged.

### 5) Per-File JSON Safety Gates (Mandatory)

Run gates in strict order with fail-fast behavior (`set -euo pipefail`). Do not continue after any failed gate.

Gate A: JSON parse

```bash
node -e "JSON.parse(require('fs').readFileSync(process.argv[1], 'utf8'));" apps/brikette/src/locales/<locale>/<path>.json
```

Gate B: No duplicate keys

```bash
python - <<'PY' apps/brikette/src/locales/<locale>/<path>.json
import json, sys
path = sys.argv[1]
def hook(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise SystemExit(f"Duplicate key in {path}: {k}")
        out[k] = v
    return out
with open(path, 'r', encoding='utf-8') as f:
    json.load(f, object_pairs_hook=hook)
print("OK no duplicate keys:", path)
PY
```

Normalization Step C (run only after A+B pass): Canonical JSON formatting

Use repo formatter when available (preferred). Fallback deterministic JSON emitter:

```bash
node -e "const fs=require('fs');const p=process.argv[1];const j=JSON.parse(fs.readFileSync(p,'utf8'));fs.writeFileSync(p,JSON.stringify(j,null,2)+'\n');" apps/brikette/src/locales/<locale>/<path>.json
```

Gate D: EN parity contract (strict type + placeholder + escape semantics + no extra keys)

```bash
node - <<'NODE' apps/brikette/src/locales/en/<path>.json apps/brikette/src/locales/<locale>/<path>.json
const fs = require('fs');
const [enPath, localePath] = process.argv.slice(2);
const en = JSON.parse(fs.readFileSync(enPath, 'utf8'));
const lc = JSON.parse(fs.readFileSync(localePath, 'utf8'));
const errs = [];

const tokenRegexes = [
  /\{\{\s*[^{}]+\s*\}\}/g,
  /%(\d+\$)?[+#0\- ]*(\d+|\*)?(?:\.(\d+|\*))?[sdif]/g,
  /%\([^)]+\)[sdif]/g,
  /<[0-9]+>/g,
  /<\/[0-9]+>/g,
  /<[0-9]+\s*\/>/g,
  /%[A-Z]+:[^%]+%/g,
];

const tokenBag = (s) => {
  const bag = [];
  for (const rx of tokenRegexes) {
    const matches = s.match(rx);
    if (matches) bag.push(...matches);
  }
  return bag.sort();
};

const validateNumericTagNesting = (s) => {
  const tokenRe = /<\/?[0-9]+>|<[0-9]+\s*\/>/g;
  const stack = [];
  for (const token of s.match(tokenRe) || []) {
    if (/^<[0-9]+\s*\/>$/.test(token)) continue;
    if (/^<[0-9]+>$/.test(token)) {
      stack.push(token.slice(1, -1));
      continue;
    }
    const closeId = token.slice(2, -1);
    const openId = stack.pop();
    if (openId !== closeId) return false;
  }
  return stack.length === 0;
};

const scalarType = (v) => {
  if (v === null) return 'null';
  if (Array.isArray(v)) return 'array';
  return typeof v;
};

const countChar = (s, ch) => (s.match(new RegExp(ch, 'g')) || []).length;

const walk = (a, b, p) => {
  if (b === undefined) {
    errs.push(`${p}: missing in locale`);
    return;
  }

  const ta = scalarType(a);
  const tb = scalarType(b);
  if (ta !== tb) {
    errs.push(`${p}: type mismatch en=${ta} locale=${tb}`);
    return;
  }

  if (ta === 'object') {
    for (const k of Object.keys(a)) walk(a[k], b[k], p ? `${p}.${k}` : k);
    return;
  }

  if (ta === 'array') {
    if (a.length !== b.length) errs.push(`${p}: array length mismatch en=${a.length} locale=${b.length}`);
    for (let i = 0; i < Math.min(a.length, b.length); i += 1) walk(a[i], b[i], `${p}[${i}]`);
    return;
  }

  if (ta === 'string') {
    const enTokens = tokenBag(a);
    const lcTokens = tokenBag(b);
    if (JSON.stringify(enTokens) !== JSON.stringify(lcTokens)) {
      errs.push(`${p}: placeholder/token mismatch`);
    }
    if (!validateNumericTagNesting(b)) {
      errs.push(`${p}: invalid numeric-tag nesting`);
    }

    const enNl = countChar(a, '\\n');
    const lcNl = countChar(b, '\\n');
    if (enNl !== lcNl) errs.push(`${p}: newline count mismatch en=${enNl} locale=${lcNl}`);

    const enTab = countChar(a, '\\t');
    const lcTab = countChar(b, '\\t');
    if (enTab !== lcTab) errs.push(`${p}: tab count mismatch en=${enTab} locale=${lcTab}`);
  }
};

const checkNoExtraKeys = (a, b, p) => {
  if (scalarType(a) !== 'object' || scalarType(b) !== 'object') return;
  for (const key of Object.keys(b)) {
    if (!(key in a)) errs.push(`${p ? `${p}.` : ''}${key}: extra key in locale`);
  }
  for (const key of Object.keys(a)) {
    if (key in b) checkNoExtraKeys(a[key], b[key], p ? `${p}.${key}` : key);
  }
};

walk(en, lc, '');
checkNoExtraKeys(en, lc, '');
if (errs.length) {
  console.error(errs.join('\n'));
  process.exit(1);
}
console.log('OK EN parity contract:', localePath);
NODE
```

Gate E: Targeted coverage recheck

```bash
pnpm --filter @apps/brikette check-i18n-coverage --locales=<locale> --format=json --output=i18n-coverage-report.after.<slice-tag>.json
```

Optional wrapper snippet (recommended):

```bash
set -euo pipefail
# A parse -> B duplicate keys -> C normalize -> D EN parity -> E targeted coverage
```

### 6) Batch Completion Gate

After each batch (locale or namespace):

```bash
pnpm --filter @apps/brikette check-i18n-coverage --format=json --output=i18n-coverage-report.after.<slice-tag>.json
```

Acceptance for selected scope:
- Missing files reduced (or zero if in scope)
- Missing keys reduced (or zero if in scope)
- Untranslated keys reduced for files touched
- No regressions introduced outside touched scope

## Translation Guardrails

- Translate text, not data contracts.
- Do not translate:
  - Placeholder/token syntax
  - URLs and route fragments
  - Internal IDs / enum-like values
- If a string is intentionally same as EN (brand/proper noun), keep it and annotate rationale.

## Recommended Execution Slicing

- Slice by one namespace at a time (for example `guides/*`, `how-to-get-here/*`, `bookPage.json` cluster).
- Keep each `/lp-do-build` cycle atomic and verifiable.
- Re-baseline after every slice; do not batch many unverified writes.

## Output Contract

Always report:
- Before vs after totals (`missing files`, `missing keys`, `untranslated keys`)
- Exact files changed
- Gate status: parse + no-duplicate-keys + EN parity contract
- Any intentionally retained EN strings with rationale
- Coverage artifact paths used (`before` and `after`)
- Next highest-impact slice
