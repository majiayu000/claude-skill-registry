---
sidebar_position: 0
title: "Build Your Operational Excellence Skill"
description: "Create your operational excellence skill in one prompt, then learn to improve it throughout the chapter"
keywords: [operational excellence, opencost, vpa, velero, chaos mesh, finops, disaster recovery, kubernetes]
chapter: 59
lesson: 0
duration_minutes: 15

skills:
  - name: "Skill-First Learning"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Apply"
    digcomp_area: "3. Digital Content Creation"
    measurable_at_this_level: "Student creates a working operational excellence skill using natural language and official documentation"

learning_objectives:
  - objective: "Build an operational excellence skill using natural conversation with Claude"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Student has a working operational-excellence skill in .claude/skills/"

cognitive_load:
  new_concepts: 1
  assessment: "Single concept: use Claude to build a skill from official docs for VPA, OpenCost, Velero, and Chaos Mesh"

differentiation:
  extension_for_advanced: "Add FinOps maturity stages and Game Day patterns during creation"
  remedial_for_struggling: "Follow exact prompt provided; focus on VPA recommendations first"
---

# Build Your Operational Excellence Skill

Your Task API runs in Kubernetes. You provisioned 2 CPU cores and 4GB memory per pod because "that seemed reasonable." Three months later, you're getting invoices you can't explain. Finance asks which team is driving costs. You have no idea.

Then disaster strikes: a developer accidentally deletes the production namespace. You scramble to restore from... backups you never tested. The database comes back, but half the configuration is missing. Downtime stretches from hours to days.

This chapter teaches you to see where money goes, protect against failures, and prove your systems can survive chaos. But you won't start by reading documentation and hoping you remember which VPA mode is safe for production. You'll start by **owning a skill** that encodes production patterns from OpenCost, VPA, Velero, and Chaos Mesh.

When your CFO asks why Kubernetes costs doubled, you won't search Stack Overflow. You'll invoke your skill, and it will generate the exact cost allocation queries, VPA configurations, and optimization recommendations you need. That's the difference between learning FinOps and owning operational excellence.

---

## Step 1: Get the Skills Lab

Clone a fresh skills lab to ensure a clean starting point:

1. Go to [github.com/panaversity/claude-code-skills-lab](https://github.com/panaversity/claude-code-skills-lab)
2. Click the green **Code** button
3. Select **Download ZIP**
4. Extract the ZIP file
5. Open the extracted folder in your terminal

```bash
cd claude-code-skills-lab
claude
```

---

## Step 2: Write Your Learning Spec

Before building the skill, define what you want to accomplish. Create a file called `LEARNING-SPEC.md`:

```markdown
# Operational Excellence Learning Spec

## What I Want to Learn
- Right-size pods using VPA recommendations without breaking production
- Track Kubernetes costs by namespace, team, and application with OpenCost
- Implement backup and disaster recovery with Velero
- Validate system resilience through chaos engineering with Chaos Mesh
- Design around RTO and RPO requirements

## Success Criteria
- I can generate VPA recommendations and understand when it's safe to apply them
- I can answer "Which namespace costs the most and why?" within 5 minutes
- I can restore a deleted namespace from backup in under 30 minutes
- I can run a pod-kill experiment in staging and measure recovery time
```

This spec guides both you and Claude on what the skill should cover.

---

## Step 3: Fetch Official Documentation

Use the `/fetching-library-docs` skill (or Context7 directly) to gather authoritative sources:

```
Using your fetching-library-docs skill, gather official documentation for:
1. Kubernetes VPA (Vertical Pod Autoscaler) - recommendation modes and policies
2. OpenCost - cost allocation and FinOps patterns
3. Velero - backup schedules, hooks, and restore procedures
4. Chaos Mesh - experiment types and safety controls

I need production-ready patterns, not just API references.
```

Claude fetches production-relevant patterns from official sources, not outdated blog posts.

---

## Step 4: Create the Skill

Now build your operational excellence skill with everything grounded in what you just fetched:

```
Using your skill creator skill, create a new skill for Kubernetes operational
excellence. I will use it to optimize costs, implement disaster recovery, and
validate resilience. Include:

- VPA modes (Off, Initial, Recreate) and when each is safe
- VPA + HPA coexistence patterns
- OpenCost installation and cost allocation queries
- FinOps progression: showback → allocation → chargeback
- Velero Schedule configuration with pre/post hooks
- RTO vs RPO definitions and how they affect backup frequency
- 3-2-1 backup rule implementation
- Chaos Mesh PodChaos and NetworkChaos examples
- Game Day planning pattern
- Safety guardrails for each technology

Use the documentation you just fetched - no self-assumed knowledge.
```

Claude will:
1. Reference the official docs it gathered
2. Ask clarifying questions (VPA update modes, backup retention, chaos scope)
3. Create the complete skill with tested patterns

Your skill appears at `.claude/skills/operational-excellence/`.

---

## Step 5: Test Your Skill

Verify the skill works by generating a valid manifest:

**Test 1: VPA Manifest**

```
Using your operational-excellence skill, generate a VPA manifest for the
task-api Deployment that starts in "Off" mode for safe recommendation
gathering. Include resource boundaries appropriate for a FastAPI service.
```

If the skill returns a valid VPA with proper updateMode and resourcePolicy, it's working.

**Test 2: Velero Schedule**

```
Using your operational-excellence skill, create a Velero Schedule that backs
up the production namespace daily at 2am with 30-day retention. Include a
pre-backup hook that runs pg_dump for the postgres container.
```

If the skill returns a valid Schedule with proper hooks syntax, it's ready for the chapter.

---

## What Happens Next

Each lesson in this chapter tests and improves your skill:

| Lesson | What You Learn | Skill Improvement |
|--------|----------------|-------------------|
| L01 | Resource Efficiency Fundamentals | Add right-sizing decision framework |
| L02 | VPA Configuration | Add VPA mode selection logic and HPA coexistence rules |
| L03 | OpenCost for Cost Visibility | Add cost allocation queries and label templates |
| L04 | FinOps Practices | Add showback/chargeback progression patterns |
| L05 | RTO/RPO Planning | Add backup strategy calculator based on business requirements |
| L06 | Velero Backup and Restore | Add Schedule templates with application-aware hooks |
| L07 | Chaos Engineering | Add PodChaos/NetworkChaos experiments and Game Day playbook |
| L08 | Data Sovereignty | Add multi-region backup patterns for compliance |
| L09 | Capstone | Complete integration testing and skill finalization |

By chapter end, your skill contains production-tested patterns for the entire operational excellence lifecycle.

---

## Try With AI

### Prompt 1: Assess Your Current Operational State

```
I'm about to learn Kubernetes operational excellence. Before diving into tools,
help me understand my gaps. Ask me about my current setup:
1. How do I know if my pods are over or under-provisioned?
2. Can I answer "What does Kubernetes cost per team?" right now?
3. When was the last time I tested restoring from backup?

Based on my answers, tell me which area needs attention first: cost visibility,
right-sizing, backup reliability, or resilience testing.
```

**What you're learning**: Self-assessment of current operational gaps through Socratic dialogue. Your skill will encode these patterns, but understanding your starting point helps you prioritize what to learn first.

### Prompt 2: Validate Your Skill's Coverage

```
I just created an operational excellence skill. Here's what it covers: [paste
your skill's key sections]. Review this against production SRE requirements.
What's missing? What would a senior SRE or FinOps practitioner add? Ask me
about my cluster size and budget constraints so your recommendations are
specific to my situation.
```

**What you're learning**: Skill validation through expert review. You're teaching your AI partner about your context so it can identify gaps specific to your organization's operational maturity.

### Prompt 3: Plan Your Operational Excellence Priorities

```
I have a Kubernetes cluster running Task API in production. I want to improve
operational excellence but can only focus on one area this sprint. Help me
decide between:
1. Setting up OpenCost for cost visibility
2. Implementing VPA for right-sizing
3. Configuring Velero backups
4. Running chaos experiments

Ask me about my biggest operational pain point right now and my team's
experience level with Kubernetes.
```

**What you're learning**: Strategic prioritization under constraints. Not every cluster needs every tool immediately. Your skill contains patterns for all four areas; this exercise teaches you which patterns to apply first based on your specific situation.

### Safety Note

Operational excellence tools interact with production infrastructure in powerful ways. VPA in Recreate mode will restart your pods. Velero can delete resources during restore. Chaos Mesh will intentionally break things. The patterns in your skill include safety guardrails, but always start with staging environments and Off/dry-run modes before touching production.
