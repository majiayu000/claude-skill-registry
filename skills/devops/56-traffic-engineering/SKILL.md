---
sidebar_position: 0
title: "Build Your Traffic Engineering Skill"
description: "Create your traffic engineering skill in one prompt, then learn to improve it throughout the chapter"
chapter: 56
lesson: 0
duration_minutes: 25

skills:
  - name: "Skill-First Learning"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Apply"
    digcomp_area: "3. Digital Content Creation"
    measurable_at_this_level: "Student creates a working traffic-engineer skill using natural language"

learning_objectives:
  - objective: "Build a traffic-engineer skill using natural conversation with Claude"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Student has a working traffic-engineer skill in .claude/skills/"
  - objective: "Write a LEARNING-SPEC.md defining what, why, and success criteria"
    proficiency_level: "B1"
    bloom_level: "Create"
    assessment_method: "LEARNING-SPEC.md exists with clear success criteria"
  - objective: "Fetch official Envoy Gateway documentation via Context7"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Student can demonstrate Context7 usage"
  - objective: "Test skill generates valid Gateway API YAML"
    proficiency_level: "B1"
    bloom_level: "Evaluate"
    assessment_method: "kubectl apply --dry-run accepts generated YAML"

cognitive_load:
  new_concepts: 4
  assessment: "Four concepts: LEARNING-SPEC.md structure, Context7 docs, skill structure, grounded knowledge"

differentiation:
  extension_for_advanced: "Add rate limiting and TLS patterns during creation"
  remedial_for_struggling: "Follow exact prompt provided"
---

# Build Your Traffic Engineering Skill

Your AI agent is deployed to Kubernetes, but external users still cannot reach it. Before learning how to solve this problem—controlling traffic flow, rate limiting abuse, terminating TLS, and autoscaling under load—you will **own** a traffic-engineer skill.

This skill becomes a component of your sellable Digital FTE portfolio. By the end of this chapter, you will have a production-tested skill that generates Gateway API configurations, rate limiting policies, and autoscaling rules for any AI agent deployment.

---

## Step 1: Get the Skills Lab

1. Go to [github.com/panaversity/claude-code-skills-lab](https://github.com/panaversity/claude-code-skills-lab)
2. Click the green **Code** button
3. Select **Download ZIP**
4. Extract the ZIP file
5. Open the extracted folder in your terminal

```bash
cd claude-code-skills-lab
claude
```

**Output:**

```
Claude Code v1.0.0
Type your message or ? for help

>
```

---

## Step 2: Write Your LEARNING-SPEC.md

Before asking Claude to build your skill, define what you want to learn. Create a file named `LEARNING-SPEC.md`:

```markdown
# Traffic Engineering Learning Specification

## What
A skill for managing external traffic to Kubernetes services using:
- Gateway API (GatewayClass, Gateway, HTTPRoute)
- Rate limiting and circuit breaking
- TLS termination with CertManager
- Autoscaling with KEDA

## Why
External users need to reach my AI agents securely and reliably. Traffic
engineering protects services from abuse, terminates TLS at the edge, and
scales capacity based on demand.

## Success Criteria
- [ ] Skill generates valid Gateway + HTTPRoute YAML
- [ ] kubectl apply --dry-run=client accepts generated configurations
- [ ] Skill includes rate limiting patterns (per-user and global)
- [ ] Skill references official Envoy Gateway documentation
```

**Output:**

```
LEARNING-SPEC.md created (847 bytes)
```

This specification tells Claude exactly what you need and how you will measure success.

---

## Step 3: Fetch Official Documentation

Ask Claude to gather the authoritative source material:

```
Using your Context7 skill, fetch the official Envoy Gateway documentation.
I need to understand Gateway API resources (GatewayClass, Gateway, HTTPRoute)
and BackendTrafficPolicy for rate limiting.
```

Claude will retrieve documentation from the official Envoy Gateway project, giving your skill accurate, up-to-date patterns rather than hallucinated configurations.

**Output:**

```
Fetching Envoy Gateway documentation via Context7...

Retrieved:
- GatewayClass configuration
- Gateway resource patterns
- HTTPRoute matching rules
- BackendTrafficPolicy for rate limiting
- SecurityPolicy for authentication

Documentation ready for skill creation.
```

---

## Step 4: Create Your Skill

Now prompt Claude to build the skill using the fetched documentation:

```
Using your skill creator skill, create a new skill for traffic engineering
using Gateway API and Envoy Gateway. Use the Envoy Gateway docs you just
fetched. I will use it to manage ingress, rate limiting, TLS, and autoscaling
for my AI agents.
```

Claude will:
1. Study the fetched documentation
2. Ask clarifying questions about your traffic patterns
3. Create the skill with Gateway API templates and best practices

**Output:**

```
Creating traffic-engineer skill...

Questions:
1. Do you need both HTTP and HTTPS routes?
2. What rate limits should I include (requests per second)?
3. Should I include KEDA ScaledObject templates?

[After your answers]

Skill created at .claude/skills/traffic-engineer/
- SKILL.md: Core patterns and decision trees
- templates/: Gateway, HTTPRoute, BackendTrafficPolicy examples
- references/: Links to official documentation
```

Your skill appears at `.claude/skills/traffic-engineer/`.

---

## Step 5: Test Your Skill

Verify your new skill generates valid Kubernetes YAML:

```
Using my traffic-engineer skill, generate a Gateway and HTTPRoute
for my Task API running in the task-api namespace on port 8000.
```

**Output:**

```yaml
# gateway.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: task-api-gateway
  namespace: task-api
spec:
  gatewayClassName: eg
  listeners:
    - name: http
      protocol: HTTP
      port: 80
---
# httproute.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: task-api-route
  namespace: task-api
spec:
  parentRefs:
    - name: task-api-gateway
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /
      backendRefs:
        - name: task-api
          port: 8000
```

Save the output and validate:

```bash
kubectl apply --dry-run=client -f gateway.yaml
kubectl apply --dry-run=client -f httproute.yaml
```

**Output:**

```
gateway.gateway.networking.k8s.io/task-api-gateway created (dry run)
httproute.gateway.networking.k8s.io/task-api-route created (dry run)
```

If dry-run succeeds, your skill generates valid Gateway API configurations.

---

## Done

You now own a traffic-engineer skill built from official Envoy Gateway documentation. The rest of this chapter teaches you what it knows—and how to make it better.

**Next: Lesson 1 — Ingress Fundamentals**

---

## Reflect on Your Skill

Before moving on, consider:

- **What patterns from the official docs did your skill capture?** Gateway and HTTPRoute are the core resources. Did your skill include BackendTrafficPolicy for rate limiting? SecurityPolicy for authentication?

- **What is missing that you will add as you learn Gateway API, rate limiting, and KEDA?** You will likely add TLS configuration with CertManager, canary deployment patterns with traffic splitting, and KEDA ScaledObjects for autoscaling. Each lesson in this chapter strengthens your skill.

- **How does this skill compare to your Kubernetes skill from Chapter 50?** Traffic engineering operates at a higher layer—your Kubernetes skill handles pods and deployments, while this skill handles external traffic routing to those workloads.
