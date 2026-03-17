---
name: project-estimation
description: Estimate project scope, timeline, and resource requirements using multiple estimation techniques including bottom-up, top-down, and analogous estimation methods for accurate project planning.
---

# Project Estimation

## Overview

Accurate project estimation determines realistic timelines, budgets, and resource allocation. Effective estimation combines historical data, expert judgment, and structured techniques to minimize surprises.

## When to Use

- Defining project scope and deliverables
- Creating project budgets and timelines
- Allocating team resources
- Managing stakeholder expectations
- Assessing project feasibility
- Planning for contingencies
- Updating estimates during project execution

## Instructions

### 1. **Three-Point Estimation (PERT)**

```python
# Three-point estimation technique for uncertainty

class ThreePointEstimation:
    @staticmethod
    def calculate_pert_estimate(optimistic, most_likely, pessimistic):
        """
        PERT formula: (O + 4M + P) / 6
        Weighted toward most likely estimate
        """
        pert = (optimistic + 4 * most_likely + pessimistic) / 6
        return round(pert, 2)

    @staticmethod
    def calculate_standard_deviation(optimistic, pessimistic):
        """Standard deviation for risk analysis"""
        sigma = (pessimistic - optimistic) / 6
        return round(sigma, 2)

    @staticmethod
    def calculate_confidence_interval(pert_estimate, std_dev, confidence=0.95):
        """
        Calculate confidence interval for estimate
        95% confidence ≈ ±2 sigma
        """
        z_score = 1.96 if confidence == 0.95 else 2.576
        margin = z_score * std_dev

        return {
            'estimate': pert_estimate,
            'lower_bound': round(pert_estimate - margin, 2),
            'upper_bound': round(pert_estimate + margin, 2),
            'range': f"{pert_estimate - margin:.1f} - {pert_estimate + margin:.1f}"
        }

# Example
optimistic = 10  # best case
most_likely = 20  # expected
pessimistic = 40  # worst case

pert = ThreePointEstimation.calculate_pert_estimate(optimistic, most_likely, pessimistic)
std_dev = ThreePointEstimation.calculate_standard_deviation(optimistic, pessimistic)
confidence = ThreePointEstimation.calculate_confidence_interval(pert, std_dev)

print(f"PERT Estimate: {pert} days")
print(f"Standard Deviation: {std_dev}")
print(f"95% Confidence Range: {confidence['range']}")
```

### 2. **Bottom-Up Estimation**

```javascript
// Bottom-up estimation from detailed task breakdown

class BottomUpEstimation {
  constructor(project) {
    this.project = project;
    this.tasks = [];
    this.workBreakdownStructure = {};
  }

  createWBS() {
    // Work Breakdown Structure example
    return {
      level1: 'Full Project',
      level2: ['Planning', 'Design', 'Development', 'Testing', 'Deployment'],
      level3: {
        'Development': [
          'Backend API',
          'Frontend UI',
          'Database Schema',
          'Integration'
        ],
        'Testing': [
          'Unit Testing',
          'Integration Testing',
          'UAT',
          'Performance Testing'
        ]
      }
    };
  }

  estimateTasks(tasks) {
    let totalEstimate = 0;
    const estimates = [];

    for (let task of tasks) {
      const taskEstimate = this.estimateSingleTask(task);
      estimates.push({
        name: task.name,
        effort: taskEstimate.effort,
        resources: taskEstimate.resources,
        risk: taskEstimate.risk,
        duration: taskEstimate.duration
      });
      totalEstimate += taskEstimate.effort;
    }

    return {
      totalEffortHours: totalEstimate,
      totalWorkDays: totalEstimate / 8,
      taskDetails: estimates,
      criticalPath: this.identifyCriticalPath(estimates)
    };
  }

  estimateSingleTask(task) {
    // Base effort
    let effort = task.complexity * task.scope;

    // Adjust for team experience
    const experienceFactor = task.teamExperience / 100; // 0.5 to 1.5
    effort = effort * experienceFactor;

    // Adjust for risk
    const riskFactor = 1 + (task.riskLevel * 0.1);
    effort = effort * riskFactor;

    return {
      effort: Math.ceil(effort),
      resources: Math.ceil(effort / 8), // days
      risk: task.riskLevel,
      duration: Math.ceil(effort / (8 * task.teamSize))
    };
  }

  identifyCriticalPath(estimates) {
    // Return tasks with longest duration
    return estimates
      .sort((a, b) => b.duration - a.duration)
      .slice(0, 5);
  }
}
```

### 3. **Analogous Estimation**

```yaml
Analogous Estimation Template:

Historical Project Comparison:

Current Project:
  Type: E-commerce Payment System
  Complexity: High
  Scope: Medium
  Team Size: 5 developers

Similar Historical Projects:

Project A (2 years ago):
  Type: E-commerce Shipping System
  Complexity: High
  Scope: Medium
  Team Size: 5 developers
  Actual Duration: 16 weeks
  Actual Cost: $180,000
  Lessons: Underestimated integration work

Project B (1 year ago):
  Type: Payment Gateway Integration
  Complexity: High
  Scope: Small
  Team Size: 3 developers
  Actual Duration: 8 weeks
  Actual Cost: $95,000
  Lessons: Security review added 2 weeks

Adjustments:
  - Current project 20% larger than Project B
  - Similar complexity and team composition
  - Estimated Duration: 10-12 weeks
  - Estimated Cost: $120,000-$140,000

Confidence Level: 75% (medium, due to some differences)
```

### 4. **Resource Estimation**

```javascript
// Resource allocation and estimation

class ResourceEstimation {
  calculateResourceNeeds(projectDuration, tasks) {
    const resourceMap = {
      'Senior Developer': 0,
      'Mid-Level Developer': 0,
      'Junior Developer': 0,
      'QA Engineer': 0,
      'DevOps Engineer': 0,
      'Project Manager': 0
    };

    let totalEffort = 0;

    for (let task of tasks) {
      resourceMap[task.requiredRole] += task.effortHours;
      totalEffort += task.effortHours;
    }

    // Calculate FTE (Full Time Equivalent) needed
    const fteMap = {};
    for (let role in resourceMap) {
      fteMap[role] = (resourceMap[role] / (projectDuration * 8 * 5)).toFixed(2);
    }

    return {
      effortByRole: resourceMap,
      fte: fteMap,
      totalEffortHours: totalEffort,
      totalWorkDays: totalEffort / 8,
      costEstimate: this.calculateCost(fteMap)
    };
  }

  calculateCost(fteMap) {
    const dailyRates = {
      'Senior Developer': 1200,
      'Mid-Level Developer': 900,
      'Junior Developer': 600,
      'QA Engineer': 700,
      'DevOps Engineer': 950,
      'Project Manager': 800
    };

    let totalCost = 0;
    const costByRole = {};

    for (let role in fteMap) {
      const fteDays = fteMap[role] * 250; // 250 working days/year
      costByRole[role] = fteDays * dailyRates[role];
      totalCost += costByRole[role];
    }

    return {
      byRole: costByRole,
      total: totalCost,
      currency: 'USD'
    };
  }
}
```

### 5. **Estimation Templates**

```markdown
## Project Estimation Summary

Project Name: [Project Name]
Date: [Date]
Estimator: [Name]

### Scope Summary
- Deliverables: [List key deliverables]
- Exclusions: [What's NOT included]
- Assumptions: [Key assumptions]

### Effort Estimation
| Phase | Effort (Days) | Resources | Notes |
|-------|---------------|-----------|-------|
| Planning | 5 | 1 PM | Requirement gathering |
| Design | 10 | 2 Architects | UI/UX & Technical |
| Development | 40 | 4 Devs | 5 features total |
| Testing | 15 | 2 QA | Manual + Automation |
| Deployment | 5 | 1 DevOps | Staging & Production |
| **Total** | **75 Days** | **Avg 3.0 FTE** | |

### Schedule Estimate
- Start Date: [Date]
- Duration: 15 weeks
- End Date: [Date]
- Critical Path: Development & Testing phases

### Risk & Contingency
- Risk Buffer: 20% (15 days)
- Optimistic: 12 weeks
- Most Likely: 15 weeks
- Pessimistic: 18 weeks

### Cost Estimate
- Labor: $125,000
- Infrastructure: $15,000
- Tools/Licenses: $5,000
- **Total**: $145,000

### Confidence Level
- Estimation Confidence: 80% (Medium-High)
- Key Uncertainties: Third-party integrations
```

## Best Practices

### ✅ DO
- Use multiple estimation techniques and compare results
- Include contingency buffers (15-25% for new projects)
- Base estimates on historical data from similar projects
- Break down large efforts into smaller components
- Get input from team members doing the actual work
- Document assumptions and exclusions clearly
- Review and adjust estimates regularly
- Track actual vs. estimated metrics for improvement
- Include non-development tasks (planning, testing, deployment)
- Account for learning curve on unfamiliar technologies

### ❌ DON'T
- Estimate without clear scope definition
- Use unrealistic best-case scenarios
- Ignore historical project data
- Estimate under pressure to hit arbitrary targets
- Forget to include non-coding activities
- Use estimates as performance metrics for individuals
- Change estimates mid-project without clear reason
- Estimate without team input
- Ignore risks and contingencies
- Use one technique exclusively

## Estimation Tips

- Add 20-30% buffer for unknown unknowns
- Review estimates weekly and adjust as needed
- Track estimation accuracy to improve future estimates
- Use estimation to identify scope issues early
- Communicate confidence level with stakeholders
