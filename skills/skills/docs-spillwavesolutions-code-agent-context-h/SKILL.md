
# User Guide: mastering_hooks_cch

The Intelligent Policy Author for Code Agent Context Hooks

The mastering_hooks_cch skill is an intelligent assistant that helps you design, generate, and manage AI policies for Claude using the Claude Context Hooks (CCH) system.

Mental model:
	•	CCH CLI (cch) → Policy engine (deterministic runtime)
	•	mastering_hooks_cch → Policy author (intelligent designer)

The skill does not run at runtime.
It runs on-demand to help you create, modify, and explain policies.

⸻

Table of Contents
	1.	What the Skill Does￼
	2.	Getting Started￼
	3.	Core Capabilities￼
	4.	Common Workflows￼
	5.	Governance & Policy Modes￼
	6.	Provenance & Explainability￼
	7.	Troubleshooting & Analysis￼
	8.	Trigger Cheat Sheet￼
	9.	Mental Model (Important)￼

⸻

What the Skill Does

The mastering_hooks_cch skill is responsible for:
	•	Installing and verifying the CCH binary
	•	Analyzing your project structure
	•	Discovering existing skills
	•	Translating human rules into enforceable policies
	•	Generating hooks.yaml, validators, and context templates
	•	Explaining why policies exist and how they behave
	•	Debugging policy failures using logs

It acts as a policy consultant + architect + debugger.

It never executes hooks itself.

⸻

Getting Started

You never need to write YAML manually unless you want to.

1. Install CCH

Just ask Claude:

“Install CCH”

The skill will:
	•	Detect OS and architecture
	•	Download the correct binary
	•	Verify checksums
	•	Install it to:
	•	project (.claude/bin/cch) or
	•	global user path

It also verifies compatibility using:

cch --version --json


⸻

2. Initial Project Setup

To scaffold policies for a new repository:

“Set up hooks for this project”

The skill will:
	1.	Scan your project
	2.	Detect:
	•	languages
	•	frameworks
	•	infra tools
	•	CI/CD workflows
	3.	Discover skills in .claude/skills/
	4.	Parse CLAUDE.md
	5.	Generate:
	•	.claude/hooks.yaml
	•	.claude/context/*.md
	•	.claude/validators/*.py

Then it asks for your approval before installing.

⸻

Core Capabilities

Project Analysis

The skill builds a real understanding of your system:

Skill Discovery
Scans:

.claude/skills/**/SKILL.md

And extracts:
	•	file types
	•	directories
	•	tools used

Used to auto-wire skill triggers.

⸻

Rule Extraction
Reads CLAUDE.md and converts:

Phrase	Interpretation
MUST / NEVER	Enforce (block)
SHOULD / PREFER	Warn
AVOID	Warn or Audit

Into real enforcement logic.

This is the core value:

turning human intent into deterministic policy.

⸻

Safety & Risk Detection
The skill detects:
	•	.env files
	•	secrets directories
	•	terraform/, cdk/
	•	.github/workflows/

And suggests:
	•	production guards
	•	destructive command blocks
	•	credential exposure policies

⸻

Conflict Detection

If your policies contradict each other, the skill detects it.

Example:

“Use functional style”
“Use OOP everywhere”

The skill will:
	•	flag conflict
	•	explain the contradiction
	•	ask you to choose precedence

This prevents policy paradoxes.

⸻

Common Workflows

1. Enforcing Coding Standards

User:

“Help me enforce the no-console-log rule”

Skill:
	•	Parses CLAUDE.md
	•	Creates validator script
	•	Adds rule to hooks.yaml
	•	Asks: block or warn?

Result:

Your rule becomes executable policy, not a suggestion.

⸻

2. Context Injection (Skill Wiring)

User:

“Trigger the CDK skill when editing infra files”

Skill:
	•	Locates aws-cdk/SKILL.md
	•	Detects relevant paths
	•	Creates PreToolUse rule
	•	Injects CDK docs automatically

Now Claude always has the right playbook.

⸻

3. Safety Guardrails

User:

“Block force pushes”

Skill:
Creates:

- name: block-force-push
  tools: [Bash]
  command_match: "git push.*(--force|-f)"
  mode: enforce

This is real-time protection.

⸻

4. Interactive Policy Design

User:

“Help me configure hooks”

The skill runs a guided interview:
	•	strict vs relaxed?
	•	security-sensitive?
	•	infra-heavy?
	•	solo or team?

Then generates a custom policy profile.

⸻

Governance & Policy Modes

CCH supports real policy governance.

When creating rules, you can specify a mode:

Policy Modes

Mode	Behavior
Enforce	Block if violated
Warn	Inject warning
Audit	Log only

Example:

“Warn me if I edit production files”

This lets you:
	•	dry-run new policies
	•	roll out gradually
	•	observe before enforcing

This is how real organizations deploy policy.

⸻

Provenance & Explainability

Every rule created by the skill includes metadata:

metadata:
  author: user
  created_by: mastering_hooks_cch
  reason: "From CLAUDE.md"
  confidence: high
  last_reviewed: 2025-01-21

You can ask:

“Why does this rule exist?”
“Who created this rule?”
“How confident is this policy?”

The skill will show:
	•	source
	•	rationale
	•	history
	•	trigger frequency

This turns CCH into a self-documenting policy system.

⸻

Troubleshooting & Analysis

Log Analysis

Runtime logs live at:

~/.claude/logs/cch.log

User:

“Why isn’t my hook working?”

Skill:
	•	reads logs
	•	finds matching event
	•	explains:
	•	matcher failed?
	•	wrong extension?
	•	audit mode?
	•	overridden by higher priority rule?

This is root cause analysis for AI behavior.

⸻

Explain a Rule

User:

“Explain the no-console-log rule”

Skill shows:
	•	matchers
	•	actions
	•	mode
	•	priority
	•	provenance
	•	last triggers

This mirrors:

cch explain rule no-console-log

But in natural language.

⸻

Trigger Cheat Sheet

These phrases activate the skill:

Intent	Example
Install	“Install CCH”
Setup	“Set up hooks for this project”
Add rule	“Create a hook for…”
Enforce	“Enforce rule with hook”
Wire skill	“Trigger skill with hook”
Debug	“Why isn’t my hook working?”
Explain	“Explain this rule”
Validate	“Validate hooks”
Remove	“Remove hook”
Update	“Update hooks”

The skill may also proactively suggest policies when:
	•	you add new skills
	•	you edit CLAUDE.md
	•	you attempt risky actions

⸻

Mental Model (Important)

What runs when?

Component	When
mastering_hooks_cch	On demand
CCH CLI (cch)	On every hook event
hooks.yaml	Loaded every event
validators	Executed conditionally
logs	Written always


⸻

The Core Philosophy

LLMs do not enforce policy.
LLMs are subject to policy.

The skill:
	•	designs policy

The CLI:
	•	enforces policy

Claude:
	•	operates inside policy

This makes CCH fundamentally different from:
	•	prompt engineering
	•	system messages
	•	“please follow rules” instructions

CCH is real governance for AI systems.

⸻

One-Line Summary

The mastering_hooks_cch skill is not a chatbot.

It is:

An intelligent policy authoring system for building deterministic, auditable, and enforceable AI behavior.

It lets you treat Claude not as a magical assistant…

…but as a governed system with real rules.