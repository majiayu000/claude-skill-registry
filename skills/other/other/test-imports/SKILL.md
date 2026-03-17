---
description: Test Python module imports to verify correct installation and structure
handoffs:
  - label: Fix Import Errors
    agent: backend-engineer
    prompt: Fix the import errors identified in the test report
    send: false
---

## User Input

```text
$ARGUMENTS
```

(Arguments are ignored - this skill auto-discovers all modules)

## Task

Test Python module imports to ensure all modules are correctly structured and importable. Automatically discovers all Python modules in the src/ directory.

### Steps

1. **Navigate to Backend Directory and Run Import Test**:

   ```bash
   cd backend && python -c "
import sys
import os
sys.path.insert(0, '.')

# Auto-discover all modules in src/
modules_to_test = []

def find_modules(directory, prefix=''):
    \"\"\"Recursively find all importable Python modules\"\"\"
    for item in sorted(os.listdir(directory)):
        item_path = os.path.join(directory, item)

        # Skip __pycache__ and hidden directories
        if item.startswith('__') or item.startswith('.'):
            continue

        if os.path.isdir(item_path):
            # If directory has __init__.py, it's a package
            init_file = os.path.join(item_path, '__init__.py')
            if os.path.exists(init_file):
                module_name = prefix + item
                modules_to_test.append(module_name)
                # Recursively check subdirectories
                find_modules(item_path, module_name + '.')
        elif item.endswith('.py') and not item.startswith('__'):
            # Python module file
            module_name = prefix + item[:-3]  # Remove .py extension
            modules_to_test.append(module_name)

# Start discovery from src/
if os.path.exists('src'):
    find_modules('src', 'src.')

print('Testing Python module imports...')
print('=' * 60)
print('Auto-discovered {} modules'.format(len(modules_to_test)))
print('=' * 60)

failed_imports = []
successful_imports = []

for module_name in modules_to_test:
    try:
        module = __import__(module_name, fromlist=[''])
        if hasattr(module, '__all__'):
            exports = module.__all__
            print('[OK] {} ({} exports)'.format(module_name, len(exports)))
        elif hasattr(module, '__dict__'):
            public_items = [k for k in module.__dict__.keys() if not k.startswith('_')]
            print('[OK] {} ({} public items)'.format(module_name, len(public_items)))
        else:
            print('[OK] {}'.format(module_name))
        successful_imports.append(module_name)
    except Exception as e:
        print('[FAIL] {}: {}'.format(module_name, str(e)))
        failed_imports.append((module_name, str(e)))

print('=' * 60)
print('Results: {} passed, {} failed'.format(len(successful_imports), len(failed_imports)))
if failed_imports:
    print()
    print('Failed Imports:')
    for module, error in failed_imports:
        print('  - {}: {}'.format(module, error))
    sys.exit(1)
else:
    print()
    print('All imports successful!')
    sys.exit(0)
"
   ```

2. **Report Results**:
   - Shows count of auto-discovered modules
   - If all imports successful: Exit with code 0
   - If any imports failed: Show error details and exit with code 1

### How It Works

- Scans `backend/src/` directory recursively
- Finds all directories with `__init__.py` (packages)
- Finds all `.py` files (modules)
- Skips `__pycache__` and hidden directories
- Automatically tests all discovered modules

### Success Criteria

- All discovered modules import without errors
- No missing dependencies
- No circular import issues
- All exports are accessible

### Error Handling

If imports fail:
1. Check error message for missing dependencies (e.g., "No module named 'pydantic'")
2. Install missing dependencies: `pip install <package-name>`
3. Rerun the test-imports skill
4. Verify file structure matches module paths
5. Ensure `__init__.py` files exist in all package directories

### Benefits

- **Future-proof**: Automatically finds new modules as you add them
- **No maintenance**: No need to update hardcoded module list
- **Complete coverage**: Tests all modules in src/ directory
- **Consistent**: Uses the proven working test method

This skill should be run:
- After creating new modules or schemas
- After refactoring imports
- Before committing code changes
- To quickly verify all imports are working
