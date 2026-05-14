# Output formats — normal & roast digest

This reference defines the two digest variants the skill produces: the **normal** version (default, sober summary) and the **roast** version (毒舌，sarcastic critique, opt-in). Load this file during Step 4 (skeleton) and keep it open through Step 6 (audit).

Both versions share the same overall layout and writing rules; the differences are tone, the leaderboard annotations, the portraits, and the footer. Write the normal version first when both are requested — it's the anchor for incremental mode and the source of truth for the profile updates.

---

## 1. Normal version

### 1.1 Five-part structure

```
[Title line]
[📊 Stats block + Top 10 leaderboard]
[Opening summary — 1-2 paragraphs of prose]
[群友画像 — one entry per active user (3+ msgs)]
[Categorized body — 3-6 self-named sections per day]
[Optional pain-point section]
[Fixed footer]
```

### 1.2 Title line

- Single line, no markdown heading.
- Form: `{群名} 群聊精华 · {日期或日期区间}`
- Date single day: `2026-03-12`. Date range: `2026-03-12 ~ 2026-03-15`.

Example:

```
相亲相爱一家人 群聊精华 · 2026-03-12
```

### 1.3 Statistics block

- Starts with `📊 消息统计: 共 N 条消息`.
- Followed by a leaderboard, top 10 senders by message count, one per line.
- Form per line: `{排名}. {昵称}: {消息数} 条`
- Counting rules:
  - Include images, emojis, links, voice transcripts — anything that occupies a chat row is one message.
  - Exclude system messages and revoked messages (`[系统]`, `revokemsg`).
  - For the `self_wxid` user, substitute `self_display` from EXTEND.md before counting/displaying.
  - Resolve ambiguous nicknames (per SKILL.md Step 3.6) before tallying so the same person isn't double-counted.

Example:

```
📊 消息统计: 共 387 条消息
1. 蛙总: 92 条
2. 老王: 58 条
3. 阿喵: 41 条
...
```

### 1.4 Opening summary

- 1-2 paragraphs, plain prose, no headings, no bullets.
- Hook the reader: lead with the most distinctive thread of the day (a heated debate, a surprising announcement, a market move someone reacted to).
- Reference 2-4 of the day's category titles in the prose so the reader knows what's coming.
- Mention 1-2 specific people only if their contribution is central; otherwise stay topic-focused.
- No timestamps, no message counts (those live in the stats block).

### 1.5 群友画像 section

- Heading line: `群友画像`
- One entry per user with 3+ messages this batch.
- Order: by message count, descending.
- Entry header: `{昵称}（{角色标签}）` — the role tag is your one-line read on this person *today*. Examples: `做空美股的乐子人`, `深夜技术指导`, `论坛级吐槽担当`.
- Body: 2-5 bullets with `•` prefix. Each bullet states one observation. Quote evidence inline where natural.
- Continuity: if you loaded a prior profile in Step 3.7, carry forward the established tags/observations that still apply, and call out *change* explicitly (`今天罕见地没提空头`, `从昨天的乐观转向今天的焦虑`).
- Don't invent backstory — only what's in the messages or the prior profile.

Example:

```
群友画像

蛙总（做空美股的乐子人）
• 全天反复提"做空 SPY"，被群友提醒已连续三周看错方向
• 难得正面回应技术问题："我那个脚本是用 Bun 跑的，慢得跟蜗牛似的"
• 临近收盘转为沉默，与昨日大放厥词的状态对比明显
```

### 1.6 Categorized body

- 3-6 self-named categories per day.
- Each category is a thematic bucket — name it for the *topic*, not generic ("讨论"、"闲聊" are forbidden labels).
- Category header: `{emoji} {标题}` — one emoji prefix, then a short noun phrase.
  - Suggested emoji: 🛠 工具/技术，📦 产品发布，📰 新闻/市场，💬 观点辩论，😄 笑料/段子，📚 学习分享，💸 钱与消费，🍜 生活日常。
- Body inside each category: prose with embedded quotes. Use `•` bullets when listing 3+ parallel items; otherwise paragraphs.
- Attribution: name the speaker on first mention in a thread (`蛙总说他...`). For follow-on lines in the same thread, attribution can be implicit if the chain is short and clear.
- Quotes: use 「」 for direct quotes. Quote when the wording is vivid, surprising, or characteristic; paraphrase otherwise.
- Merge: a multi-person discussion is one entry, not a list of one-line replies.
- Links: preserve the full URL inline. Article titles stay verbatim.

Example:

```
🛠 Claude Code 4.7 实测

蛙总下午把 4.7 装上后第一反应是「比 4.6 慢一倍」，老王跟着复现，怀疑是 Opus 默认配置导致。阿喵贴了官方文档 https://docs.claude.com/.../opus-4-7 ，提到可以切回 Sonnet 4.6 跑速测，三人最终结论：复杂任务 4.7 强，日常用 4.6 更顺手。
```

### 1.7 Pain-point section (optional)

- Include only when the day's chat contains at least one concrete unresolved or partially-resolved problem.
- Heading: `今日待解决问题` or `本周悬而未决`.
- One entry per problem. Format:
  ```
  问题：<一句话描述>
  提出者：<昵称>
  背景：<1-2 句来龙去脉>
  状态：<✅ 已解决 / ⚠️ 部分解决 / ❌ 仍未解决>
  方案：<若有人提了方案，写在这；否则写"暂无方案">
  ```
- Skip the section entirely if there are no genuine pain points — don't pad with trivial questions.

### 1.8 Footer

Fixed line, last in file:

```
本简报由 AI 自动生成
```

No date, no signature, no version number.

---

## 2. Roast version (毒舌版)

The roast version mirrors the normal version's structure but inverts the tone. Generate only when `include_roast=true` (configured via EXTEND.md `default_version` or triggered by request keywords like 毒舌/roast/挑衅).

### 2.1 Structural parity

```
[Title line — adds "毒舌版" suffix]
[📊 Stats block — each leaderboard row gets a roast comment]
[Opening summary — absurd recap, sarcastic]
[群友画像 — 不留情面版]
[Categorized body — louder, more brutal category titles]
[Fixed footer — roast version]
```

Pain-point section is **dropped** in the roast version.

### 2.2 Title line

Form: `{群名} 群聊精华 · {日期} · 毒舌版`

Example: `相亲相爱一家人 群聊精华 · 2026-03-12 · 毒舌版`

### 2.3 Statistics block (roast)

- Same `📊 消息统计: 共 N 条消息` opener.
- Leaderboard: each row gets a parenthetical roast comment.
- Form: `{排名}. {昵称}: {消息数} 条 ({一句毒舌评语})`

Example:

```
📊 消息统计: 共 387 条消息
1. 蛙总: 92 条 (一个人撑起了空头的体面)
2. 老王: 58 条 (主要功能是给蛙总当反例)
3. 阿喵: 41 条 (发的链接比发的话还多)
```

### 2.4 Opening summary (roast)

- 1-2 paragraphs, sarcastic recap tone.
- Highlight the day's most ridiculous beat (a failed prediction, a heated argument over something trivial, a wild flex).
- Reference 2-3 of the roast category titles in the prose.

### 2.5 群友画像 (roast — 不留情面版)

- Same per-user entry format as normal, but with the role tag dialed up.
- Amplify quirks, contradictions, fail moments visible in the messages.
- 2-5 bullets with `•`. Each bullet is a roastable observation backed by a direct quote.
- Don't invent — every roast must trace back to something the person actually said in the batch (or in the loaded roast profile from prior batches).

Example:

```
群友画像

蛙总（做空美股钉子户，三周亏损不改其志）
• 今天第 47 次预测 SPY 见顶，给出的理由是"我感觉"
• 被老王翻出上周聊天记录后嘴硬：「上周的不算，那是市场不理性」
• 收盘前突然安静，疑似刚看完账户
```

### 2.6 Categorized body (roast)

- Same 3-6 category structure.
- Titles can be louder, more brutal, mock-headline style.
- Examples of acceptable roast titles:
  - `蛙总做空翻车: 一个人对抗整个美股`
  - `老王再次试图当人生导师, 群友集体打哈欠`
  - `阿喵又分享了一篇没人读完的长文`
- Bodies still preserve real quotes and traceability — sarcasm is in framing, not fabrication.

### 2.7 Footer (roast)

Fixed line, last in file:

```
本简报由一个没有感情的 AI 自动生成,如有冒犯,概不负责
```

### 2.8 Red lines (non-negotiable)

These rules override style; violate them and the roast becomes harmful. Write the spicy version first, then audit against this list and rewrite anything that crosses a line.

- **Mock public group behavior only.** Never appearance, weight, body, health, mental state, family, relationships (unless openly group-discussed at the person's own initiative), finances beyond what they publicly mention.
- **调侃 ≠ 人身攻击。** Readers should laugh at the situation, not feel sorry for the target. If you can't think of a joke that doesn't read as cruel, drop the bullet.
- **No timestamp-based sleep/timezone jokes.** Server time ≠ recipient's local time; also implies surveillance. Forbidden: `凌晨 3 点还在群里发言，怕是没睡好`, `这位是哪个时区的`, etc.
- **No medical/psychological speculation.** Even joking diagnoses (`这位需要看医生`, `典型 ADHD`) are out.
- **No outing.** Don't infer identity attributes the person hasn't volunteered (orientation, religion, politics beyond direct quotes).
- **Roast the take, not the person's right to have a take.** `这个观点错得离谱` is fine. `连这都不懂还敢发言` is not.

If a target hasn't said anything roastable in this batch (3+ messages but all neutral), give them a one-line affectionate ribbing and move on. Don't manufacture conflict.

### 2.9 Writing order

1. Draft the spicy version freely — don't self-censor mid-sentence.
2. After the body is complete, do a separate audit pass against §2.8.
3. Rewrite or delete any line that crosses a red line.
4. Then read the whole thing once more for tone calibration: is it fun, or is it mean?

---

## 3. Common formatting rules (both versions)

- **No markdown.** No `**bold**`, no `# headings`, no `*italic*`, no `[link](url)` syntax. Headings are plain text on their own line.
- **Bullets use `•`.** Not `-`, not `*`, not `1.` for prose-style bullets.
- **Numbered lists** (`1.`, `2.`) are reserved for the leaderboard.
- **Subcategory hints** within a body block are plain text with no symbol prefix.
- **Links preserved verbatim.** Paste the full URL inline. Don't shorten, don't hide behind text.
- **One emoji per category title.** Don't stack 🛠💬 etc.
- **Pain-point statuses** use ✅⚠️❌ verbatim.
- **Quotes use 「」.** Single quotes for nested.
- **Names verbatim.** Don't abbreviate `蛙总` to `蛙`, don't translate Chinese names, don't anonymize.

---

## 4. Common content rules (both versions)

- **Filter only pure noise.** Cut: lone emoji reactions, "好的"/"收到"/"哈哈哈" with no follow-on, duplicate forwards.
- **Keep gossip, anecdotes, signature moments.** These are the highlight reel — the whole point of the digest.
- **Plain language.** Preserve vivid expressions and idiosyncratic phrasings — that's what makes the speaker recognizable.
- **Keep real names.** Both for traceability and so the digest is useful as memory.
- **Tool, product, URL names complete.** `Claude Code 4.7`, not `CC`. `https://github.com/...`, not `GitHub 上那个项目`.
- **Merge, don't list.** A 30-message debate becomes one paragraph, not 30 bullet points.
- **Direct-quote deep observations.** When someone says something striking, quote it verbatim with 「」 rather than paraphrase.
- **Shared articles → title + sharer.** `阿喵分享了《一个 Rust 工程师的反思》` — include the title and who shared.
- **No timestamp-based sleep/timezone inference.** (Repeated here because it applies to both versions, not just roast — never say `凌晨 3 点还在线` in either.)
- **No fabricated facts.** Every claim must be supported by an actual message in the batch (or in a loaded profile). If you're tempted to "add color," stop.

---

## 5. Output skeleton — quick reference

When you forget the structure mid-write, this is the skeleton:

### Normal

```
{群名} 群聊精华 · {日期}

📊 消息统计: 共 N 条消息
1. {昵称}: N 条
2. {昵称}: N 条
...
10. {昵称}: N 条

{开篇 1-2 段，无标题，直入主题}

群友画像

{昵称}（{角色标签}）
• {观察 1}
• {观察 2}
• {观察 3}

{昵称}（{角色标签}）
• {观察 1}
• {观察 2}

🛠 {分类标题 1}

{该分类下的整理过的讨论 / 段落 / 引用}

📦 {分类标题 2}

{...}

今日待解决问题（可选，没有就不写）

问题: {一句话}
提出者: {昵称}
背景: {1-2 句}
状态: ⚠️ 部分解决
方案: {若有}

本简报由 AI 自动生成
```

### Roast

```
{群名} 群聊精华 · {日期} · 毒舌版

📊 消息统计: 共 N 条消息
1. {昵称}: N 条 ({毒舌评语})
2. {昵称}: N 条 ({毒舌评语})
...

{毒舌开篇 1-2 段}

群友画像

{昵称}（{放大的角色标签}）
• {毒舌观察 1}
• {毒舌观察 2}

🛠 {更大声的分类标题}

{保留真实引用的毒舌叙述}

本简报由一个没有感情的 AI 自动生成,如有冒犯,概不负责
```

---

## 6. Self-check before saving

Before writing the digest file, mentally walk through:

1. Stats block accurate? Counts match the filtered message set?
2. Top 10 names resolved (self_display substituted, ambiguous nicknames disambiguated)?
3. Opening hooks at least one real category title?
4. Every active user (3+ msgs) has a 画像 entry?
5. Every category has a topic-named title (not "讨论")?
6. Every quote uses 「」 and is traceable to a real message?
7. Links inline and complete?
8. No markdown bold/heading/link syntax leaked through?
9. (Roast only) Every roast bullet would pass the §2.8 red-line audit?
10. Footer line exact match?
