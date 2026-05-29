---
name: interpolation-skill
description: Tests variable interpolation features like {baseDir}. Use for testing path expansion.
allowed-tools: Read Glob
---

# Interpolation Skill

This skill demonstrates variable interpolation.

## Base Directory

The base directory for this skill is: {baseDir}

## Instructions

When invoked, this skill should:

1. Read configuration from {baseDir}/config.json
2. Load reference data from {baseDir}/references/data.txt
3. Execute scripts from {baseDir}/scripts/process.sh

## File References

See [the reference guide]({baseDir}/references/REFERENCE.md) for details.

Run the extraction script:
```bash
{baseDir}/scripts/extract.py
```

## Notes

All paths using {baseDir} should be expanded to the absolute path
of the directory containing this SKILL.md file.
