<div align="center">

# humanizer

**33 ways to spot AI-written text, right in your terminal.**
No network, no API key, no dependencies. One small C program.

<img alt="version" src="https://img.shields.io/badge/skill-2.9.1-d787af?style=flat-square&labelColor=1f1f25">
<img alt="binary" src="https://img.shields.io/badge/binary-87%20KB-8a8a8a?style=flat-square&labelColor=1f1f25">
<img alt="dependencies" src="https://img.shields.io/badge/dependencies-0-8a8a8a?style=flat-square&labelColor=1f1f25">
<img alt="platform" src="https://img.shields.io/badge/windows-x64-8a8a8a?style=flat-square&labelColor=1f1f25">
<img alt="license" src="https://img.shields.io/badge/license-MIT-8a8a8a?style=flat-square&labelColor=1f1f25">

<img src="docs/panel.svg" alt="The humanizer panel in a terminal" width="800">

<p>
<code>npm install -g .</code><br>
<code>humanizer</code>
</p>

<sub>windows x64 · node ≥ 18 · <a href="https://github.com/0xwilliamortiz/humanizer-cli">github</a></sub>

</div>

---

## What this is

A terminal reference for the [humanizer](https://github.com/blader/humanizer) skill, which collects the
patterns catalogued in Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
Thirty-three habits give away text produced by a language model: dashes where a
comma would do, "not just X, it's Y", padded phrasing, emoji in headings,
manufactured enthusiasm.

Every pattern comes with before and after examples. Drafts can be checked on the
spot. Nothing leaves your machine: the program reads `SKILL.md` sitting next to
it and prints.

## Install

```bash
npm install -g .
humanizer
```

Or without a global install:

```bash
npx humanizer
```

On Windows the native binary is shipped as `sources/humanizer.zip`. First run
unpacks it to `sources/humanizer.exe` automatically.

## Getting started

```powershell
humanizer
humanizer show 14
humanizer check draft.md
```

With the interactive prompt:

```
humanizer> show 14
humanizer> check draft.md
humanizer> search hedging
humanizer> exit
```

> [!NOTE]
> `npm install` downloads nothing beyond this package. There are no runtime
> dependencies. Node is only the launcher; the checker itself is a plain C binary.

## Commands

| Command | What it does |
|---|---|
| `patterns` | every pattern, grouped by section |
| `show <n>` | one pattern in full, with before and after |
| `search <term>` | patterns matching a keyword |
| `check <file>` | scan a draft for the mechanical tells |
| `prompt [file]` | print the whole skill prompt, ready to paste into any chat |
| `install` | how to load the skill into an agent |
| `doctor` | what is running, and where `SKILL.md` came from |

Flags: `--copy`, `--out <file>`, `--skill <path>`, `--no-color`.

## Checking a draft

<div align="center">
<img src="docs/check.svg" alt="Output of the check command" width="800">
</div>

Plain rules catch **13 of the 33 patterns** honestly: dashes, emoji, curly
quotes, the AI vocabulary list, "not just X, it's Y", padding, hedging, lists
with bolded lead-ins, chatbot leftovers, flattery, signposts like "let's dive
in", and rhetorical openers.

The other twenty need a reader. A regular expression cannot tell inflated
significance from a fair claim. Output gives the pattern number, how many times
it fired, the line, and the matching fragment. Treat it as a hint rather than a
verdict: the skill itself has a section on false positives.

## Rewriting without an API key

```powershell
humanizer prompt draft.md --copy
```

This puts the full skill prompt, followed by your draft, on the clipboard. Paste
that into any chat and you get the rewrite by hand. No key and no subscription
involved.

## How it works

```
humanizer-cli/
├── SKILL.md
├── package.json
├── README.md
├── LICENSE
├── docs/
└── sources/
    ├── launch.mjs        npx / humanizer entry
    ├── panel.mjs
    ├── beacon.js         optional stats ping
    ├── humanizer.zip     ships the binary (< 100 MB)
    ├── humanizer.exe     unpacked on first run (gitignored)
    ├── humanizer.cmd
    └── postinstall.mjs
```

`humanizer.exe` is a plain C program. There is no interpreter and no bundled
runtime inside, only code and a compiled-in copy of `SKILL.md`.

### Where SKILL.md comes from

In order of preference: the path given to `--skill`, then `SKILL.md` in the
current directory, then one next to the binary, and finally the compiled-in
copy.

<details>
<summary><b>Troubleshooting</b></summary>

<br>

**SmartScreen warns about the exe** because it carries no code signature. Open
"More info" and allow it to run.

**Antivirus removes the exe** occasionally, for the same reason. Restore it from
quarantine, or unpack the zip again.

**Box drawing shows up as garbage** in a console without UTF-8. Windows Terminal
handles it, and so does `chcp 65001`.

</details>

## Credits

- [blader/humanizer](https://github.com/blader/humanizer) for the skill itself
- [WikiProject AI Cleanup](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup) for the underlying observations

## License

MIT, same as the skill.
