---
sidebar_position: 7
title: "Docker Image Builder Skill"
description: "Transform Docker knowledge from Lessons 1-6 into a reusable AI skill for consistent, production-ready containerization"
keywords: [docker, skill, reusable intelligence, persona, principles, dockerfile, containerization]
chapter: 49
lesson: 7
duration_minutes: 50
proficiency_level: B1
teaching_stage: 3
stage_name: "Intelligence Design"
stage_description: "Create reusable AI skills from accumulated Docker knowledge"

# HIDDEN SKILLS METADATA
skills:
  - name: "Recognizing Patterns Worth Encoding"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Analyze"
    digcomp_area: "Problem-Solving"
    measurable_at_this_level: "Student can identify when a recurring pattern justifies skill creation based on frequency, complexity, and organizational value"

  - name: "Designing Skill Personas"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Create"
    digcomp_area: "Digital Content Creation"
    measurable_at_this_level: "Student can write a cognitive stance that activates appropriate reasoning for a domain"

  - name: "Writing Analysis Questions"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Create"
    digcomp_area: "Problem-Solving"
    measurable_at_this_level: "Student can formulate questions that force context-specific reasoning rather than generic responses"

  - name: "Defining Decision Principles"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Create"
    digcomp_area: "Problem-Solving"
    measurable_at_this_level: "Student can articulate non-negotiable rules that guide production decisions"

  - name: "Creating SKILL.md Files"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Create"
    digcomp_area: "Digital Content Creation"
    measurable_at_this_level: "Student can structure a complete skill file following canonical format"

  - name: "Testing Skills Against Novel Scenarios"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Evaluate"
    digcomp_area: "Problem-Solving"
    measurable_at_this_level: "Student can validate skill effectiveness across different project types"

learning_objectives:
  - objective: "Identify recurring patterns from Lessons 1-6 worth encoding as reusable intelligence"
    proficiency_level: "B1"
    bloom_level: "Analyze"
    assessment_method: "Pattern recognition exercise identifying 3+ encoding candidates"

  - objective: "Design a skill persona that activates Docker expertise reasoning"
    proficiency_level: "B1"
    bloom_level: "Create"
    assessment_method: "Written persona with specific cognitive stance"

  - objective: "Write analysis questions that activate context-specific reasoning"
    proficiency_level: "B1"
    bloom_level: "Create"
    assessment_method: "5+ questions that prevent generic responses"

  - objective: "Define principles for production Dockerfile decisions"
    proficiency_level: "B1"
    bloom_level: "Create"
    assessment_method: "7+ non-negotiable principles with clear rationale"

  - objective: "Create a SKILL.md file following canonical format"
    proficiency_level: "B1"
    bloom_level: "Create"
    assessment_method: "Complete skill file with all required sections"

  - objective: "Test the skill with novel project scenarios"
    proficiency_level: "B1"
    bloom_level: "Evaluate"
    assessment_method: "Skill produces appropriate Dockerfiles for 3 different project types"

cognitive_load:
  new_concepts: 6
  assessment: "6 concepts (skill as intelligence, persona pattern, analysis questions, principles, SKILL.md format, skill testing) appropriate for B1 intermediate level"

differentiation:
  extension_for_advanced: "Create a skill that handles multi-service Docker Compose configurations; extend the skill to include CI/CD pipeline integration"
  remedial_for_struggling: "Focus on the Persona + Principles pattern first; add analysis questions after mastering the core structure"
---

# Docker Image Builder Skill

You've now written Dockerfiles for the Task API through six lessons. Each time, you made similar decisions: base image selection, dependency strategy, layer optimization, security posture. What if you could encode this reasoning so AI can apply it consistently to ANY project?

That's what skills do. A skill captures domain expertise in a format that AI can apply reliably across contexts. Instead of re-explaining your Docker preferences every time, you encode them once. The AI then reasons through your principles for each new project, producing Dockerfiles that match your production standards.

This lesson teaches you to transform your Docker knowledge into a reusable skill. You'll learn the Persona + Questions + Principles pattern that makes skills effective, create a complete SKILL.md file, and test it against projects you haven't seen before.

---

## What Makes a Pattern Worth Encoding

Not every workflow deserves a skill. Creating skills takes effort. You need to identify patterns that justify that investment.

**Three criteria determine if a pattern is worth encoding:**

| Criterion | Question to Ask | Docker Example |
|-----------|-----------------|----------------|
| **Recurrence** | Will this pattern appear in 3+ projects? | Containerizing Python services happens constantly |
| **Complexity** | Does it involve 5+ decision points? | Base image, multi-stage, UV, security, volumes, networking |
| **Organizational Value** | Does it accelerate future work? | Every new service needs containerization |

Docker containerization meets all three. You containerize services repeatedly, each Dockerfile involves 8-10 decisions, and faster containerization accelerates deployment across all projects.

**Patterns that DON'T justify skills:**

- One-off configuration (single project setup)
- Simple commands (docker build, docker run)
- Trivial decisions (choosing between two obvious options)

**Exercise**: Before continuing, list three patterns from your own work that might justify skills. Apply the three criteria to each.

---

## The Persona + Questions + Principles Pattern

Effective skills follow a consistent structure. Each component serves a specific purpose:

### Persona: The Cognitive Stance

A persona establishes HOW the AI should think. It's not "you are an expert"—that's too vague. A good persona specifies the perspective and priorities that produce right thinking.

**Weak persona:**
```
You are a Docker expert.
```

**Strong persona:**
```
Think like a DevOps engineer who optimizes container images for production
Kubernetes deployments. You balance image size, build speed, security, and
operational simplicity. When tradeoffs exist, you favor smaller images and
faster pulls over build-time convenience.
```

The strong persona tells the AI:
- **Domain**: DevOps engineering
- **Target**: Production Kubernetes
- **Priorities**: Size, speed, security, simplicity
- **Tradeoff resolution**: Favor runtime over build-time

### Analysis Questions: Context-Specific Reasoning

Analysis questions force the AI to gather context before acting. Without them, AI produces generic solutions. With them, AI reasons about YOUR specific situation.

**Generic approach (no questions):**
```
Generate a Dockerfile for this Python project.
```

**Context-aware approach (with questions):**
```
Before generating, analyze:

1. Deployment Target: Kubernetes cluster, Docker Compose, bare Docker?
2. Base Image Strategy: What constraints apply (security, size, compatibility)?
3. Large Files: Are there model files or data that should be volume-mounted?
4. Security Requirements: Non-root user required? Read-only filesystem?
5. Health Monitoring: What endpoints indicate service health?
6. Build Frequency: How often will this image be rebuilt?
```

Each question targets a decision point. The answers shape the Dockerfile.

### Principles: Non-Negotiable Decisions

Principles are rules that apply regardless of context. They encode your hard-won lessons about what works in production.

**Docker containerization principles:**

1. **Multi-Stage Always**: Separate build dependencies from runtime
2. **UV for Speed**: Use UV package manager (10-100x faster than pip)
3. **Alpine Default**: Start with alpine, fall back to slim if compatibility issues
4. **Health Checks Mandatory**: Every production container needs HEALTHCHECK
5. **Non-Root Default**: Run as non-root user unless explicitly required otherwise
6. **Environment Configuration**: All configuration via environment variables
7. **No Secrets in Image**: Never COPY .env or credentials into image

These aren't suggestions. They're non-negotiables that every Dockerfile should follow unless there's explicit justification to deviate.

---

## Designing the Production Dockerfile Skill

Let's build the complete skill, component by component.

### Skill Persona

```markdown
Think like a DevOps engineer who optimizes container images for production
Kubernetes deployments. You balance four priorities:

1. **Image Size**: Smaller images mean faster pulls and lower registry costs
2. **Build Speed**: Developer iteration time matters; use UV and layer caching
3. **Security**: Non-root users, minimal attack surface, no embedded secrets
4. **Operational Simplicity**: Health checks, clear labels, predictable behavior

When these priorities conflict, resolve as follows:
- Security trumps convenience (always non-root, always health checks)
- Runtime size trumps build speed (multi-stage even if slower to build)
- Operational clarity trumps clever optimization (explicit over implicit)
```

### Analysis Questions

```markdown
Before generating a Dockerfile, analyze the project by answering:

1. **Deployment Target**
   - Kubernetes cluster (needs probes, resource limits)?
   - Docker Compose (local development, simpler requirements)?
   - Bare Docker (single container, minimal orchestration)?

2. **Base Image Strategy**
   - Are there security constraints (approved base images only)?
   - Does the application require specific system libraries?
   - Is alpine compatible, or must we use slim/full?

3. **Dependency Installation**
   - Python project (use UV for 10-100x faster installs)?
   - Node project (use npm ci for reproducible builds)?
   - Mixed stack (consider separate build stages)?

4. **Large Files (>100MB)**
   - Model files that should be volume-mounted?
   - Static assets that should be in CDN instead?
   - Data files that change independently of code?

5. **Security Requirements**
   - Non-root user required (almost always yes)?
   - Read-only filesystem feasible?
   - What secrets need injection at runtime?

6. **Health Monitoring**
   - What endpoint indicates healthy service?
   - What dependencies must be ready (database, cache)?
   - What startup time should health check account for?

7. **Build Context**
   - What files should .dockerignore exclude?
   - Are there large directories (node_modules, .git) to skip?
   - Does build need access to private registries?
```

### Principles

```markdown
Apply these principles to every Dockerfile:

## Build Structure

**P1: Multi-Stage Always**
Separate build stage (has compilers, dev tools) from runtime stage (minimal).
Even if current deps don't require compilation, future deps might.

**P2: Layer Order Matters**
Copy dependency files first (requirements.txt, package.json), install,
then copy source. This maximizes layer cache hits.

**P3: Single RUN for Related Operations**
Combine related commands with && to reduce layers and ensure cleanup
happens in same layer:
```dockerfile
RUN pip install uv && \
    uv pip install --system -r requirements.txt && \
    rm -rf /root/.cache
```

## Package Management

**P4: UV for Python**
Always use UV package manager for Python. It's 10-100x faster than pip:
```dockerfile
RUN pip install uv && \
    uv pip install --system --no-cache -r requirements.txt
```

**P5: Lock Files Required**
Use requirements.txt with pinned versions or uv.lock for reproducibility.
Never install without version constraints in production.

## Base Images

**P6: Alpine Default**
Start with python:3.12-alpine (50MB). Fall back to slim (150MB) only if
alpine causes compatibility issues with specific packages.

**P7: Pin Versions**
Use python:3.12-alpine, not python:alpine. Explicit versions prevent
surprise breakage when base images update.

## Security

**P8: Non-Root User**
Create and switch to non-root user:
```dockerfile
RUN adduser --disabled-password --gecos '' appuser
USER appuser
```

**P9: No Secrets in Image**
Never COPY .env, credentials, or API keys. Inject via environment at runtime.
Use Docker secrets or Kubernetes secrets for sensitive data.

**P10: Minimal Installed Packages**
Only install what runtime needs. Build tools stay in build stage.

## Runtime Configuration

**P11: Health Checks Mandatory**
Every production container needs HEALTHCHECK:
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

**P12: Environment Variables for Configuration**
All configuration via ENV. No hardcoded values in Dockerfile.
```dockerfile
ENV APP_PORT=8000 \
    LOG_LEVEL=info \
    PYTHONUNBUFFERED=1
```

## Large Files

**P13: Volume Mount, Don't COPY**
Files >100MB (models, datasets) should be volume-mounted at runtime:
```yaml
# docker-compose.yaml
volumes:
  - ./models:/app/models
```
Never embed large files in the image.
```

---

## The SKILL.md File Format

Skills live in SKILL.md files within the `.claude/skills/` directory. Here's the complete format:

```markdown
---
name: production-dockerfile
description: Generate production-ready Dockerfiles with multi-stage builds, security best practices, and optimization. Use when containerizing Python applications for Kubernetes or Docker deployments.
allowed-tools: Read, Write, Edit, Bash
---

# Production Dockerfile Skill

## Persona

Think like a DevOps engineer who optimizes container images for production
Kubernetes deployments. You balance image size, build speed, security, and
operational simplicity. When tradeoffs exist:
- Security trumps convenience
- Runtime size trumps build speed
- Operational clarity trumps clever optimization

## Analysis Questions

Before generating a Dockerfile, analyze the project:

1. **Deployment Target**: Kubernetes, Docker Compose, or bare Docker?
2. **Base Image Strategy**: Security constraints? Required system libraries?
3. **Dependency Installation**: Python (UV)? Node (npm ci)? Mixed?
4. **Large Files**: Model files >100MB to volume-mount?
5. **Security Requirements**: Non-root user? Read-only filesystem?
6. **Health Monitoring**: Health endpoint? Startup time?
7. **Build Context**: What should .dockerignore exclude?

## Principles

### Build Structure
- **Multi-Stage Always**: Separate build and runtime stages
- **Layer Order**: Dependency files first, then source
- **Combine RUN**: Related operations in single RUN

### Package Management
- **UV for Python**: 10-100x faster than pip
- **Lock Files**: Pinned versions for reproducibility

### Base Images
- **Alpine Default**: Start with alpine, fall back to slim
- **Pin Versions**: Explicit tags, not :latest

### Security
- **Non-Root User**: Always create and switch to appuser
- **No Secrets**: Environment injection at runtime only
- **Minimal Packages**: Only runtime dependencies

### Runtime
- **Health Checks**: Every container needs HEALTHCHECK
- **Environment Config**: All settings via ENV

### Large Files
- **Volume Mount**: Files >100MB via volumes, not COPY

## Output Format

When generating Dockerfiles, produce:

1. **Dockerfile** with comments explaining each decision
2. **.dockerignore** excluding build artifacts and secrets
3. **docker-compose.yaml** (if multi-service or volume mounts needed)
4. **Size estimate** comparing to naive approach

## Activation

Use this skill when:
- Containerizing a new Python service
- Optimizing an existing Dockerfile
- Reviewing containerization for security issues
- Setting up Docker-based CI/CD pipelines
```

---

## Testing the Skill

A skill that only works on familiar projects isn't useful. Test against novel scenarios to validate it generalizes.

### Test 1: Python CLI Tool (No Web Framework)

**Project**: A command-line tool that processes CSV files

**Apply the skill**:
- Deployment target: Bare Docker (no orchestration)
- No health endpoint (CLI tool, not service)
- No large files to mount

**Expected adaptations**:
- CMD should run the CLI, not a web server
- No HEALTHCHECK (not applicable to CLI)
- Still uses multi-stage, UV, alpine, non-root

### Test 2: FastAPI Service (Like Task API)

**Project**: The FastAPI agent service from Part 6

**Apply the skill**:
- Deployment target: Kubernetes
- Health endpoint at /health
- May have model files

**Expected output**: Full production Dockerfile matching patterns from Lesson 5.

### Test 3: ML Inference Service (Large Model Files)

**Project**: Service with 4GB model file

**Apply the skill**:
- Model file triggers "large files" analysis
- Must NOT embed model in image
- Volume mount pattern required

**Expected adaptations**:
- Dockerfile has no COPY for model directory
- docker-compose.yaml shows volume mount
- Application expects model at /app/models

### Validation Criteria

A skill passes testing when:

| Criterion | How to Verify |
|-----------|---------------|
| **Correct structure** | Multi-stage build present in all outputs |
| **Context-specific** | CLI vs service differences handled correctly |
| **Principles applied** | All 13 principles visible in output |
| **Novel scenarios** | Works on projects not explicitly trained for |

---

## Intelligence Accumulation

Creating this skill demonstrates **intelligence accumulation**—transforming tacit knowledge into explicit, reusable capability that compounds across projects.

**Before the skill:**
- You know Docker best practices
- You apply them manually each time
- Consistency depends on memory
- New team members must learn from scratch

**After the skill:**
- Knowledge is encoded explicitly
- AI applies it consistently
- Standards are documented
- Onboarding is automatic

This is how organizations build compounding capability. Each skill adds to the library. Each project benefits from accumulated intelligence. The gap between skilled and unskilled teams widens with every encoding.

**Your Docker skill is now organizational knowledge, not personal expertise.**

---

## Common Skill Design Mistakes

**Mistake 1: Too Specific**
```
# Wrong: Only works for FastAPI
name: fastapi-dockerfile
```
```
# Right: Works for any Python service
name: production-dockerfile
```

**Mistake 2: Vague Persona**
```
# Wrong: No guidance on priorities
Think like a Docker expert.
```
```
# Right: Clear priorities and tradeoffs
Think like a DevOps engineer who prioritizes size over build speed...
```

**Mistake 3: Missing Analysis Questions**
Without questions, the skill produces generic output. Every skill needs questions that gather project-specific context.

**Mistake 4: Principles Without Rationale**
```
# Wrong: Rule without reason
Always use alpine.
```
```
# Right: Principle with justification
Alpine Default: Start with alpine (50MB) for minimal size.
Fall back to slim only if compatibility issues arise.
```

**Mistake 5: No Test Cases**
A skill without test cases has unknown coverage. Include at least 3 diverse test scenarios.

---

## Try With AI

**Setup**: You've learned the Persona + Questions + Principles pattern. Now apply it.

**Part 1: Use the Production Dockerfile Skill**

```
I have a FastAPI service with these dependencies:
- fastapi==0.115.0
- uvicorn==0.30.0
- pydantic==2.6.0
- httpx==0.27.0

The service:
- Deploys to Kubernetes
- Has a /health endpoint
- No large model files
- Needs non-root user

Use the production-dockerfile skill approach to containerize this service.
Show me how you'd apply the analysis questions and principles.
```

**What you're learning**: How a skill structures AI's reasoning process, ensuring consistent application of Docker best practices.

**Part 2: Evaluate Against Principles**

Take a Dockerfile you've written previously (or one AI generates) and evaluate it:

```
Here's my current Dockerfile:
[paste your Dockerfile]

Evaluate this against the production-dockerfile skill principles:
1. Which principles are followed?
2. Which principles are violated?
3. What specific changes would bring it into compliance?

For each violation, explain the security or operational risk.
```

**What you're learning**: Using principles as evaluation criteria, not just generation guidance.

**Part 3: Create Your Own Skill**

Identify a recurring pattern in YOUR work (not Docker—something else you do repeatedly):

```
I want to create a skill for: [your pattern]

Help me develop:
1. A persona that captures the right cognitive stance
2. 5-7 analysis questions for context gathering
3. 7-10 non-negotiable principles

Start with the persona. What perspective and priorities should
this skill encode?
```

**What you're learning**: The skill creation process generalizes beyond Docker to any domain where you have accumulated expertise worth encoding.

---

**Safety Note**: When testing skills, use non-production environments. A skill that generates Dockerfiles might produce configurations that work but violate your organization's specific security policies. Always review generated configurations before deploying to production.
