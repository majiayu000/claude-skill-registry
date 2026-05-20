---
name: skill-i18n
description: Translate SKILL.md and README.md files into multiple languages for sharing skills internationally
---

# Skill i18n

Translate skill documentation files (SKILL.md, README.md) into multiple languages, making it easier to share skills with international users.

## Usage

| Command | Description |
|---------|-------------|
| `/skill-i18n` | Translate files in current skill directory |
| `/skill-i18n <skill-name>` | Translate files for specified skill |
| `/skill-i18n config` | Configure default languages and file types |
| `/skill-i18n --lang zh-CN,ja` | Translate to specified languages (for integration) |
| `/skill-i18n --files SKILL.md,README.md` | Translate specified files |

## Supported Languages

| Language | Code | Output File |
|----------|------|-------------|
| 简体中文 | `zh-CN` | `SKILL.zh-CN.md` |
| 日本語 | `ja` | `SKILL.ja.md` |
| 한국어 | `ko` | `SKILL.ko.md` |
| Español | `es` | `SKILL.es.md` |
| Custom | User-defined | `SKILL.<code>.md` |

## Configuration

All settings are stored in `~/.claude/skill-i18n-config.json`:

```json
{
  "default_languages": ["zh-CN", "ja"],
  "default_files": ["SKILL.md"],
  "skills_config": {
    "port-allocator": {
      "languages": ["zh-CN", "ja", "ko"],
      "files": ["SKILL.md", "README.md"]
    }
  }
}
```

**Configuration Fields:**

| Field | Description | Default |
|-------|-------------|---------|
| `default_languages` | Languages to translate by default | `["zh-CN", "ja"]` |
| `default_files` | Files to translate by default | `["SKILL.md"]` |
| `skills_config` | Per-skill configuration | `{}` |

## Execution Steps

### Command: `/skill-i18n`

Translate files in current skill directory:

1. **Detect current directory**
   ```bash
   # Check if current directory contains SKILL.md
   if [ ! -f SKILL.md ]; then
     echo "Error: SKILL.md not found in current directory"
     exit 1
   fi
   ```

2. **Load configuration**
   ```bash
   # Read config file
   CONFIG=$(cat ~/.claude/skill-i18n-config.json 2>/dev/null || echo '{}')

   # Get skill name from directory
   SKILL_NAME=$(basename "$(pwd)")

   # Check for skill-specific config
   SKILL_CONFIG=$(echo "$CONFIG" | jq -r ".skills_config[\"$SKILL_NAME\"] // null")
   ```

3. **First-run selection (if no config)**

   If no configuration exists for this skill, show TUI selection:

   ```json
   {
     "questions": [
       {
         "question": "Which languages should be generated?",
         "header": "Languages",
         "multiSelect": true,
         "options": [
           { "label": "简体中文 (zh-CN)", "description": "Simplified Chinese" },
           { "label": "日本語 (ja)", "description": "Japanese" },
           { "label": "한국어 (ko)", "description": "Korean" },
           { "label": "Español (es)", "description": "Spanish" }
         ]
       },
       {
         "question": "Which files should be translated?",
         "header": "Files",
         "multiSelect": true,
         "options": [
           { "label": "SKILL.md", "description": "Skill documentation (recommended)" },
           { "label": "README.md", "description": "Repository readme" }
         ]
       }
     ]
   }
   ```

4. **Save configuration**
   ```bash
   # Save selection to config for future runs
   jq --arg skill "$SKILL_NAME" \
      --argjson langs '["zh-CN", "ja"]' \
      --argjson files '["SKILL.md"]' \
      '.skills_config[$skill] = {"languages": $langs, "files": $files}' \
      ~/.claude/skill-i18n-config.json > tmp.json && mv tmp.json ~/.claude/skill-i18n-config.json
   ```

5. **Execute translation**
   - For each selected file and language, generate translation
   - See "Translation Rules" section below

### Command: `/skill-i18n <skill-name>`

Translate files for specified skill:

1. **Search skill location**
   ```bash
   # Search in common locations
   SKILL_PATH=""

   # Check ~/.claude/skills/
   if [ -d ~/.claude/skills/"$SKILL_NAME" ]; then
     SKILL_PATH=~/.claude/skills/"$SKILL_NAME"
   fi

   # Check code repository (if configured)
   if [ -z "$SKILL_PATH" ] && [ -d ~/Codes/skills/"$SKILL_NAME" ]; then
     SKILL_PATH=~/Codes/skills/"$SKILL_NAME"
   fi

   if [ -z "$SKILL_PATH" ]; then
     echo "Error: Skill '$SKILL_NAME' not found"
     exit 1
   fi
   ```

2. **Execute translation** (same as default command)

### Command: `/skill-i18n config`

Configure default settings:

1. **Show current configuration**
   ```bash
   echo "Current configuration:"
   cat ~/.claude/skill-i18n-config.json | jq .
   ```

2. **Interactive configuration via AskUserQuestion**
   ```json
   {
     "questions": [
       {
         "question": "Select default languages for new skills:",
         "header": "Defaults",
         "multiSelect": true,
         "options": [
           { "label": "简体中文 (zh-CN)", "description": "Simplified Chinese" },
           { "label": "日本語 (ja)", "description": "Japanese" },
           { "label": "한국어 (ko)", "description": "Korean" },
           { "label": "Español (es)", "description": "Spanish" }
         ]
       }
     ]
   }
   ```

3. **Update configuration file**

### Command-Line Flags

For integration with other skills (e.g., share-skill):

| Flag | Description | Example |
|------|-------------|---------|
| `--lang <codes>` | Comma-separated language codes | `--lang zh-CN,ja,ko` |
| `--files <names>` | Comma-separated file names | `--files SKILL.md,README.md` |
| `--skill <name>` | Target skill name | `--skill port-allocator` |
| `--no-prompt` | Skip TUI, use flags/config directly | For automated workflows |
| `--overwrite` | Overwrite existing translations | Skip confirmation |

**Priority order:**
1. Command-line flags (highest priority)
2. Skill-specific config in `skills_config`
3. Global `default_languages` and `default_files`
4. Interactive TUI selection (if no config exists)

**Example integration:**
```bash
# share-skill calls skill-i18n internally
/skill-i18n --lang zh-CN,ja --files SKILL.md --skill port-allocator --no-prompt
```

## Translation Rules

### Preserve Unchanged

These elements must NOT be translated:

- **Code blocks** (```bash, ```json, etc.)
- **File paths** (`~/.claude/settings.json`, `~/Codes/skills/`)
- **Command names** (`/port-allocator`, `/skill-i18n`, `git push`)
- **Technical identifiers** (variable names, JSON keys)
- **URLs and links**

### Translate Naturally

- Adapt sentence structure to target language
- Use appropriate formality level:
  - Japanese: Polite form (です/ます)
  - Chinese: Standard written form
  - Korean: Polite form (합니다/습니다)
  - Spanish: Formal usted form
- Localize examples where appropriate

### Frontmatter Handling

```yaml
---
name: port-allocator          # Keep unchanged (identifier)
description: Translate this   # Translate to target language
---
```

### Style Adaptation

Different languages may use different visual styles:

| Language | Emoji Usage | Example |
|----------|-------------|---------|
| Chinese (zh-CN) | Common | ✅ 正确 / ❌ 错误 |
| Japanese (ja) | Minimal | 正しい / 間違い |
| Korean (ko) | Moderate | ✅ 올바름 / ❌ 잘못됨 |
| Spanish (es) | Minimal | Correcto / Incorrecto |

Follow existing translation patterns in the project if available.

## Output Format

### Translation Success

```
Translation complete

Skill: port-allocator
Source: SKILL.md

Generated:
  - SKILL.zh-CN.md (简体中文)
  - SKILL.ja.md (日本語)

Config saved for: port-allocator
Next run will auto-translate to: zh-CN, ja
```

### Existing Files Detected

```
Existing translations detected:
  - SKILL.zh-CN.md (modified 2 days ago)
  - SKILL.ja.md (modified 2 days ago)

Options:
  [ ] Overwrite all
  [ ] Skip existing
  [ ] Select individually
```

### Configuration Saved

```
Configuration updated

Default languages: zh-CN, ja
Default files: SKILL.md

Skill-specific config:
  port-allocator: zh-CN, ja, ko (SKILL.md, README.md)
  share-skill: zh-CN, ja (SKILL.md)
```

## Integration with share-skill

skill-i18n integrates with share-skill for documentation generation:

```bash
# share-skill docs with i18n
/share-skill docs --i18n

# This internally calls:
/skill-i18n --lang <configured-langs> --files SKILL.md --no-prompt
```

When share-skill detects `--i18n` flag:
1. Check if skill-i18n is available
2. Load language configuration
3. Call skill-i18n to generate translations
4. Include translated files in documentation site

## Notes

1. **Source file safety** - Never overwrite the source `SKILL.md` file
2. **First-run prompt** - First translation requires language selection
3. **Per-skill config** - Different skills can have different language settings
4. **Incremental updates** - Only translate when source file is newer than translations
5. **Integration-friendly** - Command-line flags allow other skills to call skill-i18n
