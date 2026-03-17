---
name: web-interface-guidelines-review
description: "Review UI files against accessibility, UX, and performance rules, then output terse findings grouped by file. Use when: (1) Auditing frontend code quality, (2) Enforcing design-system rules in PRs, or (3) Generating actionable file:line compliance reports."
---

# Web Interface Guidelines Review

Audit frontend files for accessibility, interaction quality, performance, and content rules. Return concise findings in `file:line` format grouped by file, with no preamble.

## When to use

- Use case 1: When you need a fast compliance pass on UI components before merge
- Use case 2: When a team wants consistent accessibility and interaction quality checks
- Use case 3: When reviewers need terse, high-signal findings instead of long explanations

## Required tools / APIs

- `rg` (ripgrep) — fast code search across source files
- `node` (optional) — structured scans and report generation
- No external API required

Install options:

```bash
# Ubuntu/Debian
sudo apt-get install -y ripgrep nodejs npm

# macOS
brew install ripgrep node
```

## Skills

### basic_usage

Run a pattern-based compliance scan and emit grouped findings.

```bash
# 1) Choose files (example)
FILES="src/**/*.{vue,js,jsx,html,css}"

# 2) Run targeted checks (examples)
rg -n "<button[^>]*>\s*(<svg|<i)" $FILES
rg -n "<img(?![^>]*\balt=)" -P $FILES
rg -n "transition\s*:\s*all" -P $FILES
rg -n "outline-none|outline:\s*none" -P $FILES
rg -n "onPaste\s*=\s*\{[^}]*preventDefault" -P $FILES
rg -n "user-scalable\s*=\s*no|maximum-scale\s*=\s*1" -P $FILES
```

**Node.js:**

```javascript
const { execSync } = require('node:child_process');

const checks = [
  { rule: 'icon button missing aria-label', cmd: "rg -n \"<button[^>]*>\\s*(<svg|<i)\" src" },
  { rule: 'image missing alt', cmd: "rg -n -P \"<img(?![^>]*\\balt=)\" src" },
  { rule: 'transition: all used', cmd: "rg -n -P \"transition\\s*:\\s*all\" src" },
  { rule: 'outline removed without replacement', cmd: "rg -n -P \"outline-none|outline:\\s*none\" src" }
];

function runCheck({ rule, cmd }) {
  try {
    const out = execSync(cmd, { encoding: 'utf8' }).trim();
    if (!out) return [];
    return out.split('\n').map((line) => {
      const [file, lineNo] = line.split(':');
      return `${file}:${lineNo} - ${rule}`;
    });
  } catch {
    return [];
  }
}

const findings = checks.flatMap(runCheck);
if (!findings.length) {
  console.log('✓ pass');
} else {
  console.log(findings.join('\n'));
}
```

### robust_usage

Run a broader review using grouped output, anti-pattern checks, and severity tags.

```bash
# Save report in required style (grouped by file)
node scripts/review-ui-guidelines.js "src/**/*.{vue,js,jsx,html,css}" > ui-guidelines-report.txt
cat ui-guidelines-report.txt
```

**Node.js:**

```javascript
const { execSync } = require('node:child_process');

const inputGlob = process.argv[2] || 'src/**/*.{vue,js,jsx,html,css}';

const checks = [
  { id: 'a11y-icon-label', label: 'icon button missing aria-label', pattern: '<button[^>]*>\\s*(<svg|<i)' },
  { id: 'a11y-input-label', label: 'input lacks label/aria-label', pattern: '<input(?![^>]*(aria-label|id=|name=))' },
  { id: 'a11y-img-alt', label: 'image missing alt', pattern: '<img(?![^>]*\\balt=)' },
  { id: 'focus-outline', label: 'outline removed without focus replacement', pattern: 'outline-none|outline:\\s*none' },
  { id: 'anim-all', label: 'transition: all → list properties', pattern: 'transition\\s*:\\s*all' },
  { id: 'paste-block', label: 'onPaste preventDefault anti-pattern', pattern: 'onPaste\\s*=\\s*\\{[^}]*preventDefault' },
  { id: 'zoom-block', label: 'zoom disabled (user-scalable=no or maximum-scale=1)', pattern: 'user-scalable\\s*=\\s*no|maximum-scale\\s*=\\s*1' },
  { id: 'click-div', label: 'click handler on div/span should be button', pattern: '<(div|span)[^>]*onClick=' }
];

function grep(pattern) {
  try {
    const cmd = `rg -n -P "${pattern}" ${inputGlob}`;
    const out = execSync(cmd, { encoding: 'utf8' }).trim();
    return out ? out.split('\n') : [];
  } catch {
    return [];
  }
}

const grouped = new Map();

for (const check of checks) {
  for (const hit of grep(check.pattern)) {
    const first = hit.indexOf(':');
    const second = hit.indexOf(':', first + 1);
    if (first === -1 || second === -1) continue;

    const file = hit.slice(0, first);
    const line = hit.slice(first + 1, second);
    const finding = `${file}:${line} - ${check.label}`;

    if (!grouped.has(file)) grouped.set(file, []);
    grouped.get(file).push(finding);
  }
}

if (!grouped.size) {
  console.log('✓ pass');
  process.exit(0);
}

for (const [file, items] of grouped.entries()) {
  console.log(`## ${file}`);
  console.log('');
  for (const item of items) console.log(item);
  console.log('');
}
```

## Vue + Tailwind report view (optional)

Use this lightweight UI when you want readable review output in-browser.

```vue
<template>
  <a href="#main" class="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:rounded focus:bg-white focus:px-3 focus:py-2 focus:ring-2 focus:ring-slate-500">Skip to Main Content</a>

  <main id="main" class="mx-auto max-w-4xl p-4 sm:p-6 text-slate-900">
    <h1 class="text-2xl font-semibold text-balance">Web Interface Guidelines Report</h1>

    <p aria-live="polite" class="mt-2 text-sm text-slate-600">
      {{ loading ? 'Loading…' : `${groups.length} files checked` }}
    </p>

    <section v-if="!loading && groups.length === 0" class="mt-6 rounded border border-emerald-200 bg-emerald-50 p-4">
      <p class="font-medium">✓ pass</p>
    </section>

    <section v-for="group in groups" :key="group.file" class="mt-6 rounded border border-slate-200 bg-white p-4 shadow-sm">
      <h2 class="text-lg font-semibold text-wrap-balance">{{ group.file }}</h2>
      <ul class="mt-3 space-y-2">
        <li v-for="item in group.items" :key="item" class="min-w-0 break-words rounded bg-slate-50 px-3 py-2 font-mono text-sm tabular-nums">
          {{ item }}
        </li>
      </ul>
    </section>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const loading = ref(true);
const groups = ref([]);

onMounted(async () => {
  try {
    const res = await fetch('/ui-guidelines-report.json');
    groups.value = await res.json();
  } finally {
    loading.value = false;
  }
});
</script>
```

## Output format

Use this exact shape.

```text
## src/Button.vue

src/Button.vue:42 - icon button missing aria-label
src/Button.vue:18 - input lacks label
src/Button.vue:55 - animation missing prefers-reduced-motion
src/Button.vue:67 - transition: all → list properties

## src/Modal.vue

src/Modal.vue:12 - missing overscroll-behavior: contain
src/Modal.vue:34 - "..." → "…"

## src/Card.vue

✓ pass
```

Rules for output:
- Group by file
- Use `file:line - issue` format
- Keep text terse, high signal
- Skip explanation unless fix is non-obvious
- No preamble

## Agent prompt

```text
You have a Web Interface Guidelines Review skill.

When the user asks to review frontend files, run rule-based checks across the provided paths and return findings grouped by file.

Requirements:
1. Follow accessibility, focus, forms, animation, typography, content handling, images, performance, navigation/state, touch, layout, theming, i18n, hydration, hover, and copy rules.
2. Flag anti-patterns explicitly.
3. Output ONLY in this format:

## path/to/file

path/to/file:line - concise issue

If a file has no issues:

## path/to/file

✓ pass

Do not force a framework or language. Prefer Vue + Tailwind examples when a UI example is needed. Avoid TypeScript unless the user explicitly requests it.
```

## Troubleshooting

**No findings but issues exist:**
- Symptom: Report shows `✓ pass` unexpectedly
- Solution: Expand file glob, include template/style files, and add missing regex checks

**Too many false positives:**
- Symptom: Findings are noisy or duplicated
- Solution: Narrow patterns, add context-aware checks, and suppress known-safe paths

## See also

- [../using-web-scraping/SKILL.md](../using-web-scraping/SKILL.md) — Extracting source data from web pages
- [../city-tourism-website-builder/SKILL.md](../city-tourism-website-builder/SKILL.md) — Building polished static pages quickly

---

## Notes

- Recommended path: `skills/web-interface-guidelines-review/SKILL.md`
- Keep examples copy-paste runnable in clean environments
- Prefer semantic HTML first; use ARIA to complement semantics
