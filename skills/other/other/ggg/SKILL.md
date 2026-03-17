---
name: ggg
description: Smart context filter - reduce tokens 50-90% before sending to Claude. Use when reading large files (>1000 lines), analyzing complex codebases, or when user types 'ggg'. Saves ~69% cost per task.
model: haiku
---

# GGG - Gatekeeper (Smart Context Filter)

## Purpose
Reduce token count by 50-90% before sending context to Claude using Gemini Flash or Local LLM. This dramatically reduces costs while maintaining quality.

## When to Use
- User explicitly types `ggg`
- Before reading large files (>1000 lines)
- When analyzing complex codebases
- Fixing bugs in specific areas
- Adding features to existing code
- Any task where you need focused context

## Cost Comparison
```
Before Gatekeeper:
  - Read 20k tokens: $0.06 (Claude input)
  - Total: $0.075/task

After Gatekeeper:
  - Filter 20k→2k: $0.0021 (Gemini Flash)
  - Read 2k tokens: $0.006 (Claude input)
  - Total: $0.0231/task
  - SAVINGS: 69% 🎉
```

## Steps

### 1. Check Prerequisites

Verify Python script exists:
```bash
test -f gatekeeper.py && echo "✅ Found" || echo "❌ Missing: gatekeeper.py"
```

### 2. Get Task Details

Ask user (if not already provided):
- What file to analyze?
- What task to perform? (e.g., "Fix login bug", "Add rate limiting")

### 3. Run Gatekeeper

**Mode Selection:**
- `auto` (default): Try Gemini Flash → fallback to Local LLM
- `flash`: Force Gemini Flash (best quality)
- `local`: Force Local LLM (offline/privacy)

**Execute:**
```bash
python gatekeeper.py [file-path] "[task description]" --mode auto
```

**Examples:**
```bash
# Auto mode (recommended)
python gatekeeper.py src/auth.ts "Fix login bug" --mode auto

# Force Gemini Flash
python gatekeeper.py api/routes.ts "Add rate limiting" --mode flash

# Force Local LLM
python gatekeeper.py utils.js "Refactor error handling" --mode local

# Extract specific keywords
python gatekeeper.py large_file.py "token,auth,jwt" --extract
```

### 4. Review Output

Gatekeeper will output:
```json
{
  "relevant_code": "[filtered code]",
  "summary": "[brief summary]",
  "tokens_original": 20000,
  "tokens_filtered": 2000,
  "reduction_percent": 90
}
```

### 5. Use Filtered Content

**Present to user:**
```
✅ Gatekeeper Filter Complete!

**Original Size**: 20,000 tokens
**Filtered Size**: 2,000 tokens
**Reduction**: 90%
**Cost Savings**: $0.054 (69%)

**Filtered Content:**
[Show filtered code]

**Summary:**
[Show summary]

Ready to proceed with: [task description]
```

**Then proceed with the task using the filtered content instead of the full file.**

## Important Notes

### Quality
- **Always review filtered content** before using
- If filter seems to miss important context, use `--mode flash` for better quality
- If filter fails entirely, fall back to reading full file

### Modes
- **Auto Mode**: Recommended for most cases (tries flash, falls back to local)
- **Flash Mode**: Best quality, requires GEMINI_API_KEY env var
- **Local Mode**: Works offline, quality varies

### Environment Variables
```bash
# Gemini Flash API (recommended)
export GEMINI_API_KEY="your-key-here"

# Local LLM URL (optional, fallback)
export LOCAL_LLM_URL="http://192.168.1.202:8088/v1/chat/completions"
```

### When NOT to Use
- Files < 500 lines (overhead not worth it)
- When you need complete file context
- When keywords aren't clear
- When filter consistently fails for a file type

### Fallback Strategy
If gatekeeper fails:
1. Try different mode (flash → local or vice versa)
2. Try more specific task description
3. Try `--extract` with explicit keywords
4. Fall back to reading full file

## Error Handling

**"gatekeeper.py not found":**
```bash
# Check if script exists
ls -la gatekeeper.py

# If missing, inform user:
"❌ Gatekeeper script not found. Using full file instead."
```

**"Gemini API key not set":**
```bash
# Fall back to local mode
python gatekeeper.py [file] "[task]" --mode local

# Or inform user:
"⚠️ GEMINI_API_KEY not set. Using local LLM (quality may vary)."
```

**"Local LLM not responding":**
```bash
# Inform user and fall back
"❌ Local LLM not available. Using full file instead."
```

**"Filter quality poor":**
```bash
# Try flash mode if was using local
python gatekeeper.py [file] "[task]" --mode flash

# Or fall back to full file
"⚠️ Filter quality insufficient. Using full file for accuracy."
```

## Success Criteria
- ✅ Gatekeeper script executed successfully
- ✅ Token reduction 50-90%
- ✅ Filtered content reviewed and approved
- ✅ Cost savings calculated and shown to user
- ✅ Task proceeds with filtered content
- ✅ User informed of savings

## Advanced Usage

### Batch Processing
```bash
# Filter multiple files
for file in src/*.ts; do
  python gatekeeper.py "$file" "security audit" --mode flash
done
```

### Integration with Other Skills
```bash
# Use with nnn (planning)
ggg [file] "[task]" --mode flash
# Then create plan with filtered context

# Use with gogogo (execution)
ggg [file] "[task]" --mode auto
# Then implement using focused context
```

## Performance Tips
- Use `flash` mode for production tasks (consistent quality)
- Use `local` mode for experimentation (faster, offline)
- Use `auto` mode when unsure (best of both worlds)
- Provide specific task descriptions for better filtering
- Review filtered content before relying on it
