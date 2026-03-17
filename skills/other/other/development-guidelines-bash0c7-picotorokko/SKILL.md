---
name: Development Guidelines
description: Defines coding standards, test patterns, and language conventions for this project. Use this when writing code, comments, documentation, or git commit messages.
---

# Development Guidelines

Coding standards, naming conventions, and language conventions for PicoRuby development.

## Output Style & Language

For complete output style requirements (Japanese output with ピョン。ending, etc.), see:

**`.claude/docs/output-style.md`** — PROTECTED output style requirements

## Code Comments

**Ruby files (.rb)**:
- Language: Japanese
- Style: Noun-ending (体言止め) — no period needed
- Purpose: Explain the *why*, not the *what*

```ruby
# ピクセルの色計算
def calc_color(intensity)
  # 0-255 スケールで正規化
  # グリーンチャネル優先
  [0, intensity, intensity / 2]
end
```

## Documentation Files

**Markdown (.md)**:
- Language: English
- Purpose: Reference material, API docs, architecture
- No Japanese in `.md` files (except code comments within blocks)

## Git Commits

**Format**: English, imperative mood

```
Add LED animation feature
Implement blinking pattern with configurable frequency.
```

**Guidelines**:
- Title: 50 chars max, imperative ("Add", "Fix", "Refactor")
- Body: Explain *why* the change matters (if needed)
- Always use `commit` subagent (never raw git commands)

**Examples**:
- ✅ "Add MP3 playback support"
- ✅ "Fix memory leak in LED buffer"
- ✅ "Refactor IMU data reading for clarity"
- ❌ "Added new feature"
- ❌ "Fixed stuff"

## Test Temporary Files Management

### Principle: Block-Based Temp File Creation

**Reasons**:
- **Security**: Prevent symlink attacks (IPA security guidelines)
- **Safety**: Guaranteed cleanup on block exit (even on exceptions)
- **Reference**: Rubyist Magazine 0029, "安全に一時ファイルを作成するのは素人には難しく"

### Pattern A: File Operations (Preferred)

```ruby
test "file operation" do
  Tempfile.open('test') do |file|
    file.write("content")
    # Assertions
  end  # Auto-deleted
end
```

**Docs**: https://docs.ruby-lang.org/ja/latest/class/Tempfile.html

### Pattern B: Directory Structures (When Needed)

```ruby
test "directory structure" do
  Dir.mktmpdir do |tmpdir|
    Dir.chdir(tmpdir) do
      FileUtils.mkdir_p("foo/bar")
      # Assertions
    end
  end  # Removed by FileUtils.remove_entry_secure
end
```

**Docs**: https://docs.ruby-lang.org/ja/latest/method/Dir/s/mktmpdir.html

### Exception: setup/teardown (Discouraged)

- **Use only when**: Multiple tests must share state
- **Must**: Implement teardown for guaranteed cleanup (FileUtils.rm_rf)
- **Risk**: Cleanup failure if teardown not executed

### References

- https://docs.ruby-lang.org/ja/latest/class/Tempfile.html
- https://docs.ruby-lang.org/ja/latest/method/Dir/s/mktmpdir.html
- https://magazine.rubyist.net/articles/0029/0029-BundledLibraries.html
