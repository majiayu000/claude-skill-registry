---
name: jta
description: Translate JSON i18n files to multiple languages with AI-powered quality optimization. Use when user mentions translating JSON, i18n files, internationalization, locale files, or needs to convert language files to other languages.
version: 1.0.0
allowed-tools: Read, Write, Bash, Glob
---

# Jta Translation

AI-powered JSON internationalization file translator with Agentic reflection mechanism.

## When to Use This Skill

- User asks to translate JSON i18n/locale files
- User mentions "internationalization", "i18n", "l10n", or "locale"
- User wants to add new languages to their project
- User needs to update existing translations
- User mentions specific languages like "translate to Chinese/Japanese/Korean"

## Core Capabilities

1. **Agentic Translation**: AI translates, evaluates, and improves its own work (3x API calls per batch)
2. **Smart Terminology**: Automatically detects and maintains consistent terms (brand names, technical terms)
3. **Format Protection**: Preserves `{variables}`, `{{placeholders}}`, HTML tags, URLs, Markdown
4. **Incremental Mode**: Only translates new/changed content (saves 80-90% API cost on updates)
5. **27 Languages**: Including RTL languages (Arabic, Hebrew, Persian, Urdu)

## Instructions

### Step 1: Check if jta is installed

```bash
# Check if jta exists
if ! command -v jta &> /dev/null; then
  echo "jta not found, will install"
fi
```

### Step 2: Install jta if needed

```bash
# Detect OS and install jta
OS="$(uname -s)"
ARCH="$(uname -m)"

if [[ "$OS" == "Darwin"* ]]; then
  # macOS - try Homebrew first
  if command -v brew &> /dev/null; then
    brew tap hikanner/jta
    brew install jta
  else
    # Download binary
    if [[ "$ARCH" == "arm64" ]]; then
      curl -L https://github.com/hikanner/jta/releases/latest/download/jta-darwin-arm64 -o jta
    else
      curl -L https://github.com/hikanner/jta/releases/latest/download/jta-darwin-amd64 -o jta
    fi
    chmod +x jta
    sudo mv jta /usr/local/bin/
  fi
elif [[ "$OS" == "Linux"* ]]; then
  # Linux
  curl -L https://github.com/hikanner/jta/releases/latest/download/jta-linux-amd64 -o jta
  chmod +x jta
  sudo mv jta /usr/local/bin/
fi

# Verify installation
jta --version
```

### Step 3: Check for API key and set provider

Jta requires an AI provider API key. Check in this order and set the provider flag:

```bash
# Detect API key and set provider flag
if [[ -n "$ANTHROPIC_API_KEY" ]]; then
  echo "✓ Anthropic API key found"
  PROVIDER_FLAG="--provider anthropic"
elif [[ -n "$GEMINI_API_KEY" ]]; then
  echo "✓ Gemini API key found"
  PROVIDER_FLAG="--provider gemini"
elif [[ -n "$OPENAI_API_KEY" ]]; then
  echo "✓ OpenAI API key found"
  PROVIDER_FLAG=""  # OpenAI is default, no flag needed
else
  echo "✗ No API key found. Please set one of:"
  echo "  export OPENAI_API_KEY=sk-..."
  echo "  export ANTHROPIC_API_KEY=sk-ant-..."
  echo "  export GEMINI_API_KEY=..."
  exit 1
fi
```

**Important:** Save the `PROVIDER_FLAG` value to use in translation commands.

### Step 4: Identify source file

```bash
# Find JSON files in common i18n/locale directories
find . -type f -name "*.json" \
  \( -path "*/locales/*" -o \
     -path "*/locale/*" -o \
     -path "*/i18n/*" -o \
     -path "*/lang/*" -o \
     -path "*/translations/*" \) \
  | head -20
```

Ask user to confirm which file to translate if multiple found.

### Step 5: Determine translation requirements

Ask user (if not specified in their request):
- Target languages (e.g., "zh,ja,ko")
- Whether to use incremental mode (recommended for updates)
- Output location preference

### Step 6: Execute translation

**Always use `$PROVIDER_FLAG` from Step 3** to ensure the correct AI provider is used:

```bash
# Basic translation with detected provider
jta <source-file> --to <target-langs> $PROVIDER_FLAG

# Examples:
# Single language
jta en.json --to zh $PROVIDER_FLAG

# Multiple languages
jta en.json --to zh,ja,ko $PROVIDER_FLAG

# Incremental mode (for updates)
jta en.json --to zh --incremental $PROVIDER_FLAG

# With custom output
jta en.json --to zh --output ./locales/zh.json $PROVIDER_FLAG

# Non-interactive mode (for multiple languages)
jta en.json --to zh,ja,ko,es,fr -y $PROVIDER_FLAG

# Override with specific model for quality
jta en.json --to zh --provider anthropic --model claude-sonnet-4-5

# Translate specific keys only
jta en.json --to zh --keys "settings.*,user.*" $PROVIDER_FLAG

# Exclude certain keys
jta en.json --to zh --exclude-keys "admin.*,internal.*" $PROVIDER_FLAG
```

### Step 7: Verify results

After translation completes:

```bash
# Check output files exist
ls -lh <output-files>

# Validate JSON structure
for file in <output-files>; do
  if jq empty "$file" 2>/dev/null; then
    echo "✓ $file is valid JSON"
  else
    echo "✗ $file has invalid JSON"
  fi
done
```

### Step 8: Report to user

Show the user:
- Translation statistics (total items, success rate, API calls, duration)
- Location of output files
- Any errors or warnings
- Cost implications if significant (e.g., "Used 15 API calls, estimated $0.30")

## Terminology Management

Jta automatically creates a `.jta/` directory to store terminology:

```
.jta/
├── terminology.json       # Source language terms (preserve + consistent)
├── terminology.zh.json    # Chinese translations
├── terminology.ja.json    # Japanese translations
└── terminology.ko.json    # Korean translations
```

**terminology.json** structure:
```json
{
  "version": "1.0",
  "sourceLanguage": "en",
  "preserveTerms": ["API", "OAuth", "GitHub"],
  "consistentTerms": ["credits", "workspace", "prompt"]
}
```

Users can manually edit these files for custom terminology.

## Common Patterns

**Note:** Always include `$PROVIDER_FLAG` (from Step 3) in your commands.

### Pattern 1: First-time translation
```bash
# User: "Translate my en.json to Chinese and Japanese"
jta locales/en.json --to zh,ja -y $PROVIDER_FLAG
```

### Pattern 2: Update existing translations
```bash
# User: "I added new keys to en.json, update the translations"
jta locales/en.json --to zh,ja --incremental -y $PROVIDER_FLAG
```

### Pattern 3: Translate specific sections
```bash
# User: "Only translate the settings and user sections"
jta en.json --to zh --keys "settings.**,user.**" $PROVIDER_FLAG
```

### Pattern 4: High-quality translation
```bash
# User: "Use the best model for highest quality"
jta en.json --to zh --provider anthropic --model claude-sonnet-4-5
```

### Pattern 5: RTL languages
```bash
# User: "Translate to Arabic and Hebrew"
jta en.json --to ar,he -y $PROVIDER_FLAG
# Jta automatically handles bidirectional text markers
```

## Error Handling

### Error: "jta: command not found"
- Run the installation script from Step 2
- Verify with `jta --version`

### Error: "API key not set"
Prompt user:
```
Jta requires an AI provider API key. Please set one of:

For OpenAI (recommended):
  export OPENAI_API_KEY=sk-...
  Get key at: https://platform.openai.com/api-keys

For Anthropic:
  export ANTHROPIC_API_KEY=sk-ant-...
  Get key at: https://console.anthropic.com/

For Google Gemini:
  export GEMINI_API_KEY=...
  Get key at: https://aistudio.google.com/app/apikey
```

### Error: "Rate limit exceeded"
```bash
# Reduce batch size and concurrency
jta en.json --to zh --batch-size 10 --concurrency 1
```

### Error: "Invalid JSON"
```bash
# Validate source file
jq . source.json
```

### Error: Translation quality issues
1. Try a better model:
   ```bash
   jta en.json --to zh --provider anthropic --model claude-sonnet-4-5
   ```

2. Check terminology files in `.jta/` and edit if needed

3. Use verbose mode to debug:
   ```bash
   jta en.json --to zh --verbose
   ```

## Performance Tips

- **Small files (<100 keys)**: Use default settings
- **Large files (>500 keys)**: Use `--batch-size 10 --concurrency 2`
- **Frequent updates**: Always use `--incremental` to save cost
- **Quality priority**: Use `--provider anthropic --model claude-sonnet-4-5`
- **Speed priority**: Use `--provider openai --model gpt-3.5-turbo` (if available)
- **Cost priority**: Use incremental mode + larger batch sizes

## Supported Languages

27 languages with full support:

**Left-to-Right (LTR):**
- European: en, es, fr, de, it, pt, ru, nl, pl, tr
- Asian: zh, zh-TW, ja, ko, th, vi, id, ms, hi, bn, si, ne, my

**Right-to-Left (RTL):**
- Middle Eastern: ar, fa, he, ur

View all supported languages:
```bash
jta --list-languages
```

## Output Format

Jta produces:
1. **Translated JSON files**: Same structure as source, with translations
2. **Statistics**: Printed to console
3. **Terminology files**: In `.jta/` directory for consistency

Always inform the user of:
- Number of items translated
- Success/failure count
- Output file locations
- Any errors or warnings
- API usage and estimated cost (if significant)

## Advanced Options

**Note:** Remember to include `$PROVIDER_FLAG` in your commands.

```bash
# Skip terminology detection (use existing)
jta en.json --to zh --skip-terminology $PROVIDER_FLAG

# Disable terminology management completely
jta en.json --to zh --no-terminology $PROVIDER_FLAG

# Re-detect terminology (when source language changes)
jta en.json --to zh --redetect-terms $PROVIDER_FLAG

# Custom terminology directory (for shared terms)
jta en.json --to zh --terminology-dir ../shared-terms/ $PROVIDER_FLAG

# Specify source language explicitly
jta myfile.json --source-lang en --to zh $PROVIDER_FLAG

# Custom batch size and concurrency
jta en.json --to zh --batch-size 20 --concurrency 3 $PROVIDER_FLAG

# Verbose output for debugging
jta en.json --to zh --verbose $PROVIDER_FLAG
```

## Examples

See [examples/](examples/) directory for detailed, step-by-step use cases.
