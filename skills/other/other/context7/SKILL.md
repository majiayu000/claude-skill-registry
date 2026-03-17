---
name: context7
description: Search GitHub issues, pull requests, and discussions across any repository. Activates when researching external dependencies (whisper.cpp, NAudio), looking for similar bugs, or finding implementation examples.
---

# Context7 - GitHub Search

Search GitHub repositories for issues, PRs, discussions, and code examples to research solutions and best practices.

## 执行环境

| 路径类型 | 说明 |
|---------|------|
| **使用方式** | 此技能通过 API 调用使用，无需本地脚本执行 |
| **调用场景** | 当用户需要搜索 GitHub 仓库时自动激活 |
| **输入参数** | 仓库名称 (owner/repo)、搜索关键词、过滤条件 |

## 路径说明

- **无本地路径依赖**：此技能不涉及本地文件系统操作
- **仓库引用**：使用 GitHub 标准格式 `owner/repo`（如 `ggerganov/whisper.cpp`）
- **所有路径都是 GitHub 仓库内的路径**，与本地文件系统无关

## When This Skill Activates

- Keywords: "search GitHub", "find issues", "look up PR", "GitHub discussion"
- Research patterns: "Are there any [repo] issues about [topic]?"
- Dependency research: Mentions of whisper.cpp, NAudio, WPF, Inno Setup
- Bug investigation: "Has anyone else experienced [problem]?"
- Implementation examples: "How do others implement [feature]?"

## Frequently Searched Repositories

VoiceLite dependencies and related projects:

| Repository | Purpose | When to Search |
|------------|---------|----------------|
| **ggerganov/whisper.cpp** | Core transcription engine | Performance optimization, model loading, quantization issues |
| **naudio/NAudio** | Audio recording library | WaveInEvent issues, audio format problems, disposal patterns |
| **dotnet/wpf** | WPF framework | UI threading, XAML binding, Dispatcher issues |
| **jrsoftware/issrc** | Inno Setup installer | Installer configuration, file inclusion, signing |
| **dotnet/runtime** | .NET runtime | Performance issues, GC problems, async/await patterns |

## Search Syntax Examples

### Search whisper.cpp Performance Issues

```
Repository: ggerganov/whisper.cpp
Query: "performance optimization" label:performance
Sort: Most commented
Filter: Created after 2024-01-01

# Look for:
- Quantization discussions (Q8_0, Q4_0)
- Flash attention implementations
- Beam size optimization
- Model loading speed improvements
```

### Search NAudio Recording Problems

```
Repository: naudio/NAudio
Query: "WaveInEvent" label:bug is:closed
Sort: Recently updated

# Look for:
- Disposal patterns (memory leaks)
- Buffer size configurations
- Sample rate issues (16kHz mono)
- Event subscription patterns
```

### Find WPF Dispatcher Examples

```
Repository: dotnet/wpf
Query: "Dispatcher.Invoke" in:code language:csharp
Filter: Stars >100

# Look for:
- Thread-safe UI updates
- Background worker patterns
- Async dispatcher usage
```

## Search Strategies

### 1. Start Broad, Then Narrow

```
Step 1: Search issue titles
  → "transcription slow"

Step 2: Add labels
  → "transcription slow" label:performance

Step 3: Check discussions
  → Switch to Discussions tab for detailed solutions

Step 4: Look at closed issues
  → is:closed (solutions often in closed issues)
```

### 2. Finding Solutions

**For bugs**:
1. Search closed issues first (likely fixed)
2. Check PR descriptions for implementation details
3. Look for "fixed in version X" comments
4. Check release notes for related fixes

**For features**:
1. Search discussions for design rationale
2. Check PRs for code examples
3. Look for "how to" issues with detailed responses

### 3. Code Examples

```
# Search for actual code implementation
in:code language:csharp "WaveInEvent"

# Search for configuration examples
in:file filename:.csproj "NAudio"

# Search for specific patterns
in:code "async Task TranscribeAsync"
```

## Common VoiceLite Research Queries

### Whisper.cpp Performance

```
Query: "Q8_0 quantization" OR "performance improvement"
Repo: ggerganov/whisper.cpp
Labels: performance, optimization
Date: After 2024-01-01

Expected: Quantization benchmarks, speed comparisons, optimization tips
```

### NAudio Memory Leaks

```
Query: "memory leak" OR "dispose" "WaveInEvent"
Repo: naudio/NAudio
State: Closed (to find fixes)
Sort: Most commented

Expected: Disposal patterns, IDisposable best practices
```

### Inno Setup File Inclusion

```
Query: "files not included" OR "missing from installer"
Repo: jrsoftware/issrc
Labels: bug, question

Expected: Common .iss mistakes, file path issues, git ignore problems
```

### .NET Process Management

```
Query: "Process.Kill" OR "zombie process"
Repo: dotnet/runtime
Language: C#

Expected: Proper disposal patterns, timeout handling
```

## Advanced Search Operators

```
# Combine multiple terms
"whisper performance" AND "quantization"

# Exclude terms
"audio recording" NOT "streaming"

# Search specific user
author:ggerganov "optimization"

# Search by date range
created:>=2024-01-01

# Search by reactions
reactions:>10

# Search by comments
comments:>5

# Search in specific locations
in:title "memory leak"
in:body "WaveInEvent"
in:comments "fixed in"
```

## Workflow Example

**Scenario**: VoiceLite transcription is slow with tiny model

```
Step 1: Search whisper.cpp issues
  → Query: "tiny model slow" label:performance
  → Find: Issue #1234 - "Tiny model slower than expected"

Step 2: Read discussion
  → Solution: Enable flash attention, adjust beam size
  → PR #5678 has implementation

Step 3: Check PR for code changes
  → Command line flag: --flash-attn
  → Configuration: beam_size=1

Step 4: Check if applied to VoiceLite
  → Review PersistentWhisperService.cs whisper command
  → Verify flags are present

Step 5: Test & validate
  → Apply if missing, test performance improvement
```

## Troubleshooting Search Results

### "Too many results"
- Add more specific labels
- Filter by date (recent issues more relevant)
- Use `is:closed` for solved problems
- Sort by "Most commented" for well-discussed issues

### "No results found"
- Remove labels, search broadly first
- Try synonyms ("slow" vs "performance", "crash" vs "exception")
- Search discussions instead of issues
- Check if repository is active (last commit date)

### "Results not relevant"
- Add language filter (language:csharp)
- Search in code instead of issues (in:code)
- Use exact phrases with quotes: "exact error message"
- Exclude common false positives: NOT "unrelated term"

## Integration with VoiceLite Development

When researching VoiceLite issues, search these patterns:

**Audio Issues**: NAudio + "16kHz" OR "mono" OR "WAV format"
**Transcription Issues**: whisper.cpp + "model loading" OR "timeout" OR "process"
**Performance Issues**: whisper.cpp + "Q8_0" OR "optimization" OR "speed"
**Installer Issues**: Inno Setup + "missing files" OR "not included"
**Memory Issues**: .NET + "memory leak" OR "dispose" OR "GC"
