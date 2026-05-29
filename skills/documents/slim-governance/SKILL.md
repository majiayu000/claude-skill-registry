---
name: slim-governance
description: Create governance models and structures for open source projects with team-specific templates for small, medium, and large teams, including NASA/government compliance guidance
---

# Project Governance Model Writer

## Overview

This skill helps establish clear governance structures for open source projects, particularly those sponsored by government organizations like NASA. A well-defined governance model ensures transparency, encourages contributions, maintains technical standards, and provides clear decision-making processes.

The skill provides three specialized governance templates optimized for different team sizes and organizational complexity, each designed to foster healthy open source communities while meeting institutional requirements.

## When to Use This Skill

- **Starting new open source projects** that need governance structure
- **Converting private projects** to open source with proper governance
- **Establishing team roles** and decision-making processes
- **Meeting compliance requirements** for government-sponsored projects
- **Scaling team governance** as projects grow
- **Clarifying contributor pathways** and responsibilities
- **Setting up transparent development processes**

## Team Size Assessment Guide

Before selecting a template, assess your team size and organizational needs:

### Small Teams (2-5 active contributors)
**Characteristics:**
- Direct communication between all members
- Simple decision-making process
- Minimal bureaucracy needed
- Close collaboration on most decisions
- Limited formal roles required

**Best for:** Early-stage projects, research projects, small utilities, proof-of-concepts

### Medium Teams (6-20 active contributors)
**Characteristics:**
- Mix of direct and structured communication
- Need for some formal roles and processes
- Multiple areas of expertise/ownership
- Balance between flexibility and structure
- Growing external contributor base

**Best for:** Established projects, multi-component systems, growing communities

### Large Teams (20+ active contributors)
**Characteristics:**
- Formal communication structures required
- Complex decision-making processes
- Multiple committees or working groups
- Diverse stakeholder representation
- High volume of contributions and decisions

**Best for:** Enterprise projects, multi-organization initiatives, mature ecosystems

## Template Selection Workflow

### Step 1: Assess Your Current State

Ask these key questions:

1. **Team Size**: How many active contributors do you have?
2. **Growth Trajectory**: How quickly is the team expected to grow?
3. **Organizational Complexity**: How many organizations are involved?
4. **Decision Complexity**: How complex are typical technical decisions?
5. **Compliance Requirements**: Are there government/institutional requirements?

### Step 2: Choose Your Template

**Choose Small Teams Template when:**
- ≤5 active contributors
- Single organization primary
- Simple technical decisions
- Rapid iteration needed
- Minimal bureaucracy preferred

**Choose Medium Teams Template when:**
- 6-20 active contributors
- Multi-organization involvement
- Moderate decision complexity
- Balance of speed and process needed
- Growing external interest

**Choose Large Teams Template when:**
- 20+ active contributors
- Complex multi-organization structure
- High-stakes technical decisions
- Formal process requirements
- Established community governance needed

### Step 3: Consider Special Requirements

**Government/NASA Projects:**
- Choose template one size larger than assessment suggests
- Ensure compliance sections are properly filled
- Include institutional copyright requirements
- Add security and export control considerations

## Government Project Specifics

### NASA/JPL Compliance Considerations

When working on NASA or other government-sponsored projects:

1. **Institutional Requirements**:
   - Include appropriate copyright headers
   - Reference institutional policies
   - Ensure export control compliance
   - Follow security guidelines

2. **Role Definitions**:
   - Include government oversight roles
   - Define contractor vs. civil servant responsibilities
   - Establish foreign national participation rules
   - Set up approval workflows for sensitive decisions

3. **Documentation Standards**:
   - Meet federal record-keeping requirements
   - Ensure transparency in decision-making
   - Maintain audit trails for key decisions
   - Follow accessibility standards (Section 508)

4. **Contribution Guidelines**:
   - Implement contributor license agreements (CLAs)
   - Set up IP clearance processes
   - Define acceptable contribution sources
   - Establish security review procedures

## Customization Guide

### Common Customizations

1. **Project Information**:
   - Replace `[INSERT PROJECT NAME]` with your project name
   - Update `[INSERT PROJECT DOMAIN]` with your domain area
   - Add your project's specific links and contacts

2. **Role Modifications**:
   - Adjust role names to match your organization
   - Modify permission levels based on your needs
   - Add specialized roles (e.g., Security Officer, Documentation Lead)
   - Define term limits for leadership positions

3. **Decision-Making Processes**:
   - Choose voting thresholds (majority, supermajority, consensus)
   - Define escalation procedures
   - Set meeting schedules and formats
   - Establish tie-breaking mechanisms

4. **Communication Channels**:
   - Specify your discussion platforms (GitHub Discussions, Slack, etc.)
   - Define which decisions require public discussion
   - Set up mailing lists or forums
   - Establish meeting cadences

### Example Customizations by Team Size

**Small Teams:**
- Combine Product Manager and Technical Lead roles
- Use informal consensus for most decisions
- Weekly team check-ins instead of formal meetings
- Direct GitHub issues for most governance discussions

**Medium Teams:**
- Separate Product and Technical Steering
- Establish Working Groups for specialized areas
- Monthly steering committee meetings
- Formal RFC process for major changes

**Large Teams:**
- Multiple specialized committees
- Formal governance board
- Quarterly community meetings
- Structured proposal and review processes

## Deployment Workflow

### Step 1: Check for Existing Governance

```bash
ls -la GOVERNANCE.md GOVERNANCE/ governance/
```

If governance documents exist:
- Review existing structure
- Plan migration strategy
- Consider versioning the transition
- Communicate changes to community

### Step 2: Select and Customize Template

1. **Copy the appropriate template**:
   ```bash
   cp assets/governance-[small|medium|large].md GOVERNANCE.md
   ```

2. **Review and customize**:
   - Search for all `[INSERT...]` placeholders
   - Replace with project-specific information
   - Adjust roles and permissions as needed
   - Add any missing sections for your context

### Step 3: Team Review and Approval

1. **Internal Review**:
   - Share draft with current team members
   - Gather feedback on roles and processes
   - Ensure institutional requirements are met
   - Test decision-making scenarios

2. **Stakeholder Approval**:
   - Get sign-off from organizational sponsors
   - Review with legal/compliance teams if required
   - Ensure alignment with institutional policies
   - Document any required modifications

### Step 4: Community Introduction

1. **Announce the governance model**:
   - Create issue or discussion explaining the new governance
   - Highlight benefits and opportunities for contributors
   - Explain transition timeline if replacing existing governance
   - Invite community feedback and questions

2. **Update project documentation**:
   - Link to GOVERNANCE.md from README
   - Update CONTRIBUTING.md with role information
   - Add governance references to project websites
   - Include in new contributor onboarding

### Step 5: Implementation and Evolution

1. **Put governance into practice**:
   - Start using defined roles and processes
   - Hold first governance meetings
   - Begin contributor onboarding process
   - Establish regular review cycles

2. **Monitor and iterate**:
   - Collect feedback on governance effectiveness
   - Adjust processes based on real-world usage
   - Scale governance as team grows
   - Document lessons learned

## Best Practices

### Starting with Governance

1. **Start Simple**: Choose the smallest viable governance structure
2. **Grow Gradually**: Add complexity only as team size demands it
3. **Document Everything**: Keep clear records of governance decisions
4. **Regular Reviews**: Assess governance effectiveness quarterly
5. **Community First**: Prioritize contributor experience and transparency

### Common Pitfalls to Avoid

- ❌ **Over-engineering**: Starting with too complex a governance structure
- ❌ **Under-communicating**: Not explaining governance changes clearly
- ❌ **Rigid Processes**: Making governance too bureaucratic
- ❌ **Unclear Roles**: Defining overlapping or ambiguous responsibilities
- ❌ **No Evolution**: Failing to adapt governance as team grows

## Assets Available

This skill includes three complete governance templates:

- **`governance-small.md`**: Streamlined governance for small teams (2-5 contributors)
  - Simple role structure: Contributor → Committer → Product Manager
  - Lightweight decision-making processes
  - Focus on direct collaboration and rapid iteration

- **`governance-medium.md`**: Balanced governance for medium teams (6-20 contributors)
  - Expanded roles including Technical Steering Committee
  - Structured decision-making with multiple approval paths
  - Balance of flexibility and formal process

- **`governance-large.md`**: Comprehensive governance for large teams (20+ contributors)
  - Complex role hierarchy with specialized positions
  - Formal committees and working groups
  - Detailed procedures for large-scale collaboration

All templates include:
- Role definitions and responsibilities
- Decision-making processes
- Contribution guidelines
- Conflict resolution procedures
- Template placeholders for easy customization

## Additional Resources

- [Open Source Governance Models](https://opensource.guide/leadership-and-governance/)
- [NASA Open Source Agreement](https://opensource.org/licenses/NASA-1.3)
- [Contributor License Agreements](https://www.apache.org/licenses/contributor-agreements.html)
- [GitHub Community Guidelines](https://docs.github.com/en/communities)
- [SLIM Governance Documentation](https://nasa-ammos.github.io/slim/docs/guides/governance/)

## Troubleshooting

**Q: Which template should I choose if I'm between sizes?**
A: When in doubt, start with the smaller template. It's easier to add complexity than remove it.

**Q: What if my organization has specific governance requirements?**
A: Use the closest template as a starting point, then customize roles and processes to meet your organizational needs.

**Q: How often should governance be reviewed?**
A: Review governance effectiveness quarterly in the first year, then annually or when significant team changes occur.

**Q: Can I mix elements from different templates?**
A: Yes! The templates are starting points. Customize by mixing and matching elements that work for your specific context.
