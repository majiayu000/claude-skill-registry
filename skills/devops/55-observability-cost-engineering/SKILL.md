---
sidebar_position: 0
title: "Build Your Observability Skill"
description: "Create your observability and cost engineering skill in one prompt, then learn to improve it throughout the chapter"
keywords: [observability, prometheus, grafana, opentelemetry, jaeger, loki, finops, kubernetes monitoring]
chapter: 55
lesson: 0
duration_minutes: 15

skills:
  - name: "Skill-First Learning"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Apply"
    digcomp_area: "3. Digital Content Creation"
    measurable_at_this_level: "Student creates a working observability skill using natural language and official documentation"

learning_objectives:
  - objective: "Build an observability skill using natural conversation with Claude"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Student has a working observability-cost-engineer skill in .claude/skills/"

cognitive_load:
  new_concepts: 1
  assessment: "Single concept: use Claude to build a skill from official docs for Prometheus, OpenTelemetry, and Loki"

differentiation:
  extension_for_advanced: "Add SLO alerting and OpenCost patterns during creation"
  remedial_for_struggling: "Follow exact prompt provided; focus on Prometheus first"
---

# Build Your Observability Skill

Your Task API runs in Kubernetes. Users report slow responses, but you have no visibility. Is it the database? The network? A memory leak? Without observability, you're debugging in the dark.

This chapter teaches you to instrument applications, build dashboards, and manage cloud costs. But you won't start by reading documentation and hoping you remember the right PromQL syntax. You'll start by **owning a skill** that encodes production patterns from Prometheus, OpenTelemetry, Jaeger, Loki, and OpenCost.

When you face a production incident at 2am, you won't search Stack Overflow. You'll invoke your skill, and it will generate the exact queries, dashboards, and alerts you need. That's the difference between learning observability and owning observability.

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
# Observability Learning Spec

## What I Want to Learn
- Monitor Kubernetes applications with Prometheus metrics
- Trace requests across services with OpenTelemetry and Jaeger
- Aggregate logs with Loki and query with LogQL
- Define SLOs and create multi-burn-rate alerts
- Track cloud costs with OpenCost

## Success Criteria
- I can deploy a full observability stack in under 30 minutes
- I can write PromQL queries for the 4 golden signals
- I can instrument a FastAPI app and see traces in Jaeger
- I can identify the top 3 cost drivers in my cluster
```

This spec guides both you and Claude on what the skill should cover.

---

## Step 3: Fetch Official Documentation

Use the `/fetching-library-docs` skill (or Context7 directly) to gather authoritative sources:

```
Using your fetching-library-docs skill, gather official documentation for:
1. Prometheus - metrics collection and PromQL
2. OpenTelemetry Python SDK - instrumentation
3. Grafana Loki - log aggregation and LogQL

I need patterns for Kubernetes monitoring, not just API references.
```

Claude fetches production-relevant patterns from official sources, not Stack Overflow answers from 2019.

---

## Step 4: Create the Skill

Now build your observability skill with everything grounded in what you just fetched:

```
Using your skill creator skill, create a new skill for Kubernetes observability
and cost engineering. I will use it to monitor applications from basic metrics
to production SRE practices. Include:

- Prometheus installation and ServiceMonitor configuration
- PromQL patterns for 4 golden signals
- OpenTelemetry FastAPI instrumentation
- Loki LogQL query patterns
- SLO/error budget alerting
- OpenCost cost allocation

Use the documentation you just fetched - no self-assumed knowledge.
```

Claude will:
1. Reference the official docs it gathered
2. Ask clarifying questions (sampling rates, retention, alert thresholds)
3. Create the complete skill with tested patterns

Your skill appears at `.claude/skills/observability-cost-engineer/`.

---

## Step 5: Test Your Skill

Verify the skill works by asking it a question:

```
Using your observability-cost-engineer skill, write a PromQL query that shows
the P95 latency for the task-api service over the last hour, broken down by
endpoint.
```

If the skill returns a correct histogram_quantile query, it's working. If it hallucinates syntax, refine the skill with corrections.

---

## What Happens Next

Each lesson in this chapter tests and improves your skill:

| Lesson | What You Learn | Skill Improvement |
|--------|----------------|-------------------|
| L01 | Three Pillars of Observability | Add decision framework: metrics vs traces vs logs |
| L02 | Prometheus + PromQL | Add recording rules and ServiceMonitor templates |
| L03 | Grafana Dashboards | Add dashboard JSON templates for golden signals |
| L04 | OpenTelemetry + Jaeger | Add FastAPI instrumentation code and sampling config |
| L05 | Loki + LogQL | Add structured logging patterns and log-trace correlation |
| L06 | SLIs, SLOs, Error Budgets | Add SLO calculation formulas and budget burn rates |
| L07 | Alerting | Add multi-burn-rate PrometheusRule templates |
| L08 | Cost Engineering | Add OpenCost queries and right-sizing recommendations |
| L09 | Dapr Integration | Add Dapr observability Configuration CRD |
| L10 | Capstone | Complete integration testing and skill finalization |

By chapter end, your skill contains production-tested patterns for the entire observability stack.

---

## Try With AI

### Prompt 1: Explore the Three Pillars

```
I'm about to learn Kubernetes observability. Before diving into tools, help me
understand the landscape. Ask me about a recent debugging experience where I
wished I had more visibility. Based on that, explain which of the three pillars
(metrics, traces, logs) would have helped most and why.
```

**What you're learning**: Self-assessment of current observability gaps through Socratic dialogue. Your skill will encode these patterns, but understanding the "why" helps you know when to apply each pillar.

### Prompt 2: Validate Your Skill's Coverage

```
I just created an observability skill. Here's what it covers: [paste your skill's
key sections]. Review this against production SRE requirements. What's missing?
What would a senior SRE add? Ask me about my deployment environment so your
recommendations are specific to my needs.
```

**What you're learning**: Skill validation through expert review. You're teaching your AI partner about your context so it can identify gaps specific to your situation.

### Prompt 3: Plan Your Observability Stack

```
I'm deploying Task API to Kubernetes and need to choose observability tools.
I know about Prometheus, Grafana, Jaeger, and Loki from my new skill. Help me
prioritize: If I can only deploy two tools this week, which two give me the
most value? Ask me about my team size, budget, and biggest operational pain
points.
```

**What you're learning**: Strategic prioritization under constraints. Not every stack needs every tool. Your skill contains patterns for all; this exercise teaches you which patterns apply to your situation first.

### Safety Note

Observability tools collect sensitive data about your applications and infrastructure. When configuring Prometheus scrape targets, Loki log streams, or OpenTelemetry traces, ensure you're not capturing secrets, PII, or credentials. The patterns in your skill include security considerations, but always validate against your organization's data handling policies.
