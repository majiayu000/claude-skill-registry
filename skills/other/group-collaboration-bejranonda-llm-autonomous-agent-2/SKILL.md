---
name: Group Collaboration
description: Best practices for inter-group communication, knowledge sharing, and collaborative workflows in four-tier architecture
version: 7.0.0
category: collaboration
tags: [four-tier, inter-group, communication, knowledge-transfer, coordination]
related_skills: [pattern-learning, contextual-pattern-learning]
---

# Group Collaboration Skill

## Overview

This skill provides guidelines, patterns, and best practices for effective collaboration between the four agent groups in the four-tier architecture. It covers communication protocols, knowledge transfer strategies, feedback mechanisms, and coordination patterns that enable autonomous learning and continuous improvement across groups.

## When to Apply This Skill

**Use this skill when:**
- Implementing inter-group communication between any two groups
- Designing handoff protocols between analysis, decision, execution, and validation phases
- Setting up feedback loops for continuous improvement
- Sharing knowledge and patterns across groups
- Coordinating multi-group workflows
- Troubleshooting collaboration issues between groups
- Optimizing group performance through better coordination

**Required for:**
- All agents in four-tier architecture (Groups 1, 2, 3, 4)
- Orchestrator coordination logic
- Cross-group pattern learning
- Workflow optimization

## Four-Tier Architecture Recap

**Group 1: Strategic Analysis & Intelligence (The "Brain")**
- **Role**: Analyze and recommend
- **Output**: Recommendations with confidence scores
- **Key Agents**: code-analyzer, security-auditor, smart-recommender

**Group 2: Decision Making & Planning (The "Council")**
- **Role**: Evaluate and decide
- **Output**: Execution plans with priorities
- **Key Agents**: strategic-planner, preference-coordinator

**Group 3: Execution & Implementation (The "Hand")**
- **Role**: Execute decisions
- **Output**: Execution results with metrics
- **Key Agents**: quality-controller, test-engineer, documentation-generator

**Group 4: Validation & Optimization (The "Guardian")**
- **Role**: Validate and optimize
- **Output**: Validation results and feedback
- **Key Agents**: post-execution-validator, performance-optimizer, continuous-improvement

## Communication Patterns

### Pattern 1: Analysis → Decision (Group 1 → Group 2)

**Purpose**: Transfer analysis findings and recommendations to decision-makers

**Structure**:
```python
from lib.group_collaboration_system import record_communication

record_communication(
    from_agent="code-analyzer",  # Group 1
    to_agent="strategic-planner",  # Group 2
    task_id=task_id,
    communication_type="recommendation",
    message="Code analysis complete with 5 recommendations",
    data={
        "quality_score": 72,
        "recommendations": [
            {
                "type": "refactoring",
                "priority": "high",
                "confidence": 0.92,  # High confidence
                "description": "Extract login method complexity",
                "rationale": "Cyclomatic complexity 15, threshold 10",
                "estimated_effort_hours": 2.5,
                "expected_impact": "high",
                "files_affected": ["src/auth.py"]
            }
        ],
        "patterns_detected": ["token_auth", "validation_duplication"],
        "metrics": {
            "complexity_avg": 8.5,
            "duplication_rate": 0.12,
            "test_coverage": 0.78
        }
    }
)
```

**Best Practices**:
- Always include confidence scores (0.0-1.0)
- Provide rationale for each recommendation
- Include estimated effort and expected impact
- Attach relevant metrics and context
- Reference detected patterns
- List affected files

**Anti-Patterns to Avoid**:
- ❌ Recommendations without confidence scores
- ❌ Missing rationale or context
- ❌ Vague impact estimates ("it will be better")
- ❌ No prioritization
- ❌ Execution commands (that's Group 3's job)

### Pattern 2: Decision → Execution (Group 2 → Group 3)

**Purpose**: Communicate execution plan with priorities and user preferences

**Structure**:
```python
record_communication(
    from_agent="strategic-planner",  # Group 2
    to_agent="quality-controller",  # Group 3
    task_id=task_id,
    communication_type="execution_plan",
    message="Execute quality improvement plan with 3 priorities",
    data={
        "decision_rationale": "High-priority refactoring based on user preferences",
        "execution_plan": {
            "quality_targets": {
                "tests": 80,
                "standards": 90,
                "documentation": 70
            },
            "priority_order": [
                "fix_failing_tests",  # Highest priority
                "apply_code_standards",
                "add_missing_docs"
            ],
            "approach": "incremental",  # or "comprehensive"
            "risk_tolerance": "low"  # User preference
        },
        "user_preferences": {
            "auto_fix_threshold": 0.9,
            "coding_style": "concise",
            "comment_level": "moderate",
            "documentation_level": "standard"
        },
        "constraints": {
            "max_iterations": 3,
            "time_budget_minutes": 15,
            "files_in_scope": ["src/auth.py", "src/utils.py"]
        },
        "decision_confidence": 0.88
    }
)
```

**Best Practices**:
- Include clear execution plan with priorities
- Apply user preferences to the plan
- Set realistic constraints (time, iterations)
- Provide decision rationale
- Specify risk tolerance
- Define success criteria

**Anti-Patterns to Avoid**:
- ❌ Plans without priorities
- ❌ Missing user preferences
- ❌ Unrealistic constraints
- ❌ No success criteria
- ❌ Ambiguous instructions

### Pattern 3: Execution → Validation (Group 3 → Group 4)

**Purpose**: Send execution results for validation and quality assessment

**Structure**:
```python
record_communication(
    from_agent="quality-controller",  # Group 3
    to_agent="post-execution-validator",  # Group 4
    task_id=task_id,
    communication_type="execution_result",
    message="Quality improvement complete: 68 → 84",
    data={
        "metrics_before": {
            "quality_score": 68,
            "tests_passing": 45,
            "standards_violations": 23,
            "doc_coverage": 0.60
        },
        "metrics_after": {
            "quality_score": 84,
            "tests_passing": 50,
            "standards_violations": 2,
            "doc_coverage": 0.75
        },
        "changes_made": {
            "tests_fixed": 5,
            "standards_violations_fixed": 21,
            "docs_generated": 10
        },
        "files_modified": ["src/auth.py", "tests/test_auth.py"],
        "auto_corrections_applied": 30,
        "manual_review_needed": [],
        "iterations_used": 2,
        "execution_time_seconds": 145,
        "component_scores": {
            "tests": 28,
            "standards": 22,
            "documentation": 16,
            "patterns": 13,
            "code_metrics": 5
        },
        "issues_encountered": []
    }
)
```

**Best Practices**:
- Show before/after metrics clearly
- List all changes made
- Include execution statistics
- Report any issues encountered
- Specify files modified
- Break down component scores

**Anti-Patterns to Avoid**:
- ❌ Only showing final metrics without before state
- ❌ Missing execution time and iterations
- ❌ No breakdown of what was changed
- ❌ Hiding issues or failures
- ❌ Incomplete component scoring

### Pattern 4: Validation → Analysis (Group 4 → Group 1)

**Purpose**: Provide feedback on recommendation effectiveness for learning

**Structure**:
```python
from lib.agent_feedback_system import add_feedback

add_feedback(
    from_agent="post-execution-validator",  # Group 4
    to_agent="code-analyzer",  # Group 1
    task_id=task_id,
    feedback_type="success",  # or "improvement", "warning", "error"
    message="Recommendations were highly effective",
    details={
        "recommendations_followed": 3,
        "recommendations_effective": 3,
        "quality_improvement": 16,  # points improved
        "execution_smooth": True,
        "user_satisfaction": "high",
        "suggestions_for_improvement": []
    },
    impact="quality_score +16, all recommendations effective"
)
```

**Best Practices**:
- Specific feedback on recommendation effectiveness
- Quantify impact (quality score improvement)
- Note which recommendations worked best
- Suggest improvements for future
- Track user satisfaction

**Anti-Patterns to Avoid**:
- ❌ Vague feedback ("it was good")
- ❌ No quantified impact
- ❌ Only negative feedback without suggestions
- ❌ Missing context about what worked
- ❌ Not closing the feedback loop

## Knowledge Transfer Strategies

### Strategy 1: Pattern Propagation

**When to Use**: Share successful patterns across groups

```python
from lib.inter_group_knowledge_transfer import add_knowledge

add_knowledge(
    source_group=1,  # Group 1 discovered this
    knowledge_type="pattern",
    title="Modular Authentication Pattern",
    description="Breaking auth logic into validate(), authenticate(), authorize() improves testability and maintainability",
    context={
        "applies_to": ["authentication", "authorization", "security"],
        "languages": ["python", "typescript"],
        "frameworks": ["flask", "fastapi"]
    },
    evidence={
        "quality_score_improvement": 12,
        "test_coverage_improvement": 0.15,
        "reuse_count": 5,
        "success_rate": 0.92
    }
)
```

### Strategy 2: Anti-Pattern Sharing

**When to Use**: Share what NOT to do based on failures

```python
add_knowledge(
    source_group=3,  # Group 3 encountered this during execution
    knowledge_type="anti_pattern",
    title="Avoid Nested Ternary Operators",
    description="Nested ternary operators reduce readability and increase cognitive complexity significantly",
    context={
        "applies_to": ["code_quality", "readability"],
        "severity": "medium"
    },
    evidence={
        "complexity_increase": 8,  # Cyclomatic complexity
        "maintenance_issues": 3,
        "refactoring_time_hours": 1.5
    }
)
```

### Strategy 3: Best Practice Sharing

**When to Use**: Share techniques that consistently work well

```python
add_knowledge(
    source_group=4,  # Group 4 validated this across tasks
    knowledge_type="best_practice",
    title="Test Fixtures with CASCADE for PostgreSQL",
    description="Always use CASCADE in test fixture teardown to avoid foreign key constraint errors",
    context={
        "applies_to": ["testing", "database"],
        "frameworks": ["pytest"],
        "databases": ["postgresql"]
    },
    evidence={
        "success_rate": 1.0,
        "fixes_applied": 15,
        "issues_prevented": 30
    }
)
```

### Strategy 4: Optimization Tip Sharing

**When to Use**: Share performance improvements

```python
add_knowledge(
    source_group=4,  # Group 4 performance-optimizer discovered this
    knowledge_type="optimization",
    title="Batch Database Queries in Loops",
    description="Replace N+1 query patterns with batch queries using IN clause or JOINs",
    context={
        "applies_to": ["performance", "database"],
        "orm": ["sqlalchemy", "sequelize"]
    },
    evidence={
        "performance_improvement": "80%",  # 5x faster
        "query_reduction": 0.95,  # 95% fewer queries
        "cases_improved": 8
    }
)
```

## Feedback Loop Best Practices

### 1. Timely Feedback

**Principle**: Provide feedback immediately after validation, not days later

```python
# ✅ GOOD: Immediate feedback
validate_results()
send_feedback_to_group_1()
send_feedback_to_group_3()

# ❌ BAD: Delayed feedback loses context
validate_results()
# ... days later ...
send_feedback()  # Context is lost
```

### 2. Actionable Feedback

**Principle**: Feedback must be specific and actionable, not vague

```python
# ✅ GOOD: Specific and actionable
add_feedback(
    message="Recommendation confidence was too high (0.92) for untested pattern. Consider 0.75-0.85 for new patterns",
    suggestions=["Add confidence penalty for untested patterns", "Increase confidence gradually with reuse"]
)

# ❌ BAD: Vague
add_feedback(
    message="Confidence was wrong",
    suggestions=[]
)
```

### 3. Balanced Feedback

**Principle**: Highlight successes and areas for improvement

```python
# ✅ GOOD: Balanced
add_feedback(
    positive=[
        "Priority ranking was excellent - high priority items were truly critical",
        "User preference integration worked perfectly"
    ],
    improvements=[
        "Estimated effort was 40% too low - consider adjusting effort formula",
        "Could benefit from more error handling recommendations"
    ]
)
```

### 4. Learning-Oriented Feedback

**Principle**: Focus on how the agent can improve, not blame

```python
# ✅ GOOD: Learning-oriented
add_feedback(
    feedback_type="improvement",
    message="Analysis missed security vulnerability in auth flow",
    learning_opportunity="Add OWASP Top 10 checks to security analysis workflow",
    how_to_improve="Integrate security-auditor findings into code-analyzer reports"
)

# ❌ BAD: Blame-oriented
add_feedback(
    feedback_type="error",
    message="You failed to find the security issue",
    # No suggestions for improvement
)
```

## Coordination Patterns

### Pattern 1: Parallel Execution

**When to Use**: Multiple Group 1 agents can analyze simultaneously

```python
# Orchestrator coordinates parallel Group 1 analysis
from lib.group_collaboration_system import coordinate_parallel_execution

results = coordinate_parallel_execution(
    group=1,
    agents=["code-analyzer", "security-auditor", "smart-recommender"],
    task_id=task_id,
    timeout_minutes=5
)

# All Group 1 findings consolidated before sending to Group 2
consolidated_findings = consolidate_findings(results)
send_to_group_2(consolidated_findings)
```

### Pattern 2: Sequential Coordination

**When to Use**: Groups must execute in order (1→2→3→4)

```python
# Standard workflow
findings = execute_group_1_analysis()  # Group 1: Analyze
plan = execute_group_2_decision(findings)  # Group 2: Decide
results = execute_group_3_execution(plan)  # Group 3: Execute
validation = execute_group_4_validation(results)  # Group 4: Validate
```

### Pattern 3: Iterative Coordination

**When to Use**: Quality doesn't meet threshold, needs iteration

```python
for iteration in range(max_iterations):
    # Group 3 executes
    results = execute_group_3(plan)

    # Group 4 validates
    validation = execute_group_4(results)

    if validation.quality_score >= 70:
        break  # Success!

    # Group 4 sends feedback to Group 2 for plan adjustment
    feedback = validation.get_improvement_suggestions()
    plan = group_2_adjust_plan(plan, feedback)

    # Group 3 re-executes with adjusted plan
```

### Pattern 4: Conditional Coordination

**When to Use**: Execution path depends on analysis results

```python
# Group 1 analysis
security_findings = security_auditor.analyze()

if security_findings.critical_count > 0:
    # Critical security issues → immediate path
    plan = group_2_create_security_fix_plan(security_findings)
    results = group_3_execute_security_fixes(plan)
else:
    # Normal path
    all_findings = consolidate_all_group_1_findings()
    plan = group_2_create_standard_plan(all_findings)
    results = group_3_execute_standard(plan)
```

## Troubleshooting Collaboration Issues

### Issue 1: Communication Not Reaching Target

**Symptoms**:
- Group 2 doesn't receive Group 1 recommendations
- Group 3 doesn't receive execution plan

**Diagnosis**:
```python
from lib.group_collaboration_system import get_communications_for_agent

# Check if communications are recorded
comms = get_communications_for_agent("strategic-planner", communication_type="recommendation")
if not comms:
    print("❌ No communications found - sender may not be recording properly")
```

**Fix**:
- Ensure `record_communication()` is called after analysis
- Verify task_id is consistent across groups
- Check communication_type matches expected type

### Issue 2: Feedback Loop Not Learning

**Symptoms**:
- Same mistakes repeated
- No improvement in recommendation confidence
- Agents don't adjust based on feedback

**Diagnosis**:
```python
from lib.agent_feedback_system import get_feedback_stats

stats = get_feedback_stats("code-analyzer")
if stats["total_feedback"] == 0:
    print("❌ No feedback received - feedback loop broken")
```

**Fix**:
- Ensure Group 4 sends feedback after validation
- Verify agents query feedback before making decisions
- Check feedback is actionable and specific

### Issue 3: Knowledge Not Transferring

**Symptoms**:
- Groups rediscover same patterns
- Best practices not reused
- Learning not retained

**Diagnosis**:
```python
from lib.inter_group_knowledge_transfer import get_knowledge_transfer_stats

stats = get_knowledge_transfer_stats()
if stats["successful_transfers"] < stats["total_knowledge"] * 0.5:
    print("⚠️ Low knowledge transfer success rate")
```

**Fix**:
- Ensure agents query knowledge before tasks
- Add context matching to knowledge queries
- Increase knowledge confidence through successful applications

### Issue 4: Group Specialization Not Developing

**Symptoms**:
- All agents perform similarly across task types
- No clear specialization patterns
- Sub-optimal task routing

**Diagnosis**:
```python
from lib.group_specialization_learner import get_specialization_profile

profile = get_specialization_profile(group_num=3)
if not profile.get("specializations"):
    print("⚠️ No specializations detected - need more task diversity")
```

**Fix**:
- Record observations for all task executions
- Ensure task types are correctly labeled
- Allow sufficient tasks (50+) for specialization to emerge
- Review specialization insights regularly

## Success Metrics

**Effective Group Collaboration Indicators**:
- ✅ Communication flow rate > 95% (messages reach intended recipients)
- ✅ Feedback loop cycle time < 5 minutes (validation → feedback → learning)
- ✅ Knowledge reuse rate > 60% (discovered patterns applied in future tasks)
- ✅ Recommendation effectiveness > 85% (Group 1 recommendations followed and successful)
- ✅ Execution success rate > 90% (Group 3 executes plans successfully first time)
- ✅ Validation pass rate > 80% (Group 4 validates without requiring major iterations)
- ✅ Specialization emergence rate: Each group develops 3+ specializations after 100 tasks

**Track with:**
```python
from lib.group_collaboration_system import get_group_collaboration_stats

stats = get_group_collaboration_stats()
print(f"Communication success rate: {stats['communication_success_rate']:.1%}")
print(f"Average feedback cycle time: {stats['avg_feedback_cycle_seconds']}s")
print(f"Knowledge reuse rate: {stats['knowledge_reuse_rate']:.1%}")
```

## Integration Examples

### Example 1: Complete Four-Tier Workflow

```python
# Orchestrator coordinates complete workflow
from lib.group_collaboration_system import record_communication
from lib.agent_feedback_system import add_feedback
from lib.inter_group_knowledge_transfer import query_knowledge, add_knowledge
from lib.group_specialization_learner import get_recommended_group_for_task

# Step 0: Get specialization recommendations
routing = get_recommended_group_for_task(
    task_type="refactoring",
    complexity="medium",
    domain="authentication"
)
print(f"Recommended: {routing['recommended_agents']}")

# Step 1: Group 1 analyzes (code-analyzer)
analysis = code_analyzer.analyze(task)

# Query existing knowledge
existing_patterns = query_knowledge(
    for_group=1,
    knowledge_type="pattern",
    task_context={"task_type": "refactoring", "domain": "authentication"}
)

# Send findings to Group 2
record_communication(
    from_agent="code-analyzer",
    to_agent="strategic-planner",
    task_id=task_id,
    communication_type="recommendation",
    data=analysis
)

# Step 2: Group 2 decides (strategic-planner)
user_prefs = preference_coordinator.load_preferences()
plan = strategic_planner.create_plan(analysis, user_prefs)

# Send plan to Group 3
record_communication(
    from_agent="strategic-planner",
    to_agent="quality-controller",
    task_id=task_id,
    communication_type="execution_plan",
    data=plan
)

# Step 3: Group 3 executes (quality-controller)
results = quality_controller.execute(plan)

# Send results to Group 4
record_communication(
    from_agent="quality-controller",
    to_agent="post-execution-validator",
    task_id=task_id,
    communication_type="execution_result",
    data=results
)

# Step 4: Group 4 validates (post-execution-validator)
validation = post_execution_validator.validate(results)

# Send feedback to Group 1
add_feedback(
    from_agent="post-execution-validator",
    to_agent="code-analyzer",
    task_id=task_id,
    feedback_type="success",
    message="Recommendations were 95% effective",
    details={"quality_improvement": 18}
)

# Send feedback to Group 3
add_feedback(
    from_agent="post-execution-validator",
    to_agent="quality-controller",
    task_id=task_id,
    feedback_type="success",
    message="Execution was efficient and effective"
)

# Share successful pattern
if validation.quality_score >= 90:
    add_knowledge(
        source_group=4,
        knowledge_type="pattern",
        title="Successful Authentication Refactoring Pattern",
        description=f"Pattern used in task {task_id} achieved quality score {validation.quality_score}",
        context={"task_type": "refactoring", "domain": "authentication"},
        evidence={"quality_score": validation.quality_score}
    )
```

## References

**Related Systems**:
- `lib/group_collaboration_system.py` - Communication tracking
- `lib/agent_feedback_system.py` - Feedback management
- `lib/inter_group_knowledge_transfer.py` - Knowledge sharing
- `lib/group_specialization_learner.py` - Specialization tracking
- `lib/agent_performance_tracker.py` - Performance metrics

**Related Documentation**:
- `docs/FOUR_TIER_ARCHITECTURE.md` - Complete architecture design
- `docs/FOUR_TIER_ENHANCEMENTS.md` - Advanced features
- `agents/orchestrator.md` - Orchestrator coordination logic
