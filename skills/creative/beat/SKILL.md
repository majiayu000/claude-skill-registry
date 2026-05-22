---
name: beat
description: 16ステップビートを生成 (JSON + ASCII grid + MIDI + WAV)。スタイルプロンプトからビートを作成。トリガー: /beat, ビートを生成, ビートを作って
allowed-tools: Read, Write, Bash(date:*), Bash(which:*), Bash(mkdir:*), Bash(uv:*), Bash(ffmpeg:*), Bash(cp:*)
---

# Beat Generator

16ステップビートシーケンサー。スタイルプロンプトから JSON / MIDI / WAV / MP3 を生成する。

## Context (auto-collected)

実行時に以下を取得:
- run_id: `date +%Y%m%d_%H%M%S`
- ffmpeg: `which ffmpeg || echo "(no ffmpeg)"`

## Pipeline

### Step 0: Prepare dirs
- `beats/` と `.beatlab/` を作成
- 出力先: `beats/<run_id>/`

### Step 1: Generate (up to 3 attempts)

最大3回リトライ:
1. `music-reference-agent` でスタイルプロンプト → BeatSpec YAML
2. `music-generation-agent` で BeatSpec → Beat JSON
3. JSON を `beats/<run_id>/beat.json` に保存
4. バリデーション:
   ```bash
   uv run python .claude/skills/beatlab-pipeline/scripts/validate.py beats/<run_id>/beat.json --inplace
   ```
5. 失敗時は `music-generation-agent` に修正を依頼してリトライ

### Step 2: Update current
```bash
cp beats/<run_id>/beat.json .beatlab/current.json
```

### Step 3: Render grid
```bash
uv run python .claude/skills/beatlab-pipeline/scripts/render_grid.py beats/<run_id>/beat.json
```

### Step 4: Export files
```bash
# MIDI
uv run python .claude/skills/beatlab-pipeline/scripts/export_midi.py beats/<run_id>/beat.json beats/<run_id>/beat.mid

# WAV
uv run python .claude/skills/beatlab-pipeline/scripts/render_wav.py beats/<run_id>/beat.json beats/<run_id>/beat.wav

# MP3 (ffmpeg がある場合)
ffmpeg -y -i beats/<run_id>/beat.wav beats/<run_id>/beat.mp3
```

## Output Format

レスポンスに含める:
- Summary: bpm, swing, run_id
- ファイルパス: beat.json / beat.mid / beat.wav (/ beat.mp3)
- ASCII 16-step grid
