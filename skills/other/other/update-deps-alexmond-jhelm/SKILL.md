---
name: update-deps
description: Check for dependency and plugin updates, review and apply selected upgrades
allowed-tools: Bash(./mvnw *), Bash(python3 *)
---

## Dependency & Plugin Update Workflow

Scan for available updates, filter out noise, present options, apply selected upgrades, and verify the build.

---

### Step 1: Scan for updates

Run both scans in parallel:

```bash
./mvnw versions:display-property-updates -N 2>&1 | grep '\->' > /tmp/jhelm-property-updates.txt
```

```bash
./mvnw versions:display-plugin-updates -N 2>&1 | grep '\->' | grep -v 'reactor\|Help\|Could not' > /tmp/jhelm-plugin-updates.txt
```

---

### Step 2: Parse and filter results

Run this script to produce a clean update table. It excludes:
- **Spring Boot managed dependencies** (jackson, spring-framework/security/session, snakeyaml, logback, slf4j, junit, mockito, lombok, hibernate, tomcat, netty, reactor, micrometer, h2, flyway, liquibase) — these are pinned by the Spring Boot BOM and must not be overridden individually. Note: `spring-retry` is NOT managed by the BOM.
- **Internal modules** (`org.alexmond`)
- **False-positive classifiers** (e.g. `25.0.0 -> 25.0.0-legacy`)
- **Downgrade suggestions** or versions older than current

```python
python3 -c "
import re, sys

SPRING_BOOT_MANAGED = {
    'jackson', 'spring-', 'snakeyaml', 'logback', 'slf4j',
    'junit', 'mockito', 'lombok', 'hibernate', 'tomcat',
    'netty', 'reactor', 'micrometer', 'h2', 'flyway',
    'liquibase', 'assertj', 'byte-buddy', 'objenesis',
    'jakarta', 'aspectj', 'thymeleaf', 'commons-compress',
    'httpclient', 'httpcore',
}

def is_managed(name):
    lower = name.lower()
    return any(m in lower for m in SPRING_BOOT_MANAGED)

def is_false_positive(current, new):
    # Reject classifier-only changes (e.g. 25.0.0 -> 25.0.0-legacy)
    if new.startswith(current + '-'):
        return True
    return False

updates = []

# Parse property updates
try:
    with open('/tmp/jhelm-property-updates.txt') as f:
        for line in f:
            m = re.search(r'\\\$\{(.+?)\}\s+\.+\s+(\S+)\s+->\s+(\S+)', line)
            if m:
                prop, cur, new = m.group(1), m.group(2), m.group(3)
                if not is_managed(prop) and not is_false_positive(cur, new):
                    updates.append(('property', prop, cur, new))
except FileNotFoundError:
    pass

# Parse plugin updates
try:
    with open('/tmp/jhelm-plugin-updates.txt') as f:
        for line in f:
            m = re.search(r'(\S+:\S+)\s+(\S+)\s+->\s+(\S+)', line)
            if m:
                plugin, cur, new = m.group(1), m.group(2), m.group(3)
                if not is_managed(plugin) and not is_false_positive(cur, new):
                    updates.append(('plugin', plugin, cur, new))
except FileNotFoundError:
    pass

if not updates:
    print('All dependencies and plugins are up to date.')
    sys.exit(0)

print(f\"{'#':>3}  {'Type':<10} {'Name':<50} {'Current':<15} {'New':<15}\")
print('-' * 97)
for i, (typ, name, cur, new) in enumerate(updates, 1):
    print(f'{i:>3}  {typ:<10} {name:<50} {cur:<15} {new:<15}')
"
```

---

### Step 3: Present updates and ask for confirmation

Show the table to the user. For each update, note:
- **Major version jumps** (e.g. `9.3 -> 13.2.0`) — flag as potentially breaking
- **Patch/minor bumps** — generally safe

Use `AskUserQuestion` with `multiSelect: true` to let the user pick which updates to apply. Group options sensibly (e.g. "All safe updates", individual items for risky ones).

---

### Step 4: Apply selected updates

For **property updates**, modify `pom.xml` properties:

```bash
# Example: update a property version
# Use Edit tool to change <property.version>old</property.version> to <property.version>new</property.version>
```

For **plugin updates** defined via properties, update the property. For plugins without a property, update the `<version>` tag directly in `<pluginManagement>`.

After applying, run the formatter:

```bash
./mvnw spring-javaformat:apply
```

---

### Step 5: Validate the build

Run a full build to verify nothing broke:

```bash
./mvnw clean install 2>&1 | tail -30
```

Check for:
- **Compilation errors** — API changes in upgraded dependencies
- **Test failures** — behavioral changes
- **PMD / Checkstyle violations** — new rules from upgraded plugins
- **Deprecation warnings** — new deprecations introduced by upgrades

If any failures occur, report them to the user with context about which upgrade likely caused the issue.

---

### Step 6: Summary

Report a table of applied changes:

| Dependency | Old | New | Status |
|---|---|---|---|
| `${property}` | x.y.z | a.b.c | Applied / Skipped / Failed |

If the build is green, the changes are ready to commit.

---

### Notes

- **Never override Spring Boot managed versions** unless the user explicitly asks. The Spring Boot BOM ensures compatible versions across the ecosystem.
- **`checkstyle.version`** is intentionally pinned to `9.3` for compatibility with `spring-javaformat-checkstyle`. Do not upgrade without verifying compatibility.
- **`spring-javaformat.version`** affects both the formatter plugin and the checkstyle dependency — upgrading requires testing both `spring-javaformat:apply` and `validate`.
- When upgrading **`maven-pmd-plugin`**, check for deprecated/renamed/removed PMD rules in `pmd-ruleset.xml` (see `/checkstyle` skill and project memory for past examples).
