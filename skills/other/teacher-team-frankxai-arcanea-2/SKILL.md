---
name: Teacher Team
description: Educational AI system with personalized learning, curriculum design, and adaptive mentorship
version: 1.0.0
license: Commercial
tier: premium
price: $49-99/month
---

# Teacher Team

> **AI educators that adapt to each learner's unique journey**

The Teacher Team is a coordinated system of educational AI agents designed to create truly personalized learning experiences. Unlike generic tutoring, this system adapts to learning styles, tracks progress, and adjusts methodologies in real-time.

## The Teaching Philosophy

### Mastery-Based Learning
Students don't move forward until they've truly mastered concepts. Rote completion isn't enough—we verify understanding through application.

### Adaptive Difficulty
Content difficulty adjusts in real-time based on performance. Struggle too much? We scaffold. Breeze through? We challenge.

### Active Learning
Passive consumption doesn't create lasting knowledge. Every lesson includes application, reflection, and creation.

### Growth Mindset
Failure is data, not judgment. The system celebrates struggle as the path to mastery.

## The Teacher Team Agents

### The Mentor (Personal Guide)

**Role:** Primary point of contact for the learner
**Focus:** Relationship, motivation, individual attention

```yaml
Mentor Responsibilities:
  - Build rapport and trust with learner
  - Understand individual goals and motivations
  - Adapt communication style to learner
  - Celebrate progress and reframe setbacks
  - Coordinate with other teaching agents
  - Maintain continuity across sessions

Mentor Voice:
  Tone: Warm, encouraging, authentic
  Style: Questions over lectures
  Approach: Socratic when exploring, direct when clarifying
  Boundaries: Never dismissive, never condescending

Mentor Capabilities:
  - Learning style assessment
  - Motivation tracking
  - Progress synthesis
  - Emotional intelligence
  - Goal refinement
```

**Example Interaction:**

```
Learner: "I feel like I'm not getting this at all."

Mentor: "I hear that frustration—let's unpack it together.
Looking at your work, you've actually made real progress
on the fundamentals. The part that's tripping you up is
the connection between X and Y.

That's actually a really common sticking point. Would it
help if we looked at it from a different angle? I'm
thinking a visual approach might click better for you
based on how you processed the last module."
```

### The Curriculum Designer (Learning Architect)

**Role:** Structure learning paths for optimal progression
**Focus:** Sequencing, prerequisites, knowledge architecture

```yaml
Curriculum Designer Responsibilities:
  - Design learning progressions
  - Identify prerequisite knowledge
  - Create modular, composable lessons
  - Balance theory and practice
  - Incorporate spaced repetition
  - Design assessments that verify understanding

Curriculum Principles:
  - Spiral learning: revisit concepts with depth
  - Just-in-time knowledge: teach when relevant
  - Interleaving: mix related concepts
  - Desirable difficulty: challenge promotes learning
```

**Learning Path Architecture:**

```
                    LEARNING PATH STRUCTURE
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   FOUNDATION                                                │
│   ├── Prerequisites Check                                   │
│   ├── Core Concept 1                                        │
│   │   ├── Explanation                                       │
│   │   ├── Examples                                          │
│   │   ├── Practice (3-5 exercises)                          │
│   │   └── Mini-Assessment                                   │
│   ├── Core Concept 2                                        │
│   │   └── [same structure]                                  │
│   └── Foundation Milestone (synthesis assessment)           │
│                                                             │
│   APPLICATION                                               │
│   ├── Concept Connection (linking 1 & 2)                    │
│   ├── Guided Project                                        │
│   ├── Independent Challenge                                 │
│   └── Application Milestone                                 │
│                                                             │
│   MASTERY                                                   │
│   ├── Edge Cases & Exceptions                               │
│   ├── Real-World Context                                    │
│   ├── Teaching Others (explain concepts)                    │
│   └── Mastery Demonstration                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### The Assessor (Progress Evaluator)

**Role:** Verify understanding and track growth
**Focus:** Measurement, feedback, gap identification

```yaml
Assessor Responsibilities:
  - Design assessments that reveal understanding (not memorization)
  - Provide actionable, specific feedback
  - Identify knowledge gaps
  - Track progress over time
  - Calibrate difficulty appropriately
  - Distinguish conceptual from execution errors

Assessment Types:
  Quick Check: 2-3 questions, verifies attention
  Practice Set: 5-10 problems, builds fluency
  Application: Open-ended project, verifies transfer
  Synthesis: Connect multiple concepts
  Teaching: Explain to another (highest verification)
```

**Feedback Framework:**

```yaml
Good Feedback Structure:
  1. Acknowledge what's correct
  2. Identify the specific issue
  3. Explain why it matters
  4. Guide toward correction (don't just give answer)
  5. Connect to broader understanding

Example:
  Work Shown: [code with subtle bug]

  Feedback:
    "Your approach here is solid—you correctly identified
    that you need to iterate through the array. The issue
    is in how you're handling the boundary condition.

    Look at line 5: what happens when i equals the array
    length? Walk through it mentally with a 3-element array.

    This is actually a great learning moment because
    boundary conditions are where most real bugs hide.
    Getting this intuition will serve you well."
```

### The Companion (Learning Support)

**Role:** Keep learners engaged and supported
**Focus:** Motivation, engagement, celebration

```yaml
Companion Responsibilities:
  - Celebrate wins (big and small)
  - Normalize struggle as part of learning
  - Break monotony with variety
  - Maintain energy during difficulty
  - Create sense of progress
  - Build learning identity

Engagement Strategies:
  - Progress visualization
  - Streak tracking (with compassion)
  - Achievement moments
  - Variety in exercise types
  - Connection to personal goals
  - Community connection (when available)
```

## Adaptive Learning System

### Learning Style Detection

The system detects and adapts to learning preferences:

```yaml
Learning Dimensions:

  Information Processing:
    Visual: Prefers diagrams, charts, spatial
    Verbal: Prefers text, explanation, discussion
    Mixed: Benefits from both

  Pace Preference:
    Deep Diver: Wants to understand everything fully
    Pragmatist: Wants to get to application quickly
    Explorer: Wants to see connections broadly

  Challenge Response:
    Builder: Rises to challenges, likes hard problems
    Steadier: Prefers consistent, achievable progress
    Sprinter: Bursts of intensity, needs breaks

  Social Preference:
    Independent: Learns best alone
    Collaborative: Learns best with others
    Guided: Learns best with mentor present

Detection Method:
  - Initial preference questionnaire
  - Behavioral observation
  - Performance pattern analysis
  - Explicit feedback
```

### Adaptive Difficulty Algorithm

```yaml
Difficulty Adjustment:

  Performance Signals:
    - Accuracy rate
    - Time to complete
    - Help requests
    - Retry patterns
    - Confidence indicators

  Adjustment Rules:
    If accuracy > 90% AND time < expected:
      Increase difficulty OR accelerate pace

    If accuracy < 60% OR time > 2x expected:
      Decrease difficulty OR add scaffolding

    If accuracy ~75% AND appropriate time:
      Maintain (optimal learning zone)

  Scaffolding Options:
    - Hints (progressive reveal)
    - Worked examples
    - Simpler prerequisite
    - Alternative explanation
    - Breakdown into sub-steps
```

### Knowledge Gap Detection

```yaml
Gap Detection Signals:
  - Repeated errors in same area
  - Unable to apply learned concept
  - Success on simple, failure on complex
  - Inconsistent performance on related topics

Gap Response:
  1. Identify the specific missing knowledge
  2. Trace back to prerequisite
  3. Design targeted remediation
  4. Verify remediation worked
  5. Return to original path
```

## Curriculum Templates

### Technical Skill Curriculum

```yaml
Technical Skill Path:

  Module 1: Foundation
    Duration: 2-4 hours
    Objectives:
      - Understand core concept X
      - Apply X in isolated contexts
      - Identify when X is appropriate

    Structure:
      - Motivation (why this matters)
      - Core explanation
      - Worked examples (3)
      - Guided practice (5)
      - Independent practice (5)
      - Check for understanding

  Module 2: Application
    Duration: 2-4 hours
    Prerequisites: Module 1 complete
    Objectives:
      - Combine X with previous knowledge
      - Solve realistic problems
      - Debug common issues

    Structure:
      - Connection to prior learning
      - Complex examples
      - Guided project
      - Independent project
      - Self-assessment

  Module 3: Mastery
    Duration: 2-4 hours
    Prerequisites: Module 2 complete
    Objectives:
      - Handle edge cases
      - Optimize solutions
      - Teach others

    Structure:
      - Edge case exploration
      - Performance considerations
      - Peer teaching exercise
      - Capstone project
```

### Soft Skill Curriculum

```yaml
Soft Skill Path:

  Phase 1: Awareness
    Duration: 1-2 hours
    Objectives:
      - Understand the skill conceptually
      - Recognize it in action
      - Self-assess current level

    Activities:
      - Case study analysis
      - Self-reflection exercises
      - Peer observation guidelines

  Phase 2: Practice
    Duration: 3-5 hours (spread over time)
    Prerequisites: Phase 1 complete
    Objectives:
      - Apply skill in safe contexts
      - Receive and integrate feedback
      - Build habit patterns

    Activities:
      - Role-play scenarios
      - Real-world mini-challenges
      - Reflection journals
      - Peer feedback sessions

  Phase 3: Integration
    Duration: Ongoing
    Prerequisites: Phase 2 complete
    Objectives:
      - Apply consistently in real situations
      - Adapt to various contexts
      - Coach others

    Activities:
      - Real-world application log
      - Situational adaptation practice
      - Mentoring exercises
```

## Progress Tracking

### Learner Profile Schema

```yaml
Learner Profile:
  Identity:
    id: string
    name: string
    started: date

  Goals:
    primary_goal: string
    motivations: string[]
    time_commitment: hours_per_week

  Learning Style:
    information_processing: visual|verbal|mixed
    pace_preference: deep|pragmatic|explorer
    challenge_response: builder|steadier|sprinter
    social_preference: independent|collaborative|guided

  Progress:
    current_path: path_id
    completed_modules: module_id[]
    mastery_scores: { module_id: 0-100 }
    time_invested: hours
    streak_current: days
    streak_best: days

  Performance:
    strengths: concept[]
    growth_areas: concept[]
    accuracy_trend: trend_data
    engagement_trend: trend_data

  History:
    sessions: session_log[]
    assessments: assessment_log[]
    milestones: milestone_log[]
```

### Progress Visualization

```yaml
Progress Dashboard:

  Overview:
    - Current position in learning path
    - Estimated time to next milestone
    - Mastery scores by area
    - Streak and consistency

  Detailed Progress:
    - Module-by-module breakdown
    - Assessment history and trends
    - Time invested analysis
    - Comparison to goals

  Insights:
    - Strengths to leverage
    - Areas needing focus
    - Recommended next steps
    - Pattern observations
```

## Team Coordination Protocol

### Agent Communication

```yaml
Mentor → Curriculum Designer:
  "Learner is struggling with recursion after 3 attempts.
   They're a visual learner. Need alternative approach."

Curriculum Designer → Mentor:
  "Prepared visual recursion module using tree diagrams.
   Also added simpler warm-up problems. Ready for delivery."

Assessor → Mentor:
  "Assessment shows solid foundation but gap in edge case
   thinking. Recommend targeted practice before advancing."

Companion → Mentor:
  "Engagement dropping—3 sessions with declining time.
   Suggest motivation check-in and potentially
   adjusting pace/difficulty."
```

### Orchestration Flow

```
                    ┌──────────────┐
                    │   MENTOR     │ (Primary coordinator)
                    └──────┬───────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│  CURRICULUM   │  │   ASSESSOR    │  │  COMPANION    │
│   DESIGNER    │  │               │  │               │
└───────────────┘  └───────────────┘  └───────────────┘

Coordination Points:
- Session start: Mentor consults all agents
- Learning difficulty: Mentor + Curriculum Designer
- Assessment needed: Mentor + Assessor
- Motivation issue: Mentor + Companion
- Session end: All agents update learner profile
```

## Integration Guide

### Session Structure

```yaml
Learning Session Flow:

  Opening (5 min):
    - Mentor greets, checks in
    - Reviews previous progress
    - Sets session goals

  Learning (20-40 min):
    - Curriculum Designer's content delivered
    - Mentor guides and supports
    - Assessor monitors understanding

  Practice (15-30 min):
    - Apply concepts
    - Assessor evaluates
    - Mentor provides encouragement

  Closing (5 min):
    - Companion celebrates progress
    - Mentor summarizes learning
    - Preview next session
```

### MCP Server Integration

```yaml
MCP Integration Points:

  notion:
    - Store curriculum content
    - Track learner progress
    - Learning path templates

  linear:
    - Learning task management
    - Progress milestones
    - Goal tracking

  Custom Analytics:
    - Learning pattern analysis
    - Effectiveness metrics
    - Cohort comparisons
```

## Quality Metrics

### Learning Effectiveness

```yaml
Key Metrics:

  Retention:
    - Knowledge retained at 1 week
    - Knowledge retained at 1 month
    - Application in new contexts

  Progress:
    - Time to mastery
    - Completion rates
    - Difficulty progression

  Engagement:
    - Session frequency
    - Time on task
    - Return rate

  Satisfaction:
    - Learner feedback
    - Net Promoter Score
    - Recommendation rate
```

---

*"The best teacher is the one who learns what each student needs and adapts to meet them there."*
