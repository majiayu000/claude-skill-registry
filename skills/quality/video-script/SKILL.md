---
name: video-script
description: >
 Write a timestamped Chinese narration script (解说词 / 旁白) for an already-analyzed video,
 then lint/validate it. Use after video-understanding has produced agent_narration_brief.md +
 vlm_analysis.json, when you need to author the recap narration (style, anti-hallucination,
 字数公式, density, hook/throughline). Input: the understanding index in work_dir. Output:
 narration.json (validated). 触发词: 解说词, 写解说, 视频旁白, narration script, 写稿, 解说文案.
---

## What this does

Authoring + validation of the narration script. The **agent writes `work_dir/narration.json`**
following the rules below; then `validate.py` lints it against the understanding index, and in
full mode time-aligns it to quiet windows.

> **Running the scripts below** — the `scripts/…` paths are relative to this skill's own directory (the folder containing this `SKILL.md`). Claude Code runs commands from there, so they work as written. If your harness runs commands from the project root instead (opencode / Codex / OpenClaw commonly do), prefix this skill's absolute directory — e.g. `<skill-dir>/scripts/…`, using the directory your harness reports when it loads the skill. The scripts self-locate from their own path, so once started by the correct path they resolve their sibling skills and assets regardless of the working directory. Some steps here call the sibling **video-recap** skill's `scripts/` (e.g. `recap_inspect.py`); resolve those the same way, via that skill's directory.

## Step 1 — read the brief

Read `work_dir/agent_narration_brief.md` (scenes, durations, quiet windows, char budget) first.
Digest long dialogue via `asr_writing_chunks.json`; judge "is there speech/a silent slot here?"
via `timeline_fusion.json`. Check raw `vlm_analysis.json` / `asr_result.json` for details.
In full mode, timestamps are **original-video time**. In orchestrated cut mode, pass 1 only writes `clip_plan.json`; after `edited_source.mp4` exists, pass 2 writes `narration.json` in **output timeline time**.

写稿前先跑同捆 video-recap skill 的 `scripts/recap_inspect.py`（即 `recap_inspect.py --work-dir <work_dir> state`，用其绝对路径调起，见上方「Running the scripts」说明）看清楚当前模式、缺哪个产物、下一步该写什么。cut pass 2 写解说时用 `recap_inspect.py --work-dir <work_dir> clip-map --output-start <s> --output-end <e>`（或 `--source-start/--source-end`）核对输出↔原片时间轴，确认某段成片对应哪段原片、有没有跨剪辑边界或落进被剪掉的区间。

## Step 2 — write narration.json

```json
[
  {"start": 5.0, "end": 12.0, "narration": "解说文本。", "pause_after_ms": 250, "overlaps_speech": true}
]
```

| Field | Meaning |
|------|------|
| `start` / `end` | narration start/end seconds: original-video time in full mode; output timeline time in orchestrated cut pass 2 |
| `narration` | narration text |
| `pause_after_ms` | pause after segment, default 250 (keeps a tight rhythm) |
| `overlaps_speech` | overlaps original dialogue; default `true` for continuous-bed style, `false` only in true silence |

Optionally also author `original_subtitles.json` — `[{start,end,text}]` (OUTPUT time) — the calibrated
original dialogue burned during the original-audio gaps (ASR errors/names fixed, only what is actually
spoken there). Rendered in `「」` to set it apart from narration. If omitted, assemble falls back to a
conservative auto-ASR mapping. See the brief's `原声留白字幕` section.

### 写作规则（BLOCK recap + 原声留白）

1. **按 BLOCK 写**：每个 beat 是一个 2–4 句的连续想法，合成为一条流畅 TTS；不要回到“一句一停”的碎句模式。
2. **约 7:3 节奏**：让解说覆盖约 70% 成片时间，刻意留下约 30% 多秒原声留白，让关键对白、动作或音乐完整呼吸。
3. **块与原声交替**：一块解说铺垫原声留白，下一块承接原声刚呈现的信息；禁止墙到墙不停讲，也禁止每句之间机械小缝。
4. **按 brief 的 block 数量和有效语速控量**：每块窗口按 `字数 / brief 头部 speech budget` 估算，太长就拆块，太短就合并成完整想法。
5. **不要看图说话**：观众看得见动作表情，解说讲动机、关系、潜台词和剧情意义（基于画面**可见的证据**，不要编造）。
6. **用已知角色名**：`--context` 或 `background_research.json` 给出角色名时优先使用。
7. **完整句子**：以句号 / 问号 / 感叹号结束，不写半句。

### 解说手法（区分“解说”和“字幕”）

- **钩子**：开头 1-2 个 beat 制造悬念或利害，不是交代场景。
- **主线**：选一条主线（目标 / 关系 / 悬念），每个 beat 都推进它。
- **递进**：信息和张力逐步升级。**悬念缺口**：提前埋后果，后面回收。
- **收尾**：最后 1-2 个 beat 给出结果或反转，不要泛泛收场。
- **衔接**：解说块和它旁边的原声留白是同一个 beat——块尾给原声铺垫，下一块承接原声刚呈现的内容，别和原声各说各的。
- **给信息而非念画面**；**去废词**：用具体名词动词，删空泛形容。

## Step 2.5 — review GATE (advisory, logged, overridable)

A separate **quality** pass (LLM-as-judge), distinct from the mechanical lint below. Needs the chat API key (same as VLM).

1. Run: `python3 scripts/review.py --work-dir <work_dir>` (auto-detects cut mode and grounds against the OUTPUT timeline when a validated cut is present; pass `--timeline source` to force source grounding)
2. Open `narration_review.md`. For every `error` finding (ESPECIALLY `category=hallucination` — a claim
   not grounded in the visual/ASR evidence), revise `narration.json` and re-run review until either:
   - (a) verdict == `OK` with zero `error` findings, OR
   - (b) you consciously **OVERRIDE** a remaining finding (next step).
3. To OVERRIDE: append a block to `work_dir/narration_review_override.md` naming WHICH finding
   (segment + category), WHY it is acceptable, and who signed off. Unaddressed `error` findings with
   no override entry mean the draft is **NOT ready**.
4. Only then proceed to Step 3 (`validate.py` — the hard gate).

**GATE rule:** review NEVER blocks the tooling (it leans on a flaky chat API and a re-render is cheap).
`validate.py` is the deterministic hard gate. The override log makes "we saw the finding and chose to
ship it" auditable — review.py / validate.py never read it; it is a record for the human in the loop.

Override block shape — `work_dir/narration_review_override.md` (append-only):

```
## Override — <date>
- Finding: segment 4 / category=hallucination
- Reviewer said: "‘他早已知情’无画面/对白依据"
- Decision: KEEP — grounded in the --context synopsis (s2 reveal); reviewer lacked that context.
- Signed: <agent/human>
```

## Step 3 — validate

```bash
python3 scripts/validate.py --work-dir <work_dir> --mode full   # or --mode cut
```

Writes `narration_lint.json`; in `full` mode rewrites `narration.json` with quiet-window alignment.
Fix any lint errors and re-run until clean.

## Cut mode (long video → short recap)

The orchestrated `video-recap --edit-mode cut` flow is **cut-first / narrate-second**:

1. Pass 1: write `work_dir/clip_plan.json` only, using original-time source ranges to keep.
2. The CLI renders `edited_source.mp4` and rebuilds the brief with kept clips on the output timeline.
3. Pass 2: write `narration.json` directly in **output time** (`0..edited_source.mp4 duration`). Validate with `--mode cut_output` via the orchestrator.

The direct `video-cut` legacy path can still map original-time narration, but the orchestrated recap path does not use that remap.

```json
{"target_duration": "10m", "clips": [{"start": 12.0, "end": 38.0, "reason": "冲突开端"}]}
```

**剪辑模式写作要点（解说要对上剪后的画面，不是原片）：**
- **Pass 1 只选片段**：`clip_plan.json` 使用原片 source timestamps，挑出完整故事弧，不写解说。
- **Pass 2 按实际成片写**：`edited_source.mp4` 已存在时，brief 会列出 kept clips 的 OUTPUT ranges；解说 beat 数量按实际剪后时长估算，不按原片时长。
- **时间轴是 OUTPUT time**：`narration.json` 的 `[start,end]` 直接落在剪后成片 `0..total` 时间轴上，不会再做 source→output 映射，也不会静默丢弃。
- **按成片顺序讲**：围绕输出时间轴讲一条连续故事线，块尾给原声留白铺垫，下一块承接留白里的对白/动作。

> 片名/题材明确但缺乏剧情上下文时，先按 [背景调研指南](../video-understanding/references/research-guide.md) 写 `background_research.json` 再写解说——否则解说只能"看图说话"。brief 在 substrate 偏薄时会把密度目标降为上限而非配额：宁可少写、写实，也不要为凑数堆画面描述。

## What this skill does NOT do
- Does NOT run ASR/VLM or analyze the video — it consumes the understanding index.
- Does NOT synthesize audio or render video.
- `review.py` does NOT edit narration.json and does NOT block the pipeline — it is advisory.
- `validate.py` does NOT rewrite the meaning of the text — it only checks/aligns timing and quiet windows.
