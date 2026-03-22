---
name: checkstyle
description: Check and fix Checkstyle violations in jhelm modules
argument-hint: [module]
allowed-tools: Bash(./mvnw *), Bash(python3 *)
---

## Check and Fix Checkstyle Violations

### Configuration

- **Plugin**: `maven-checkstyle-plugin` 3.6.0 with `spring-javaformat-checkstyle` 0.0.43
- **Suppressions**: `checkstyle-suppressions.xml` in project root
- **Violations fail the build** at `validate` phase (before compile)

### Step 1: Check violations

**All modules**:
```bash
./mvnw validate 2>&1 | grep -E "violations|ERROR.*\.java"
```

**Specific module** (e.g., `/checkstyle jhelm-core`):
```bash
./mvnw validate -pl $ARGUMENTS 2>&1 | grep "^\[ERROR\]"
```

### Step 2: Auto-format first

Always run `spring-javaformat:apply` before checking violations — it fixes indentation/spacing automatically:
```bash
./mvnw spring-javaformat:apply
```

### Step 3: Fix remaining violations with Python script

Save this script as `/tmp/fix_violations.py` and run for any module:

```python
#!/usr/bin/env python3
"""Fix checkstyle violations: SpringCatch, NeedBraces, SpringLambda, SpringTernary,
AvoidStarImport, UnusedImports, AnnotationUseStyle."""

import re, os
from pathlib import Path

JAVA_KEYWORDS = {
    'abstract','assert','boolean','break','byte','case','catch','char','class',
    'const','continue','default','do','double','else','enum','extends','final',
    'finally','float','for','goto','if','implements','import','instanceof','int',
    'interface','long','native','new','package','private','protected','public',
    'return','short','static','strictfp','super','switch','synchronized','this',
    'throw','throws','transient','try','void','volatile','while',
    'null','true','false','var','record','sealed','permits','yield',
}

STATIC_STAR_IMPORTS = {
    'org.junit.jupiter.api.Assertions': [
        'assertEquals','assertNotEquals','assertTrue','assertFalse','assertNull',
        'assertNotNull','assertThrows','assertDoesNotThrow','assertSame','assertNotSame',
        'fail','assertAll','assertArrayEquals','assertIterableEquals','assertInstanceOf',
    ],
    'org.mockito.Mockito': [
        'mock','when','verify','doReturn','doThrow','doNothing','doAnswer','spy',
        'times','never','atLeast','atLeastOnce','atMost','reset',
        'verifyNoInteractions','verifyNoMoreInteractions','lenient','inOrder',
        'mockConstruction','mockStatic','any','anyString','anyInt','anyLong',
        'anyBoolean','anyList','anyMap','anySet','eq','isNull','isNotNull','same','argThat',
    ],
    'org.mockito.ArgumentMatchers': [
        'any','anyString','anyInt','anyLong','anyBoolean','anyList','anyMap',
        'anySet','eq','isNull','isNotNull','same','argThat',
    ],
}

REGULAR_STAR_IMPORTS = {
    'java.util': ['List','ArrayList','Map','HashMap','LinkedHashMap','TreeMap',
        'Set','HashSet','LinkedHashSet','TreeSet','Collections','Arrays','Optional',
        'Iterator','Queue','Deque','LinkedList','Objects','Comparator','UUID',],
    'java.io': ['File','InputStream','OutputStream','IOException','FileInputStream',
        'FileOutputStream','BufferedInputStream','BufferedReader','BufferedWriter',
        'StringWriter','StringReader','Closeable','ByteArrayInputStream','ByteArrayOutputStream',],
    'org.alexmond.jhelm.core': ['Engine','Chart','ChartMetadata','ChartLoader',
        'ChartLock','Dependency','DependencyResolver','Release','RepositoryConfig',
        'KubeService','ListAction','InstallAction','UpgradeAction','UninstallAction',
        'RollbackAction','GetAction','StatusAction','HistoryAction','ShowAction',
        'TemplateAction','CreateAction','RepoManager','RegistryManager',
        'HelmChartTemplates','CoreConfig',],
    'io.kubernetes.client.openapi.models': None,  # auto-detect V1* classes
}

def fix_spring_catch(content):
    lines = content.split('\n')
    result, i = [], 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r'^(\s*catch\s*\(\s*(?:\w+(?:\s*\|\s*\w+)*)\s+)(e)(\s*\)\s*)\{(.*)$', line)
        if m:
            result.append(m.group(1) + 'ex' + m.group(3) + '{' + m.group(4))
            i += 1
            depth = 1
            while i < len(lines) and depth > 0:
                bl = lines[i]
                for ch in bl:
                    if ch == '{': depth += 1
                    elif ch == '}': depth -= 1
                if depth > 0:
                    bl = re.sub(r'\be\.', 'ex.', bl)
                    bl = re.sub(r'(?<=[,\s(])\be\b(?=[,\s);])', 'ex', bl)
                    bl = re.sub(r'\bthrow\s+e\s*;', 'throw ex;', bl)
                result.append(bl)
                i += 1
        else:
            result.append(line)
            i += 1
    return '\n'.join(result)

def count_net_parens(line):
    depth, in_str, str_ch, esc = 0, False, None, False
    for ch in line:
        if esc: esc = False; continue
        if ch == '\\': esc = True; continue
        if in_str:
            if ch == str_ch: in_str = False
        else:
            if ch in ('"', "'"): in_str, str_ch = True, ch
            elif ch == '(': depth += 1
            elif ch == ')': depth -= 1
    return depth

def fix_need_braces(content):
    lines = content.split('\n')
    result, i = [], 0
    CTRL = re.compile(r'^\s*(?:(?:else\s+)?if|for|while)\s*\(')
    ELSE = re.compile(r'^(\s*)else\s*$')
    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip()
        em = ELSE.match(stripped)
        if em and i + 1 < len(lines):
            indent = em.group(1)
            ns = lines[i+1].strip()
            if ns and not ns.startswith(('{','//','*','@')):
                result.extend([line + ' {', lines[i+1], indent + '}'])
                i += 2; continue
        if CTRL.match(stripped):
            net = count_net_parens(stripped)
            if net == 0 and not stripped.endswith('{') and stripped.endswith(')'):
                if i + 1 < len(lines):
                    ns = lines[i+1].strip()
                    if ns and not ns.startswith(('{','//','*','@')) and not CTRL.match(ns):
                        indent = re.match(r'^(\s*)', line).group(1)
                        result.extend([line + ' {', lines[i+1], indent + '}'])
                        i += 2; continue
        result.append(line); i += 1
    return '\n'.join(result)

def fix_lambda_blocks(content):
    lines = content.split('\n')
    result, i = [], 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r'^(.*?)\s*->\s*\{\s*$', line.rstrip())
        if m and i + 2 < len(lines):
            body = lines[i+1].strip()
            close = lines[i+2].strip()
            if re.match(r'^\}\s*[\);]*\s*$', close) and body.endswith(';'):
                val = body[7:-1] if body.startswith('return ') else body[:-1]
                suffix = close[1:]
                result.append(f'{m.group(1)} -> {val}{suffix}')
                i += 3; continue
        result.append(line); i += 1
    return '\n'.join(result)

def fix_lambda_parens(content):
    def fix_line(line):
        def replacer(m):
            ident = m.group(1)
            if ident in JAVA_KEYWORDS: return m.group(0)
            pre = line[:m.start(1)]
            if re.search(r'\bcase\b', pre): return m.group(0)
            if pre.rstrip() and re.search(r'\b[A-Z]\w*(?:<[^>]*>)?\s*$', pre.rstrip()): return m.group(0)
            if line[m.end(1):m.end(1)+1] == ')': return m.group(0)
            return f'({ident}) ->'
        return re.sub(r'\b([a-zA-Z_]\w*)\s+->', replacer, line)
    return '\n'.join(fix_line(l) for l in content.split('\n'))

def fix_spring_ternary(content):
    def fix_line(line):
        if '?' not in line or line.strip().startswith(('//','*')): return line
        # != null
        line = re.sub(r'(?<!\()(\b[\w][\w.()]*(?:\(\))?)\s+!=\s+null\s+\?(?!\s*\))',
                      r'(\1 != null) ?', line)
        # == null with return (swap branches)
        def swap(m):
            p,v,tb,eb = m.group(1),m.group(2),m.group(3).strip(),m.group(4).strip()
            sfx = ';' if eb.endswith(';') else ''
            if sfx: eb = eb[:-1].rstrip()
            return f'{p}({v} != null) ? {eb} : {tb}{sfx}'
        line = re.sub(r'(\breturn\s+)(\w+)\s+==\s+null\s+\?\s+([\w".\(\)]+)\s*:\s*([\w".\(\)]+\s*;?)', swap, line)
        # instanceof
        line = re.sub(r'(?<!\()(\b[\w][\w.]*)\s+(instanceof\s+[\w<>?.]+(?:\s+\w+)?)\s+\?(?!\s*\))',
                      r'(\1 \2) ?', line)
        # simple comparison <
        line = re.sub(r'(?<!\()(\b\w+)\s+(<)\s+([\w.]+)\s+\?(?!\s*\))', r'(\1 \2 \3) ?', line)
        return line
    return '\n'.join(fix_line(l) for l in content.split('\n'))

def fix_star_imports(content):
    lines = content.split('\n')
    imp_lines = [i for i,l in enumerate(lines) if l.strip().startswith('import ')]
    if not imp_lines: return content
    s, e = imp_lines[0], imp_lines[-1]
    body = '\n'.join(lines[:s] + lines[e+1:])
    new_imps = []
    for i in range(s, e+1):
        stripped = lines[i].strip()
        ms = re.match(r'^import\s+static\s+([\w.]+)\.\*\s*;', stripped)
        if ms:
            pkg = ms.group(1)
            if pkg in STATIC_STAR_IMPORTS:
                for m in STATIC_STAR_IMPORTS[pkg]:
                    if re.search(r'\b' + re.escape(m) + r'\s*\(', body):
                        new_imps.append(f'import static {pkg}.{m};')
            else: new_imps.append(lines[i])
            continue
        mr = re.match(r'^import\s+([\w.]+)\.\*\s*;', stripped)
        if mr:
            pkg = mr.group(1)
            classes = REGULAR_STAR_IMPORTS.get(pkg)
            if classes is None and pkg == 'io.kubernetes.client.openapi.models':
                used = sorted(set(re.findall(r'\bV1[A-Z]\w+\b', body)))
                for cls in used: new_imps.append(f'import {pkg}.{cls};')
            elif classes is not None:
                for cls in classes:
                    if re.search(r'\b' + re.escape(cls) + r'\b', body):
                        new_imps.append(f'import {pkg}.{cls};')
            else: new_imps.append(lines[i])
            continue
        new_imps.append(lines[i])
    seen, deduped = set(), []
    for imp in new_imps:
        if imp.strip() not in seen:
            seen.add(imp.strip()); deduped.append(imp.strip())
    return '\n'.join(lines[:s] + deduped + lines[e+1:])

def process(src_dirs):
    for src_dir in src_dirs:
        for root, dirs, files in os.walk(src_dir):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for fname in files:
                if not fname.endswith('.java'): continue
                fp = os.path.join(root, fname)
                with open(fp) as f: orig = f.read()
                c = orig
                c = fix_spring_catch(c)
                c = fix_need_braces(c)
                c = fix_lambda_blocks(c)
                c = fix_lambda_parens(c)
                c = fix_spring_ternary(c)
                if '.*' in c: c = fix_star_imports(c)
                if c != orig:
                    with open(fp, 'w') as f: f.write(c)
                    print(f'  Fixed: {fp}')

if __name__ == '__main__':
    base = Path('/Users/alex.mondshain/claude/jhelm')
    process([str(base / m / 'src') for m in ['jhelm-core','jhelm-kube','jhelm-app','jhelm-gotemplate']])
```

### Step 4: Handle special violations manually

| Violation | Fix |
|-----------|-----|
| `InnerTypeLast` | Move inner classes AFTER all methods |
| `SpringHideUtilityClassConstructor` | Add `private Constructor() {}` AND make class `final` |
| `FinalClass` | Add `final` to class declaration |
| `NestedIfDepth > 3` | Extract helper method or add to `checkstyle-suppressions.xml` |
| `SpringMethodVisibility` (interface impl) | Add suppression to `checkstyle-suppressions.xml` |
| `AnnotationUseStyle` trailing comma | Remove `,` before `})` in `@CsvSource` etc. |

### Step 5: Re-format and validate

```bash
./mvnw spring-javaformat:apply && ./mvnw validate
```

### Critical Pitfalls

1. **Lambda parens vs switch patterns**: `case Boolean b -> b` — do NOT add parens to switch pattern variables. Check if preceded by uppercase type name or `case` keyword.
2. **Lambda parens vs switch default**: `default -> value` — do NOT add parens. `default` is a Java keyword.
3. **Ternary in lambda body**: `(args) -> condition ? a : b` — the `->` arrow is a boundary; the condition starts AFTER `->`. Do NOT wrap the lambda params in the ternary condition.
4. **`==` vs `=` in find_condition_start**: When scanning backward for ternary condition start, `==` at position `i` has `line[i-1]='='` — skip it. AND `line[i+1]='='` also means it's `==`, skip.
5. **Star import for `removeIf(r ->`)**: `r` is preceded by `(` from the method call, NOT from lambda parens. Check if char AFTER identifier is `)` to detect already-parenthesized.
6. **Missing imports after star import expansion**: Manually check for `Base64`, `BufferedInputStream`, `VersionInfo`, etc. that may not be in the predefined class lists.

### Suppressions file (`checkstyle-suppressions.xml`)

Located at project root. Current suppressions:
- `SpringHeader`, `SpringTestFileName`, `JavadocPackage` — project conventions differ
- `RegexpSinglelineJava` — JUnit 5 assertions used instead of AssertJ
- `SpringImportOrder` — handled by `spring-javaformat:apply`
- `RequireThis` — not enforced in this project
- All `Javadoc*` and `SpringJavadoc` — not required
- `SpringMethodVisibility` for `KpsComparisonTest.java` — TrustManager interface requires public
- `NestedIfDepth` for `RepoManager.java` — intentional deep YAML parsing
