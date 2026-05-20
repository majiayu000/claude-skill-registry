---
name: when-analyzing-skill-gaps-use-skill-gap-analyzer
version: 1.0.0
description: Analyze skill library to identify coverage gaps, redundant overlaps, optimization opportunities, and provide recommendations for skill portfolio improvement
tags:
  - meta-tool
  - skill-management
  - gap-analysis
  - portfolio-optimization
complexity: MEDIUM
agents_required:
  - researcher
  - code-analyzer
auto_trigger: false
---

# Skill Gap Analyzer

**Purpose:** Perform comprehensive analysis of skill library to identify missing capabilities, redundant functionality, optimization opportunities, and provide actionable recommendations for skill portfolio improvement.

## When to Use This Skill

- When building a new skill library
- Quarterly skill portfolio reviews
- Before large refactoring efforts
- When considering new skill additions
- After major project pivots
- When optimizing resource allocation

## Analysis Dimensions

### 1. Coverage Gap Analysis
- Domain coverage mapping
- Missing capability identification
- Use case scenario testing
- Workflow completeness assessment
- Integration point analysis

### 2. Redundancy Detection
- Duplicate functionality identification
- Overlapping capability mapping
- Consolidation opportunity analysis
- Version conflict detection
- Naming collision identification

### 3. Optimization Opportunities
- Under-utilized skill detection
- Over-complex skill identification
- Composability improvement suggestions
- Dependency optimization
- Performance bottleneck analysis

### 4. Usage Pattern Analysis
- Frequency metrics
- Co-occurrence patterns
- Success rate tracking
- Token efficiency measurement
- Agent utilization patterns

### 5. Recommendation Generation
- Prioritized action items
- Consolidation strategies
- New skill proposals
- Deprecation candidates
- Restructuring plans

## Execution Process

### Phase 1: Library Inventory

```bash
# Initialize analysis session
npx claude-flow@alpha hooks pre-task --description "Analyzing skill library gaps"

# Scan skill directories
find ~/.claude/skills -name "SKILL.md" -o -name "*.skill.md"
```

**Inventory Script:**
```javascript
function inventorySkills(skillDirectory) {
  const inventory = {
    totalSkills: 0,
    categories: {},
    capabilities: {},
    agents: {},
    complexity: {},
    tags: {}
  };

  // Parse each SKILL.md file
  const skillFiles = findSkillFiles(skillDirectory);

  for (const file of skillFiles) {
    const metadata = parseYAMLFrontmatter(file);

    inventory.totalSkills++;

    // Categorize by path
    const category = extractCategory(file);
    inventory.categories[category] = (inventory.categories[category] || 0) + 1;

    // Track capabilities
    const capabilities = extractCapabilities(metadata.description);
    capabilities.forEach(cap => {
      inventory.capabilities[cap] = (inventory.capabilities[cap] || []);
      inventory.capabilities[cap].push(metadata.name);
    });

    // Track required agents
    if (metadata.agents_required) {
      metadata.agents_required.forEach(agent => {
        inventory.agents[agent] = (inventory.agents[agent] || 0) + 1;
      });
    }

    // Track complexity
    inventory.complexity[metadata.complexity || 'UNKNOWN'] =
      (inventory.complexity[metadata.complexity || 'UNKNOWN'] || 0) + 1;

    // Track tags
    if (metadata.tags) {
      metadata.tags.forEach(tag => {
        inventory.tags[tag] = (inventory.tags[tag] || 0) + 1;
      });
    }
  }

  return inventory;
}

function extractCapabilities(description) {
  // Extract action verbs and key nouns
  const capabilities = [];

  const verbs = description.match(/\b(analyz|creat|generat|optimiz|manag|coordinat|orchestrat|deploy|monitor|test|review|document|integrat|automat|validat|secur|perform|debug|refactor|migrat|transform)\w+/gi) || [];

  capabilities.push(...verbs.map(v => v.toLowerCase()));

  return [...new Set(capabilities)]; // Deduplicate
}
```

**Store Inventory:**
```bash
npx claude-flow@alpha memory store --key "gap-analysis/inventory" --value "{
  \"totalSkills\": <count>,
  \"categories\": {...},
  \"capabilities\": {...},
  \"timestamp\": \"<ISO8601>\"
}"
```

### Phase 2: Coverage Gap Detection

**Domain Coverage Matrix:**
```javascript
function analyzeCoverageGaps(inventory, requiredDomains) {
  const gaps = [];

  // Define comprehensive domain requirements
  const domains = {
    "Development": [
      "code-generation", "testing", "debugging", "refactoring",
      "documentation", "code-review", "architecture"
    ],
    "DevOps": [
      "deployment", "monitoring", "ci-cd", "infrastructure",
      "security", "scaling", "backup-recovery"
    ],
    "Project Management": [
      "planning", "estimation", "tracking", "reporting",
      "risk-management", "stakeholder-communication"
    ],
    "Data": [
      "data-analysis", "data-transformation", "data-validation",
      "data-migration", "data-visualization"
    ],
    "AI/ML": [
      "model-training", "inference", "optimization",
      "evaluation", "deployment", "monitoring"
    ],
    "Integration": [
      "api-integration", "webhook-handling", "event-processing",
      "message-queue", "service-mesh"
    ]
  };

  // Check coverage for each domain
  for (const [domain, capabilities] of Object.entries(domains)) {
    const coverage = capabilities.map(cap => {
      const covered = inventory.capabilities[cap]?.length > 0;
      const skills = inventory.capabilities[cap] || [];
      return { capability: cap, covered, skills };
    });

    const missingCaps = coverage.filter(c => !c.covered);

    if (missingCaps.length > 0) {
      gaps.push({
        domain: domain,
        coverage: ((capabilities.length - missingCaps.length) / capabilities.length * 100).toFixed(1) + "%",
        missingCapabilities: missingCaps.map(c => c.capability),
        priority: calculatePriority(domain, missingCaps.length, capabilities.length)
      });
    }
  }

  return gaps;
}

function calculatePriority(domain, missingCount, totalCount) {
  const coverageRatio = 1 - (missingCount / totalCount);
  const domainImportance = {
    "Development": 1.0,
    "DevOps": 0.9,
    "Project Management": 0.7,
    "Data": 0.8,
    "AI/ML": 0.8,
    "Integration": 0.9
  };

  const score = coverageRatio * (domainImportance[domain] || 0.5);

  if (score < 0.3) return "critical";
  if (score < 0.6) return "high";
  if (score < 0.8) return "medium";
  return "low";
}
```

**Use Case Scenario Testing:**
```javascript
function testScenarioCoverage(inventory) {
  const scenarios = [
    {
      name: "Full-stack web app development",
      requiredCapabilities: [
        "code-generation", "testing", "database-design",
        "api-integration", "deployment", "monitoring"
      ]
    },
    {
      name: "ML model training and deployment",
      requiredCapabilities: [
        "data-analysis", "model-training", "evaluation",
        "optimization", "deployment", "monitoring"
      ]
    },
    {
      name: "GitHub workflow automation",
      requiredCapabilities: [
        "code-review", "testing", "ci-cd", "release-management",
        "issue-tracking", "documentation"
      ]
    },
    {
      name: "Prompt engineering and optimization",
      requiredCapabilities: [
        "prompt-analysis", "optimization", "testing",
        "documentation", "version-control"
      ]
    }
  ];

  const scenarioResults = scenarios.map(scenario => {
    const coverage = scenario.requiredCapabilities.map(cap => ({
      capability: cap,
      covered: inventory.capabilities[cap]?.length > 0,
      skills: inventory.capabilities[cap] || []
    }));

    const coveragePercent = (coverage.filter(c => c.covered).length /
                            coverage.length * 100).toFixed(1);

    return {
      scenario: scenario.name,
      coverage: coveragePercent + "%",
      missing: coverage.filter(c => !c.covered).map(c => c.capability),
      canExecute: coverage.every(c => c.covered)
    };
  });

  return scenarioResults;
}
```

### Phase 3: Redundancy Detection

**Overlap Analysis:**
```javascript
function detectRedundancy(inventory) {
  const redundancies = [];

  // Find capabilities handled by multiple skills
  for (const [capability, skills] of Object.entries(inventory.capabilities)) {
    if (skills.length > 2) {
      // Analyze actual overlap
      const skillDetails = skills.map(name => loadSkillDetails(name));
      const overlap = analyzeOverlap(skillDetails);

      if (overlap.percentage > 70) {
        redundancies.push({
          capability: capability,
          skillCount: skills.length,
          skills: skills,
          overlapPercentage: overlap.percentage,
          recommendation: generateConsolidationRecommendation(skillDetails)
        });
      }
    }
  }

  // Find naming collisions
  const namePatterns = {};
  for (const [category, skillList] of Object.entries(inventory.categories)) {
    // Extract common patterns
    const patterns = skillList.map(extractNamePattern);
    // Identify potential confusion
  }

  return redundancies;
}

function analyzeOverlap(skills) {
  // Compare descriptions, capabilities, processes
  const descriptions = skills.map(s => s.description);
  const commonWords = findCommonWords(descriptions);

  // Calculate Jaccard similarity
  const allWords = new Set(descriptions.flatMap(d => d.split(/\s+/)));
  const overlap = commonWords.size / allWords.size * 100;

  return { percentage: overlap, commonWords: Array.from(commonWords) };
}
```

### Phase 4: Optimization Opportunities

**Researcher Agent Task:**
```bash
# Spawn researcher agent for optimization analysis
# Agent instructions:
# 1. Analyze usage patterns from memory
# 2. Identify under-utilized skills (low frequency)
# 3. Identify over-complex skills (high token cost, low success rate)
# 4. Suggest composability improvements
# 5. Recommend dependency optimizations
# 6. Store findings in memory

npx claude-flow@alpha memory store --key "gap-analysis/optimization" --value "{
  \"underutilized\": [...],
  \"overcomplicated\": [...],
  \"composability\": [...],
  \"dependencies\": [...]
}"
```

**Optimization Detection:**
```javascript
function identifyOptimizations(inventory, usageMetrics) {
  const optimizations = [];

  // Under-utilized skills
  const underutilized = usageMetrics.filter(m =>
    m.frequency < 0.05 && // Less than 5% usage
    m.lastUsed > 90 // Days since last use
  ).map(m => ({
    skill: m.name,
    frequency: m.frequency,
    lastUsed: m.lastUsed + " days ago",
    recommendation: "Review for deprecation or promotion"
  }));

  optimizations.push({
    type: "under-utilized",
    count: underutilized.length,
    skills: underutilized
  });

  // Over-complex skills
  const overcomplex = usageMetrics.filter(m =>
    m.avgTokens > 5000 && // High token usage
    m.successRate < 0.7 // Low success rate
  ).map(m => ({
    skill: m.name,
    avgTokens: m.avgTokens,
    successRate: (m.successRate * 100).toFixed(1) + "%",
    recommendation: "Break into smaller skills or simplify"
  }));

  optimizations.push({
    type: "over-complex",
    count: overcomplex.length,
    skills: overcomplex
  });

  // Composability improvements
  const composable = identifyComposablePatterns(inventory);
  optimizations.push({
    type: "composability",
    count: composable.length,
    opportunities: composable
  });

  return optimizations;
}
```

### Phase 5: Recommendation Generation

**Report Format:**
```markdown
## Skill Gap Analysis Report
**Date:** <timestamp>
**Total Skills Analyzed:** <count>
**Analysis Duration:** <time>

---

## Executive Summary

### Coverage
- Overall coverage: <percentage>%
- Critical gaps: <count>
- High-priority gaps: <count>

### Redundancy
- Duplicate functionality: <count> instances
- Consolidation opportunities: <count>
- Potential savings: <tokens/storage>

### Optimization
- Under-utilized skills: <count>
- Over-complex skills: <count>
- Composability improvements: <count>

---

## Coverage Gaps

### Critical Priority
1. **Domain:** [name]
   - Coverage: [percentage]%
   - Missing capabilities:
     - [capability 1]
     - [capability 2]
   - Recommended action: Create skill "[proposed-name]"
   - Impact: [high/medium/low]

### High Priority
...

---

## Redundancy Analysis

### Duplicate Functionality
1. **Capability:** [name]
   - Handled by: [skill1], [skill2], [skill3]
   - Overlap: [percentage]%
   - Recommendation: Consolidate into "[new-skill-name]"
   - Estimated savings: [tokens] tokens, [storage] MB

---

## Optimization Opportunities

### Under-Utilized Skills
| Skill | Frequency | Last Used | Recommendation |
|-------|-----------|-----------|----------------|
| [name] | [%] | [days] ago | [action] |

### Over-Complex Skills
| Skill | Avg Tokens | Success Rate | Recommendation |
|-------|------------|--------------|----------------|
| [name] | [count] | [%] | [action] |

### Composability Improvements
1. **Pattern:** [description]
   - Current approach: [details]
   - Improved approach: [details]
   - Benefits: [list]

---

## Scenario Coverage

| Scenario | Coverage | Missing | Can Execute? |
|----------|----------|---------|--------------|
| Full-stack web app | [%] | [list] | [yes/no] |
| ML deployment | [%] | [list] | [yes/no] |
| GitHub automation | [%] | [list] | [yes/no] |

---

## Prioritized Recommendations

### Immediate Actions (This Week)
1. [ ] Create skill: [name] - [justification]
2. [ ] Consolidate: [skills] → [new-skill]
3. [ ] Deprecate: [skill] - [reason]

### Short-Term (This Month)
1. [ ] Optimize: [skill] - [changes]
2. [ ] Document: [skill] - [missing-docs]
3. [ ] Test: [scenario] - [coverage-improvement]

### Long-Term (This Quarter)
1. [ ] Refactor: [domain] - [architecture]
2. [ ] Integrate: [external-tool] - [capability]
3. [ ] Research: [emerging-technology] - [potential]

---

## Metrics Comparison

| Metric | Current | Target | Gap |
|--------|---------|--------|-----|
| Total skills | [count] | - | - |
| Domain coverage | [%] | 90% | [%] |
| Redundancy rate | [%] | <10% | [%] |
| Avg complexity | [level] | MEDIUM | - |
| Under-utilization | [%] | <5% | [%] |
```

## Concrete Example: Real Analysis

### Input: Skill Library (Fragment)

**Inventory:**
- Total skills: 47
- Categories: development (15), github (12), optimization (8), testing (5), meta-tools (3), misc (4)
- Capabilities mapped: 127
- Agents used: 18 distinct types

### Analysis Output

**Coverage Gaps Detected:**

```json
{
  "domain": "Data Engineering",
  "coverage": "23.1%",
  "missingCapabilities": [
    "data-transformation",
    "data-validation",
    "data-migration",
    "data-visualization",
    "etl-pipeline"
  ],
  "priority": "high",
  "recommendation": "Create 'data-engineering-workflow' skill"
}
```

**Redundancy Detected:**

```json
{
  "capability": "code-review",
  "skillCount": 4,
  "skills": [
    "code-review-assistant",
    "github-code-review",
    "pr-review-automation",
    "code-quality-checker"
  ],
  "overlapPercentage": 78,
  "recommendation": "Consolidate into unified 'code-review-orchestrator' with specialized sub-skills"
}
```

**Optimization Opportunities:**

```json
{
  "type": "under-utilized",
  "skills": [
    {
      "skill": "legacy-converter",
      "frequency": 0.02,
      "lastUsed": "127 days ago",
      "recommendation": "Archive or promote with use-case documentation"
    }
  ]
},
{
  "type": "over-complex",
  "skills": [
    {
      "skill": "full-stack-architect",
      "avgTokens": 8743,
      "successRate": "64.3%",
      "recommendation": "Break into: backend-architect, frontend-architect, database-architect"
    }
  ]
}
```

**Recommendations:**

1. **Critical:** Create data engineering skill (coverage: 23% → 85%)
2. **High:** Consolidate 4 code review skills (save ~15K tokens, reduce confusion)
3. **Medium:** Break full-stack-architect into 3 focused skills
4. **Low:** Archive legacy-converter or add promotion documentation

**Expected Impact:**
- Coverage improvement: 67% → 89%
- Redundancy reduction: 18% → 7%
- Avg token efficiency: +32%
- Maintenance overhead: -40%

## Integration with Development Workflow

### Quarterly Review Process
```bash
# 1. Run gap analysis
npx claude-flow@alpha hooks pre-task --description "Quarterly skill gap analysis"

# 2. Spawn researcher agent for analysis
# Agent performs comprehensive inventory and analysis

# 3. Review recommendations
npx claude-flow@alpha memory retrieve --key "gap-analysis/recommendations"

# 4. Create action plan
# Prioritize and schedule improvements

# 5. Track progress
npx claude-flow@alpha hooks post-task --task-id "gap-analysis-q1-2025"
```

### Continuous Monitoring
```bash
# Track skill usage
npx claude-flow@alpha hooks post-task --skill-used "[name]"

# Aggregate metrics monthly
npx claude-flow@alpha memory aggregate --pattern "skills/usage/*" --period "monthly"
```

## Success Metrics

- Domain coverage: >85%
- Redundancy rate: <10%
- Under-utilization: <5%
- Scenario execution: 100% of core scenarios
- Optimization adoption: >80% of recommendations implemented

## Related Skills

- `when-optimizing-prompts-use-prompt-optimization-analyzer` - Optimize individual skills
- `when-managing-token-budget-use-token-budget-advisor` - Budget impact analysis
- `skill-forge` - Create new skills based on recommendations

## Notes

- Run quarterly or after major changes
- Involve team in recommendation review
- Track recommendation adoption rate
- Update analysis criteria as needs evolve
- Share findings across teams
