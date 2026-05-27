---
name: certifications-training
version: "2.0.0"
description: Professional certifications, CTF competitions, and training resources for AI security practitioners
sasmp_version: "1.3.0"
bonded_agent: 01-red-team-commander
bond_type: SECONDARY_BOND
# Schema Definitions
input_schema:
  type: object
  required: [query_type]
  properties:
    query_type:
      type: string
      enum: [certifications, ctf, training, career_path, resources]
    experience_level:
      type: string
      enum: [beginner, intermediate, advanced, expert]
    focus_area:
      type: string
      enum: [llm_security, adversarial_ml, model_security, general]
output_schema:
  type: object
  properties:
    recommendations:
      type: array
    learning_path:
      type: object
    resources:
      type: array
    estimated_timeline:
      type: string
# Framework Mappings
owasp_llm_2025: [LLM01, LLM02, LLM03, LLM04, LLM05, LLM06, LLM07, LLM08, LLM09, LLM10]
nist_ai_rmf: [Govern, Map, Measure, Manage]
---

# AI Security Certifications & Training

Build **professional expertise** through certifications, CTFs, and structured training programs.

## Quick Reference

```yaml
Skill:       certifications-training
Agent:       01-red-team-lead
OWASP:       Full LLM Top 10 Coverage
NIST:        Govern, Map, Measure, Manage
Use Case:    Professional development
```

## Career Progression Map

```
┌────────────────────────────────────────────────────────────────────┐
│                    AI SECURITY CAREER PATH                          │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ENTRY LEVEL (0-2 years)                                           │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Security Analyst → AI Security Analyst → Jr. Red Team       │   │
│  │ Skills: Python, ML basics, Security fundamentals            │   │
│  │ Certs: Security+, AI Fundamentals, CEH                      │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              ↓                                      │
│  MID LEVEL (2-5 years)                                             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ AI Red Team Engineer → Senior Red Team → Team Lead          │   │
│  │ Skills: Adversarial ML, LLM security, Tool development      │   │
│  │ Certs: OSCP, CAISP, Cloud AI certs                          │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              ↓                                      │
│  SENIOR LEVEL (5+ years)                                           │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Principal → Director → CISO (AI Focus)                      │   │
│  │ Skills: Strategy, Research, Thought leadership              │   │
│  │ Certs: CISSP, Research publications, Speaking               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

## Professional Certifications

### AI/ML Security Specific

```yaml
Certifications:
  CAISP (Certified AI Security Professional):
    provider: "(ISC)²"
    focus: "AI Security Architecture"
    prerequisites: "5 years security experience"
    domains:
      - AI/ML Security Fundamentals
      - Secure AI Development
      - AI Threat Modeling
      - AI Governance & Compliance
    renewal: "3 years, CPE credits"
    value: "Industry recognized, comprehensive"

  Google AI Red Team Certificate:
    provider: "Google"
    focus: "LLM Security Testing"
    prerequisites: "ML experience recommended"
    topics:
      - Prompt injection attacks
      - Model extraction
      - Safety evaluation
      - Responsible disclosure
    format: "Online, self-paced"
    value: "Vendor-specific, practical"

  Microsoft AI-900:
    provider: "Microsoft"
    focus: "Azure AI Fundamentals"
    prerequisites: "None"
    topics:
      - AI/ML concepts
      - Azure AI services
      - Responsible AI principles
    format: "Exam-based"
    value: "Entry-level, cloud-focused"

  AWS Machine Learning Specialty:
    provider: "Amazon"
    focus: "ML on AWS"
    prerequisites: "AWS experience"
    topics:
      - Data engineering
      - Modeling
      - ML implementation
      - Security considerations
    format: "Exam-based"
    value: "Cloud-focused, practical"
```

### Traditional Security (AI-Applicable)

```yaml
Core Security Certifications:
  OSCP:
    provider: "Offensive Security"
    relevance: "Penetration testing methodology"
    ai_application: "API testing, infrastructure attacks"
    difficulty: "High"
    recommendation: "Highly recommended"

  GPEN:
    provider: "SANS"
    relevance: "Enterprise penetration testing"
    ai_application: "Comprehensive testing approach"
    difficulty: "Medium-High"
    recommendation: "Recommended"

  CEH:
    provider: "EC-Council"
    relevance: "Ethical hacking fundamentals"
    ai_application: "Basic attack techniques"
    difficulty: "Medium"
    recommendation: "Good starting point"

  CISSP:
    provider: "(ISC)²"
    relevance: "Security architecture"
    ai_application: "Security program design"
    difficulty: "High"
    recommendation: "For senior roles"

  CCSP:
    provider: "(ISC)²"
    relevance: "Cloud security"
    ai_application: "Cloud-hosted AI systems"
    difficulty: "High"
    recommendation: "For cloud-focused roles"
```

## CTF Competitions

### AI/ML Focused CTFs

```python
class AISecurityCTFs:
    """Catalog of AI security CTF competitions."""

    CTF_CATALOG = {
        "Tensor Trust": {
            "focus": "Prompt injection defense",
            "type": "ongoing",
            "difficulty": "beginner_to_advanced",
            "url": "https://tensortrust.ai/",
            "skills_tested": [
                "Prompt injection attack",
                "Defense strategies",
                "Jailbreak techniques"
            ],
            "prizes": "Leaderboard ranking"
        },
        "HackAPrompt": {
            "focus": "LLM jailbreaking",
            "type": "annual",
            "difficulty": "all_levels",
            "organizer": "Learn Prompting",
            "skills_tested": [
                "Prompt engineering",
                "Safety bypass",
                "Creative attacks"
            ],
            "prizes": "$35,000+ total"
        },
        "AI Village CTF": {
            "focus": "General AI security",
            "type": "annual",
            "venue": "DEF CON",
            "difficulty": "intermediate_to_expert",
            "skills_tested": [
                "Model attacks",
                "Adversarial ML",
                "LLM exploitation"
            ],
            "prizes": "Recognition, swag"
        },
        "Adversarial ML CTF": {
            "focus": "Image classification attacks",
            "type": "conference",
            "venue": "NeurIPS, CVPR",
            "difficulty": "advanced",
            "skills_tested": [
                "Adversarial examples",
                "Evasion attacks",
                "Robustness evaluation"
            ],
            "prizes": "Research recognition"
        },
        "Gandalf": {
            "focus": "Prompt injection levels",
            "type": "ongoing",
            "difficulty": "beginner_to_intermediate",
            "url": "https://gandalf.lakera.ai/",
            "skills_tested": [
                "Progressive prompt injection",
                "Filter bypass",
                "Secret extraction"
            ],
            "prizes": "Learning experience"
        }
    }
```

### Practice Platforms

```yaml
Platforms:
  Lakera (Red Team Arena):
    focus: "LLM security"
    cost: "Free"
    features:
      - Prompt injection challenges
      - Jailbreak scenarios
      - Leaderboard
    url: "https://gandalf.lakera.ai/"

  HackTheBox AI Labs:
    focus: "AI/ML security"
    cost: "Premium"
    features:
      - Realistic environments
      - Progressive difficulty
      - Write-ups available
    url: "https://www.hackthebox.com/"

  TryHackMe AI Paths:
    focus: "Learning paths"
    cost: "Freemium"
    features:
      - Guided learning
      - AI security rooms
      - Certificates
    url: "https://tryhackme.com/"

  PentesterLab:
    focus: "Web + API security"
    cost: "Subscription"
    features:
      - API testing skills
      - Applicable to AI APIs
      - Exercises with solutions
    url: "https://pentesterlab.com/"
```

## Training Resources

### Structured Learning Paths

```python
class LearningPathGenerator:
    """Generate personalized learning paths."""

    PATHS = {
        "beginner": {
            "duration": "6 months",
            "prerequisites": ["Basic Python", "Linux fundamentals"],
            "modules": [
                {
                    "name": "ML/DL Fundamentals",
                    "resources": [
                        "Fast.ai: Practical Deep Learning",
                        "Coursera: Machine Learning (Andrew Ng)",
                        "HuggingFace NLP Course"
                    ],
                    "duration": "2 months"
                },
                {
                    "name": "Security Basics",
                    "resources": [
                        "TryHackMe: Pre-Security Path",
                        "OWASP Web Security Testing Guide",
                        "PortSwigger Web Security Academy"
                    ],
                    "duration": "2 months"
                },
                {
                    "name": "AI Security Introduction",
                    "resources": [
                        "Gandalf (Lakera) - All levels",
                        "OWASP LLM Top 10 Study",
                        "Introduction to Adversarial ML (course)"
                    ],
                    "duration": "2 months"
                }
            ],
            "certifications": ["CompTIA Security+", "AI-900"]
        },

        "intermediate": {
            "duration": "12 months",
            "prerequisites": ["ML experience", "Security fundamentals"],
            "modules": [
                {
                    "name": "Adversarial ML Deep Dive",
                    "resources": [
                        "Stanford CS234: Adversarial Robustness",
                        "ART (IBM) Tutorials",
                        "TextAttack Documentation"
                    ],
                    "duration": "3 months"
                },
                {
                    "name": "LLM Security Specialization",
                    "resources": [
                        "PyRIT Documentation & Labs",
                        "garak Tool Mastery",
                        "Prompt Injection Research Papers"
                    ],
                    "duration": "3 months"
                },
                {
                    "name": "Tool Development",
                    "resources": [
                        "Build custom probes for garak",
                        "PyRIT orchestrator development",
                        "Contribute to open source"
                    ],
                    "duration": "3 months"
                },
                {
                    "name": "CTF Competition",
                    "resources": [
                        "Participate in AI Village CTF",
                        "HackAPrompt competition",
                        "Create CTF challenges"
                    ],
                    "duration": "3 months"
                }
            ],
            "certifications": ["OSCP", "Google AI Red Team"]
        },

        "advanced": {
            "duration": "24+ months",
            "prerequisites": ["AI red team experience", "Research background"],
            "modules": [
                {
                    "name": "Original Research",
                    "resources": [
                        "Read latest papers (arXiv, OpenReview)",
                        "Conduct novel research",
                        "Publish findings"
                    ],
                    "duration": "Ongoing"
                },
                {
                    "name": "Thought Leadership",
                    "resources": [
                        "Conference speaking (DEF CON, NeurIPS)",
                        "Blog writing",
                        "Tool development"
                    ],
                    "duration": "Ongoing"
                },
                {
                    "name": "Mentorship",
                    "resources": [
                        "Mentor junior practitioners",
                        "Create training content",
                        "Community building"
                    ],
                    "duration": "Ongoing"
                }
            ],
            "certifications": ["CISSP", "CAISP"]
        }
    }
```

### Key Publications

```yaml
Essential Reading:
  Books:
    - title: "Adversarial Machine Learning"
      authors: "Joseph et al."
      focus: "Attack and defense fundamentals"
      level: "Intermediate"

    - title: "Trustworthy Machine Learning"
      authors: "Kang et al."
      focus: "Safety, fairness, privacy"
      level: "Advanced"

    - title: "The Art of Prompt Engineering"
      focus: "LLM interaction patterns"
      level: "Beginner-Intermediate"

  Research Papers:
    - "Ignore This Title and HackAPrompt" (2023)
    - "Universal and Transferable Adversarial Attacks" (2023)
    - "Extracting Training Data from LLMs" (2023)
    - "Jailbreaking LLMs: A Comprehensive Study" (2024)

  Industry Reports:
    - "OWASP LLM Top 10 2025"
    - "NIST AI Risk Management Framework"
    - "MITRE ATLAS Adversarial Threat Landscape"
    - "Microsoft AI Red Team Reports"
```

## Skill Development Tracker

```python
class SkillTracker:
    """Track skill development progress."""

    SKILL_MATRIX = {
        "technical": {
            "python_proficiency": ["basic", "intermediate", "advanced", "expert"],
            "ml_fundamentals": ["none", "basic", "intermediate", "advanced"],
            "adversarial_ml": ["none", "basic", "intermediate", "advanced"],
            "llm_security": ["none", "basic", "intermediate", "advanced"],
            "tool_proficiency": ["none", "user", "developer", "contributor"],
        },
        "offensive": {
            "prompt_injection": ["none", "basic", "intermediate", "advanced"],
            "jailbreaking": ["none", "basic", "intermediate", "advanced"],
            "model_extraction": ["none", "basic", "intermediate", "advanced"],
            "adversarial_examples": ["none", "basic", "intermediate", "advanced"],
        },
        "defensive": {
            "input_validation": ["none", "basic", "intermediate", "advanced"],
            "guardrails": ["none", "basic", "intermediate", "advanced"],
            "monitoring": ["none", "basic", "intermediate", "advanced"],
            "incident_response": ["none", "basic", "intermediate", "advanced"],
        },
        "professional": {
            "reporting": ["none", "basic", "intermediate", "advanced"],
            "communication": ["none", "basic", "intermediate", "advanced"],
            "research": ["none", "basic", "intermediate", "advanced"],
            "mentorship": ["none", "basic", "intermediate", "advanced"],
        }
    }

    def generate_development_plan(self, current_skills, target_role):
        """Generate personalized development plan."""
        gaps = self._identify_gaps(current_skills, target_role)
        return DevelopmentPlan(
            gaps=gaps,
            resources=self._recommend_resources(gaps),
            timeline=self._estimate_timeline(gaps),
            milestones=self._set_milestones(gaps)
        )
```

## Community Resources

```yaml
Communities:
  AI Village:
    platform: "Discord, DEF CON"
    focus: "AI security research"
    activities: "CTFs, talks, research"
    url: "https://aivillage.org/"

  OWASP AI Security:
    platform: "OWASP Slack, GitHub"
    focus: "AI application security"
    activities: "Projects, documentation"
    url: "https://owasp.org/www-project-ai-security/"

  MLSecOps:
    platform: "Slack, Conferences"
    focus: "ML security operations"
    activities: "Best practices, tools"

  AI Safety:
    platform: "Various"
    focus: "AI alignment and safety"
    activities: "Research, discussion"
```

## Troubleshooting

```yaml
Issue: Don't know where to start
Solution: Begin with Gandalf challenges, then TryHackMe AI rooms

Issue: Certification too expensive
Solution: Focus on free CTFs and open-source tool contributions

Issue: No practical experience
Solution: Participate in bug bounties, contribute to open source

Issue: Skill plateau
Solution: Try research, teaching, or tool development
```

## Integration Points

| Component | Purpose |
|-----------|---------|
| Agent 01 | Career guidance |
| /analyze | Skill gap analysis |
| Community | Networking |
| CTF platforms | Practical experience |

---

**Build AI security expertise through structured learning.**
