---
name: slim-contributing-guide
description: Create comprehensive contributing guides for open source projects with customizable templates, including guidance for developers, documentation contributors, issue reporters, and community reviewers. Use when helping projects establish clear contribution workflows, onboard new contributors, set up development processes, integrate with project governance, or meet NASA/government institutional requirements for open source collaboration.
---

# Contributing Guide Writer

## Overview

This skill helps create comprehensive contributing guides that make open source projects welcoming and accessible to new contributors. A well-crafted contributing guide serves as the foundation for healthy community collaboration, providing clear pathways for developers, documentarians, issue reporters, and reviewers to meaningfully participate in your project.

The skill provides a comprehensive CONTRIBUTING.md template with 15+ customizable sections and extensive guidance for creating effective contributor experiences that align with project governance, development workflows, and institutional requirements.

## When to Use This Skill

- **Starting new open source projects** that need contributor onboarding
- **Converting private projects** to open source with clear contribution processes
- **Improving existing projects** with outdated or minimal contributing guidelines
- **Establishing development workflows** for team collaboration
- **Meeting compliance requirements** for government-sponsored open source projects
- **Onboarding new team members** to project contribution standards
- **Integrating with project governance** and community management
- **Setting up issue tracking** and pull request workflows
- **Creating contributor pathways** from first contribution to maintainership

## Project Assessment Guide

Before implementing a contributing guide, assess your project's current state and needs:

### Development Infrastructure Assessment

**Repository Structure:**
- Is there a clear README with project overview?
- Are there existing development setup instructions?
- Is the project structure intuitive for newcomers?
- Are dependencies and build processes documented?

**Communication Channels:**
- Where do contributors currently ask questions?
- Is there an issue tracking system in place?
- Are there existing discussion forums or chat platforms?
- How do maintainers currently communicate with each other?

**Governance Integration:**
- Does the project have a governance model? (see governance skill)
- Is there a code of conduct? (see code-of-conduct skill)
- Are there defined maintainer roles and responsibilities?
- How are decisions currently made?

### Contributor Experience Analysis

**Current Pain Points:**
- What questions do new contributors frequently ask?
- Where do contributors get stuck in the contribution process?
- What types of contributions are most needed?
- How long does it typically take to get contributions reviewed?

**Community Maturity:**
- How many active contributors are there?
- What's the current contribution volume?
- Are there different skill levels contributing?
- Is there mentorship or support for newcomers?

## Workflow

### Step 1: Project Context Analysis

Before customizing the contributing guide template, analyze your project to understand the appropriate level of detail and specific requirements.

**Assess Repository State:**
```bash
# Check for existing contributing documentation
ls -la CONTRIBUTING.md CONTRIBUTING/ contributing/ .github/CONTRIBUTING.md

# Review current project documentation
ls -la README.md LICENSE CODE_OF_CONDUCT.md GOVERNANCE.md

# Examine development setup complexity
ls -la package.json requirements.txt Dockerfile docker-compose.yml Makefile
```

**Analyze Development Workflow:**
- How do developers set up the local environment?
- What's the testing and build process?
- How are branches organized?
- What's the code review process?
- Are there CI/CD pipelines contributors should know about?

**Identify Integration Points:**
- Link to existing governance documentation
- Reference code of conduct requirements
- Connect with issue and pull request templates
- Align with project README and documentation

### Step 2: Template Customization Strategy

The CONTRIBUTING.md template contains 15 distinct placeholder categories that need customization based on your project's specific context.

**Template Deployment:**
```bash
# Copy template to project root
cp assets/CONTRIBUTING.md CONTRIBUTING.md

# Review all placeholders requiring customization
grep -n "\[INSERT" CONTRIBUTING.md
```

**Customization Priority:**
1. **Critical Placeholders** (must be filled): Issue tracking, development guide, communication channels
2. **Important Placeholders** (strongly recommended): Branch names, security contact, documentation structure
3. **Optional Placeholders** (project-specific): Additional sections, platform-specific instructions

### Step 3: Detailed Placeholder Customization

#### Core Infrastructure Placeholders

**`[INSERT YOUR DEVELOPMENT GUIDE LINK HERE]`**
- **Purpose**: Link to detailed setup instructions for contributors
- **Common Values**:
  - `docs/development.md` - Dedicated development documentation
  - `README.md#development` - Section in main README
  - `https://project-name.readthedocs.io/en/latest/contributing/setup/` - Hosted documentation
- **Guidance**: Ensure this link provides complete environment setup instructions including:
  - System requirements and dependencies
  - Installation steps
  - Build and test commands
  - IDE/editor configuration recommendations
  - Troubleshooting common setup issues

**`[INSERT LINK TO ISSUE TRACKING SYSTEM]`** (appears 8+ times)
- **Purpose**: Central location for bug reports, feature requests, and project discussions
- **Common Values**:
  - `https://github.com/owner/repo/issues` - GitHub Issues (most common)
  - `https://gitlab.com/owner/repo/-/issues` - GitLab Issues
  - `https://owner.atlassian.net/jira/projects/PROJECT` - JIRA (enterprise)
- **Consistency**: Use the same URL throughout the document
- **Configuration**: Ensure issue templates are set up (see issue-templates skill)

**`[INSERT LINK TO DISCUSSION BOARD OR MAILING LIST]`**
- **Purpose**: Permanent archived location for project discussions
- **Common Options**:
  - `https://github.com/owner/repo/discussions` - GitHub Discussions
  - `https://groups.google.com/g/project-name` - Google Groups
  - `https://discourse.project-name.org` - Discourse forum
  - `https://reddit.com/r/project-name` - Reddit community
- **Selection Criteria**: Choose based on your community's preferences and archival needs

#### Communication Infrastructure

**`[INSERT ADDITIONAL COMMUNICATION CHANNELS FOR YOUR PROJECT, EX: SLACK, TWITTER, YOUTUBE, ETC.]`**
- **Purpose**: List all ways contributors can connect with the community
- **Format Example**:
  ```markdown
  - [Slack workspace](https://project-slack.slack.com) - Real-time chat for quick questions
  - [Twitter](https://twitter.com/project_name) - Project announcements and news
  - [YouTube](https://youtube.com/c/project-name) - Tutorials and community calls
  - [Discord](https://discord.gg/project-invite) - Community chat and support
  ```
- **Best Practices**:
  - Only list actively monitored channels
  - Specify the purpose of each channel
  - Include invitation links where applicable

#### Version Control Configuration

**`[INSERT DEFAULT VCS BRANCH NAME HERE]`**
- **Purpose**: Specify the main development branch
- **Common Values**:
  - `main` - Modern GitHub default
  - `master` - Traditional Git default
  - `develop` - GitFlow development branch
- **Project Alignment**: Use whatever your repository actually uses as the default

**`[INSERT ADDITIONAL TYPICAL VCS BRANCH NAMES HERE]`**
- **Purpose**: Document branch naming conventions and special branches
- **Format Example**:
  ```markdown
  - `develop` - Integration branch for new features
  - `release/v*` - Release preparation branches
  - `hotfix/*` - Emergency fixes for production issues
  - `feature/*` - New feature development branches
  ```

#### Process Documentation

**`[INSERT LINK TO YOUR PULL REQUEST TEMPLATE, ex: .github/PULL_REQUEST_TEMPLATE.md]`**
- **Purpose**: Reference to PR template for consistent pull requests
- **Common Values**:
  - `.github/PULL_REQUEST_TEMPLATE.md` - GitHub PR template
  - `.gitlab/merge_request_templates/default.md` - GitLab MR template
  - `docs/pull-request-template.md` - Documentation-based template
- **Integration**: Ensure the template exists (see pull-requests skill)

**`[INSERT LINK FOR PULL REQUESTS TRACKING SYSTEM]`**
- **Purpose**: Where contributors can view and review open pull requests
- **Common Values**:
  - `https://github.com/owner/repo/pulls` - GitHub Pull Requests
  - `https://gitlab.com/owner/repo/-/merge_requests` - GitLab Merge Requests
  - Project-specific review dashboard

#### Security and Contact Information

**`[INSERT SECURITY CONTACT LINK HERE]`**
- **Purpose**: How to report security vulnerabilities privately
- **Options**:
  - `mailto:security@organization.org` - Direct email contact
  - `https://github.com/owner/repo/security/advisories/new` - GitHub Security Advisories
  - `SECURITY.md` - Dedicated security policy file
  - Bug bounty platform link
- **Government Projects**: Especially important for NASA/federal projects with security requirements

#### Technical Documentation

**`[INSERT YOUR CODING LANGUAGE FILE EXTENSIONS HERE]`**
- **Purpose**: Specify file types that contain inline documentation
- **Examples by Language**:
  - Python: `*.py` - docstrings in Python files
  - JavaScript: `*.js, *.ts` - JSDoc comments
  - Java: `*.java` - Javadoc comments
  - C++: `*.cpp, *.h` - Doxygen comments
  - Go: `*.go` - godoc comments

**`[INSERT ADDITIONAL DOCUMENTATION CLASSES AND ORGANIZATION STRUCTURE HERE, SEE EXAMPLE IN COMMENTS BELOW]`**
- **Purpose**: Document the project's documentation structure and types
- **Format Example**:
  ```markdown
  - **API Documentation** - `docs/api/` - Auto-generated from code comments
  - **User Guides** - `docs/user/` - End-user documentation
  - **Developer Guides** - `docs/developer/` - Technical implementation details
  - **Architecture Documentation** - `docs/architecture/` - System design and decisions
  ```

**`[INSERT HOSTED DOCUMENTATION PLATFORM SPECIFIC INSTRUCTIONS HERE FOR HOW TO CONTRIBUTE]`**
- **Purpose**: Platform-specific contribution instructions
- **Examples by Platform**:
  - **Read the Docs**: "Documentation is built automatically from the `docs/` directory using Sphinx"
  - **GitBook**: "Edit documentation through the GitBook web interface or sync with GitHub"
  - **Docusaurus**: "Documentation lives in `website/docs/` and uses Markdown with frontmatter"
  - **GitHub Pages**: "Documentation is in the `gh-pages` branch and built with Jekyll"

#### Project-Specific Content

**`[INSERT ADDITIONAL SECTIONS HERE FOR MORE SPECIFIC CLASSES OF CODE CONTRIBUTIONS DEPENDING ON YOUR MODULES, LANGUAGES, PLATFORMS IN USE BY YOUR PROJECT. THE MORE DETAILS YOU OFFER, THE MORE LIKELY SOMEONE IS TO UNDERSTAND HOW TO CONTRIBUTE]`**
- **Purpose**: Add project-specific contribution guidance
- **Examples**:
  - **Web Applications**: Frontend vs. backend contribution guidelines
  - **Libraries**: API design principles and backwards compatibility
  - **CLI Tools**: Command-line interface design standards
  - **Mobile Apps**: Platform-specific (iOS/Android) guidelines
  - **Scientific Software**: Computational accuracy and validation requirements

**`[INSERT YOUR PROJECT SPECIFIC COMMON TERMS AND HOW TO USE THEM]`**
- **Purpose**: Define project-specific terminology and concepts
- **Format Example**:
  ```markdown
  - **Pipeline**: Our data processing workflow system
  - **Module**: Individual functional components (prefer over "plugin")
  - **Dataset**: Input data collections (use "dataset", not "data set")
  - **Endpoint**: API service interfaces (RESTful endpoints)
  ```

### Step 4: Integration and Testing

#### Integration with Project Ecosystem

**Link to Governance Documentation:**
If using the governance skill, reference your GOVERNANCE.md:
```markdown
For information about project roles and decision-making processes,
see our [Governance Model](GOVERNANCE.md).
```

**Code of Conduct Integration:**
Ensure consistency with your CODE_OF_CONDUCT.md:
```markdown
All contributors are expected to follow our [Code of Conduct](CODE_OF_CONDUCT.md).
```

**Issue Template Coordination:**
If using issue-templates skill, reference your templates:
```markdown
When filing issues, please use our issue templates in `.github/ISSUE_TEMPLATE/`.
```

#### Testing the Contributing Guide

**New Contributor Walkthrough:**
1. Follow your own contributing guide from start to finish
2. Test all links and ensure they work
3. Verify setup instructions are complete and accurate
4. Check that the workflow actually matches your development process

**Community Review:**
- Share draft with existing contributors for feedback
- Ask newcomers to try following the guide
- Collect feedback on clarity and completeness
- Update based on real-world usage

### Step 5: Community Launch and Maintenance

#### Announcing the Contributing Guide

**Internal Announcement:**
1. Update project README with link to CONTRIBUTING.md
2. Notify existing contributors about the new guide
3. Update any existing documentation that references contribution processes
4. Train maintainers on the new processes

**Community Communication:**
```markdown
## 🎉 New Contributing Guide Available!

We've created a comprehensive guide to help new and existing contributors
get involved with our project. Check out our new [CONTRIBUTING.md](CONTRIBUTING.md)
for detailed instructions on:

- Setting up your development environment
- Finding good first issues to work on
- Submitting pull requests
- Contributing documentation
- Reporting bugs and requesting features

We're excited to welcome more contributors to our community!
```

#### Ongoing Maintenance

**Regular Review Schedule:**
- **Quarterly**: Review contributor feedback and pain points
- **After major releases**: Update any process changes
- **When onboarding new maintainers**: Gather fresh perspective on clarity
- **When development workflow changes**: Update relevant sections

**Metrics to Track:**
- Time from first contribution to successful merge
- Number of questions about contribution process
- Contributor retention rates
- Types of contributions being made

## Government and Institutional Requirements

### NASA/JPL Compliance Considerations

When creating contributing guides for NASA or other government-sponsored projects:

**Institutional Policies:**
- Include references to institutional open source policies
- Add export control compliance requirements where applicable
- Reference appropriate terms of use and licensing requirements
- Include institutional copyright and attribution requirements

**Contributor Eligibility:**
- Document any restrictions on foreign national contributions
- Specify security clearance requirements if applicable
- Include contractor vs. civil servant contribution guidelines
- Reference any required contributor license agreements (CLAs)

**Security and Compliance:**
- Reference security reporting procedures specific to government projects
- Include data handling and classification guidelines
- Document any code review requirements for security-sensitive changes
- Reference institutional cybersecurity policies

**Example Government-Specific Section:**
```markdown
### Government Project Requirements

This project is sponsored by NASA/JPL and follows institutional policies:

- **Export Control**: Contributions may be subject to export control regulations
- **Security**: Report security issues to [security@institution.gov](mailto:security@institution.gov)
- **CLA Required**: Contributors must sign our Contributor License Agreement
- **Background Checks**: Some contributions may require security clearance verification
- **Review Process**: Government oversight may be required for certain changes

For questions about these requirements, contact [project-admin@institution.gov](mailto:project-admin@institution.gov).
```

## Integration with Other SLIM Skills

### Related Skills Integration

**Governance Skill Connection:**
- Reference governance skill for team structure and decision-making
- Align contributing guide roles with governance roles
- Ensure contributing processes support governance requirements

**Code of Conduct Skill:**
- Link to code of conduct for community behavior standards
- Reference code of conduct in conflict resolution procedures
- Ensure contributing guide supports inclusive community goals

**Issue Templates Skill:**
- Reference issue templates in bug reporting sections
- Coordinate contributing guide with issue template workflows
- Ensure consistency in issue filing instructions

**Pull Request Templates Skill:**
- Link to pull request templates in contribution workflow
- Align contributing guide with PR template requirements
- Coordinate review criteria and checklists

**License Skill:**
- Reference project licensing terms in contribution requirements
- Ensure contributor agreement with license terms
- Coordinate with any contributor license agreements

## Best Practices

### Writing Effective Contributing Guides

**Clarity and Accessibility:**
- Use clear, simple language appropriate for various skill levels
- Provide step-by-step instructions rather than assumptions
- Include examples and concrete guidance
- Organize information logically with clear headings

**Comprehensive Coverage:**
- Address different types of contributions (code, docs, issues, reviews)
- Include both quick start and detailed instructions
- Cover edge cases and troubleshooting
- Provide multiple communication channels

**Community Focus:**
- Emphasize welcoming and inclusive language
- Acknowledge different contribution styles and skills
- Provide clear pathways for growing involvement
- Include recognition and appreciation for contributors

### Maintenance and Evolution

**Keep It Current:**
- Update links and references regularly
- Reflect actual project practices, not aspirational ones
- Gather and incorporate contributor feedback
- Adapt to tool and process changes

**Community-Driven Improvement:**
- Encourage contributors to suggest improvements to the guide
- Make the guide itself a contribution opportunity
- Track and address common questions or confusion
- Regular review and update cycles

## Common Pitfalls to Avoid

- ❌ **Over-complexity**: Making the guide too detailed or overwhelming for newcomers
- ❌ **Outdated Information**: Failing to maintain accuracy as processes evolve
- ❌ **Missing Links**: Placeholder links that are never filled in
- ❌ **Assumption of Knowledge**: Assuming contributors know project-specific terms or processes
- ❌ **Process Mismatch**: Documenting ideal processes that don't match reality
- ❌ **Single Contribution Type**: Focusing only on code contributions and ignoring other ways to help
- ❌ **Institutional Assumptions**: Assuming all projects have the same organizational structure

## Assets Available

This skill includes one comprehensive template:

- **`CONTRIBUTING.md`**: Complete contributing guide template with 15+ customizable sections
  - Developer onboarding and setup instructions
  - Multi-type contribution guidance (code, documentation, issues, reviews)
  - Communication channel integration
  - Process workflows for different contribution types
  - Security and institutional compliance sections
  - Community guidelines and expectations
  - Integration points for governance and code of conduct
  - Placeholder guidance for complete customization

The template covers:
- **Prerequisites**: License, code of conduct, development environment, communication channels
- **Development Process**: Fork workflow, issue tracking, branch management, pull requests
- **Contribution Types**: Code contributions, bug reports, feature requests, security reports
- **Code Review**: Review guidelines and process participation
- **Documentation**: Various documentation types and contribution methods
- **Community**: Discussion participation and support provision

## FAQ

**Q: Should I customize all 15+ placeholders immediately?**
A: Focus on critical placeholders first (issue tracking, development guide, communication channels). You can iteratively improve other sections based on contributor feedback.

**Q: How detailed should the development setup instructions be?**
A: Include enough detail that a newcomer can successfully contribute without asking questions. Link to separate detailed documentation rather than making CONTRIBUTING.md too long.

**Q: How do I handle projects with complex contribution requirements?**
A: Start with a clear overview and quick start, then provide links to detailed documentation for specific contribution types. Use the "Additional Sections" placeholder for project-specific requirements.

**Q: Should I include governance information in the contributing guide?**
A: Reference your governance model but keep detailed governance in GOVERNANCE.md. Focus the contributing guide on practical contribution steps.

**Q: How often should I update the contributing guide?**
A: Review quarterly and update immediately when development processes change. Track contributor questions to identify areas needing clarification.

**Q: What if my project doesn't have all the infrastructure mentioned in the template?**
A: Fill in what you have and remove or modify sections that don't apply. The template is comprehensive to cover various project types, but not all sections are required.

## Troubleshooting

**Issue: Contributors aren't following the guide**
- Check if the guide matches your actual development workflow
- Ask contributors what's confusing or unclear
- Make sure the guide is prominently linked from README and other documentation
- Consider shorter quick-start sections for common contribution types

**Issue: Too many questions about basic contribution process**
- Review your development environment setup instructions for completeness
- Add more examples and concrete guidance
- Consider creating video walkthroughs for complex setup processes
- Ensure all placeholder links are filled and working

**Issue: Contributing guide is getting too long**
- Move detailed technical information to separate documentation
- Use clear headings and table of contents for navigation
- Focus on essential information in main sections
- Use the "Additional Sections" approach for project-specific details

**Issue: Difficulty maintaining consistency with other project documentation**
- Create a documentation review process that includes contributing guide updates
- Use the same terminology and concepts across all project documentation
- Regular cross-reference checks between CONTRIBUTING.md, README.md, and governance documents
- Consider using documentation templates or style guides for consistency
