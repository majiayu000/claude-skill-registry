---
name: standards-updates-tracker
description: Track changes to standards frameworks over time, identify when standards are revised, analyze impact on existing curriculum, recommend updates, and flag deprecated standards. Use for maintaining current alignment. Activates on "standards updates", "framework revisions", or "standards changes".
---

# Standards: Updates Tracker

Monitor changes to educational standards and manage curriculum updates in response to revisions.

## When to Use

- Standards revision announcements
- Periodic curriculum maintenance
- Multi-year curriculum review cycles
- Staying current with frameworks
- Planning professional development

## Types of Standards Changes

### 1. Major Revisions

**Characteristics**:
- Complete framework overhaul
- Significant content changes
- Structure/organization changes
- New philosophy or approach

**Examples**:
- NGSS (2013) replaced previous science standards
- Common Core adoption (2010)
- State standards major updates

**Impact**: High - may require substantial curriculum rewrite

### 2. Minor Revisions

**Characteristics**:
- Clarifications
- Wording improvements
- Minor additions/deletions
- Numbering changes

**Examples**:
- WCAG 2.1 → 2.2 (additional success criteria)
- State standards annual updates

**Impact**: Low-Medium - targeted curriculum adjustments

### 3. Interpretive Guidance

**Characteristics**:
- No standard text changes
- Clarification documents released
- Examples and non-examples
- Assessment guidance

**Impact**: Low - may affect instruction emphasis, not content

### 4. Deprecated Standards

**Characteristics**:
- Standards removed
- Consolidated into other standards
- No longer assessed

**Impact**: Medium - remove from curriculum, reallocate time

## Change Tracking Process

### 1. Monitor for Updates

**Information Sources**:
- State education department websites
- Professional associations (NSTA, NCTM, NCTE)
- Standards organization announcements
- Education news
- District communications

**Frequency**:
- Annual review minimum
- Alert subscriptions for immediate notification

### 2. Analyze Changes

**For Each Change**:
- **What changed**: Specific additions, deletions, modifications
- **Why changed**: Rationale (if provided)
- **When effective**: Implementation date, phase-in period
- **Assessment impact**: Will tests change?

### 3. Impact Assessment

**Curriculum Impact**:
- Which units/lessons affected
- How many standards changed
- Depth of change required
- Timeline for updates

**Categories**:
- **Critical**: Affects tested standards, needs immediate update
- **Important**: Significant but not immediately tested
- **Minor**: Can wait for next curriculum cycle

### 4. Change Management

**Update Process**:
1. Prioritize changes (critical first)
2. Assign to curriculum writers
3. Set deadlines
4. Review and approval
5. Professional development
6. Implementation
7. Monitor and adjust

## Tracking System

### Change Log

**Record for Each Update**:
- **Date Announced**: When change published
- **Effective Date**: When implementation required
- **Framework/Standard**: What changed
- **Type**: Major/minor/guidance/deprecated
- **Old → New**: Specific changes
- **Curriculum Impact**: Which materials affected
- **Action Needed**: What must be updated
- **Responsible**: Who will update
- **Due Date**: Deadline
- **Status**: Planned/In Progress/Complete
- **PD Needed**: Teacher training required

### Version Control

**Maintain**:
- Current standards version in use
- Previous versions (for reference)
- Crosswalks between versions
- Implementation timeline
- Transition period plans

## Revision Examples

### NGSS Implementation

**Timeline**:
- 2013: NGSS released
- 2013-2015: State adoption decisions
- 2015-2020: Curriculum development
- 2020+: Assessment alignment

**Changes**:
- Three-dimensional learning (SEP, DCI, CCC)
- Performance Expectations replace content standards
- Engineering added
- Nature of science emphasized

**Curriculum Impact**: Complete rewrite required

### Common Core to State Variants

**Timeline**:
- 2010: Common Core released
- 2010-2015: State adoptions
- 2015-2020: Some states withdrew or modified

**Changes**:
- Some states added standards (financial literacy, state history)
- Some states changed grade-level placement
- Some states renamed but kept content

**Curriculum Impact**: Moderate - additions and adjustments

### WCAG 2.1 → 2.2

**Timeline**:
- 2018: WCAG 2.1
- 2023: WCAG 2.2

**Changes**:
- 9 new success criteria added
- Focus on mobile, cognitive disabilities
- No removed criteria

**Curriculum Impact**: Minor - add coverage of new criteria

## Proactive Maintenance

### Annual Review Cycle

**Schedule**:
- **Summer**: Review for next year
- **Fall**: Minor updates
- **Winter**: Assessment for spring testing
- **Spring**: Plan summer revisions

### Curriculum Lifespan

**Typical Cycles**:
- **Textbooks**: 5-7 years
- **Digital curriculum**: 2-3 years (easier to update)
- **Standards**: 5-10 years major revisions
- **Assessments**: 3-5 years

**Strategy**: Plan for mid-cycle updates

## CLI Interface

```bash
# Check for updates
/standards.updates-tracker --framework "NGSS" --current-version "2013-Final" --check-updates

# Analyze impact
/standards.updates-tracker --old "State-Math-2015" --new "State-Math-2024" --curriculum "existing-math-curriculum/" --impact-analysis

# Generate update plan
/standards.updates-tracker --changes "standards-changes.json" --curriculum "science-program/" --create-update-plan --timeline "1-year"

# Track multiple frameworks
/standards.updates-tracker --monitor --frameworks "CCSS,NGSS,State-Standards,ISTE" --alert-email "curriculum@district.org"

# Version comparison
/standards.updates-tracker --compare-versions --framework "Common-Core-Math" --version-a "2010" --version-b "2024" --crosswalk
```

## Output

- Standards change notifications
- Impact analysis report
- Update priority list
- Curriculum revision plan
- Timeline for implementation
- Professional development needs
- Version comparison/crosswalk
- Ongoing monitoring alerts

## Composition

**Input from**: `/standards.us-state-mapper`, `/standards.subject-standards`
**Works with**: `/standards.crosswalk-mapper`, `/standards.gap-analysis`, `/curriculum.iterate-feedback`
**Output to**: Updated curriculum, change management plans

## Exit Codes

- **0**: Tracking complete, updates identified
- **1**: Framework version not found
- **2**: Unable to access update information
- **3**: Critical updates require immediate attention
