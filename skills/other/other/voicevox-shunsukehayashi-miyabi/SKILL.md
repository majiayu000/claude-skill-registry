---
name: VOICEVOX Narration System
description: Generate Yukkuri-style voice narration from Git commits using VOICEVOX Engine. Use when creating development progress audio guides, YouTube content, or team reports from Git history.
allowed-tools: Bash, Read, Write, Grep, Glob
---

# VOICEVOX Narration System

Complete workflow for converting Miyabi development progress into Yukkuri-style voice narration using VOICEVOX Engine API.

## When to Use

- User requests "create voice narration", "generate audio guide", "create development report"
- After significant development milestones (weekly/daily reports)
- When preparing YouTube content for development updates
- For team communication in audio format

## Workflow Steps

### 1. VOICEVOX Engine Status Check

```bash
# Check if VOICEVOX Engine is running
curl -s http://127.0.0.1:50021/version

# If not running, start it (optional with -s flag)
cd /Users/a003/dev/voicevox_engine
uv run run.py --enable_mock --host 127.0.0.1 --port 50021
```

### 2. Generate Script from Git Commits

```bash
cd /Users/a003/dev/miyabi-private/tools

# Basic execution (last 3 days)
python3 yukkuri-narration-generator.py

# Custom time range
python3 yukkuri-narration-generator.py --days 7

# Outputs:
# - script.md: Yukkuri-style dialogue script (Reimu & Marisa)
# - voicevox_requests.json: API request data
```

### 3. Synthesize Audio with VOICEVOX

```bash
# Generate WAV files from script
python3 voicevox-synthesizer.py

# Outputs:
# - audio/speaker0_000.wav (Reimu)
# - audio/speaker1_001.wav (Marisa)
# - ... (multiple audio files)
```

### 4. Unified Execution (Recommended)

```bash
# All-in-one script with options
./miyabi-narrate.sh

# With custom options
./miyabi-narrate.sh --days 7 --output ~/Desktop/narration --start-engine

# Options:
#   -d, --days N         Past N days of commits (default: 3)
#   -o, --output DIR     Output directory (default: ./output)
#   -s, --start-engine   Auto-start VOICEVOX Engine
#   -k, --keep-engine    Keep Engine running after completion
```

### 5. Verify Output

```bash
# Check generated files
ls -lh output/

# Play audio (macOS)
afplay output/audio/speaker0_000.wav

# Read script
cat output/script.md
```

## Project-Specific Considerations

### Git Commits Parsing

The system parses Conventional Commits format:
- **Type**: feat, fix, docs, security, test, refactor
- **Scope**: Module name (e.g., design, web-ui)
- **Issue Number**: Extracted from #XXX format
- **Phase**: Extracted from "Phase X.X" format

Example commit message:
```
feat(design): complete Phase 0.4 - Issue #425
```

### VOICEVOX Speaker IDs

Default configuration:
- **Speaker ID 0**: Reimu (霊夢) - Explanation role
- **Speaker ID 1**: Marisa (魔理沙) - Reaction role

To customize speakers:
1. Check available speakers:
   ```bash
   curl http://127.0.0.1:50021/speakers | python -m json.tool
   ```

2. Edit `tools/yukkuri-narration-generator.py`:
   ```python
   self.reimu_speaker_id = 3   # Change to desired speaker
   self.marisa_speaker_id = 6  # Change to desired speaker
   ```

### Output Structure

```
output/
├── script.md                   # Yukkuri-style dialogue script
├── voicevox_requests.json      # VOICEVOX API request data
├── SUMMARY.md                  # Execution summary report
└── audio/                      # Audio files (WAV format)
    ├── speaker0_000.wav        # Reimu (intro)
    ├── speaker1_001.wav        # Marisa (response)
    ├── speaker0_002.wav        # Reimu (commit 1)
    └── ...
```

## Common Issues

### Issue: VOICEVOX Engine Connection Failed

**Symptoms**:
```
❌ VOICEVOX Engineに接続できません
```

**Solutions**:
1. Check if Engine is running:
   ```bash
   curl http://127.0.0.1:50021/version
   ```

2. Start Engine manually:
   ```bash
   cd /Users/a003/dev/voicevox_engine
   uv run run.py --enable_mock
   ```

3. Or use auto-start option:
   ```bash
   ./miyabi-narrate.sh --start-engine
   ```

### Issue: No Audio Files Generated

**Symptoms**:
- `audio/` directory is empty
- VOICEVOX API errors

**Solutions**:
1. Verify `voicevox_requests.json` exists:
   ```bash
   cat voicevox_requests.json
   ```

2. Check speaker IDs are valid:
   ```bash
   curl http://127.0.0.1:50021/speakers
   ```

3. Re-run synthesis:
   ```bash
   python3 voicevox-synthesizer.py
   ```

### Issue: No Git Commits Found

**Symptoms**:
```
0件のコミットを取得しました
```

**Solutions**:
1. Verify you're in a Git repository:
   ```bash
   git log --oneline --since="3 days ago"
   ```

2. Check if commits exist in the time range:
   ```bash
   git log --oneline --since="7 days ago"
   ```

3. Run from correct directory:
   ```bash
   cd /Users/a003/dev/miyabi-private
   tools/yukkuri-narration-generator.py
   ```

## Success Criteria

All checks must pass:
- ✅ VOICEVOX Engine is running (http://127.0.0.1:50021)
- ✅ Git commits are successfully parsed
- ✅ `script.md` is generated with dialogue
- ✅ `voicevox_requests.json` contains API requests
- ✅ Audio files are created in `audio/` directory
- ✅ All files are copied to `output/` directory

## Output Format

Report results in this format:

```
🎤 Miyabi開発進捗 → ゆっくり解説音声ガイド

✅ VOICEVOX Engine: 接続確認OK
✅ Git commits: XX件のコミットを取得
✅ 台本生成: script.md (XX行)
✅ 音声合成: XX件のファイルを生成 (XX MB)

📁 出力: output/
  - script.md
  - voicevox_requests.json
  - SUMMARY.md
  - audio/*.wav (XX files)

Ready for YouTube production ✓
```

## Integration with Miyabi

### Command Integration

Use the `/narrate` command for simplified execution:
```
/narrate
/narrate --days 7
/narrate --output ~/reports --start-engine
```

See `.claude/commands/narrate.md` for full documentation.

### Agent Integration

The NarrationAgent (`narration-agent.md`) provides automated workflow:
- Automated Git history analysis
- Context-aware dialogue generation
- Quality validation
- YouTube metadata generation

### GitHub Actions Integration

Automated daily execution:
```yaml
# .github/workflows/miyabi-narration.yml
on:
  schedule:
    - cron: '0 9 * * *'  # Daily at 18:00 JST
```

See `tools/GITHUB_ACTIONS.md` for CI/CD setup.

## Related Skills

- **Agent Execution**: For running NarrationAgent
- **Git Workflow**: For commit history management
- **Content Marketing Strategy**: For YouTube content planning

## References

- **VOICEVOX Engine**: https://github.com/VOICEVOX/voicevox_engine
- **VOICEVOX API**: https://voicevox.github.io/voicevox_engine/api/
- **Conventional Commits**: https://www.conventionalcommits.org/
- **Documentation**: `tools/README.md`, `tools/PROJECT_SUMMARY.md`
