---
sidebar_position: 0
title: "Build Your Cloud Security Skill"
description: "Create your cloud security skill in one prompt, then learn to improve it throughout the chapter"
keywords: [kubernetes security, rbac, pod security, network policies, secrets management, cloud security skill]
chapter: 58
lesson: 0
duration_minutes: 15

skills:
  - name: "Skill-First Learning"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Apply"
    digcomp_area: "3. Digital Content Creation"
    measurable_at_this_level: "Student creates a working cloud-security skill using natural language"
  - name: "Kubernetes Security Fundamentals"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Understand"
    digcomp_area: "4. Safety"
    measurable_at_this_level: "Student identifies core security concepts: RBAC, NetworkPolicy, Pod Security Standards"

learning_objectives:
  - objective: "Build a cloud-security skill using natural conversation with Claude"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Student has a working cloud-security skill in .claude/skills/"
  - objective: "Write a LEARNING-SPEC.md defining security learning goals and success criteria"
    proficiency_level: "B1"
    bloom_level: "Create"
    assessment_method: "LEARNING-SPEC.md exists with clear success criteria"
  - objective: "Fetch official Kubernetes security documentation via Context7"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Student can demonstrate Context7 usage for security docs"
  - objective: "Test skill generates valid RBAC YAML"
    proficiency_level: "B1"
    bloom_level: "Evaluate"
    assessment_method: "kubectl apply --dry-run accepts generated YAML"

cognitive_load:
  new_concepts: 4
  assessment: "Four concepts: LEARNING-SPEC.md structure, Context7 docs, skill structure, 4C security model"

differentiation:
  extension_for_advanced: "Add NetworkPolicy and PSS patterns during creation"
  remedial_for_struggling: "Follow exact prompt provided"
---

# Build Your Cloud Security Skill

In January 2024, a major cryptocurrency exchange lost $230 million because an attacker exploited misconfigured Kubernetes RBAC—a service account with cluster-admin privileges was exposed through a debugging pod left running in production. The attacker didn't break encryption or exploit zero-days. They walked through a door that should have been locked.

Your Task API is running in Kubernetes. Before learning how to protect it—configuring RBAC, isolating network traffic, enforcing Pod Security Standards—you will **own** a cloud-security skill that generates secure configurations from day one.

This skill becomes a component of your sellable Digital FTE portfolio. By the end of this chapter, you will have a production-tested skill that implements defense-in-depth security for any Kubernetes workload.

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
# Cloud Security Learning Specification

## What
A skill for securing Kubernetes workloads using:
- RBAC (Roles, RoleBindings, ServiceAccounts)
- NetworkPolicies (default deny, explicit allow)
- Pod Security Standards (PSS enforcement)
- Secrets management (External Secrets Operator patterns)
- Image scanning (Trivy integration)
- Dapr security (mTLS, component scopes)

## Why
Production AI agents handle sensitive data and make autonomous decisions.
A single misconfiguration—an overprivileged service account, missing
network isolation, a container running as root—can expose the entire
cluster. The 4C security model (Cloud, Cluster, Container, Code)
provides defense-in-depth.

## Success Criteria
- [ ] Skill generates valid ServiceAccount + Role + RoleBinding YAML
- [ ] kubectl apply --dry-run=client accepts generated configurations
- [ ] Skill enforces least privilege (no wildcards in RBAC rules)
- [ ] Skill references official Kubernetes security documentation
```

**Output:**

```
LEARNING-SPEC.md created (892 bytes)
```

This specification tells Claude exactly what you need and how you will measure success.

---

## Step 3: Fetch Official Documentation

Ask Claude to gather the authoritative source material:

```
Using your Context7 skill, fetch the official Kubernetes security
documentation. I need to understand RBAC (Roles, ClusterRoles,
RoleBindings), NetworkPolicy, and Pod Security Standards.
```

Claude will retrieve documentation from the official Kubernetes project, giving your skill accurate, up-to-date patterns rather than hallucinated configurations.

**Output:**

```
Fetching Kubernetes security documentation via Context7...

Retrieved:
- RBAC authorization patterns
- NetworkPolicy specification
- Pod Security Standards (Privileged, Baseline, Restricted)
- Secrets management best practices
- Security context configuration

Documentation ready for skill creation.
```

---

## Step 4: Create Your Skill

Now prompt Claude to build the skill using the fetched documentation:

```
Using your skill creator skill, create a new skill for Kubernetes security.
I will use it to secure Python/FastAPI applications from dev to production.
Cover RBAC, NetworkPolicies, Pod Security Standards, secrets management,
image scanning with Trivy, and Dapr security. Use the Kubernetes security
docs you just fetched.
```

Claude will:
1. Study the fetched documentation
2. Ask clarifying questions about your security requirements
3. Create the skill with security templates and best practices

**Output:**

```
Creating cloud-security skill...

Questions:
1. Should I include patterns for External Secrets Operator?
2. What base PSS level should be the default (baseline or restricted)?
3. Do you need Dapr-specific security patterns?

[After your answers]

Skill created at .claude/skills/cloud-security/
- SKILL.md: Core patterns and decision trees
- templates/: RBAC, NetworkPolicy, PSS examples
- references/: Links to official documentation
```

Your skill appears at `.claude/skills/cloud-security/`.

---

## Step 5: Test Your Skill

Verify your new skill generates valid Kubernetes YAML:

```
Using my cloud-security skill, show me how to create a dedicated
ServiceAccount for my Task API with minimal permissions.
```

**Output:**

```yaml
# task-api-rbac.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: task-api-sa
  namespace: task-api
automountServiceAccountToken: false
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: task-api-role
  namespace: task-api
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: task-api-binding
  namespace: task-api
subjects:
- kind: ServiceAccount
  name: task-api-sa
roleRef:
  kind: Role
  name: task-api-role
  apiGroup: rbac.authorization.k8s.io
```

Save the output and validate:

```bash
kubectl apply --dry-run=client -f task-api-rbac.yaml
```

**Output:**

```
serviceaccount/task-api-sa created (dry run)
role.rbac.authorization.k8s.io/task-api-role created (dry run)
rolebinding.rbac.authorization.k8s.io/task-api-binding created (dry run)
```

If dry-run succeeds, your skill generates valid RBAC configurations following least privilege principles. Notice that the Role specifies only `configmaps` with `get` and `list` verbs—no wildcards, no cluster-wide access.

---

## Done

You now own a cloud-security skill built from official Kubernetes security documentation. The rest of this chapter teaches you what it knows—and how to make it better.

**Next: Lesson 1 — The 4C Security Model**

---

## Try With AI

Now that you have a working skill, test its gap identification capabilities.

**Prompt 1:**

```
Using my cloud-security skill, show me how to create a dedicated
ServiceAccount for my Task API with minimal permissions.
```

**What you're learning:** How your skill generates RBAC patterns following least privilege. Notice whether it avoids wildcards (*) in verbs and resources, and whether it suggests `automountServiceAccountToken: false` by default.

**Prompt 2:**

```
What's missing from this skill for production workloads?
```

**What you're learning:** Gap identification is a critical meta-skill. Your skill might be missing NetworkPolicy defaults, PSS enforcement labels, Trivy scanning integration, or Dapr component scopes. Each gap becomes a learning target for this chapter's lessons.

:::warning Security Reminder
Never test security configurations on production clusters. Always use `--dry-run=client` first, then apply to a development namespace. Security misconfigurations can expose your entire cluster.
:::
