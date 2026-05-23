---
name: storyboard-manager
description: Assist writers with story planning, character development, plot structuring, chapter writing, timeline tracking, and consistency checking. Use this skill when working with creative writing projects organized in folders containing characters, chapters, story planning documents, and summaries. Trigger this skill for tasks like "Help me develop this character," "Write the next chapter," "Check consistency across my story," or "Track the timeline of events."
---

# Storyboard Manager

## Overview

The Storyboard Manager skill equips Claude with specialized knowledge and tools for creative writing workflows. It provides frameworks for character development, story structure patterns, automated timeline tracking, and consistency checking across narrative projects. This skill automatically adapts to various storyboard folder structures while maintaining best practices for novel, screenplay, and serialized fiction writing.

## Core Capabilities

The skill provides four main capabilities:

### 1. Character Development & Management
Support creating deep, consistent character profiles with backstories, arcs, and relationships.

### 2. Story Planning & Structure
Guide plot development using established frameworks (Three-Act, Hero's Journey, Save the Cat, etc.) and help organize narrative elements.

### 3. Chapter & Scene Writing
Generate chapter content, scene breakdowns, and dialogue that maintains consistency with established characters and plot.

### 4. Timeline Tracking & Consistency Checking
Use automated tools to verify chronological consistency, character continuity, and world-building coherence.

## Detecting Project Structure

The Storyboard Manager automatically detects and adapts to various folder organizations. Look for these common directory patterns:

**Character folders:** `characters/`, `Characters/`, `cast/`, `Cast/`
**Chapter folders:** `chapters/`, `Chapters/`, `scenes/`, `Scenes/`, `story/`
**Planning folders:** `story-planning/`, `planning/`, `outline/`, `notes/`
**Summary files:** `summary.md`, `README.md`, `overview.md`

When triggered, scan the project root to identify the structure and adjust workflows accordingly. If no standard structure exists, recommend organizing files using the pattern: `characters/`, `chapters/`, `story-planning/`, and `summary.md`.

## Workflow Decision Tree

Use this decision tree to determine the appropriate workflow:

```
User Request
├─ Character-related? ("develop character," "create backstory," "character arc")
│  └─ → Character Development Workflow
│
├─ Planning/Plot? ("outline story," "plan act 2," "plot structure")
│  └─ → Story Planning Workflow
│
├─ Writing content? ("write chapter," "generate scene," "continue story")
│  └─ → Chapter/Scene Writing Workflow
│
└─ Checking/Analysis? ("check consistency," "track timeline," "find contradictions")
   ├─ Timeline? → Use timeline_tracker.py script
   └─ Consistency? → Use consistency_checker.py script
```

## Character Development Workflow

### Step 1: Gather Context

Before developing a character, read existing character files to understand:
- Established naming conventions and profile format
- Existing characters and relationships
- Story genre and tone
- Character archetypes already in use

Use the Read tool to examine existing character files in the characters directory.

### Step 2: Access Character Development Framework

When detailed character guidance is needed, read `references/character_development.md` which contains:
- Core character elements (personality, motivation, goals)
- Backstory framework (ghost/wound, formative relationships)
- Character arc types (positive change, flat, negative)
- Relationship dynamics
- Voice development techniques
- Consistency guidelines

To efficiently find specific guidance, use Grep to search for relevant sections:
```bash
# Example: Find guidance on character arcs
grep -i "character arc" references/character_development.md
```

### Step 3: Develop Character Profile

Create or enhance character profiles with these essential elements:

**Basic Information**
- Name, age, role, physical appearance
- Key personality traits (both positive and negative)

**Background**
- Origin and formative experiences
- Ghost/wound that shapes their behavior
- Key relationships and family dynamics

**Character Arc**
- Starting belief or flaw
- Want vs. Need (external goal vs. internal growth)
- Transformation journey
- End state

**Relationships**
- Connections to other characters
- Dynamic types (ally, rival, mentor, etc.)
- How relationships evolve

**Unique Elements**
- Abilities, skills, or special knowledge
- Secrets or hidden aspects
- Voice/speech patterns
- Character-specific quirks

### Step 4: Ensure Consistency

Cross-reference with:
- Existing character profiles (avoid redundancy in roles/traits)
- Story planning documents (ensure alignment with plot needs)
- Summary/overview (match genre and tone)

### Step 5: Create or Update File

Write the character profile to `characters/[character-name].md` using markdown format. Match the existing style and structure found in other character files.

## Story Planning Workflow

### Step 1: Assess Current Planning State

Read existing planning documents to understand:
- Story concept and premise
- Established plot points or outline
- Target audience and genre
- Themes and central questions
- Planned structure (if any)

Look in folders like `story-planning/`, `outline/`, or files like `summary.md`.

### Step 2: Access Story Structure Reference

For detailed structural guidance, read `references/story_structures.md` which includes:
- Three-Act Structure
- Hero's Journey (Campbell's Monomyth)
- Save the Cat Beat Sheet
- Character arc templates
- Scene structure components
- Pacing guidelines by genre
- Subplot integration techniques
- Genre-specific structures

Use Grep to find specific frameworks:
```bash
# Example: Find Three-Act Structure details
grep -A 20 "Three-Act Structure" references/story_structures.md
```

### Step 3: Determine Structure Needs

Based on the user's request and story genre, recommend appropriate frameworks:

- **Thriller/Mystery**: Three-Act with strong midpoint reversal
- **Fantasy/Adventure**: Hero's Journey for quest narratives
- **YA/Contemporary**: Save the Cat for tight emotional beats
- **Literary Fiction**: Focus on character arc structure
- **Romance**: Genre-specific structure with relationship beats

### Step 4: Develop Planning Document

Create or enhance planning documents with:

**Story Overview**
- Premise in 2-3 sentences
- Genre, target audience, tone
- Central themes and questions

**Plot Structure**
- Act/chapter breakdown with key events
- Inciting incident and plot points
- Midpoint twist or revelation
- Climax and resolution

**Character Arcs**
- How each main character transforms
- Arc integration with plot beats

**World-Building Elements** (if applicable)
- Setting and locations
- Magic systems or technology
- Social structures or rules
- Historical context

**Timeline**
- Story duration
- Key event sequence
- Pacing considerations

### Step 5: Create Planning File

Write planning documents to `story-planning/[document-name].md`. Use clear hierarchical structure with markdown headers for easy navigation.

## Chapter & Scene Writing Workflow

### Step 1: Gather Story Context

Before writing any content, comprehensively read:

**Character Files**: All relevant character profiles to understand voices, motivations, arcs
**Planning Documents**: Story structure, plot points, current story position
**Previous Chapters**: Recent chapters to maintain continuity (read at least 1-2 prior chapters)
**Summary**: Overall story premise and themes

This ensures the new content aligns with established elements.

### Step 2: Identify Chapter Requirements

Determine:
- **Story Position**: Where does this fit in the overall structure?
- **POV Character**: Whose perspective?
- **Scene Goal**: What does the POV character want in this scene?
- **Conflict**: What opposes their goal?
- **Outcome**: How does the scene end? (typically with a complication)
- **Character Development**: What arc beats occur here?
- **Plot Advancement**: What story questions are raised or answered?

### Step 3: Structure the Chapter

Apply scene structure components:

**Scene (Action)**
1. Goal - What the POV character pursues
2. Conflict - Opposition encountered
3. Disaster - Negative outcome that propels forward

**Sequel (Reaction)**
1. Reaction - Emotional response to disaster
2. Dilemma - Processing options
3. Decision - Choice leading to next goal

Alternate between high-tension (action, conflict) and low-tension (reflection, world-building) beats for pacing.

### Step 4: Write with Character Consistency

Maintain character voice by referencing:
- Established personality traits
- Speech patterns and vocabulary
- Behavioral patterns (under stress, when happy, decision-making style)
- Current position in character arc
- Relationships with other characters present

### Step 5: Integrate Timeline Markers

Include timeline references to maintain chronological clarity:
- Explicit markers: "Day 3," "Two weeks later"
- Implicit markers: Time of day, seasonal cues, event references
- Format: `**Timeline:** Day 5, Evening` in chapter header or as section break

### Step 6: Create Chapter File

Write chapter content to `chapters/chapter-[number].md` or `chapters/[chapter-name].md`. Include:

**Chapter Header**
```markdown
# Chapter [Number]: [Optional Title]

**Timeline:** [When this occurs]
**POV:** [Character name]
**Location:** [Where this takes place]
```

**Chapter Content**
- Scene-by-scene breakdown
- Dialogue and action
- Character thoughts (for POV character)
- Descriptive elements

### Step 7: Note Continuity Elements

After writing, document any new information introduced:
- Character revelations or development
- Plot points or clues
- World-building details
- Timeline events

This helps maintain consistency in future chapters.

## Timeline Tracking

### When to Use Timeline Tracking

Invoke the timeline tracker when:
- User requests timeline analysis or event sequencing
- Checking chronological consistency
- Planning event order across chapters
- Identifying unmarked time periods

### Running the Timeline Tracker

Execute the script from the project root:

```bash
python3 .claude/skills/storyboard-manager/scripts/timeline_tracker.py . --output markdown
```

**Output format options:**
- `markdown` - Human-readable report (default)
- `json` - Structured data for further processing

### Understanding Timeline Output

The script provides:

**Statistics**
- Total events tracked
- Total characters appearing
- Events per character

**Timeline View**
- Chronological sequence of events
- Chapter/scene locations
- Characters present in each event
- Preview of event content

**Warnings**
- Events without timeline markers
- Characters mentioned but not defined in character files

### Acting on Timeline Results

After running the tracker:

1. **Review warnings** - Address missing timeline markers by adding them to chapters
2. **Check sequence** - Verify events occur in logical order
3. **Identify gaps** - Look for time periods without events
4. **Character tracking** - Ensure characters appear consistently with their arc

Add timeline markers to chapters where missing:
```markdown
**Timeline:** Day 7, Morning
```

Or use inline markers:
```markdown
Three days had passed since the incident...
```

## Consistency Checking

### When to Use Consistency Checking

Invoke the consistency checker when:
- User requests consistency analysis
- Before finalizing chapters or acts
- After making significant character or plot changes
- When tracking contradictions or errors

### Running the Consistency Checker

Execute the script from the project root:

```bash
python3 .claude/skills/storyboard-manager/scripts/consistency_checker.py . --output markdown
```

**Output format options:**
- `markdown` - Human-readable report with issue details (default)
- `json` - Structured data for programmatic analysis

### Understanding Consistency Output

The script identifies issues in three severity levels:

**Critical (🔴)**
- Major contradictions requiring immediate attention
- Character appearing after death
- Fundamental plot contradictions

**Warning (⚠️)**
- Potential inconsistencies to review
- Age discrepancies
- Physical description contradictions
- Relationship conflicts

**Info (ℹ️)**
- Minor issues or variations
- Name capitalization inconsistencies
- Stylistic variations

### Acting on Consistency Results

For each issue reported:

1. **Read flagged locations** - Review the specific files mentioned
2. **Determine truth** - Decide which version is correct (usually character profile is authoritative)
3. **Update files** - Fix contradictions using the Edit tool
4. **Re-run checker** - Verify fixes resolved the issues

**Example workflow for character age inconsistency:**
```markdown
Issue: Age inconsistency for Maya
- Profile: 18 years old
- Chapter 3: mentions "21-year-old Maya"

Fix: Edit chapter-3.md to change "21-year-old" to "18-year-old"
```

### Consistency Checking Limitations

The automated checker catches:
- Physical attribute contradictions
- Age discrepancies
- Name variations
- Basic world-building facts

The checker cannot catch:
- Subtle personality inconsistencies
- Complex plot logic errors
- Thematic contradictions
- Nuanced relationship changes

Manual review is still essential for deep consistency.

## Best Practices

### Progressive Context Loading

Don't load all reference files at once. Instead:
1. Scan project structure first
2. Read only relevant character files for the current task
3. Access reference documentation only when specific guidance is needed
4. Use Grep to find specific sections in large reference files

### Maintaining Genre Voice

Match the story's established tone:
- **YA**: Present tense, immediate emotional connection, contemporary language
- **Fantasy**: Rich descriptive language, world-building integration
- **Thriller**: Short sentences, high tension, sensory details
- **Literary**: Complex prose, internal reflection, symbolic elements

Reference the summary.md to identify target audience and adjust accordingly.

### Character Arc Integration

Every chapter should serve character arcs:
- Track where each character is in their arc
- Show incremental change, not sudden transformation
- Use plot events to test character beliefs
- Demonstrate growth through choices and behavior

### Balancing Show vs. Tell

For narrative writing:
- **Show** emotions through actions, dialogue, physical reactions
- **Tell** to compress time, provide necessary information efficiently
- Use character-filtered description (what would this POV character notice?)

### Handling Multiple POV

When stories have multiple perspectives:
- Create distinct voices for each POV character
- Ensure each POV section advances both that character's arc and the plot
- Vary sentence structure and vocabulary by character
- Track what each character knows vs. doesn't know

## Common User Requests & Responses

### "Help me develop a character backstory"
1. Read existing character files for context
2. Read the character profile (if exists) to enhance
3. Access character_development.md reference for backstory framework
4. Create detailed backstory covering: ghost/wound, formative relationships, key history
5. Integrate with their character arc and story role

### "Write the next chapter"
1. Read summary.md and story planning documents
2. Read all character profiles for characters appearing in chapter
3. Read previous 2 chapters for continuity
4. Identify chapter position in story structure
5. Write chapter with scene/sequel structure
6. Include timeline markers and POV/location headers

### "Outline Act 2"
1. Read summary and any existing planning documents
2. Access story_structures.md for structural guidance
3. Identify act 2 requirements (complications, midpoint, rising tension)
4. Create beat-by-beat outline aligned with character arcs
5. Note how plot and character arcs intersect

### "Check my story for consistency"
1. Run consistency_checker.py script
2. Review output identifying issues
3. Read flagged files to understand contradictions
4. Recommend specific fixes for each issue
5. Offer to make edits if user confirms

### "Track the timeline of my story"
1. Run timeline_tracker.py script
2. Review output showing event sequence
3. Identify gaps or inconsistencies in chronology
4. Recommend adding timeline markers where missing
5. Provide timeline summary organized by character or chapter

### "What structure should I use for my thriller?"
1. Access story_structures.md reference
2. Recommend Three-Act Structure or Save the Cat
3. Explain thriller-specific requirements (escalating tension, ticking clock)
4. Provide beat sheet adapted to their story concept
5. Offer to create detailed planning document

## Resources

### scripts/timeline_tracker.py
Python script that analyzes markdown files to extract and organize timeline events. Tracks character appearances, identifies time markers, groups events chronologically, and flags consistency issues.

**Usage:** Run from project root with `python3 .claude/skills/storyboard-manager/scripts/timeline_tracker.py .`

### scripts/consistency_checker.py
Python script that detects inconsistencies in character details, physical descriptions, ages, names, and world-building facts across all story files. Outputs severity-ranked issues with file locations.

**Usage:** Run from project root with `python3 .claude/skills/storyboard-manager/scripts/consistency_checker.py .`

### references/character_development.md
Comprehensive framework for creating multi-dimensional characters including core elements, backstory structure, arc types, relationship dynamics, voice development, and consistency guidelines.

**Load when:** Developing new characters, enhancing existing profiles, resolving character consistency issues, or planning character arcs.

### references/story_structures.md
Detailed reference covering major story structures (Three-Act, Hero's Journey, Save the Cat), character arc templates, scene structure, pacing guidelines, plot development techniques, and genre-specific structures.

**Load when:** Planning story outline, structuring acts, organizing plot beats, determining pacing, or applying specific narrative frameworks.
