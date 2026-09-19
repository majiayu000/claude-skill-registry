---
name: abide-compile
description: Compile a repository's instruction files (AGENTS.md, CLAUDE.md and friends) into an Abide rubric, then validate and calibrate it.
---

# Compile an Abide rubric

You are turning the rules a person wrote for coding agents into a rubric that a checker outside your context window can enforce on every edit. The checker sees only one rule and one diff at a time. Nothing else. Every decision below follows from that.

Two facts before you start:

- Rules come only from the user's own files. Never add a rule you think they should have. If a file holds zero rules, the rubric holds zero rules and you say so.
- The rubric is a committed, hand-editable file. A person will read it, and a verdict must trace to a rule they can point at. Quote their wording.

## Step 1. Read the sources

The hook that sent you here listed the instruction files it found and where the rubric goes. Read every listed file in full. Then:

- Follow pointer files. A file whose whole content is "Read instructions from X" or "Read ./AGENTS.md" is a pointer. Read X and treat X as a source in its own right: list it under `sources` with its own path so it gets its own hash.
- Files under a subdirectory apply only there. The hook gave each one a scope glob. Rules from that file carry that glob.
- Read `CONTRIBUTING.md` only when it was listed, and keep only sentences that give an instruction. Prose about how to open a pull request is not a rule.
- If a lint config was listed (`eslint.config.*`, `.eslintrc*`, `biome.json`, stylelint config), skim it for rule names. When a rule you extract is already enforced there, keep the rule and record the lint rule name in `check.overlaps`. It stays in the rubric because lint runs later than an edit and the convention still binds; the label keeps it from being reported as a new finding.

## Step 2. Extract every statement that instructs

Go through each file top to bottom. A rule is any sentence that tells the agent to do or not do something about code. Headings, background, and rationale are not rules, but they often say what a rule is for and belong in the wording of its question.

For each rule capture:

- `text`: the user's own words, trimmed to one or two sentences. Do not paraphrase into something more general.
- `source.path` and `source.line`: where it came from. Line numbers matter; they are how the person finds it.
- Any code block next to it. A worked example or counterexample carries more signal than the prose, and belongs in the question's criteria (see step 4).

Do not merge two rules into one because they sit under one heading. Do not split a rule that is one idea.

## Step 3. Classify each rule into exactly one bucket

Ask the questions in this order and stop at the first yes.

1. Can a linter enforce it exactly? Then `check.type` is `lint`. Examples: `interface Foo` when the rule says use `type`; `as` casts; `fetch(`; `process.env.`; `Date.now()`; `console.log`; `npm install`. Put the linter rule that enforces it in `how` (`@typescript-eslint/consistent-type-definitions`, `no-restricted-syntax`, a stylelint rule) or, failing that, the AST or grep shape, and a `pattern` as a hint when one is obvious. Abide records these and reports them for the user's own linter; it never runs them and never sends them to the model. The judge is for what a linter cannot express.
2. Does the rule need counting or measuring: line lengths, line counts, selector counts, nesting depth, alphabetical or length order (imports or props ordered by line length is the common one)? That is mechanical work, and the judge cannot count. If step 1 found no regex for it, `check.type` is `deferred` with reason "needs a script, not a judge". Do not turn it into a model question; it will score about 0.4 on everything.
3. Can a judge answer it by looking at a change and nothing else? Then `check.type` is `model`. Most style, structure, comment, error handling, naming, and "do not do X" rules land here.
4. Does answering need the rest of the repository? "Reuse existing error codes", "follow existing patterns", "any visual pattern in two places becomes a shared component", "check whether a helper already exists". Then `check.type` is `deferred` with a one line `reason`. These are real rules that this version cannot check on a diff, and the report says so.
5. Is it about the conversation or the process rather than the code? "Ask when unsure", "state a plan", "run the tests before you finish", "clean up processes you started". Then `check.type` is `unenforceable` with a `reason`.

Every statement lands somewhere. Count them: the summary you give the user is the four bucket counts.

## Step 4. Write the question for each model rule

The judge is a small, fast model that answers typed questions with a probability. It is good at narrow, concrete questions and bad at vague ones. A vague question scores about 0.4 on everything and never fires, and the user reads that silence as good news. Write every question so that a violating diff scores near 1 and a clean diff scores near 0.

- One idea per question. If the rule has two parts, make two rules.
- Ask about the diff: "Does this change add ...", "Does this change put ...". Name the concrete shape you want caught: the identifier, the call, the syntax, the position. "Does this change add a comment that restates what the line below it does?" beats "Are comments sparing?".
- Never put scope in the text. "For a file under apps/web/src/server" belongs in the `scope` field, not in the question. Scope is a list of globs relative to the repo root, for example `["apps/web/src/server/**/*.service.ts"]`. Omit it when the rule applies everywhere.
- Keep instructions under about 60 words. Every word is billed on every edit whether or not the rule fires.
- Ask for existence, not for a judgment of the whole: "Among the added lines, is there at least one comment whose content a reader could reconstruct from the code directly below it?" fires on the first offending line, while "Are the comments appropriate?" averages over the hunk and never leaves the middle.
- A rule about volume or restraint ("comment sparingly", "keep it short", "minimal code") needs two questions: an existence question for the concrete offence, and a `score` question for the amount, with levels the judge can point at ("no such comments", "one or two", "several, or a multi-line block", "most lines"). Do not collapse "sparingly" into a single narrow case and lose the volume.
- Use `criteria` for a worked example: `"criteria": { "true": "a `retry`loop written by hand when Radash`retry` is installed", "false": "calling an installed utility" }`. Put the user's own code block here when they gave one.
- Question types:
  - `boolean` for almost everything. The answer is a probability that the rule is broken.
  - `choice` when the rule names a closed set of shapes and only some are wrong: `criteria` maps each option to a description, `violating` lists the wrong ones. Example: a service must be a class with static methods, so options are `class-static`, `loose-functions`, `eager-init` and `violating` is the last two.
  - `score` when the rule is a matter of degree: `criteria` is an ordered list of levels from compliant (index 0) to worst, and `violatingFrom` is the first level that counts as broken. Example for "minimum code that solves the problem": levels "as short as it can be", "somewhat longer than needed", "about twice as long", "several times longer", with `violatingFrom: 2`.

## Step 5. Decide when each model rule runs

Every model rule carries `when`: `"edit"` or `"turn"`. Get this right; the wrong phase produces false violations and each one costs the agent a repair turn.

- `"edit"` runs after every edit, against that one hunk. Use it when the lines in front of the judge are enough: raw error text reaching a user, a narrating comment, a hand rolled utility, a type cast, an if/else chain over a discriminated union, an inline style, a hardcoded color.
- `"turn"` runs once when the agent finishes its turn, against the full diff of everything it changed. Use it for any question about the change as a whole: scope creep, changes outside what was asked, an abstraction with a single caller, overall length, whether a file grew past a cap, whether a new module was needed at all, whether a helper should have been extracted. After edit 1 of 12 these questions have no answer; a helper with one caller now may have three by the end.

The test: if a careful reviewer would want to see the whole change before answering, it is `"turn"`.

Lint rules always run per edit and do not need `when`.

## Step 6. Write the rubric file

Write the file the hook named (`.abide/rubric.json` for the project, `~/.abide/global.json` for global instruction files). Global files get their own rubric because they apply in every repository.

```json
{
  "version": 1,
  "compiledAt": "2026-09-17T10:00:00.000Z",
  "compiledBy": "claude",
  "sources": [
    { "path": "AGENTS.md", "scope": "**/*" },
    { "path": "apps/web/AGENTS.md", "scope": "apps/web/**/*" }
  ],
  "rules": [
    {
      "id": "no-interface",
      "text": "Use `type`, never `interface`.",
      "source": { "path": "AGENTS.md", "line": 41 },
      "scope": ["**/*.ts", "**/*.tsx"],
      "check": {
        "type": "lint",
        "pattern": "^\\s*(export\\s+)?(declare\\s+)?interface\\s+[A-Za-z_$]",
        "how": "@typescript-eslint/consistent-type-definitions"
      }
    },
    {
      "id": "raw-error-to-user",
      "text": "Never show a user a raw error. A message reaches a user only if the code that produced it authored it for a person.",
      "source": { "path": "AGENTS.md", "line": 120 },
      "scope": ["apps/web/src/**/*.ts", "apps/web/src/**/*.tsx"],
      "when": "edit",
      "check": {
        "type": "model",
        "overlaps": "coldtea/no-raw-error-in-response",
        "question": {
          "type": "boolean",
          "instructions": "Does this change put raw exception text where a user will see it: error.message, String(error), .toString() or a template of them reaching a response body, rendered copy, or a stored column that is displayed?",
          "criteria": {
            "true": "res.status(500).json({ message: String(error) })",
            "false": "log.error(error); res.status(500).json({ message: 'Could not load this run.' })"
          }
        }
      }
    },
    {
      "id": "scope-creep",
      "text": "No features beyond what was asked. Every changed line should trace directly to the user's request.",
      "source": { "path": "AGENTS.md", "line": 22 },
      "when": "turn",
      "check": {
        "type": "model",
        "question": {
          "type": "boolean",
          "instructions": "Does this change add functionality, files, options or abstractions that the task did not ask for?"
        }
      }
    },
    {
      "id": "reuse-error-codes",
      "text": "Reuse existing codes; don't invent near-duplicates.",
      "source": { "path": "AGENTS.md", "line": 131 },
      "check": { "type": "deferred", "reason": "needs the list of codes that already exist" }
    },
    {
      "id": "ask-when-unsure",
      "text": "State your assumptions explicitly. If uncertain, ask.",
      "source": { "path": "AGENTS.md", "line": 12 },
      "check": { "type": "unenforceable", "reason": "about the conversation, not the code" }
    }
  ]
}
```

Rules of the file:

- `id` is a short kebab-case name that says what the rule catches. Ids must be unique within the file.
- Leave `sha` out of `sources`; the CLI computes it in the next step.
- Every rule's `source.path` must appear in `sources`.
- No `status` field on new rules; it defaults to `active`. Do not write `calibration`; the CLI does.
- Write it as plain JSON with your file-writing tool. Nothing else goes in the file.

## Step 7. Validate, then calibrate

Run, using the CLI invocation the hook gave you:

```
abide rubric validate            (add --global for ~/.abide/global.json)
abide calibrate                  (same flag)
```

`validate` parses the file, fills in the source hashes, and prints the bucket table. Fix every issue it prints and run it again until it is clean.

`calibrate` runs every model rule against about twenty real hunks from the repository's git history and marks rules whose scores never get near 0 or near 1 as `weak`, and rules that fire on most historic hunks as `noisy`. Both are switched off until rewritten. When it reports any, rewrite those questions once using step 4 (make them more concrete, split them, add a criteria example, or move them to the other phase), run `validate` and `calibrate` again, and stop there whatever the result. Do not loop more than once. A repository with no history skips calibration; that is fine.

If the hook said a rule is being tuned, it attached statistics. Rewrite only the rules it named. Keep every other rule byte for byte.

## Step 8. Report and move on

Tell the user, in two or three plain sentences: how many rules, split across the four buckets; which rules are weak or noisy and switched off, if any; and that the rubric is at `.abide/rubric.json` for them to read and edit. Then continue with whatever they asked for. Do not paste the rubric into the conversation.
