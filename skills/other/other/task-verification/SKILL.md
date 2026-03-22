---
name: task-verification
description: |
  MANDATORY skill. Invoke BEFORE claiming any task complete. No exceptions.
  
  TRIGGERS: creating/modifying ANY file (code, script, config, docs, data). Simple changes like renaming variables, fixing typos, adding comments ALL require verification.
  
  CORE RULE: Verification = running a Bash command (python -m py_compile, node --check, etc). Reading file back is NOT verification. "Should work" is NOT verification.
  
  If you cannot show command output as evidence, the task is NOT complete. Use this skill whenever you write, edit, fix, or create anything.
---

# Task Verification - MANDATORY

## STOP! READ THIS BEFORE CLAIMING COMPLETE

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   IF YOU DID NOT RUN A BASH/SHELL COMMAND TO VERIFY,               │
│   YOU ARE NOT DONE. STOP HERE AND VERIFY NOW.                      │
│                                                                     │
│   Reading a file with the Read tool ≠ verification                 │
│   Using cat to show file contents ≠ verification                   │
│   Thinking "it looks correct" ≠ verification                       │
│                                                                     │
│   VERIFICATION = RUNNING BASH COMMAND + CAPTURING OUTPUT           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## The Verification Requirement

### What You MUST Do

1. **Create/modify your file**
2. **RUN A BASH COMMAND** (not Read tool, not cat, but an actual verification command)
3. **Capture the bash output**
4. **Include the output in your response**

### Minimum Verification Commands by File Type

| File Type | REQUIRED Bash Command |
|-----------|----------------------|
| Any `.py` file | `python -m py_compile file.py` |
| Executable `.py` script | `python file.py [test_args]` |
| `.js` file | `node --check file.js` |
| `.json` file | `python -c "import json; json.load(open('file.json')); print('✓')"` |
| `.yaml`/`.yml` | `python -c "import yaml; yaml.safe_load(open('file.yaml')); print('✓')"` |
| `.sh` file | `bash -n file.sh` |

## Examples of CORRECT Verification

### Example: Variable Rename

```
Task: Change x = 0 to count = 0

YOUR RESPONSE MUST INCLUDE:

Created code.py with count = 0

Verification:
$ python -m py_compile code.py && echo "Syntax OK"
Syntax OK

✓ Verified
```

**WRONG** - Do NOT do this:
```
Created code.py with count = 0
Verification: read the file back, it shows count = 0
```
↑ This is NOT verification. You must RUN a command.

### Example: New Script

```
Task: Create factorial script

YOUR RESPONSE MUST INCLUDE:

Created factorial.py

Verification:
$ python factorial.py 5
120

$ python factorial.py 0
1

✓ Verified
```

## The Bash Command Requirement

**CRITICAL:** Verification MUST use the Bash tool to run a command.

**NOT acceptable:**
- Read tool to read file back
- `cat file.py` to show contents
- `head file.py` or `tail file.py`
- Saying "I verified by reading"

**REQUIRED:**
- `python -m py_compile file.py`
- `python file.py args`
- `python -c "import json; json.load(...)"`
- `node file.js`
- `pytest tests/`

## Completion Checklist

Before saying "complete", verify ALL:

- [ ] I used the **Bash tool** to run a verification command
- [ ] The command I ran was NOT `cat` or `head` or `tail`
- [ ] I captured the actual output from bash
- [ ] I included the bash output in my response
- [ ] The output proves my work is correct

## Decision Flow

```
You made a change to a file.
        │
        ▼
┌────────────────────────────────────────┐
│ Did you use Bash tool to run          │
│ python -m py_compile or similar?      │
└────────────────────────────────────────┘
        │
        ├── NO → STOP! You are NOT done.
        │          Run: python -m py_compile your_file.py
        │
        └── YES → Include the output. NOW you can be done.
```

## Quick Commands to Copy

```bash
# Python syntax check - use for ANY .py file
python -m py_compile your_file.py && echo "✓ Syntax OK"

# Run Python script
python your_script.py

# JSON validation
python -c "import json; json.load(open('file.json')); print('✓ Valid JSON')"

# YAML validation
python -c "import yaml; yaml.safe_load(open('file.yaml')); print('✓ Valid YAML')"
```

---

**FINAL REMINDER: If your "verification" involved the Read tool or cat command, you have NOT verified. Run an actual command with Bash.**