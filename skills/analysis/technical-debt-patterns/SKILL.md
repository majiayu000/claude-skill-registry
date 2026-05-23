---
name: "Technical Debt Patterns"
description: "Expert guide to detecting, categorizing, and prioritizing technical debt in Rails applications. Use when: (1) Auditing codebase health, (2) Planning refactoring sprints, (3) Estimating feature impact, (4) Identifying code smells, (5) Tracking deprecations. Trigger keywords: technical debt, code smell, complexity, cyclomatic, deprecation, legacy, refactor, audit, health check, god class"
version: 1.1.0
tags: [technical-debt, code-quality, refactoring, audit, complexity]
---

# Technical Debt Patterns

Expert patterns for detecting, categorizing, and prioritizing technical debt in Rails applications.

## Decision Tree: Debt Category Identification

```
What type of issue is this?
│
├─ Code structure problem?
│   ├─ Method too long (>20 lines) → Code Smell: Long Method
│   ├─ Class too large (>150 lines) → Code Smell: Large Class
│   ├─ Excessive parameter passing → Code Smell: Data Clump
│   └─ Method uses another object's data → Code Smell: Feature Envy
│
├─ Complexity issue?
│   ├─ Flog score >60 → Complexity: High
│   ├─ Cyclomatic complexity >10 → Complexity: High
│   ├─ Deep nesting (>3 levels) → Complexity: Nesting
│   └─ Too many conditionals → Complexity: Conditional
│
├─ Security concern?
│   ├─ SQL injection risk → Security: SQL Injection
│   ├─ XSS vulnerability → Security: XSS
│   ├─ Mass assignment issue → Security: Mass Assignment
│   └─ Outdated gem with CVE → Security: Dependency
│
├─ Outdated code?
│   ├─ Rails deprecation warning → Deprecation: Rails
│   ├─ Ruby version warning → Deprecation: Ruby
│   └─ Deprecated gem API → Deprecation: Gem
│
├─ Performance problem?
│   ├─ N+1 query pattern → Performance: N+1
│   ├─ Missing database index → Performance: Index
│   ├─ Memory bloat → Performance: Memory
│   └─ Slow query → Performance: Query
│
└─ Architecture violation?
    ├─ Fat controller → Architecture: Controller
    ├─ God object/model → Architecture: God Object
    ├─ Circular dependency → Architecture: Circular
    └─ Layer violation → Architecture: Layering
```

---

## NEVER Do These (Critical Anti-Patterns)

**NEVER ignore security debt** because "we'll fix it later":
```ruby
# WRONG - Ignoring SQL injection
User.where("name = '#{params[:name]}'")  # Security debt accumulates risk

# RIGHT - Fix immediately or track with Critical severity
User.where(name: params[:name])
```
→ Security debt has exponential risk growth. Track as Critical, not backlog.

**NEVER create technical debt to "fix" technical debt**:
```ruby
# WRONG - Adding wrapper to hide complexity
class PaymentWrapper
  def process
    @legacy_payment.complex_legacy_method  # Just hiding the problem
  end
end

# RIGHT - Either refactor properly or track explicitly
# If time-constrained, create beads issue with clear scope
```
→ Debt wrappers compound into "debt squared". Refactor or track, don't hide.

**NEVER disable linters globally to silence debt warnings**:
```ruby
# WRONG - Global disable in .rubocop.yml
Metrics/MethodLength:
  Enabled: false  # Hides ALL long method debt

# RIGHT - Explicit inline disable with justification
# rubocop:disable Metrics/MethodLength -- Legacy payment processor, tracked in PROJ-123
def complex_legacy_method
  # ...
end
# rubocop:enable Metrics/MethodLength
```
→ Global disables hide debt accumulation. Use inline disables with tracking.

**NEVER skip team discussion on Critical/High debt**:
```markdown
# WRONG - Solo decision on major debt
"I found a god object, I'll refactor it this sprint"

# RIGHT - Team alignment first
1. Document finding in debt report
2. Create beads issue with severity
3. Discuss in sprint planning
4. Get consensus on approach
```
→ Major refactoring affects the whole team. Collaborate before large changes.

**NEVER estimate features without considering debt in affected areas**:
```markdown
# WRONG - Ignoring debt in estimates
"Add payment retry logic: 2 story points"

# RIGHT - Include debt impact
"Add payment retry logic: 5 story points
 - 2 points: feature implementation
 - 3 points: PaymentService complexity (Flog 127) requires refactoring first"
```
→ Debt adds hidden cost. Include remediation in feature estimates.

---

## Code Smell Detection Patterns

### Long Method (>20 lines)

**Detection**:
```bash
# Find methods longer than 20 lines
awk '
  /^[[:space:]]*def / { start = NR; name = $2 }
  /^[[:space:]]*end/ && start > 0 {
    len = NR - start
    if (len > 20) print FILENAME ":" name " (" len " lines)"
    start = 0
  }
' app/**/*.rb
```

**Severity Thresholds**:
| Lines | Severity |
|-------|----------|
| 20-40 | Medium |
| 40-80 | High |
| >80 | Critical |

### Large Class (>150 lines)

**Detection**:
```bash
# Find classes larger than 150 lines
for file in app/models/*.rb app/services/*.rb; do
  lines=$(wc -l < "$file" 2>/dev/null)
  if [ "$lines" -gt 150 ]; then
    echo "$file: $lines lines"
  fi
done
```

**Severity Thresholds**:
| Lines | Severity |
|-------|----------|
| 150-300 | Medium |
| 300-500 | High |
| >500 | Critical |

### Feature Envy

Method uses another object's data more than its own.

**Detection Pattern**:
```ruby
# Smell: Method calls another object's methods repeatedly
def calculate_total(order)
  order.items.sum(&:price) +
    order.shipping_cost +
    order.tax_amount -
    order.discount_amount
end

# Fix: Move method to Order class
class Order
  def calculate_total
    items.sum(&:price) + shipping_cost + tax_amount - discount_amount
  end
end
```

### Data Clump

Same group of parameters passed together repeatedly.

**Detection Pattern**:
```ruby
# Smell: Repeated parameter group
def create_user(name, email, phone, address)
def update_user(name, email, phone, address)
def validate_user(name, email, phone, address)

# Fix: Extract to value object
class ContactInfo
  attr_reader :name, :email, :phone, :address
end

def create_user(contact_info)
def update_user(contact_info)
```

---

## Complexity Metrics

### Flog Score Thresholds

| Score | Rating | Action |
|-------|--------|--------|
| < 30 | Low | No action needed |
| 30-60 | Medium | Consider refactoring |
| 60-100 | High | Plan refactoring |
| > 100 | Critical | Immediate refactoring |

**Running Flog**:
```bash
# Overall complexity score
flog -q -g app/

# Top 10 most complex methods
flog -q app/ | head -10

# Score for specific file
flog app/services/payment_service.rb
```

### Cyclomatic Complexity

Measures independent execution paths through code.

| Complexity | Rating | Risk |
|------------|--------|------|
| 1-5 | Low | Easy to test |
| 6-10 | Medium | Moderate risk |
| 11-20 | High | Difficult to test |
| >20 | Critical | Very high risk |

---

## Severity Scoring Framework

Calculate overall severity using weighted factors:

```
Severity Score = (Blast × 0.30) + (Fix × 0.20) + (Risk × 0.30) + (Age × 0.10) + (Freq × 0.10)
```

| Factor | Weight | 1 (Low) | 3 (Medium) | 5 (High) |
|--------|--------|---------|------------|----------|
| Blast Radius | 30% | Single file | Module | System-wide |
| Fix Complexity | 20% | Trivial | Moderate | Major refactor |
| Risk Level | 30% | Cosmetic | Functional | Security/Data |
| Age | 10% | < 6 months | 6mo-2yr | > 2 years |
| Frequency | 10% | Rare path | Normal | Hot path |

**Severity Categories**:
- **Critical**: Score >= 4.0 (SLA: 1 sprint)
- **High**: Score >= 3.0 (SLA: 2 sprints)
- **Medium**: Score >= 2.0 (SLA: Quarterly)
- **Low**: Score < 2.0 (Opportunistic)

---

## Quick Reference Tables

### Detection Tools

| Tool | Purpose | Command |
|------|---------|---------|
| Flog | Complexity scoring | `flog -q app/` |
| Reek | Code smell detection | `reek app/` |
| Rubocop | Style + metrics | `rubocop --format json` |
| Brakeman | Security vulnerabilities | `brakeman -q` |
| bundler-audit | Gem CVEs | `bundle-audit check` |
| rails_best_practices | Rails anti-patterns | `rails_best_practices` |

### Effort Estimation

| Category | Typical Effort |
|----------|----------------|
| Long Method refactor | 2-4 hours |
| Large Class extraction | 1-3 days |
| God Object decomposition | 3-5 days |
| N+1 query fix | 1-2 hours |
| Security vulnerability | 2-8 hours |
| Deprecation update | 2-4 hours |
| Circular dependency fix | 2-5 days |

### Beads Integration

```bash
# Create debt issue
bd create --type task --priority 1 \
  --title "Tech Debt: [Description]" \
  --description "[Details]"

# Track debt item
bd update PROJ-123 --status in_progress

# Close after remediation
bd close PROJ-123 --reason "Refactored in commit abc123"
```

---

## References

For detailed patterns in each category, see:

- `references/code-smells.md` - Long method, large class, feature envy, data clump
- `references/complexity-metrics.md` - Flog, cyclomatic, cognitive complexity
- `references/deprecation-tracking.md` - Rails, Ruby, gem deprecations
- `references/security-debt.md` - Brakeman categories, OWASP patterns
- `references/performance-debt.md` - N+1 queries, indexes, memory
- `references/testing-debt.md` - Coverage gaps, flaky tests
- `references/architecture-debt.md` - God objects, circular deps, layers

---

## Integration with Other Skills

| Skill | Integration Point |
|-------|-------------------|
| `code-quality-gates` | Rubocop/Sorbet findings feed into debt report |
| `refactoring-workflow` | Debt items become refactoring targets |
| `rails-conventions` | Convention violations are architecture debt |
| `codebase-inspection` | Inspector discovers debt during analysis |
