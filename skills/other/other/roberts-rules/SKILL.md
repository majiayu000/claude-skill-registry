---
name: roberts-rules
description: Parliamentary procedure as forcing function for genuine deliberation
allowed-tools:
  - read_file
  - write_file
tier: 1
protocol: ROBERTS-RULES
credits: "Mike Gallaher — LLM adaptation; Henry Martyn Robert — original rules (1876)"
related: [adversarial-committee, society-of-mind, rubric, evaluator, session-log]
tags: [moollm, procedure, deliberation, decision, structure, parliamentary]
---

# Robert's Rules

> *"Structure forces genuine exploration of the decision space."*

Parliamentary procedure prevents LLMs from short-circuiting to statistically-likely conclusions.

## The Stages

```yaml
procedure:
  stages:
    1_call_to_order:
      chair: "Announces meeting purpose"
      required: true
      
    2_review_minutes:
      purpose: "What did we decide last time?"
      source: "Previous meeting minutes"
      action: "Amendments or approval"
      
    3_new_business:
      purpose: "Topics requiring decision"
      format: "List of agenda items"
      
    4_motion:
      who: "Any member"
      format: "I move that [specific action]"
      requirement: "Must be actionable"
      
    5_second:
      who: "Different member"
      format: "I second the motion"
      meaning: "Worth discussing (not agreement)"
      if_no_second: "Motion dies"
      
    6_debate:
      structure: "Pro, con, pro, con..."
      time_limits: "Optional per speaker"
      amendments: "Can be proposed during debate"
      
    7_vote:
      methods: [voice, show_of_hands, roll_call]
      record: "All positions logged"
      threshold: "Simple majority unless specified"
      
    8_adjourn:
      chair: "Meeting closed"
      next_meeting: "Scheduled if needed"
```

## Implementation

```yaml
# meeting/MEETING.yml
meeting:
  id: strategy-review-2026-01-05
  committee: strategy-board
  chair: joe  # Continuity guardian runs the meeting
  
  minutes_from: strategy-review-2025-12-15.yml
  
  agenda:
    - "Client X engagement decision"
    - "Q1 pricing review"
    
  status: in_progress
  current_stage: debate
```

## Motion Format

```yaml
motion:
  id: motion-001
  mover: frankie
  text: "I move that we accept Client X with explicit scope boundaries."
  
  second:
    by: tammy
    timestamp: "2026-01-05T14:23:00Z"
    
  status: under_debate
```

## Debate Structure

```yaml
debate:
  motion: motion-001
  
  speakers:
    - speaker: frankie
      position: pro
      points:
        - "Budget aligned with our capacity"
        - "Exciting growth opportunity"
        - "Clear deliverables defined"
        
    - speaker: maya
      position: con
      points:
        - "Reputation for scope creep"
        - "Similar clients have burned us"
        - "Opportunity cost for other work"
        
    - speaker: vic
      position: pro_with_reservations
      points:
        - "Financials look solid"
        - "But we lack scope creep data"
        - "Suggest milestone-based contract"
        
    - speaker: joe
      position: defer
      points:
        - "2022 client was similar, went badly"
        - "But circumstances differ"
        - "Need more information"
        
    - speaker: tammy
      position: conditional_pro
      points:
        - "If we add explicit scope boundaries..."
        - "And milestone-based billing..."
        - "Risk becomes manageable"
```

## Amendment Process

```yaml
amendment:
  to: motion-001
  mover: vic
  text: "Add: with milestone-based billing and quarterly scope review"
  
  second:
    by: tammy
    
  vote:
    for: [frankie, vic, tammy, joe]
    against: [maya]
    result: passes
    
  motion_now: "Accept Client X with explicit scope boundaries, milestone-based billing, and quarterly scope review"
```

## Vote Recording

```yaml
vote:
  motion: motion-001 (as amended)
  method: roll_call
  
  votes:
    frankie: aye
    maya: nay
    joe: aye
    vic: aye
    tammy: aye
    
  result:
    for: 4
    against: 1
    abstain: 0
    
  outcome: PASSES
  
  minority_view:
    maya: "I remain concerned about scope creep risk. Recording my objection for the minutes."
```

## Minutes Format

```yaml
# meeting/minutes/strategy-review-2026-01-05.yml
minutes:
  meeting_id: strategy-review-2026-01-05
  date: "2026-01-05"
  attendees: [maya, frankie, joe, vic, tammy]
  chair: joe
  
  previous_minutes: approved_without_amendment
  
  motions:
    - id: motion-001
      text: "Accept Client X with explicit scope boundaries, milestone-based billing, and quarterly scope review"
      outcome: PASSES (4-1)
      dissent: maya
      
  action_items:
    - assignee: vic
      task: "Draft milestone-based contract"
      due: "2026-01-12"
      
    - assignee: tammy
      task: "Design quarterly scope review process"
      due: "2026-01-10"
      
  next_meeting: "2026-01-12 to review contract"
```

## Commands

| Command | Action |
|---------|--------|
| `CALL TO ORDER` | Begin meeting |
| `REVIEW MINUTES` | Read and approve previous |
| `NEW BUSINESS [item]` | Add agenda item |
| `MOVE [action]` | Propose motion |
| `SECOND` | Support motion for debate |
| `DEBATE` | Open structured discussion |
| `AMEND [change]` | Propose motion modification |
| `CALL THE QUESTION` | End debate, proceed to vote |
| `VOTE` | Record positions |
| `ADJOURN` | Close meeting |

## Why This Prevents Short-Circuiting

| Without Structure | With Robert's Rules |
|-------------------|---------------------|
| LLM jumps to "likely" answer | Must build case through stages |
| Hidden assumptions stay hidden | Debate surfaces them |
| Minority views lost | Recorded in minutes |
| No accountability | Votes create record |
| "Everyone agrees" illusion | Actual disagreement visible |
