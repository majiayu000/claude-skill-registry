---
name: special-chars-skill
description: A skill for testing special characters and injection patterns
allowed-tools: []
---

# Special Characters Skill

This skill tests handling of special characters in $ARGUMENTS placeholder.

Test cases covered:
- HTML/XML special chars: < > & " '
- Shell metacharacters: $ ` ; | & ( ) [ ] { }
- Path traversal attempts: ../ ../../etc/passwd
- SQL injection patterns: ' OR '1'='1
- Command injection: ; rm -rf / ; $(whoami)
- Unicode and emoji: 你好 🎉 émoji

Usage: $ARGUMENTS

## Expected Behavior

The ContentProcessor should safely substitute arguments without:
1. Executing shell commands
2. Interpreting special characters
3. Allowing path traversal
4. Enabling injection attacks

All input should be treated as literal text.
