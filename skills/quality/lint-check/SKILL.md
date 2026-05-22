---
description: Checks code for linting issues and style compliance before commits
version: 1.0.0
allowed-tools: [Bash, Grep, Glob]
---

# Lint Check

This skill performs linting and style checks on YARS code before committing, as required by project guidelines.

## Usage

Automatically invoked when:
- User asks to check linting or code style
- Before creating commits or pull requests
- After writing new code
- As part of pre-commit validation

## Checks Performed

### 1. Compiler Warnings Check
```bash
cd build
cmake .. && make -j4 2>&1 | tee build-warnings.txt
grep -i "warning:" build-warnings.txt
```

### 2. Namespace Usage Check
```bash
# Verify new files use namespace yars
grep -r "namespace yars" src/ --include="*.h" --include="*.cpp"
```

### 3. Modern C++ Patterns
```bash
# Check for NULL usage (should use nullptr)
grep -r "NULL" src/ --include="*.h" --include="*.cpp" | grep -v "nullptr"

# Check for raw pointer news that might need smart pointers
grep -r "new " src/ --include="*.cpp" | grep -v "unique_ptr" | grep -v "shared_ptr"
```

### 4. Observer Pattern Check
```bash
# Track remaining observer pattern usage
grep -r "Observable\|Observer" src/ --include="*.h" --include="*.cpp" | grep -v backup
```

## Success Criteria

- ✅ No compiler warnings
- ✅ New code uses `namespace yars {}`
- ✅ No NULL usage (nullptr instead)
- ✅ Raw pointers properly justified
- ✅ Observer pattern not introduced in new code

## Reporting

Reports should include:
- Count of any warnings found
- Files with potential issues
- Specific lines that need attention
- Suggestions for fixes

## Notes

- Must pass before code can be committed
- Some warnings may be acceptable (document why)
- Focus on new code, not legacy issues
- Integrate with git pre-commit hooks if possible
