---
name: writing
description: Grounded prose composition workflow including pre-write queries, consistency checks, and post-write entity extraction for database-backed writing.
---

# Writing Skill

## Purpose

The writing skill supports the author through the actual prose composition process. It ensures writing is grounded in established corpus content, maintains consistency with previous work, and captures new details for future reference.

## Core Workflow

The writing skill follows a strict three-phase workflow:

### Phase 1: Pre-Write Queries

**Before writing any prose**, query the corpus to gather relevant context:

1. **Semantic Search**: Find content related to the scene/section topic
2. **Graph Traversal**: Identify connected characters, locations, themes
3. **Timeline Check**: Verify chronological consistency
4. **Character State**: Retrieve current character knowledge, relationships, locations
5. **World Details**: Get established facts about settings, magic systems, etc.

See `pre-write-query.surql` for query templates.

**Purpose**: Ground the writing in established canon and avoid contradictions.

### Phase 2: Grounded Writing

Write the prose using the queried context:

**Principles**:
- Stay faithful to established character voices
- Honor timeline and continuity
- Use consistent terminology and names
- Reference previously established details naturally
- Flag any new details being introduced

**Style Consistency**:
- Match voice and tone of existing work (see `voice.md`)
- Maintain POV discipline
- Use dialogue patterns consistent with characters (see `dialogue.md`)
- Apply genre conventions appropriately

**Citation Integration**:
- Incorporate research seamlessly (see `citation.md`)
- Attribute ideas appropriately
- Avoid accidental plagiarism

### Phase 3: Post-Write Storage

**After completing prose**, extract and store new information:

1. **Entity Extraction**: Identify new characters, locations, objects, events
2. **Relationship Updates**: Create or modify character relationships
3. **Timeline Additions**: Add events to chronological record
4. **Theme Tracking**: Note thematic elements introduced
5. **Knowledge Updates**: Record character knowledge gains

**Purpose**: Build corpus incrementally so future writing stays consistent.

## Writing Unit Types

### Scene Writing (Fiction)

A scene is a unit of action with:
- **POV Character**: Whose perspective we experience
- **Setting**: Where and when it occurs
- **Goal**: What POV character wants
- **Conflict**: Opposition to the goal
- **Outcome**: Result (usually setback or complication)

**Pre-Write Queries**:
- Character current state and knowledge
- Location details
- Active plot threads
- Relationship dynamics between present characters
- Timeline position

**Post-Write Storage**:
- Character emotional/physical state changes
- New relationship developments
- Timeline event entry
- New location details introduced
- Objects or lore revealed

### Section Writing (Nonfiction)

A section is a unit of argument or instruction with:
- **Main Point**: Core idea being communicated
- **Evidence**: Support for the point
- **Analysis**: How evidence supports point
- **Application**: How reader uses information

**Pre-Write Queries**:
- Previously established arguments
- Sources and citations available
- Examples and case studies in corpus
- Terminology definitions
- Related concepts covered earlier

**Post-Write Storage**:
- New arguments or claims made
- Sources cited
- Examples introduced
- Terminology defined
- Concepts explained

## Consistency Checks

Before finalizing any writing unit, verify:

### Character Consistency
- [ ] Character behavior matches established personality
- [ ] Character knows only what they should know at this point
- [ ] Character relationships reflect current state
- [ ] Character voice matches previous dialogue/thoughts
- [ ] Character location is plausible given timeline

### World Consistency
- [ ] Location details match established descriptions
- [ ] Magic/tech systems work as previously defined
- [ ] Cultural elements align with world-building
- [ ] Historical facts match established timeline
- [ ] Physical laws consistent with genre

### Plot Consistency
- [ ] Events follow logically from previous events
- [ ] Timeline is coherent
- [ ] No contradictions with earlier plot points
- [ ] Foreshadowing and setups honored
- [ ] Stakes and conflicts make sense

### Argument Consistency (Nonfiction)
- [ ] Claims align with thesis
- [ ] Evidence supports claims made
- [ ] No contradictions with earlier arguments
- [ ] Terminology used consistently
- [ ] Citations accurate and complete

## Voice and Style Maintenance

Maintain consistent voice throughout writing:

**Voice Elements**:
- Sentence structure patterns (simple vs. complex)
- Word choice (formal vs. casual, technical vs. accessible)
- Rhythm and pacing
- Use of metaphor and imagery
- Humor and tone

**Techniques**:
1. Query corpus for similar scenes/sections
2. Analyze voice patterns in existing writing
3. Match those patterns in new writing
4. Use comparable title analysis for genre norms
5. Apply author's established style guide

See `voice.md` for detailed guidance.

## Dialogue Craft

Dialogue requires special attention:

**Character Voice Differentiation**:
- Each character should sound distinct
- Consider: education, background, personality, age, culture
- Use speech patterns, vocabulary, rhythm to differentiate

**Dialogue Functions**:
- Reveal character personality
- Advance plot through information exchange
- Create or escalate conflict
- Show relationships through interaction style
- Establish or shift tone

**Technical Craft**:
- Attribution tags ("said" is usually best)
- Action beats to show physicality
- Subtext and what's not said
- Pacing through line length and interruptions

See `dialogue.md` for detailed techniques.

## Managing New Information

When introducing new details:

**Decision Framework**:
1. **Is this detail necessary?** (Avoid info-dumping)
2. **Does it contradict anything?** (Check corpus)
3. **How much should be revealed?** (Progressive disclosure)
4. **Whose perspective reveals it?** (POV-appropriate knowledge)

**Integration Techniques**:
- Show through action rather than exposition
- Reveal through dialogue naturally
- Use sensory details to ground information
- Layer details across multiple scenes/sections

**Storage Protocol**:
- Extract significant new details immediately
- Store with context (who revealed, when, how)
- Link to related entities
- Tag with confidence level if uncertain

## Iteration and Revision

Writing is iterative:

**First Draft Focus**:
- Get story/argument on page
- Maintain momentum
- Flag consistency questions but keep writing
- Capture new details for corpus

**Revision Focus**:
- Query corpus for flagged consistency issues
- Refine voice and style
- Deepen character work
- Strengthen dialogue
- Polish prose

**Corpus Updates**:
- Update entities as characters/arguments evolve
- Revise relationships as story progresses
- Track major revisions that affect continuity

## Genre-Specific Considerations

Different genres require different approaches:

**Mystery/Thriller**:
- Track clues planted and revealed
- Manage information revelation timing
- Maintain suspense through withheld information

**Romance**:
- Track relationship progression milestones
- Maintain emotional authenticity
- Balance internal and external conflict

**Fantasy/Sci-Fi**:
- Consistent magic/tech system application
- World-building detail management
- Balance exposition with action

**Literary Fiction**:
- Deep interiority and character psychology
- Thematic layering
- Prose craft emphasis

**Nonfiction**:
- Argument clarity and logic
- Evidence integration
- Reader engagement and accessibility

## Integration with Other Skills

The writing skill works with:

**Outlining**: Follow outline structure while writing
**Research**: Incorporate researched content
**Editing**: Prepare clean drafts for editing
**Corpus Analysis**: Query and update corpus continuously

## Common Pitfalls

Avoid these mistakes:

**Continuity Errors**:
- Writing without pre-querying corpus
- Forgetting to store new details
- Contradicting established facts

**Voice Inconsistency**:
- Switching tone mid-book
- Character voice drift
- Genre convention violations

**Information Overload**:
- Dumping exposition
- Revealing too much too soon
- Telling instead of showing

**Shallow Writing**:
- Generic character voices
- Thin dialogue
- Telling emotions instead of showing
- Cliché descriptions

## Quality Checklist

Before considering a writing unit complete:

- [ ] Pre-write queries executed and reviewed
- [ ] Writing grounded in established corpus
- [ ] Voice consistent with existing work
- [ ] Dialogue sounds natural and character-specific
- [ ] New details flagged and ready for extraction
- [ ] Consistency checks passed
- [ ] Prose reads smoothly
- [ ] Scene/section achieves its purpose
- [ ] Ready for post-write entity extraction
- [ ] Stored in appropriate manuscript location

## Output Storage

Store completed writing in structured format:

**Manuscript Files**:
- One file per chapter or major section
- Markdown format with metadata headers
- Version control via git
- Clear naming convention

**Corpus Integration**:
- Extract entities and store in database
- Link writing to outline entries
- Connect to research sources
- Tag with themes and plot threads

**Progress Tracking**:
- Update word count stats
- Mark outline sections as drafted
- Track writing velocity
- Note revision needs
