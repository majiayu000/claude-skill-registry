# Profiles — user portrait files

This reference defines the per-user profile system. Profiles let the digest carry forward observations across many days so the 群友画像 section in each new digest can show continuity (`蛙总今天罕见地没提空头`) instead of starting from scratch.

Two parallel profile directories live alongside each group's digests:

- `profiles/` — observations sourced from the **normal** version of the digest.
- `profiles-roast/` — observations sourced from the **roast** version.

They are kept strictly separate. The normal-version generation reads only `profiles/`; the roast-version generation reads only `profiles-roast/`. This prevents roast snark from contaminating the sober summary and vice versa.

Load this file during Step 3.7 (load profiles for active users), Step 8.5 (update profiles after digest is written), and Step 9 (backfill).

---

## 1. File format

### 1.1 Path & naming

- Normal: `wechat/{group_id}-{group_name}/profiles/{wxid}-{nickname}.md`
- Roast: `wechat/{group_id}-{group_name}/profiles-roast/{wxid}-{nickname}.md`

The **stable** identifier is the `wxid` prefix. The `-{nickname}` suffix is for human browsability — if it changes, rename the file.

Filename sanitization: replace `/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`, NUL, and control characters with `_`. Trim trailing dots and whitespace. Cap total filename length at 200 chars (rare nicknames can be very long).

### 1.2 Frontmatter

YAML frontmatter at the top of every profile file:

```yaml
---
name: "<current display name>"
wxid: "<wxid>"
aliases: ["<old nickname>", "<even older nickname>"]
first_seen: "YYYY-MM-DD"
last_seen: "YYYY-MM-DD"
total_messages: N
digest_appearances: N
avg_messages_per_digest: N.N
---
```

Field rules:

- `name`: the most recent display name from `from_nickname` (or `self_display` for the owning user).
- `wxid`: stable; never changes once written.
- `aliases`: append-only; every prior display name we've seen. Don't include the current `name` in this list.
- `first_seen` / `last_seen`: dates of first/most-recent digest appearance, YYYY-MM-DD.
- `total_messages`: cumulative count across all digests this profile has been updated from.
- `digest_appearances`: how many digest files this user has 3+ messages in.
- `avg_messages_per_digest`: `total_messages / digest_appearances`, one decimal.

### 1.3 Free-form body — normal profile

Section headers are plain text on their own line. Order is fixed.

```
角色标签

• {4-6 短语标签}

关注领域

• {领域 1}
• {领域 2}

发言风格

{1-3 句描述，可以多段}

互动模式

• {与某某的互动模式}
• {另一种互动模式}

经典金句

• [YYYY-MM-DD] 「{直接引用}」
• [YYYY-MM-DD] 「{直接引用}」

标志性事件

• [YYYY-MM-DD] {事件描述}
• [YYYY-MM-DD] {事件描述}
```

### 1.4 Free-form body — roast profile

Same plain-text section header style, different sections.

```
人设标签

• {4-6 放大版标签}

核心槽点

• {可吐槽点 1}
• {可吐槽点 2}

毒舌语录库

• [YYYY-MM-DD] 「{该用户说过的话} — {简短毒舌点评}」
• [YYYY-MM-DD] 「{...}」

经典翻车现场

• [YYYY-MM-DD] {翻车描述 + 引用 / 证据}
• [YYYY-MM-DD] {...}
```

---

## 2. Update rules

Rules differ per section. Append-only sections must never lose history; mergeable sections may be rewritten as understanding sharpens.

### 2.1 Normal profile

| Section | Update mode | Notes |
|---------|-------------|-------|
| 角色标签 | **Merge** | Cap 4-6 tags. Can replace less representative tags with stronger ones. Always keep the most consistently-supported tag. |
| 关注领域 | **Merge dedupe** | Add new domains; dedupe by meaning, not exact string. |
| 发言风格 | **Refine** | Only update when a clearly new pattern emerges. Avoid rewriting on every digest. |
| 互动模式 | **Merge** | Add new modes; can refine existing ones with more detail. |
| 经典金句 | **Append-only** | Never delete. No cap. Each entry must be dated and quoted verbatim. |
| 标志性事件 | **Append-only** | Never delete. No cap. Each entry dated. |

### 2.2 Roast profile

| Section | Update mode | Notes |
|---------|-------------|-------|
| 人设标签 | **Merge** | Cap 4-6. Can sharpen tags as patterns repeat. |
| 核心槽点 | **Append-only** | Never delete; recurring 槽点 build up here. |
| 毒舌语录库 | **Append-only** | Never delete. No cap. Each entry dated, with both the quote and the roast comment. |
| 经典翻车现场 | **Append-only** | Never delete. No cap. Each entry dated. |

### 2.3 Frontmatter on every update

- Update `name` if current display name differs from the recorded one. Push the old name onto `aliases` if not already there.
- If `name` changed, also rename the file from `{wxid}-{old_nickname}.md` to `{wxid}-{new_nickname}.md`.
- Update `last_seen` to the current digest's end date.
- Increment `total_messages` by this batch's message count for this user.
- Increment `digest_appearances` by 1.
- Recompute `avg_messages_per_digest`.

---

## 3. Step 8.5 — Update procedure

Run after the digest file(s) are written. Iterate over every user with 3+ messages in this batch.

1. **Look up the profile.**
   - Scan `profiles/` (or `profiles-roast/` for the roast pass) for a file whose name starts with `{wxid}-`.
   - If found: open it.
   - If not found: create a new file using the frontmatter template. `first_seen = last_seen = current digest end date`, `total_messages = this batch's count`, `digest_appearances = 1`.

2. **Resolve wxid for new users.** When a new user appears, you already know their `wxid` from the wx-cli message data — use it directly. If for some reason only the nickname is known, run `wx contacts --query "{nickname}" --json` to resolve; if multiple matches, prefer the one currently in the group (cross-check `wx members <group>` if needed).

3. **Update frontmatter.** Per §2.3.

4. **Update body sections.**
   - For mergeable sections (角色标签，关注领域，发言风格，互动模式 / roast: 人设标签): read the existing content, integrate new observations from this batch, rewrite the section.
   - For append-only sections (经典金句，标志性事件 / roast: 毒舌语录库，经典翻车现场，核心槽点): append new entries, each dated and verbatim. Never edit or remove prior entries.

5. **Write back.** Overwrite the file.

6. **Source separation.** Pass running for the normal digest writes only to `profiles/`. Pass running for the roast digest writes only to `profiles-roast/`. Even if both versions are generated in the same skill invocation, run two separate update passes.

---

## 4. Step 9 — Backfill procedure

Triggered when the user says `回溯画像`, `初始化画像`, `backfill profiles`, or similar. This builds initial profiles from already-written digest files without re-fetching from wx-cli.

1. **List inputs.**
   - List every `*.md` digest file under `wechat/{group_id}-{group_name}/` (top level, not inside `profiles/` or `profiles-roast/`).
   - Partition by filename suffix: `*-roast.md` → roast pass, all others → normal pass.
   - Optionally also read `history-digests.jsonl` for fast metadata lookup (date, message count) before opening individual files.

2. **Decide whether to run roast backfill.** Only run the roast pass if at least one `*-roast.md` file exists.

3. **Process in batches of 10-15 digest files.** Reading all of them at once will blow context. For each batch:
   - Read the digests.
   - For each user appearing in the leaderboard or 群友画像 across the batch, accumulate:
     - Message counts per digest (from the stats block).
     - Role tags and observations (from the 群友画像 section).
     - Quotes (from inline 「」 in the body).
     - Dated events (from category bodies — when the digest mentions specific incidents).
   - Resolve wxid for each accumulated user via `wx contacts --query "{nickname}" --json` if not already cached. Cache the wxid↔nickname mapping for the rest of the backfill.

4. **Threshold.** Generate a profile file only for users appearing in **3 or more** digests in the corpus. Below that, skip (probably one-time visitors).

5. **Write profile files.**
   - For the normal pass, write to `profiles/{wxid}-{nickname}.md`.
   - For the roast pass, write to `profiles-roast/{wxid}-{nickname}.md`.
   - Use the most recent nickname as the filename suffix. Push older nicknames into `aliases`.
   - Sort 经典金句，标志性事件，毒舌语录库，经典翻车现场 entries chronologically by date.
   - No cap on the size of append-only sections during backfill — let history flow in.

6. **Compute frontmatter.**
   - `first_seen` = earliest digest date the user appeared in.
   - `last_seen` = latest digest date the user appeared in.
   - `total_messages` = sum of per-digest counts.
   - `digest_appearances` = number of digests the user crossed the 3-message threshold in.

7. **Report.** After both passes complete, print a short summary:
   - `Backfilled {N} normal profiles from {M} digests.`
   - `Backfilled {K} roast profiles from {L} roast digests.` (only if roast pass ran)
   - List any users skipped due to wxid resolution failures so the user can fix manually.

8. **Re-running backfill is safe.** If the user runs backfill twice, treat existing profile files as the prior state and merge — same rules as Step 8.5 updates. Don't blow away existing append-only entries.

---

## 5. Privacy guardrails

These apply to both normal and roast profiles, with an extra layer for roast.

### 5.1 Forbidden (write neither in normal nor roast)

- **Real-world full names** when only a nickname was used in the group. If the person introduced themselves with `我叫王二`, `王二` is on the table; `王晓明` inferred from another channel is not.
- **Phone numbers, emails, ID numbers, home addresses, employer addresses, exact birth dates** — even if mentioned in the group, don't lift them into profile files.
- **Health, medical, psychological information.** Even self-disclosed (`我最近有点抑郁`) — don't bake it into a permanent profile.
- **Private romantic / family details** unless openly group-discussed by the person themselves. A passing mention by another member doesn't count.
- **Embarrassing private failures.** Public ones (a take that aged badly in front of the group) are fair game; private ones (a job rejection mentioned briefly) are not.
- **Sleep / timezone inference from timestamps.** Server time ≠ recipient's local time, and it implies surveillance.

### 5.2 Allowed

- **Public group behavior** — what they said, how they argued, what they shared.
- **Direct quotes** of things said in the group (these are already public to the group).
- **Interest areas, hobbies, tool preferences** as expressed in group discussion.
- **Interaction patterns** with other group members.
- **Publicly mentioned consumption** (`蛙总今天又分享了买了什么书`) — fine if they themselves mentioned it.
- **Publicly shared travel / life anecdotes** they told the group.

### 5.3 Roast-only extras

In addition to §5.1, the roast profile must **not** include:

- **Anything about appearance, weight, body, looks.**
- **Anything about family members** (their kids, parents, partners) — only the person themselves.
- **Mental-health speculation**, even as a joke. No `这位需要看医生`, no `典型 ADHD`.
- **Identity-based roasts.** No mocking of orientation, religion, ethnicity, nationality, gender.

The roast may mock:

- Stupid takes, contradictions, factual errors.
- Repetitive behavior (`第 47 次预测见顶`).
- Self-undermining moments (`昨天说 X，今天说 not X`).
- Performative flexes that didn't land.

The rule of thumb: **roast the take, not the person.**

---

## 6. Reading profiles during digest generation (Step 3.7)

When loading profile context for a fresh digest:

1. Iterate over users active in this batch (3+ messages).
2. For the normal pass, read `profiles/{wxid}-*.md` for each. Skip if missing.
3. If the current run also generates the roast version, **separately** read `profiles-roast/{wxid}-*.md` during the roast generation pass.
4. Compile a condensed working-memory block:
   - The user's current `name` and `aliases` (so you can recognize them under different names).
   - 角色标签 / 人设标签 (so you can carry forward or contrast).
   - The 3-5 most recent 经典金句 / 毒舌语录 entries (so you can detect callbacks and repeats).
   - The 3-5 most recent 标志性事件 / 翻车现场 entries (so you can spot recurring themes).
5. Don't dump the entire profile into the digest — the profile is *context*, the digest is *today*.

If a profile contradicts what you see in today's batch (e.g., the profile says `从不主动发起话题`, but today they started three threads), call that out explicitly in the day's 群友画像 — that's the kind of contrast that makes the digest interesting.
