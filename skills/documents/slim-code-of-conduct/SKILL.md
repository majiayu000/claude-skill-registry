---
name: slim-code-of-conduct
description: Create and implement code of conduct and collaboration policies using Contributor Covenant standards, with specialized templates for scientific research environments and academic citation. Use when establishing team culture, promoting inclusive communities, implementing governance policies, or setting up collaboration standards for open source, research, or academic projects.
---

# Code of Conduct Writer

## Overview

A code of conduct is essential for establishing standards of interaction within project teams, promoting positive community environments, and providing clear mechanisms for conflict resolution. This skill helps you implement professional code of conduct policies using industry-standard templates that can be customized for your specific project needs.

The skill provides three specialized templates: the widely-adopted Contributor Covenant for standard projects, a scientific collaboration policy for research environments, and academic citation guidelines for research software projects.

## When to Use This Skill

- **Starting new open source projects** that need community guidelines
- **Establishing team culture** and collaboration standards
- **Creating inclusive environments** with clear behavior expectations
- **Meeting compliance requirements** for institutional or organizational projects
- **Implementing governance policies** for project teams
- **Setting up research collaboration** guidelines and publication ethics
- **Adding academic citation** standards for research software
- **Improving existing projects** with formal conduct policies

## Prerequisites

- **Community management understanding**: Basic knowledge of team dynamics and collaboration
- **Markdown familiarity**: Ability to edit and customize Markdown documentation
- **Team leadership awareness**: Understanding of conflict resolution and policy enforcement

## Available Templates

This skill provides three templates that can be used individually or in combination:

### 1. CODE_OF_CONDUCT.md (Contributor Covenant)
**Purpose**: Standard code of conduct for open source projects and general team collaboration
**Best for**: Most open source projects, community-driven development, general team guidelines
**Key features**: Comprehensive behavior standards, reporting mechanisms, enforcement guidelines

### 2. CODE_OF_COLLAB.md (Scientific Collaboration)
**Purpose**: Specialized collaboration policy for research environments
**Best for**: Academic research projects, scientific software, publication-oriented teams
**Key features**: Publication ethics, authorship guidelines, research integrity standards

### 3. CITATION.cff (Academic Citation)
**Purpose**: Standardized citation file for research software projects
**Best for**: Academic software, research tools, projects requiring scholarly citation
**Key features**: Author metadata, DOI integration, publication references, academic formatting

## Workflow

### Step 1: Team Consultation and Planning

Before implementing any code of conduct policies, discuss with your team:

1. **Assess project needs**:
   ```bash
   # Consider your project type:
   # - General open source project → Contributor Covenant
   # - Research/academic project → Scientific Collaboration + Citation
   # - Mixed community → Multiple templates as needed
   ```

2. **Gather team consensus**:
   - Discuss the importance of formal conduct policies
   - Identify potential concerns or questions
   - Assign responsibility for policy maintenance and enforcement
   - Define reporting and escalation procedures

### Step 2: Template Selection

**I will now present the available templates. Please let me know which ones you need for your project:**

**Option A: Standard Code of Conduct**
- Use `assets/CODE_OF_CONDUCT.md` (Contributor Covenant)
- Suitable for most open source projects
- Provides comprehensive community guidelines

**Option B: Scientific Collaboration Policy**
- Use `assets/CODE_OF_COLLAB.md`
- Designed for research environments
- Covers publication ethics and authorship

**Option C: Academic Citation File**
- Use `assets/CITATION.cff`
- Enables proper scholarly citation
- Integrates with academic databases

**Option D: Combination**
- Use multiple templates as needed
- Common combinations: A+C for academic open source, B+C for research projects

*Which template(s) do you need for your project? Please specify A, B, C, or a combination.*

### Step 3: Template Customization

Based on your selection, customize the chosen template(s):

#### For CODE_OF_CONDUCT.md (Contributor Covenant):

1. **Copy and customize the template**:
   ```bash
   cp assets/CODE_OF_CONDUCT.md CODE_OF_CONDUCT.md
   ```

2. **Required customizations**:
   - Replace `[INSERT CONTACT METHOD]` with appropriate contact details:
     - Email address for reports
     - Project maintainer information
     - Community management team contact

3. **Optional customizations**:
   - Adjust enforcement procedures if needed
   - Add project-specific examples if helpful
   - Modify scope if your project has unique requirements

#### For CODE_OF_COLLAB.md (Scientific Collaboration):

1. **Copy and customize the template**:
   ```bash
   cp assets/CODE_OF_COLLAB.md CODE_OF_COLLAB.md
   ```

2. **Key customizations**:
   - Update contact information for collaboration disputes
   - Adjust publication and authorship guidelines for your field
   - Modify research integrity standards if needed
   - Add funding acknowledgment requirements

#### For CITATION.cff (Academic Citation):

1. **Copy and customize the template**:
   ```bash
   cp assets/CITATION.cff CITATION.cff
   ```

2. **Required customizations**:
   - `[INSERT PROJECT TITLE]`: Your software/project name
   - `[INSERT FIRST NAME]` and `[INSERT LAST NAME]`: Author information
   - `[INSERT EMAIL]`: Primary contact email
   - `[INSERT INSTITUTION/ORGANIZATION]`: Affiliation
   - `[INSERT REPOSITORY URL]`: GitHub/GitLab repository URL
   - `[INSERT PROJECT ABSTRACT/DESCRIPTION]`: Project summary
   - `[INSERT KEYWORDS]`: Relevant research keywords
   - `[INSERT LICENSE]`: Your project's license (e.g., Apache-2.0, MIT)
   - `[INSERT VERSION]`: Current version (e.g., 1.0.0)
   - `[INSERT RELEASE DATE]`: Release date in YYYY-MM-DD format

3. **Optional customizations**:
   - Add ORCID ID if available: `[INSERT ORCID ID]`
   - Include DOI if published: `[INSERT DOI]`
   - Add related publications in references section
   - Include project website URL

### Step 4: Project Integration

#### A. Add Badge to README.md (for Contributor Covenant):

Add this badge to your README.md for visibility:

```markdown
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)
```

#### B. Link from Project Documentation:

Add references to your code of conduct in key locations:

```markdown
## Code of Conduct

This project follows our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## Collaboration Guidelines

See our [Collaboration Policy](CODE_OF_COLLAB.md) for research-specific guidelines.

## Citation

If you use this software in your research, please cite it using the information in [CITATION.cff](CITATION.cff).
```

#### C. Update Contributing Guidelines:

Reference your conduct policies in CONTRIBUTING.md:

```markdown
## Community Standards

Before contributing, please review:
- [Code of Conduct](CODE_OF_CONDUCT.md) - Community behavior standards
- [Collaboration Policy](CODE_OF_COLLAB.md) - Research collaboration guidelines
```

### Step 5: Implementation and Maintenance

1. **Announce the policy**:
   - Create an issue or discussion announcing the new conduct policy
   - Explain the benefits and expectations
   - Invite questions and feedback

2. **Establish enforcement procedures**:
   - Designate contact persons for reports
   - Set up confidential reporting channels
   - Define escalation and resolution processes
   - Document decision-making procedures

3. **Regular review**:
   - Review policies annually or when team structure changes
   - Update contact information as needed
   - Gather feedback on policy effectiveness
   - Adjust procedures based on experience

## Best Practices

### Contact Setup

**For standard projects**:
- Use project maintainer email or team contact
- Consider creating a dedicated conduct@yourproject.org email
- Ensure multiple people can access reports if possible

**For research projects**:
- Include both technical and research leadership contacts
- Provide both institution and project-specific contacts
- Consider including ombudsman or institutional ethics contacts

### Enforcement Guidelines

1. **Be consistent**: Apply policies fairly across all community members
2. **Act promptly**: Address violations quickly to maintain community trust
3. **Document decisions**: Keep records of reports and resolutions
4. **Communicate clearly**: Explain decisions and next steps to all parties
5. **Follow up**: Check on outcomes and community health regularly

### Citation Management

- Keep CITATION.cff updated with new releases
- Connect your repository to Zenodo for DOI generation
- Include citation information in your documentation
- Consider adding a "How to Cite" section to your README

## Template-Specific Guidance

### When to Use Contributor Covenant
- General open source projects
- Community-driven development
- Projects with diverse contributor base
- Standard collaborative environments

### When to Use Scientific Collaboration Policy
- Academic research projects
- Grant-funded software development
- Projects involving publication and authorship
- Research institution requirements

### When to Use Academic Citation File
- Research software projects
- Tools used in academic publications
- Software with scholarly applications
- Projects seeking academic recognition

### Common Combinations
- **Academic open source**: Contributor Covenant + Citation file
- **Research project**: Scientific Collaboration + Citation file
- **Institutional project**: All three templates
- **Community project**: Contributor Covenant only

## FAQ

**Q: Do I need all three templates?**
A: No, choose based on your project type. Most projects need only one or two templates.

**Q: Can I customize the Contributor Covenant template?**
A: Yes, but maintain the core principles. Focus on customizing contact information and project-specific details.

**Q: How do I handle code of conduct violations?**
A: Follow your defined procedures. Document incidents, communicate with all parties, and take appropriate action based on severity.

**Q: Should I create the citation file even if my project isn't academic?**
A: If your software might be used in research or academic contexts, a citation file helps users cite your work properly.

**Q: How often should I review these policies?**
A: Review annually or when significant team changes occur. Update contact information immediately when needed.

**Q: What if my institution has specific requirements?**
A: Customize the templates to meet institutional requirements while maintaining the core principles and structure.

## Troubleshooting

**Issue: Team resistance to formal conduct policies**
- Solution: Explain benefits, provide examples from successful projects, start with minimal policies and expand gradually

**Issue: Unclear reporting procedures**
- Solution: Define specific steps, designate clear contacts, provide multiple reporting channels

**Issue: Citation file not recognized by academic databases**
- Solution: Validate CFF format, ensure proper metadata fields, connect to DOI providers

**Issue: Conflicts between different cultural norms**
- Solution: Focus on behavior rather than beliefs, provide clear examples, ensure inclusive language

**Issue: Policy enforcement challenges**
- Solution: Train designated contacts, establish clear escalation procedures, document decisions consistently

## Assets Available

- **`CODE_OF_CONDUCT.md`**: Contributor Covenant template with customization placeholders
- **`CODE_OF_COLLAB.md`**: Scientific collaboration policy template
- **`CITATION.cff`**: Academic citation file template with comprehensive metadata fields

## Additional Resources

- [Contributor Covenant](https://www.contributor-covenant.org/) - Official Contributor Covenant website
- [Citation File Format](https://citation-file-format.github.io/) - CFF specification and validation tools
- [GitHub Community Guidelines](https://docs.github.com/en/communities) - Platform-specific guidance
- [SLIM Governance Documentation](https://nasa-ammos.github.io/slim/docs/guides/governance/) - Additional governance resources
