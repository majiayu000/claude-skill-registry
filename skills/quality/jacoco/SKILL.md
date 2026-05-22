---
name: jacoco
description: Check JaCoCo code coverage for jhelm modules
argument-hint: [module]
allowed-tools: Bash(./mvnw *), Bash(python3 *)
---

## Check JaCoCo Code Coverage

Run `verify` to generate coverage reports, then parse and display results.

### Minimum threshold: **80%** line coverage

### Step 1: Generate coverage reports

**Specific module** (e.g., `/jacoco jhelm-core`):
```bash
./mvnw verify -pl $ARGUMENTS -q
```

**All modules:**
```bash
./mvnw verify -q
```

### Step 2: Module-level summary

Shows coverage percentage per module with PASS/FAIL status:

```python
python3 -c "
import xml.etree.ElementTree as ET

THRESHOLD = 80
modules = ['jhelm-gotemplate', 'jhelm-core', 'jhelm-app']
if '$ARGUMENTS':
    modules = ['$ARGUMENTS']

print(f'{'Module':<20} {'Covered':>8} {'Total':>8} {'Coverage':>10} {'Status':>8}')
print('-' * 58)
for module in modules:
    try:
        tree = ET.parse(f'{module}/target/site/jacoco/jacoco.xml')
        root = tree.getroot()
        for counter in root.findall('counter'):
            if counter.get('type') == 'LINE':
                missed = int(counter.get('missed'))
                covered = int(counter.get('covered'))
                total = missed + covered
                pct = covered / total * 100 if total > 0 else 0
                status = 'PASS' if pct >= THRESHOLD else 'FAIL'
                print(f'{module:<20} {covered:>8} {total:>8} {pct:>9.2f}% {status:>8}')
    except FileNotFoundError:
        print(f'{module:<20} {'N/A':>8} {'N/A':>8} {'N/A':>10} {'MISSING':>8}')
"
```

### Step 3: Class-level breakdown (lowest coverage first)

Find classes with lowest coverage to target improvements:

```python
python3 -c "
import xml.etree.ElementTree as ET

module = '$ARGUMENTS' if '$ARGUMENTS' else 'jhelm-gotemplate'
tree = ET.parse(f'{module}/target/site/jacoco/jacoco.xml')
root = tree.getroot()
results = []
for pkg in root.findall('.//package'):
    for cls in pkg.findall('class'):
        for counter in cls.findall('counter'):
            if counter.get('type') == 'LINE':
                missed = int(counter.get('missed'))
                covered = int(counter.get('covered'))
                total = missed + covered
                if total > 0:
                    pct = covered / total * 100
                    results.append((pct, missed, covered, total, cls.get('name')))
results.sort()
print(f'{'Coverage':>10} {'Missed':>8} {'Covered':>8} {'Total':>8}  Class')
print('-' * 80)
for pct, missed, covered, total, name in results:
    print(f'{pct:>9.1f}% {missed:>8} {covered:>8} {total:>8}  {name}')
"
```

### Step 4: Uncovered lines in a specific class

Find exact line numbers not covered (for targeted test writing):

```python
python3 -c "
import xml.etree.ElementTree as ET

module = '$ARGUMENTS' if '$ARGUMENTS' else 'jhelm-gotemplate'
tree = ET.parse(f'{module}/target/site/jacoco/jacoco.xml')
root = tree.getroot()

# Change CLASS_NAME to the target class source file
CLASS_NAME = 'REPLACE_ME.java'

for pkg in root.findall('.//package'):
    for sf in pkg.findall('sourcefile'):
        if sf.get('name') == CLASS_NAME:
            uncovered = []
            for line in sf.findall('line'):
                mi = int(line.get('mi', 0))
                if mi > 0:
                    uncovered.append(int(line.get('nr')))
            print(f'Uncovered lines in {CLASS_NAME}: {len(uncovered)} lines')
            for ln in uncovered:
                print(f'  Line {ln}')
"
```

### Step 5: Gap analysis (how many lines needed to reach threshold)

Calculate exactly how many more lines need coverage:

```python
python3 -c "
import xml.etree.ElementTree as ET
import math

THRESHOLD = 80
modules = ['jhelm-gotemplate', 'jhelm-core', 'jhelm-app']
if '$ARGUMENTS':
    modules = ['$ARGUMENTS']

for module in modules:
    try:
        tree = ET.parse(f'{module}/target/site/jacoco/jacoco.xml')
        root = tree.getroot()
        for counter in root.findall('counter'):
            if counter.get('type') == 'LINE':
                missed = int(counter.get('missed'))
                covered = int(counter.get('covered'))
                total = missed + covered
                pct = covered / total * 100 if total > 0 else 0
                needed = math.ceil(THRESHOLD / 100 * total) - covered
                if needed > 0:
                    print(f'{module}: {pct:.2f}% — need {needed} more lines covered to reach {THRESHOLD}%')
                else:
                    print(f'{module}: {pct:.2f}% — ALREADY above {THRESHOLD}% (surplus: {-needed} lines)')
    except FileNotFoundError:
        print(f'{module}: No coverage report found')
"
```

### Step 6: Quick-win targets (classes with small gaps)

Find classes where a few lines of coverage make the biggest impact:

```python
python3 -c "
import xml.etree.ElementTree as ET

module = '$ARGUMENTS' if '$ARGUMENTS' else 'jhelm-gotemplate'
tree = ET.parse(f'{module}/target/site/jacoco/jacoco.xml')
root = tree.getroot()
results = []
for pkg in root.findall('.//package'):
    for cls in pkg.findall('class'):
        for counter in cls.findall('counter'):
            if counter.get('type') == 'LINE':
                missed = int(counter.get('missed'))
                covered = int(counter.get('covered'))
                total = missed + covered
                if total > 0 and missed > 0:
                    results.append((missed, covered, total, cls.get('name')))

# Sort by fewest missed lines first (quick wins)
results.sort(key=lambda x: x[0])
print(f'{'Missed':>8} {'Covered':>8} {'Total':>8} {'Coverage':>10}  Class')
print('-' * 80)
for missed, covered, total, name in results[:20]:
    pct = covered / total * 100
    print(f'{missed:>8} {covered:>8} {total:>8} {pct:>9.1f}%  {name}')
"
```

### Step 7: Full summary report

Complete report with all counter types (LINE, BRANCH, METHOD, CLASS):

```python
python3 -c "
import xml.etree.ElementTree as ET

modules = ['jhelm-gotemplate', 'jhelm-core', 'jhelm-app']
if '$ARGUMENTS':
    modules = ['$ARGUMENTS']

for module in modules:
    try:
        tree = ET.parse(f'{module}/target/site/jacoco/jacoco.xml')
        root = tree.getroot()
        print(f'\n=== {module} ===')
        print(f'{'Type':<12} {'Covered':>8} {'Missed':>8} {'Total':>8} {'Coverage':>10}')
        print('-' * 50)
        for counter in root.findall('counter'):
            ctype = counter.get('type')
            missed = int(counter.get('missed'))
            covered = int(counter.get('covered'))
            total = missed + covered
            pct = covered / total * 100 if total > 0 else 0
            print(f'{ctype:<12} {covered:>8} {missed:>8} {total:>8} {pct:>9.2f}%')
    except FileNotFoundError:
        print(f'\n=== {module} === NO REPORT FOUND')
"
```

### Coverage improvement strategy

When coverage is below 80%:
1. Run **gap analysis** (Step 5) to see how many lines are needed
2. Run **quick-win targets** (Step 6) to find classes with fewest missed lines
3. Run **uncovered lines** (Step 4) on those classes to find exact lines
4. Write tests targeting those lines:
   - Use `@ParameterizedTest` to efficiently cover multiple code paths
   - Use Mockito for external dependencies (KubeService, RepoManager, etc.)
   - Focus on error/exception paths which are often uncovered
5. Re-run verify and summary to confirm improvement
