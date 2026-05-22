---
name: burpsuite-project-parser
description: Searches and explores Burp Suite project files (.burp) from the command line. Use when searching response headers or bodies with regex patterns, extracting security audit findings, dumping proxy history or site map data, or analyzing HTTP traffic captured in a Burp project.
category: burpsuite-project-parser
author: Trail of Bits
source: trailofbits/skills
license: AGPL-3.0
trit: -1
trit_label: MINUS
verified: true
featured: false
---

# Burpsuite Project Parser Skill

**Trit**: -1 (MINUS)
**Category**: burpsuite-project-parser
**Author**: Trail of Bits
**Source**: trailofbits/skills
**License**: AGPL-3.0

## Description

Searches and explores Burp Suite project files (.burp) from the command line. Use when searching response headers or bodies with regex patterns, extracting security audit findings, dumping proxy history or site map data, or analyzing HTTP traffic captured in a Burp project.

## When to Use

This is a Trail of Bits security skill. Refer to the original repository for detailed usage guidelines and examples.

See: https://github.com/trailofbits/skills

## Related Skills

- audit-context-building
- codeql
- semgrep
- variant-analysis


## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 4. Pattern Matching

**Concepts**: unification, match, segment variables, pattern

### GF(3) Balanced Triad

```
burpsuite-project-parser (+) + SDF.Ch4 (+) + [balancer] (+) = 0
```

**Skill Trit**: 1 (PLUS - generation)


### Connection Pattern

Pattern matching extracts structure. This skill recognizes and transforms patterns.
