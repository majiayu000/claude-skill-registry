---
name: Decision Frameworks
description: Decision-making methodologies, scoring frameworks, and planning strategies for Group 2 agents in four-tier architecture
version: 7.0.0
category: decision-making
tags: [four-tier, group-2, strategic-planning, decision-making, prioritization, user-preferences]
related_skills: [group-collaboration, pattern-learning, contextual-pattern-learning]
---

# Decision Frameworks Skill

## Overview

This skill provides decision-making frameworks, scoring methodologies, and planning strategies specifically for **Group 2 (Decision Making & Planning)** agents in the four-tier architecture. It covers how to evaluate Group 1 recommendations, incorporate user preferences, create execution plans, and make optimal decisions that balance multiple factors.

## When to Apply This Skill

**Use this skill when:**
- Evaluating recommendations from Group 1 (Strategic Analysis & Intelligence)
- Creating execution plans for Group 3 (Execution & Implementation)
- Prioritizing competing recommendations
- Incorporating user preferences into decisions
- Balancing trade-offs (speed vs quality, risk vs benefit)
- Deciding between multiple valid approaches
- Optimizing for specific objectives (quality, speed, cost)

**Required for:**
- strategic-planner (master decision-maker)
- preference-coordinator (user preference specialist)
- Any Group 2 agent making planning decisions

## Group 2 Role Recap

**Group 2: Decision Making & Planning (The "Council")**
- **Input**: Recommendations from Group 1 with confidence scores
- **Process**: Evaluate, prioritize, decide, plan
- **Output**: Execution plans for Group 3 with priorities and preferences
- **Key Responsibility**: Make optimal decisions balancing analysis, user preferences, historical success, and risk

## Decision-Making Frameworks

### Framework 1: Recommendation Evaluation Matrix

**Purpose**: Score each Group 1 recommendation on multiple dimensions

**Scoring Formula (0-100)**:
```python
Recommendation Score =
  (Confidence from Group 1    × 30%) +  # How confident is the analyst?
  (User Preference Alignment  × 25%) +  # Does it match user style?
  (Historical Success Rate    × 25%) +  # Has this worked before?
  (Risk Assessment            × 20%)    # What's the risk level?

Where each component is 0-100
```

**Implementation**:
```python
def evaluate_recommendation(recommendation, user_prefs, historical_data):
    # Component 1: Confidence from Group 1 (0-100)
    confidence_score = recommendation.get("confidence", 0.5) * 100

    # Component 2: User Preference Alignment (0-100)
    preference_score = calculate_preference_alignment(
        recommendation,
        user_prefs
    )

    # Component 3: Historical Success Rate (0-100)
    similar_patterns = query_similar_tasks(recommendation)
    if similar_patterns:
        success_rate = sum(p.success for p in similar_patterns) / len(similar_patterns)
        historical_score = success_rate * 100
    else:
        historical_score = 50  # No data → neutral

    # Component 4: Risk Assessment (0-100, higher = safer)
    risk_score = assess_risk(recommendation)

    # Weighted average
    total_score = (
        confidence_score * 0.30 +
        preference_score * 0.25 +
        historical_score * 0.25 +
        risk_score * 0.20
    )

    return {
        "total_score": total_score,
        "confidence_score": confidence_score,
        "preference_score": preference_score,
        "historical_score": historical_score,
        "risk_score": risk_score
    }
```

**Interpretation**:
- **85-100**: Excellent recommendation - high confidence to proceed
- **70-84**: Good recommendation - proceed with standard caution
- **50-69**: Moderate recommendation - proceed carefully or seek alternatives
- **0-49**: Weak recommendation - consider rejecting or modifying significantly

### Framework 2: Multi-Criteria Decision Analysis (MCDA)

**Purpose**: Choose between multiple competing recommendations

**Method**: Weighted scoring across criteria

**Example - Choosing Between 3 Refactoring Approaches**:
```python
criteria = {
    "quality_impact": 0.30,      # How much will quality improve?
    "effort_required": 0.25,     # How much time/work?
    "risk_level": 0.20,          # How risky is it?
    "user_alignment": 0.15,      # Matches user style?
    "maintainability": 0.10      # Long-term benefits?
}

options = [
    {
        "name": "Modular Refactoring",
        "quality_impact": 90,
        "effort_required": 60,  # Higher effort → lower score
        "risk_level": 80,  # Lower risk → higher score
        "user_alignment": 85,
        "maintainability": 95
    },
    {
        "name": "Incremental Refactoring",
        "quality_impact": 70,
        "effort_required": 85,  # Lower effort → higher score
        "risk_level": 90,
        "user_alignment": 90,
        "maintainability": 75
    },
    {
        "name": "Complete Rewrite",
        "quality_impact": 100,
        "effort_required": 20,  # Very high effort → very low score
        "risk_level": 40,  # High risk → low score
        "user_alignment": 60,
        "maintainability": 100
    }
]

def calculate_mcda_score(option, criteria):
    score = 0
    for criterion, weight in criteria.items():
        score += option[criterion] * weight
    return score

scores = {opt["name"]: calculate_mcda_score(opt, criteria) for opt in options}
# Result:
# Modular Refactoring: 82.5
# Incremental Refactoring: 81.0
# Complete Rewrite: 63.0
# → Choose Modular Refactoring
```

**Best Practices**:
- Adjust criterion weights based on user preferences
- Normalize all scores to 0-100 range
- Consider negative criteria (effort, risk) inversely
- Document rationale for weights used

### Framework 3: Risk-Benefit Analysis

**Purpose**: Evaluate decisions through risk-benefit lens

**Matrix**:
```
         Low Benefit    |    High Benefit
---------|---------------|------------------
Low Risk | ⚠️ Avoid      | ✅ Do It (Quick Win)
High Risk| ❌ Never Do   | 🤔 Careful Analysis Required
```

**Implementation**:
```python
def categorize_decision(benefit_score, risk_level):
    """
    benefit_score: 0-100 (higher = more benefit)
    risk_level: 0-100 (higher = more risky)
    """
    high_benefit = benefit_score >= 70
    low_risk = risk_level <= 30

    if high_benefit and low_risk:
        return "quick_win", "High benefit, low risk - proceed immediately"
    elif high_benefit and not low_risk:
        return "high_value_high_risk", "Requires careful analysis and mitigation strategies"
    elif not high_benefit and low_risk:
        return "avoid", "Not worth the effort even if safe"
    else:
        return "never_do", "High risk, low benefit - reject"
```

**Risk Factors to Consider**:
- **Technical Risk**: Breaking changes, backward compatibility, dependency issues
- **Schedule Risk**: Could delay other tasks, unknown complexity
- **Quality Risk**: Might introduce bugs, could reduce test coverage
- **User Impact**: Disrupts user workflow, changes behavior significantly
- **Reversibility**: Can we undo if it fails?

**Benefit Factors to Consider**:
- **Quality Impact**: Improves code quality, reduces technical debt
- **Performance Impact**: Makes system faster, more efficient
- **Maintainability Impact**: Easier to maintain and extend
- **User Experience Impact**: Better UX, fewer errors
- **Strategic Value**: Aligns with long-term goals

### Framework 4: Prioritization Matrix (Eisenhower Matrix)

**Purpose**: Prioritize multiple tasks by urgency and importance

**Matrix**:
```
           Not Urgent    |     Urgent
-----------|---------------|------------------
Important  | 📋 Schedule   | 🔥 Do First
Not Import | 🗑️ Eliminate  | ⚡ Delegate/Quick
```

**Implementation**:
```python
def prioritize_tasks(recommendations):
    prioritized = {
        "do_first": [],      # Urgent + Important
        "schedule": [],      # Not Urgent + Important
        "quick_wins": [],    # Urgent + Not Important
        "eliminate": []      # Not Urgent + Not Important
    }

    for rec in recommendations:
        urgent = (
            rec.get("priority") == "high" or
            rec.get("severity") in ["critical", "high"] or
            rec.get("user_impact") == "high"
        )

        important = (
            rec.get("expected_impact") == "high" or
            rec.get("quality_impact") >= 15 or
            rec.get("strategic_value") == "high"
        )

        if urgent and important:
            prioritized["do_first"].append(rec)
        elif not urgent and important:
            prioritized["schedule"].append(rec)
        elif urgent and not important:
            prioritized["quick_wins"].append(rec)
        else:
            prioritized["eliminate"].append(rec)

    return prioritized
```

**Execution Order**:
1. **Do First** (Urgent + Important) - Execute immediately
2. **Quick Wins** (Urgent + Not Important) - Execute if time permits
3. **Schedule** (Not Urgent + Important) - Plan for future iteration
4. **Eliminate** (Not Urgent + Not Important) - Reject or defer indefinitely

## User Preference Integration

### Preference Alignment Scoring

**Purpose**: Quantify how well a recommendation matches user preferences

**Implementation**:
```python
def calculate_preference_alignment(recommendation, user_prefs):
    """
    Returns 0-100 score for preference alignment
    """
    alignment_score = 0
    total_weight = 0

    # 1. Coding Style Alignment (25 points)
    coding_style_weight = 25
    total_weight += coding_style_weight

    if recommendation.get("verbosity") == user_prefs.get("coding_style", {}).get("verbosity"):
        alignment_score += coding_style_weight
    elif abs(verbosity_scale(recommendation.get("verbosity")) -
             verbosity_scale(user_prefs.get("coding_style", {}).get("verbosity"))) <= 1:
        alignment_score += coding_style_weight * 0.7  # Partial credit

    # 2. Quality Priority Alignment (30 points)
    quality_weight = 30
    total_weight += quality_weight

    user_quality_priorities = user_prefs.get("quality_priorities", {})
    rec_quality_focus = recommendation.get("quality_focus", [])

    # Check if recommendation focuses on user's top priorities
    matches = len([p for p in rec_quality_focus if user_quality_priorities.get(p, 0) >= 0.7])
    if matches > 0:
        alignment_score += quality_weight * (matches / len(rec_quality_focus))

    # 3. Workflow Compatibility (25 points)
    workflow_weight = 25
    total_weight += workflow_weight

    # Check auto-fix threshold
    if recommendation.get("confidence", 0) >= user_prefs.get("workflow", {}).get("auto_fix_threshold", 0.85):
        alignment_score += workflow_weight
    elif recommendation.get("confidence", 0) >= user_prefs.get("workflow", {}).get("auto_fix_threshold", 0.85) - 0.1:
        alignment_score += workflow_weight * 0.5

    # 4. Communication Style Alignment (20 points)
    comm_weight = 20
    total_weight += comm_weight

    rec_detail = recommendation.get("detail_level", "balanced")
    user_detail = user_prefs.get("communication", {}).get("detail_level", "balanced")

    if rec_detail == user_detail:
        alignment_score += comm_weight
    elif abs(detail_scale(rec_detail) - detail_scale(user_detail)) <= 1:
        alignment_score += comm_weight * 0.6

    return alignment_score
```

### Preference-Based Plan Adjustment

**Purpose**: Adjust execution plan to match user preferences

**Example**:
```python
def adjust_plan_for_preferences(plan, user_prefs):
    """
    Modify execution plan to incorporate user preferences
    """
    adjusted_plan = plan.copy()

    # Adjust coding style
    if user_prefs.get("coding_style", {}).get("verbosity") == "concise":
        adjusted_plan["style_instructions"] = {
            "comments": "minimal",
            "docstrings": "one_line_only",
            "variable_names": "short_but_clear"
        }
    elif user_prefs.get("coding_style", {}).get("verbosity") == "verbose":
        adjusted_plan["style_instructions"] = {
            "comments": "extensive",
            "docstrings": "detailed_with_examples",
            "variable_names": "descriptive"
        }

    # Adjust quality targets based on user priorities
    quality_prefs = user_prefs.get("quality_priorities", {})
    adjusted_plan["quality_targets"] = {
        "tests": 70 + (quality_prefs.get("tests", 0.5) * 30),  # 70-100
        "documentation": 60 + (quality_prefs.get("documentation", 0.5) * 40),  # 60-100
        "code_quality": 75 + (quality_prefs.get("code_quality", 0.5) * 25)  # 75-100
    }

    # Adjust risk tolerance
    risk_tolerance = user_prefs.get("workflow", {}).get("risk_tolerance", "medium")
    if risk_tolerance == "low":
        adjusted_plan["constraints"]["max_auto_fix"] = 0.95  # Only very safe fixes
        adjusted_plan["require_confirmation"] = True
    elif risk_tolerance == "high":
        adjusted_plan["constraints"]["max_auto_fix"] = 0.75  # More aggressive fixes
        adjusted_plan["require_confirmation"] = False

    return adjusted_plan
```

## Trade-Off Analysis

### Framework: Balanced Trade-Off Evaluation

**Common Trade-Offs**:
1. **Speed vs Quality**
2. **Risk vs Benefit**
3. **Short-term vs Long-term**
4. **Simplicity vs Flexibility**
5. **Performance vs Readability**

**Implementation**:
```python
def analyze_trade_offs(recommendation):
    """
    Identify and evaluate trade-offs in a recommendation
    """
    trade_offs = []

    # Trade-off 1: Speed vs Quality
    if recommendation.get("estimated_effort_hours", 0) < 2:
        # Quick implementation
        trade_offs.append({
            "type": "speed_vs_quality",
            "chosen": "speed",
            "gain": "Fast implementation, quick delivery",
            "cost": "May not achieve highest quality, might need refinement later",
            "acceptable": True  # Generally acceptable for small changes
        })

    # Trade-off 2: Risk vs Benefit
    benefit_score = recommendation.get("expected_impact_score", 50)
    risk_score = recommendation.get("risk_score", 50)

    if benefit_score > 80 and risk_score > 60:
        trade_offs.append({
            "type": "risk_vs_benefit",
            "chosen": "benefit",
            "gain": f"High benefit ({benefit_score}/100)",
            "cost": f"Moderate to high risk ({risk_score}/100)",
            "acceptable": benefit_score > risk_score * 1.3,  # Benefit outweighs risk by 30%+
            "mitigation": "Add extra testing, implement in phases, have rollback plan"
        })

    # Trade-off 3: Short-term vs Long-term
    if recommendation.get("type") == "quick_fix" and recommendation.get("technical_debt_added", 0) > 0:
        trade_offs.append({
            "type": "short_term_vs_long_term",
            "chosen": "short_term",
            "gain": "Immediate problem resolution",
            "cost": "Adds technical debt, will need proper fix later",
            "acceptable": recommendation.get("severity") == "critical",  # OK for critical fixes
            "followup": "Schedule proper refactoring in next sprint"
        })

    return trade_offs
```

**Decision Rule**:
```python
def should_accept_trade_off(trade_off, user_prefs):
    """
    Decide if a trade-off is acceptable
    """
    # Check if user preferences lean toward chosen side
    if trade_off["type"] == "speed_vs_quality":
        if user_prefs.get("workflow", {}).get("prefer_speed"):
            return True
        elif user_prefs.get("quality_priorities", {}).get("code_quality", 0.5) > 0.8:
            return False  # User prioritizes quality

    # Check if gains outweigh costs
    if trade_off.get("gain_score", 0) > trade_off.get("cost_score", 0) * 1.5:
        return True  # 50% more gain than cost

    # Check if mitigation strategies exist
    if trade_off.get("mitigation") and len(trade_off.get("mitigation", "")) > 10:
        return True  # Has mitigation plan

    return trade_off.get("acceptable", False)
```

## Planning Strategies

### Strategy 1: Incremental Execution Plan

**When to Use**: Large changes, high risk, or complex refactoring

**Structure**:
```python
incremental_plan = {
    "approach": "incremental",
    "phases": [
        {
            "phase": 1,
            "name": "Foundation",
            "tasks": ["Extract core functions", "Add tests for extracted functions"],
            "duration_hours": 2,
            "validation_criteria": "All tests pass, coverage ≥ 80%",
            "rollback_plan": "Revert extraction if tests fail"
        },
        {
            "phase": 2,
            "name": "Integration",
            "tasks": ["Update callers to use extracted functions", "Add integration tests"],
            "duration_hours": 1.5,
            "validation_criteria": "No regressions, all integration tests pass",
            "rollback_plan": "Keep old functions as fallback"
        },
        {
            "phase": 3,
            "name": "Cleanup",
            "tasks": ["Remove old code", "Update documentation"],
            "duration_hours": 0.5,
            "validation_criteria": "No dead code, docs updated",
            "rollback_plan": "None needed - previous phases validated"
        }
    ],
    "total_duration_hours": 4,
    "checkpoint_frequency": "after_each_phase"
}
```

**Benefits**:
- Lower risk (validate after each phase)
- Can stop early if issues arise
- Easier to debug problems
- Better for learning (feedback after each phase)

### Strategy 2: Comprehensive Execution Plan

**When to Use**: Well-understood changes, low risk, small scope

**Structure**:
```python
comprehensive_plan = {
    "approach": "comprehensive",
    "tasks": [
        {
            "task": "Refactor authentication module",
            "subtasks": [
                "Extract validation logic",
                "Extract authentication logic",
                "Extract authorization logic",
                "Add tests for all components",
                "Update callers",
                "Remove old code",
                "Update documentation"
            ],
            "duration_hours": 4,
            "validation_criteria": "All tests pass, coverage ≥ 80%, no regressions"
        }
    ],
    "checkpoint_frequency": "at_end_only"
}
```

**Benefits**:
- Faster execution (no phase overhead)
- Simpler coordination
- Good for routine changes

### Strategy 3: Parallel Execution Plan

**When to Use**: Independent changes that can happen simultaneously

**Structure**:
```python
parallel_plan = {
    "approach": "parallel",
    "parallel_tracks": [
        {
            "track": "backend",
            "agent": "quality-controller",
            "tasks": ["Refactor API endpoints", "Add backend tests"],
            "duration_hours": 3
        },
        {
            "track": "frontend",
            "agent": "frontend-analyzer",
            "tasks": ["Update React components", "Add frontend tests"],
            "duration_hours": 2.5
        },
        {
            "track": "documentation",
            "agent": "documentation-generator",
            "tasks": ["Update API docs", "Update user guide"],
            "duration_hours": 1
        }
    ],
    "coordination_points": [
        {
            "after_hours": 2,
            "sync": "Ensure API contract matches frontend expectations"
        }
    ],
    "total_duration_hours": 3  # Max of parallel tracks
}
```

**Benefits**:
- Fastest total time
- Efficient use of multiple agents
- Good for full-stack changes

**Risks**:
- Coordination complexity
- Integration issues if not synced properly

## Confidence Calibration

### Framework: Adjust Confidence Based on Context

**Purpose**: Calibrate recommendation confidence based on additional factors

**Implementation**:
```python
def calibrate_confidence(recommendation, context):
    """
    Adjust recommendation confidence based on context
    Returns adjusted confidence (0.0-1.0)
    """
    base_confidence = recommendation.get("confidence", 0.5)

    # Adjustment factors
    adjustments = []

    # 1. Historical success with similar tasks
    similar_tasks = query_similar_tasks(recommendation)
    if similar_tasks:
        success_rate = sum(t.success for t in similar_tasks) / len(similar_tasks)
        if success_rate >= 0.9:
            adjustments.append(("high_historical_success", +0.1))
        elif success_rate <= 0.5:
            adjustments.append(("low_historical_success", -0.15))

    # 2. Untested pattern penalty
    pattern_reuse = recommendation.get("pattern_reuse_count", 0)
    if pattern_reuse == 0:
        adjustments.append(("untested_pattern", -0.1))
    elif pattern_reuse >= 5:
        adjustments.append(("proven_pattern", +0.05))

    # 3. Complexity factor
    complexity = recommendation.get("complexity", "medium")
    if complexity == "high":
        adjustments.append(("high_complexity", -0.1))
    elif complexity == "low":
        adjustments.append(("low_complexity", +0.05))

    # 4. User preference mismatch
    pref_alignment = calculate_preference_alignment(recommendation, context.get("user_prefs", {}))
    if pref_alignment < 50:
        adjustments.append(("low_preference_alignment", -0.08))

    # Apply adjustments
    adjusted_confidence = base_confidence
    for reason, delta in adjustments:
        adjusted_confidence += delta

    # Clamp to [0.0, 1.0]
    adjusted_confidence = max(0.0, min(1.0, adjusted_confidence))

    return {
        "original_confidence": base_confidence,
        "adjusted_confidence": adjusted_confidence,
        "adjustments": adjustments
    }
```

## Decision Explainability

### Framework: Document Every Decision

**Purpose**: Create transparent, understandable decisions for users and learning

**Implementation**:
```python
from lib.decision_explainer import create_explanation

def create_decision_explanation(decision, recommendations, user_prefs, historical_data):
    """
    Create comprehensive explanation for a decision
    """
    explanation = create_explanation(
        decision_id=f"decision_{task_id}",
        decision=decision,
        recommendations=recommendations,
        user_preferences=user_prefs,
        historical_data=historical_data,
        context={
            "task_type": "refactoring",
            "complexity": "medium"
        }
    )

    return explanation
    # Returns:
    # - why_chosen: Primary reasons for this decision
    # - why_not_alternatives: Why other options rejected
    # - trade_offs: What was gained vs what was sacrificed
    # - confidence_factors: What increases/decreases confidence
    # - user_alignment: How decision aligns with user preferences
    # - analogy: Human-friendly comparison
```

**Example Explanation Output**:
```markdown
## Decision: Modular Refactoring Approach

### Why This Decision?
**Primary Reason**: Highest combined score (82.5/100) balancing quality impact, effort, and risk.

**Supporting Reasons**:
1. Strong quality improvement potential (90/100)
2. Manageable effort (60/100 - approximately 4 hours)
3. Low risk with clear rollback options (80/100)
4. Excellent maintainability benefits (95/100)

### Why Not Alternatives?
**Incremental Refactoring (Score: 81.0)**: Close second, but lower quality impact (70 vs 90). Would take longer to achieve same quality level.

**Complete Rewrite (Score: 63.0)**: Rejected due to:
- Very high effort (20/100 - would take 20+ hours)
- High risk (40/100 - could introduce many bugs)
- Lower user alignment (60/100 - user prefers incremental changes)
Despite perfect quality potential, the risk-benefit ratio is unfavorable.

### Trade-offs Considered
**Time vs Quality**: Choosing modular approach over quick incremental fixes means:
- ✅ Gain: Significantly better long-term code quality
- ⚠️ Cost: Takes 1.5x longer than incremental approach
- ✓ Acceptable: Quality improvement worth the extra time

**Risk vs Benefit**: Moderate complexity with high reward:
- ✅ Gain: 90/100 quality improvement potential
- ⚠️ Cost: Some architectural risk in module boundaries
- ✓ Mitigation: Incremental implementation with validation checkpoints

### Confidence Factors
**High Confidence (0.88)**:
- ✓ Similar pattern succeeded 5 times previously (100% success rate)
- ✓ Strong alignment with user preferences (85/100)
- ⚠️ Moderate complexity reduces confidence slightly (-0.05)

### User Preference Alignment
- Coding Style: ✓ Matches preference for modular, well-organized code
- Quality Focus: ✓ User prioritizes maintainability (0.85) - this approach excels here
- Risk Tolerance: ✓ Medium risk acceptable for high-quality outcomes

### Analogy
Like reorganizing a messy closet by sorting items into clearly labeled boxes (modular refactoring) rather than just pushing things around (incremental) or building an entirely new closet system (complete rewrite). The sorting approach takes reasonable time, dramatically improves organization, and can be done safely one section at a time.
```

## Success Metrics

**Effective Decision-Making Indicators**:
- ✅ Decision confidence > 0.80 (well-supported decisions)
- ✅ User preference alignment > 75% (decisions match user style)
- ✅ Execution success rate > 90% (Group 3 successfully executes plans)
- ✅ Plan adjustment rate < 20% (plans don't need major revision during execution)
- ✅ User satisfaction > 85% (users accept decisions)
- ✅ Decision explainability score > 80% (users understand why decisions were made)

**Track with**:
```python
from lib.agent_performance_tracker import get_agent_performance

performance = get_agent_performance("strategic-planner")
print(f"Decision success rate: {performance['success_rate']:.1%}")
print(f"Average confidence: {performance['avg_confidence']:.2f}")
print(f"User approval rate: {performance['user_approval_rate']:.1%}")
```

## References

**Related Systems**:
- `lib/decision_explainer.py` - Decision explanation system
- `lib/user_preference_learner.py` - User preference tracking
- `lib/agent_performance_tracker.py` - Decision outcome tracking
- `lib/inter_group_knowledge_transfer.py` - Historical success data

**Related Documentation**:
- `docs/FOUR_TIER_ARCHITECTURE.md` - Complete architecture
- `agents/strategic-planner.md` - Master decision-maker agent
- `agents/preference-coordinator.md` - User preference specialist
- `skills/group-collaboration/SKILL.md` - Inter-group communication
