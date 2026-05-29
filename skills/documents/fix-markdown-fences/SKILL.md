---
name: fix-markdown-fences
description: "Repair malformed markdown code fence closings. Use when markdown files have closing fences with language identifiers (```text instead of ```) or when generating markdown with code blocks to ensure proper fence closure."
license: MIT
metadata:
version: 1.0.0
model: claude-haiku-4-5
---

# Fix Markdown Code Fence Closings

## Problem

When generating markdown with code blocks, closing fences sometimes include language identifiers:

```markdown
<!-- Wrong -->
```python
def hello():
    print("world")
```python  <!-- Should be just ``` -->
```

The closing fence should never have a language identifier. This breaks markdown parsers and causes rendering issues.

## When to Use

1. After generating markdown with multiple code blocks
2. When fixing existing markdown files with rendering issues
3. When code blocks appear to "bleed" into surrounding content
4. As a validation step before committing markdown documentation

## Algorithm

Track fence state while scanning line by line:

1. **Opening fence**: Line matches `^\s*```\w+` and not inside a block. Record indent level. Enter "inside block" state.

2. **Malformed closing fence**: Line matches `^\s*```\w+` while inside a block. This is a closing fence with a language identifier. Fix by inserting proper closing fence before this line.

3. **Valid closing fence**: Line matches `^\s*```\s*$`. Exit "inside block" state.

4. **End of file**: If still inside a block, append closing fence.

## Implementation

### Python (Recommended)

```python
import re
from pathlib import Path

def fix_markdown_fences(content: str) -> str:
    """Fix malformed code fence closings in markdown content."""
    lines = content.splitlines()
    result = []
    in_code_block = False
    block_indent = ""
    
    opening_pattern = re.compile(r'^(\s*)```(\w+)')
    closing_pattern = re.compile(r'^(\s*)```\s*$')
    
    for line in lines:
        opening_match = opening_pattern.match(line)
        closing_match = closing_pattern.match(line)
        
        if opening_match:
            if in_code_block:
                # Malformed closing fence with language identifier
                # Insert proper closing fence before this line
                result.append(f"{block_indent}```")
            # Start new block
            result.append(line)
            block_indent = opening_match.group(1)
            in_code_block = True
        elif closing_match:
            result.append(line)
            in_code_block = False
            block_indent = ""
        else:
            result.append(line)
    
    # Handle file ending inside code block
    if in_code_block:
        result.append(f"{block_indent}```")
    
    return '\n'.join(result)


def fix_markdown_files(directory: Path, pattern: str = "**/*.md") -> list[str]:
    """Fix all markdown files in directory. Returns list of fixed files."""
    fixed = []
    for file_path in directory.glob(pattern):
        content = file_path.read_text()
        fixed_content = fix_markdown_fences(content)
        if content != fixed_content:
            file_path.write_text(fixed_content)
            fixed.append(str(file_path))
    return fixed
```

### Bash (Quick Check)

```bash
# Find files with potential issues (opening fence pattern at end of block)
grep -rn '```[a-zA-Z]' --include="*.md" | grep -v "^[^:]*:[0-9]*:\s*```[a-zA-Z]*$"
```

### PowerShell

```powershell
$directories = @('docs', 'src')

foreach ($dir in $directories) {
    Get-ChildItem -Path $dir -Filter '*.md' -Recurse | ForEach-Object {
        $file = $_.FullName
        $content = Get-Content $file -Raw
        $lines = $content -split "`r?`n"
        $result = @()
        $inCodeBlock = $false
        $codeBlockIndent = ""

        for ($i = 0; $i -lt $lines.Count; $i++) {
            $line = $lines[$i]

            if ($line -match '^(\s*)```(\w+)') {
                if ($inCodeBlock) {
                    $result += $codeBlockIndent + '```'
                    $result += $line
                    $codeBlockIndent = $Matches[1]
                } else {
                    $result += $line
                    $codeBlockIndent = $Matches[1]
                    $inCodeBlock = $true
                }
            }
            elseif ($line -match '^(\s*)```\s*$') {
                $result += $line
                $inCodeBlock = $false
                $codeBlockIndent = ""
            }
            else {
                $result += $line
            }
        }

        if ($inCodeBlock) {
            $result += $codeBlockIndent + '```'
        }

        $newContent = $result -join "`n"
        Set-Content -Path $file -Value $newContent -NoNewline
        Write-Host "Fixed: $file"
    }
}
```

## Usage

### Fix Files in Directory

```bash
# Python
python -c "
from pathlib import Path
exec(open('fix_fences.py').read())
fixed = fix_markdown_files(Path('docs'))
for f in fixed:
    print(f'Fixed: {f}')
"

# PowerShell
pwsh fix-fences.ps1
```

### Fix Single String (In-Memory)

```python
content = """
```python
def example():
    pass
```python
"""

fixed = fix_markdown_fences(content)
print(fixed)
```

## Verification

```bash
# Check what changed
git diff --stat

# Review specific file
git diff docs/example.md

# Validate markdown renders correctly
# (use your preferred markdown preview tool)
```

## Edge Cases Handled

1. **Nested indentation**: Preserves indent level from opening fence
2. **Multiple consecutive blocks**: Each block tracked independently
3. **File ending inside block**: Automatically closes unclosed blocks
4. **Mixed line endings**: Handles both `\n` and `\r\n`

## Prevention

When generating markdown with code blocks:

1. Always use plain ``` for closing fences
2. Never copy the opening fence line to close
3. Track block state when programmatically generating markdown
