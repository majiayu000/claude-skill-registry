---
name: verify-cli-run
description: Prove that a command-line tool actually did what it said, instead of trusting its exit code and its output. Snapshots the filesystem before and after, names the expected consequence in advance, and returns one of four verdicts with what could not be seen. Use after running a build, a migration, a scaffolder, a formatter, a codegen step, or an AI coding CLI; when a command printed success and you are about to report "done"; when you are about to write "exit code 0, so it worked"; or when a tool claims it edited files. Needs nothing installed.
license: Apache-2.0
metadata:
  version: 3.2.0
  homepage: https://www.reticle.sh
  repository: https://github.com/reticlehq/reticle
---

# Prove the command did what it said

A command exited 0 and printed `✓ done`. You have learned that the tool reached its own success branch. You have not learned that anything happened.

This is the whole problem with verifying a CLI: **the two things everybody checks are both the tool describing itself.** The exit code is chosen by the same code that did the work. The output is written by it. When a tool is wrong about what it did, it is wrong on both, in agreement. That is exactly why their agreement proves nothing.

This skill needs no tools installed. It is four rules and some `git`.

## The rule that decides everything

> **Evidence for a consequence must not come from the thing that performed the action.**

Grade every fact before you use it:

| What you have | Grade | Can it prove the command worked? |
| --- | --- | --- |
| Files on disk, before vs after | **consequence** | **Yes.** The filesystem decided whether the write landed, not the tool |
| An API answering when you ask it afterwards | **consequence** | **Yes.** Another party, answering you rather than the tool |
| Exit code | presence | No. The tool chose it |
| stdout / stderr | context | No. The tool wrote it |
| The tool's own `--verbose` report | context | No |

Everything in the bottom three rows is real information and none of it is proof. Use it to explain a verdict, never to reach one.

## 1. Name the consequence BEFORE you run

This is the method. An expectation written after you see the output can be talked into agreeing with whatever happened; one written in advance can only be met or missed.

Write it down in one line, in the transcript, before the command:

```
EXPECT: dist/index.js is rewritten, and no file outside dist/ changes.
EXPECT: src/utils.ts gains a function called parseConfig.
EXPECT: the migration creates 3 files under migrations/ and nothing else.
```

A consequence you cannot state in advance is one you cannot verify. If you cannot name one, say so and stop. That is an honest `no-fault`, not a pass.

## 2. Snapshot before

**In a git repo.** This is the good case, and it is one line:

```bash
git status --porcelain > /tmp/before.txt
```

`git status --porcelain` is a near-perfect evidence channel: structured, cheap, and independent of the tool. Git's index records what landed on disk, not what the tool meant to do.

**Not in a git repo**, or the paths are outside it:

```bash
find <declared-root> -type f -newermt '1970-01-01' -exec shasum -a 256 {} + | sort > /tmp/before.txt
```

Three rules for the roots you declare:

- **Exclude `node_modules`, `.git/objects` and large build caches** unless they are the subject. Hashing a full `node_modules` is tens of thousands of files.
- **Declare them explicitly.** A tool can write anywhere; you are watching a list you chose.
- **Anything outside that list is a blind spot**, and you will report it in step 6 rather than pretend it did not happen.

## 3. Check whether it is already true

The commonest false green in CLI work: `dist/index.js` exists, so "the build produced `dist/index.js`" passes, on a no-op rebuild that did nothing at all.

Before running, check whether your expected consequence **already holds**. If it does, the command cannot prove it. Either pick a consequence the command changes, or delete the artifact first and say that you did.

## 4. Run it, and capture separately

```bash
<the command> > /tmp/out.txt 2> /tmp/err.txt; echo "exit=$?"
```

Keep the exit code. You are not going to use it as proof. You are going to use it to explain the verdict, and to notice when it disagrees with the filesystem.

Two things worth knowing:

- Exit codes wrap: `sh -c 'exit 256'` exits **0**. A large code is not always what you think.
- `130` is a `SIGINT`, `137` is usually a kill. Those are facts about how the run _ended_, not about whether it worked.
- Some tools exit 0 when they declined to do anything. AI coding CLIs do this routinely.

## 5. Diff, and read the diff as the evidence

```bash
git status --porcelain > /tmp/after.txt; diff /tmp/before.txt /tmp/after.txt
git diff -- <the paths you expected to change>
```

Now answer your step-1 expectation against **this** and nothing else.

Two checks worth making every time, because they cost nothing:

- **Nothing else changed.** A build that also rewrote a lockfile, or a formatter that reformatted a file nobody asked about, is a finding.
- **Content, not just existence.** A file that exists is weaker than a file that contains what you expected. But note the asymmetry: _whether_ a file appeared is decided by the filesystem; _what is inside it_ was written entirely by the tool. Existence is stronger evidence than content.

## 6. Reach a verdict, one of four

Not two. The two extra values are the point: they are the ones that stop ignorance being rounded towards good news.

| Verdict | When |
| --- | --- |
| **yes** | The consequence you named in step 1 is visible in the diff, and it was not already true |
| **no** | The diff contradicts it, or the tool claimed something the filesystem does not show |
| **unknown** | You could not see what you needed. Nothing was watching, the window was wrong, or the effect is somewhere you were not looking |
| **no-fault** | Everything was watched, nothing was wrong, and nothing was declared to prove |

**`unknown` is not a failure and must never be reported as one.** "I could not see" and "it is broken" send somebody in opposite directions: one says look again, the other says go and fix something.

And say **what bought the `yes`**. "`dist/index.js` changed on disk" is a verdict. "The build said it succeeded" is not, and if that is all you have, the honest answer is `unknown`.

## 7. Say what you did not see

A verdict that cannot say what it missed is indistinguishable from one that saw everything. Name the gaps, every time. One line is enough:

```
Did not observe: the network (cannot see whether it called out); writes outside ./src and ./dist;
files created and deleted during the run; anything the tool's child processes did.
```

Four gaps are always present and worth naming by default:

- **The network.** You cannot see that a command dialled an endpoint. If the claim is about a remote (a push, a deploy, a PR), the filesystem cannot answer it.
- **Writes outside your declared roots.** `~/.config`, global caches, `/tmp`. Most AI coding CLIs write to their own state directory on every run.
- **Transient files.** Written and deleted inside the run. A before/after snapshot sees net effect only.
- **Child processes**, and anything that outlives the command: a fork, a deferred flush, a background upload.

## Two moves that cost nothing and catch a lot

**Run it twice.** A build, a formatter, a codegen step or a migration should produce an empty diff the second time. A tool that keeps changing things on repeat runs has a defect, and this needs no expected-value to check against.

```bash
<command> && git status --porcelain > /tmp/a.txt && <command> && git status --porcelain > /tmp/b.txt && diff /tmp/a.txt /tmp/b.txt
```

**Ask the far side.** For a network tool, the filesystem cannot help, but the service can. `gh pr view`, `git ls-remote`, a `curl` of the deployed URL. That is another party answering _you_ rather than the tool reporting on itself, so it is consequence-grade, and it is the only proof available for a remote claim.

Do not accept the tool's own local record as a substitute. `git push` writes `.git/refs/remotes/origin/main`, and that sha is **git's transcription of what it believes the remote said**. It is on disk, and it is still the tool describing itself. Ask the remote.

## Worked example: an AI coding CLI

The strongest case, because these tools' product _is_ file edits, and their transcript is the least reliable thing about them.

```
EXPECT: src/config.ts gains a function `parseConfig`. Nothing outside src/ changes.

$ git status --porcelain > /tmp/before.txt
$ grep -c "parseConfig" src/config.ts          # already-true check → 0
$ claude -p "add a parseConfig function to src/config.ts" ; echo "exit=$?"
$ git status --porcelain > /tmp/after.txt ; diff /tmp/before.txt /tmp/after.txt
 M src/config.ts
$ git diff src/config.ts | grep "^+.*parseConfig"
+export function parseConfig(raw: string): Config {

VERDICT: yes, bought by the working-tree diff, which is independent of the agent's report.
         It was not already true (grep returned 0 before).
Did not see: writes under ~/.claude (the tool records every session there); the network;
         whether a permission prompt declined an edit it also claimed.
```

Note what did **not** decide it: the exit code, and the paragraph in which the agent said it had added the function.

## When to escalate past this skill

This method tops out in four places, and each has a real answer:

| You need to | Use |
| --- | --- |
| See that a command called out to a host | a proxy, or ask the far side afterwards |
| Drive an interactive panel or a TUI | a pseudo-terminal; a shell cannot type into one |
| Verify a _web app_ rather than a CLI | [Reticle](https://www.reticle.sh) and the `verify-ui-change` skill |
| Produce a verdict somebody else can re-check | a verification artifact, not a transcript |

## The one thing not to do

Do not weaken the expectation you wrote in step 1 because the diff did not match it. Rewriting the target after seeing the result is how a verification step becomes a rationalisation step, and it is invisible in a transcript afterwards, because the amended expectation reads exactly like the original one.

If the diff does not match, that is the finding. Report it.
