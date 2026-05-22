---
sidebar_position: 15
chapter: 50
lesson: 15
duration_minutes: 20
title: "Test and Refine Your Kubernetes Skill"
proficiency_level: B1
teaching_stage: 3
stage_name: "Intelligence Refinement"
stage_description: "Validate skill transferability by applying to different application types"
cognitive_load:
  concepts_count: 2
  scaffolding_level: "Low"
learning_objectives:
  - id: LO1
    description: "Apply Kubernetes skill to an application type different from the capstone"
    bloom_level: "Apply"
  - id: LO2
    description: "Identify gaps in skill guidance through cross-application testing"
    bloom_level: "Evaluate"
  - id: LO3
    description: "Refine skill based on discovered limitations"
    bloom_level: "Create"
digcomp_mapping:
  - objective_id: LO1
    competency_area: "5. Problem Solving"
    competency: "5.1 Solving technical problems"
  - objective_id: LO2
    competency_area: "5. Problem Solving"
    competency: "5.4 Identifying digital competence gaps"
  - objective_id: LO3
    competency_area: "3. Digital Content Creation"
    competency: "3.4 Programming"
---

# Test and Refine Your Kubernetes Skill

You built your Kubernetes skill in Lesson 0 and refined it through Lessons 1-14. Now validate that it actually transfers to new projects.

A skill that only works for your FastAPI agent isn't a skill—it's a template. True skills guide decisions across different application types.

---

## Choose a Different Application

Pick one application type you haven't deployed in this chapter:

| Type | Characteristics |
|------|-----------------|
| **Data processing job** | Runs 1-2 hours, high CPU/memory, processes large files |
| **Node.js web service** | HTTP requests, external API connections, high availability |
| **Go batch processor** | Runs periodically, external config, needs graceful shutdown |
| **Python API gateway** | Routes to multiple backends, high volume, low latency |

The application type doesn't matter. What matters: it's different enough from your FastAPI agent that you can't copy manifests from Lesson 14.

---

## Work Through Your Skill

Using only your skill (not Lesson 14's code), answer these questions for your chosen application:

**1. Resource Planning**
- What CPU and memory requests/limits would you set?
- How did you arrive at these numbers?

**2. Health Checking**
- What probes does this application need?
- How would you implement them?

**3. Configuration**
- What belongs in ConfigMaps vs Secrets?
- How would you inject them?

**4. Labels**
- How would you structure labels for this application?
- What queries would operators run against these labels?

**5. Deployment Strategy**
- What special considerations exist for updating this application?
- Does it need different rollout parameters than your agent?

Your skill should guide you through these decisions without prescribing specific answers.

---

## Identify Gaps

After working through your skill on a different application:

| Question | Your Answer |
|----------|-------------|
| What worked? | Which guidance forced useful analysis? |
| What was missing? | What decisions did the skill not address? |
| What was too prescriptive? | Did any guidance feel like rules instead of frameworks? |

Document 2-3 specific gaps you discovered.

---

## Refine Your Skill

Open your skill at `.claude/skills/kubernetes-deployment/SKILL.md` and add:

1. **Missing decision points** — Questions your skill didn't help you answer
2. **Application-specific patterns** — Guidance for batch jobs, gateways, or other types you tested
3. **Edge cases** — Situations where the general guidance doesn't apply

Your skill grows with each application you deploy.

---

## Try With AI

**Validate skill transferability with Claude:**

```
I have a Kubernetes deployment skill I built during this chapter. Now I want
to deploy a [your chosen application type] that:
- [characteristic 1]
- [characteristic 2]
- [characteristic 3]

Using my skill (attached), walk me through the deployment decisions. As you
work through each decision point, tell me:
- Which parts of my skill guide clearly?
- Where is guidance missing or unclear?
- What should I add to make this skill work for this application type?

[Paste your SKILL.md content]
```

**What you're learning:** How to validate that intelligence you've captured actually transfers to new contexts—the difference between a template and a skill.

---

## Reflection

Your skill started from official documentation in Lesson 0. Through 14 lessons, you learned what those patterns mean in practice. Now you've tested whether your skill captures that learning in transferable form.

A well-designed skill guides fundamentally similar decisions (resource balance, health checking, configuration injection) even when the specific answers differ by application type.

**Next:** Optional lessons 16-22 cover advanced patterns. Each one is an opportunity to extend your skill with specialized guidance.
