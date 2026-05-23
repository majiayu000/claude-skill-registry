---
name: search-algorand-examples
description: Search GitHub for Algorand smart contract examples and patterns. Use when finding example implementations of specific patterns (BoxMap, inner transactions), looking up contract feature usage, discovering Algorand repositories, or retrieving files from algorandfoundation repos. Strong triggers include "find an example of...", "show me how to use BoxMap", "search for voting contract examples", "get the code from puya-ts examples", "find Algorand NFT repositories".
---

# Searching Algorand Examples

Find working contract examples and code patterns from Algorand Foundation repositories using GitHub tools.

## Overview / Core Workflow

1. Identify what pattern or example the user needs
2. Choose the appropriate tool (`github_search_code`, `github_get_file_contents`, or `github_search_repositories`)
3. Search priority repositories first (devportal-code-examples, puya-ts)
4. Retrieve the relevant file(s)
5. Also fetch corresponding test files when applicable

## How to proceed

1. **Determine the search type:**
   - Looking for a specific pattern → use `github_search_code`
   - Need a specific file → use `github_get_file_contents`
   - Discovering repositories → use `github_search_repositories`

2. **Search priority repositories first:**

   | Priority | Repository | Best For |
   |----------|------------|----------|
   | 1 | `algorandfoundation/devportal-code-examples` | Beginner-friendly patterns |
   | 2 | `algorandfoundation/puya-ts` | Advanced TypeScript examples |
   | 3 | `algorandfoundation/puya` | Python examples |
   | 4 | `algorandfoundation/algokit-*` | Templates and utilities |

3. **Execute the search:**

   ```
   # Search for code patterns
   github_search_code query:"BoxMap org:algorandfoundation language:typescript"

   # Get specific file
   github_get_file_contents owner:algorandfoundation repo:puya-ts path:examples/voting/contract.algo.ts

   # List directory contents
   github_get_file_contents owner:algorandfoundation repo:puya-ts path:examples

   # Find repositories
   github_search_repositories query:"topic:algorand smart-contract"
   ```

4. **Always fetch test files:**
   - For any contract file, check for corresponding `*.spec.ts` or `*_test.py`
   - Tests show how to call methods and verify behavior

## Important Rules / Guidelines

- **Search algorandfoundation first** — Official repos have vetted, up-to-date examples
- **Always include test files** — They demonstrate correct usage patterns
- **Use specific queries** — Include `org:algorandfoundation` and `language:typescript` for better results
- **Check file paths in devportal-code-examples:**
  - TypeScript: `projects/typescript-examples/contracts/`
  - Python: `projects/python-examples/contracts/`
- **Prefer puya-ts/examples for complex patterns** — Voting, AMM, auction examples are comprehensive

## If GitHub MCP Tools Unavailable

Use web search as fallback:

- **For code search**: `site:github.com algorandfoundation {pattern} language:typescript`
- **For specific files**: Browse directly to `https://github.com/algorandfoundation/puya-ts/tree/main/examples`
- **For repos**: Search `site:github.com algorand {topic}`

Key URLs to browse directly:
- https://github.com/algorandfoundation/devportal-code-examples
- https://github.com/algorandfoundation/puya-ts/tree/main/examples
- https://github.com/algorandfoundation/puya/tree/main/examples

## Common Variations / Edge Cases

| Scenario | Approach |
|----------|----------|
| Pattern not found in algorandfoundation | Expand search to all of GitHub |
| Need Python instead of TypeScript | Search `algorandfoundation/puya` instead |
| Looking for deployment patterns | Check `algokit-*-template` repos |
| Need ARC standard implementation | Search for "ARC-{number}" in code |

## References / Further Reading

- [Tool Reference](./references/REFERENCE.md)
- [DevPortal Code Examples](https://github.com/algorandfoundation/devportal-code-examples)
- [Puya TypeScript Examples](https://github.com/algorandfoundation/puya-ts/tree/main/examples)
- [Algorand Developer Portal](https://dev.algorand.co/)
