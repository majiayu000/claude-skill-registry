---
name: expert-skill-creator
description: Expert-level guidance for creating high-quality Claude Code skills. Use alongside Anthropic's skill-creator when creating new skills, improving existing skills, or needing guidance on skill content quality. Complements basic skill mechanics with research-driven content development, XML tag structuring, decision frameworks over mechanics, cross-references between skills, and systematic validation.
---

# Expert Skill Creator

<skill_scope skill="expert-skill-creator">
**Related skills:**
- `skill-creator:skill-creator` (Anthropic) - Basic skill mechanics, directory structure, initialization
- `opinionated-software-engineering:software-engineer` - Design principles that inform skill architecture
- `opinionated-software-engineering:test-driven-development` - Validation methodology parallels

**This skill complements Anthropic's `skill-creator:skill-creator` skill.** Load both when creating skills: `skill-creator:skill-creator` provides basic mechanics (directory structure, initialization scripts, packaging), while this skill provides expert-level guidance on content quality, structure, and validation.

Skills are modular packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tool integrations. They function as **retrieval triggers** that activate and organize Claude's trained knowledge, not as teaching material that explains concepts from scratch.

**Critical insight**: For LLMs, skills activate existing knowledge rather than teaching new content. The risk is that too much detail *constrains* behavior rather than enhancing it. Skills should provide high-level frameworks that trigger trained knowledge, with detailed content reserved for genuinely novel or problematic areas.
</skill_scope>

## When to Use This Skill

<when_to_use>
Use this skill when:
- Creating a new skill from scratch
- Improving or refactoring an existing skill
- Evaluating skill quality against established guidelines
- Needing guidance on skill architecture, structure, or content depth
- Researching content for a skill using agents
- Validating skill content for accuracy and completeness

Do not use this skill for:
- General prompt engineering (this is skill-specific)
- Subagent packaging mechanics (i.e., tool lists, model selection, agent frontmatter fields) — though agent prompt *content* follows similar quality principles; see `<directive_language>`
- Skill frontmatter syntax beyond `name` and `description` — see `skill-creator:skill-creator` for fields like `context`, `agent`, `allowed-tools`, `hooks`, argument substitution, and dynamic context injection
- One-off instructions that don't warrant a reusable skill
</when_to_use>

## Skill Architecture

<skill_anatomy>
### Directory Structure

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (required)
│   │   ├── name: lowercase-hyphenated (max 64 chars)
│   │   └── description: what + when (max 1024 chars)
│   └── Markdown body with XML-tagged sections
├── scripts/          - Executable code (deterministic operations)
├── references/       - Documentation loaded on-demand
└── assets/           - Files used in output (templates, icons)
```

### Progressive Disclosure

Skills use three-level loading to manage context efficiently:

| Level | Content | When Loaded | Size Target |
|-------|---------|-------------|-------------|
| 1. Metadata | name + description | Always in context | ~100 words |
| 2. SKILL.md body | Instructions, frameworks | When skill triggers | <5k words |
| 3. Bundled resources | Scripts, references, assets | As needed by Claude | Unlimited |

**Design implication**: Keep SKILL.md lean. Move detailed reference material, schemas, and examples to `references/` files. Information should live in either SKILL.md or references, never both.

### Content Patterns

<content_patterns>
Skills fall into two architectural patterns that require different content approaches:

| Pattern | Frontmatter | Content style | Example |
|---------|-------------|---------------|---------|
| **Reference** (inline) | Default | Knowledge, conventions, decision frameworks Claude applies alongside conversation context | Style guides, API conventions, language idioms |
| **Task** (fork) | `context: fork` | Self-contained task prompt with explicit steps; runs in an isolated subagent with no conversation history | Deployment workflows, research orchestration, batch operations |

**Reference skills** provide context Claude weaves into its responses. Write them as frameworks and principles (i.e., the guidance throughout this skill). They run inline with full conversation access.

**Task skills** are complete prompts that drive a subagent. They need explicit instructions because the subagent has no conversation context. Use `context: fork` and optionally `agent:` to select the execution environment (e.g., `Explore` for read-only, `general-purpose` for full tool access). Task skills can launch further agents via the Agent tool, enabling fan-out patterns like parallel research or batch code changes.

Choose the pattern based on whether the skill augments Claude's knowledge (reference) or orchestrates an independent workflow (task).
</content_patterns>
</skill_anatomy>

## Quality Guidelines

<quality_guidelines>
These guidelines emerged from creating 15+ skills and observing their performance in clean context windows. They represent hard-won lessons about what makes skills effective.

### XML Tag Structure

<xml_tag_guidelines>
**Skills are prompts—apply XML tagging best practices.[^1]**

**Why XML tags matter:**
- Clarity: Separate different parts of the skill
- Accuracy: Prevent Claude from mixing instructions with examples
- Flexibility: Easy to find, add, remove, or modify sections
- Parseability: Enable structured reasoning about skill content

**Tag naming conventions:**
- Use descriptive `snake_case` names: `<dependency_update_checklist>`, `<error_handling_patterns>`, `<api_versioning_strategy>`
- Avoid generic names—`<remember>` or `<notes>` don't describe what to remember or what the notes contain; prefer names like `<migration_safety_constraints>` or `<version_compatibility_matrix>`
- Maintain consistent names throughout—same concept, same tag name
- Wrap coherent conceptual chunks that could be referenced independently
- Nest tags for hierarchical content: `<platform_differences><macos_specifics>...</macos_specifics></platform_differences>`

**Standard tags:**
- `<skill_scope skill="skill-name">` — Use for the skill's introductory section (overview, purpose, related skills). The `skill` attribute prevents collision when multiple skills are loaded. Every skill should begin with this tag after the title.

**Explicit tag references:**
Reference tags by name when discussing their content. This reinforces connections between sections and helps readers navigate related guidance.

- Good: "Apply the guidelines in `<release_checklist>` before publishing"
- Weak: "Apply the release checklist guidelines before publishing"
- Good: "Validate inputs at system boundaries (see `<input_validation_rules>` for requirements)"

**Tag attributes:**
- Attributes carry metadata distinct from content: `<example type="good">`, `<quote source="SICP">`
- Use sparingly; content inside tags receives more attention than attributes
- Never put critical behavioral guidance in attributes—it may be overlooked
- Good uses: source attribution, example classification, conditional context markers

**Position matters (primacy bias):**
Content earlier in a tag receives more attention than content later. At the document level, placing long reference material at the top with instructions and queries at the bottom improves response quality by up to 30% on multi-document inputs.[^3] Within sections, structure accordingly:
- Put the most important guidance first within each section
- Lead with critical constraints, follow with elaboration
- If ordering a list by priority, highest priority items should come first

**Tag granularity:**
- Every markdown header's content should be wrapped in an XML tag
- This creates 1:1 correspondence between visual structure (headers) and semantic structure (tags)
- Too coarse: One tag wrapping multiple unrelated concepts under different headers
- Too fine: Tagging individual sentences or single list items
- Right-sized: Roughly 10-100 lines of conceptually unified content (approximately one header's worth)

**Combine XML with other techniques:**
- Multishot prompting: `<examples><example>...</example><example>...</example></examples>`
- Chain-of-thought: `<thinking>...</thinking><answer>...</answer>`
- Conditional sections: `<if_typescript>...</if_typescript>`

**Example structure:**
```markdown
## Section Title

<section_name>
Most important guidance first...

<subsection_name>
Nested content...
</subsection_name>

Elaboration and details follow...
</section_name>
```
</xml_tag_guidelines>

### Content Depth and Philosophy

<content_depth>
**Staff-level insights over junior-level checklists.**

**Include:**
- Philosophical foundations (the "why" behind practices)
- High-judgment principles experienced practitioners recognize
- Trade-offs, context-sensitivity, and when rules should be broken
- Distinctions less experienced practitioners miss
- Systems thinking, emergent behavior, second-order effects

**Avoid:**
- Basic syntax Claude knows from training
- Step-by-step tutorials on fundamental concepts
- Low-level implementation details unless they affect judgment
- Overly granular instructions that constrain rather than guide

**Exception—Safety constraints are valuable even for well-known content:**
Safety guardrails should be included even if Claude "knows" them. These constrain *toward* safety, not away from good behavior. Distinguish "teaching content" (condense) from "safety guardrails" (keep).
</content_depth>

### Directive Language

<directive_language>
**Skills are prompts. Directive intensity directly affects model behavior.**

Opus 4.5/4.6 overtriggers on aggressive language.[^3] Directives like "CRITICAL: You MUST use this tool" or "ALWAYS check before proceeding" cause excessive tool invocation, unnecessary exploration, and overengineering. Sonnet 4.6 follows instructions literally and precisely — aggressive language won't cause overtriggering, but it adds no value over calm, direct statements.

Write skill content the way you'd brief a senior colleague: clear, direct, without shouting.

| Instead of | Write |
|------------|-------|
| "CRITICAL: You MUST..." | "Use [tool] when..." |
| "ALWAYS check..." | "Check [condition] before..." |
| "NEVER do X" | Describe the desired behavior instead |
| "If in doubt, use [tool]" | "Use [tool] when it would improve your understanding" |

**Prefer positive framing.** Describe desired behavior rather than listing prohibitions. "Compose smoothly flowing prose paragraphs" outperforms "Do not use markdown" across all tiers.[^3] This applies at every level of skill content — from high-level behavioral guidance to specific output formatting instructions.

**Include 3-5 few-shot examples** when a skill needs to demonstrate output format, tone, or reasoning patterns.[^3] Wrap them in `<examples><example>...</example></examples>` tags. Choose diverse examples that cover edge cases; quality and variety matter more than quantity. For skills targeting Haiku in multi-tier systems (e.g., sub-agent tasks), scaling to 10 examples can close the performance gap with higher tiers.

This connects to the "retrieval trigger" philosophy in `<skill_scope>`: if skills activate existing knowledge, aggressive directives are counterproductive. They constrain behavior rather than activating capability. The right prompt intensity is the minimum needed to reliably activate the desired behavior.
</directive_language>

### Decision Frameworks

<decision_frameworks>
**Focus on WHEN/WHY, not WHAT/HOW.**

Skills should help identify when to use patterns, not teach how to write basic syntax. Include:
- Decision trees and trade-off analyses
- "When to use what" tables
- Context-dependent guidance
- Judgment frameworks for ambiguous situations

**Example format:**
```markdown
| Context | Approach | Why |
|---------|----------|-----|
| Short-lived, personal branch | Rebase | Linear history |
| Shared/public branch | Merge | Preserve collaboration |
| Audit requirements | Merge | Full history trail |
```
</decision_frameworks>

### Common Mistakes Sections

<common_mistakes_guidelines>
**Every skill should include common mistakes organized by background.**

Structure mistakes by where practitioners are coming from:
- `<from_java>` - Mistakes Java programmers make
- `<from_python>` - Mistakes Python programmers make
- `<from_bash>` - Mistakes bash users make
- `<general_anti_patterns>` - Universal mistakes

**Why background matters:** Different backgrounds create different blind spots. A Java programmer learning Clojure makes different mistakes than a Python programmer learning Clojure.

**Format:**
```markdown
### Common Mistakes

<common_mistakes>
#### From Java Users

<from_java>
- **Using class hierarchies**: Clojure prefers composition via protocols
- **Expecting mutable state**: Atoms/refs for coordinated state changes
</from_java>

#### From Python Users

<from_python>
- **Using None for missing values**: Use nil, but prefer explicit optionality
- **Imperative loops**: Use sequence operations (map, filter, reduce)
</from_python>
</common_mistakes>
```
</common_mistakes_guidelines>

### Cross-References

<cross_reference_guidelines>
**Reference authoritative skills; briefly restate critical principles.**

**Strategy:**
1. **Primary reference**: Point to authoritative skill for detailed guidance
   - "See `opinionated-software-engineering:test-driven-development` skill for general testing philosophy"
2. **Insurance duplication**: Restate essential principles briefly (1-2 sentences)
   - Core philosophy can be restated in case referenced skill not loaded
   - Critical "never do X" rules worth repeating
3. **Balance**: Enough context to work standalone, not so much that skills become redundant

**When to reference vs. duplicate:**
- Reference when: Detailed guidance, examples, multiple subsections
- Brief restatement when: Core principle is critical to this skill's domain
- Full duplication when: Never (indicates architectural problem)

**Example:**
```markdown
## Testing

**For general testing philosophy, see the `opinionated-software-engineering:test-driven-development` skill.**
Core principle (restated): Tests are contracts—fix implementation, not tests.

This section covers language-specific practices...
```
</cross_reference_guidelines>

### Resources Section

<resources_guidelines>
**Only include machine-readable resources.**

**Include:**
- Written documentation (HTML, Markdown, PDF)
- API references and generated docs
- GitHub repositories (especially with .md files)
- Local file paths (Xcode docs, language references)
- Style guides and written tutorials

**Never include:**
- Video resources (WWDC, YouTube, etc.)—Claude cannot watch videos
- Paywalled content without local copies
- Resources requiring authentication
- Quotes or paraphrases from content that don't explicitly allow reuse or wouldn't clearly be fair-use

**Local documentation is especially valuable:**
- Can be read without network calls
- Available in air-gapped environments
- Often more stable than web URLs
- Usually faster to access

**Format:**
```markdown
## Resources

<resources>
**Official:**
- [Language Documentation](https://docs.example.com/)
- [Style Guide](https://github.com/example/style-guide)

**Local:**
- `/path/to/local/docs/`
- Man pages: `/usr/share/man/man1/tool*.1`
</resources>
```
</resources_guidelines>

### Description Field Optimization

<description_optimization>
**The description field is critical for skill discovery.**

The `description` in YAML frontmatter determines when Claude invokes the skill. Include:
- WHAT the skill does
- WHEN Claude should use it
- Trigger terminology users would mention

**Good example:**
```yaml
description: Fish shell scripting judgment frameworks and critical idioms. Use when writing Fish scripts or shell automation. Focuses on when to use Fish vs bash, macOS/Fedora compatibility requirements, and Fish-specific patterns that prevent bugs.
```

**Bad example:**
```yaml
description: Fish shell scripting.
```

**Max length:** 1024 characters per description. But there's also a collective budget: all skill descriptions share 2% of the context window (fallback: 16,000 characters). If total descriptions exceed this, some skills get excluded entirely. This means concise descriptions aren't just good practice — they're a shared resource. A verbose 900-character description crowds out other skills.
</description_optimization>

### Content Assessment

<content_assessment>
**Assess what Claude knows vs. what needs detail.**

| Knowledge State | Treatment |
|-----------------|-----------|
| Well-known from training | Condense to principles and frameworks |
| After training cutoff | Include detail, examples, patterns |
| Known problem area | Justify expanded coverage |

**Example assessment (Swift skill):**
- Swift 6 concurrency (~470 lines): After cutoff, known problem → detailed coverage justified
- Protocol syntax (~30 lines): Known well → condensed to judgment framework
- Basic value types (~20 lines): Known well → brief guidance only

**Target lengths:**
- Comprehensive language skill: ~400-700 lines
- Process/standard skill: ~150-300 lines
- If exceeding 1000 lines, reconsider what can be condensed
</content_assessment>
</quality_guidelines>

## Research Phase

<research_phase>
**Use agents to research skill content before writing.**

### When to Research

Research is warranted when:
- Creating a skill for a domain you're not expert in
- Covering content after training cutoff
- Including tool/library documentation that may have changed
- Wanting to cite authoritative sources

### Research Process

<research_process>
1. **Scope the research**: Define specific questions the skill must answer
2. **Delegate to a research-specialist agent**: Use `subagent_type='opinionated-research:research-specialist-basic'` for standard research or `subagent_type='opinionated-research:research-specialist-complex'` for deep, multi-faceted topics
3. **Specify output requirements**: Request structured findings with URLs for citation
4. **Synthesize results**: Integrate research into skill content with proper citations

**Example research prompt:**
```
Research the current best practices for [topic]. Specifically:
1. What are the official documentation sources?
2. What tooling is recommended by the community?
3. What are common mistakes practitioners make?
4. What has changed since [date]?

Return findings with URLs for each source so I can create proper citations.
```
</research_process>

### Research Agent Configuration

For skill research, configure the `opinionated-research:research-specialist-basic` agent:
- **Tools needed**: WebSearch, WebFetch, Exa (web + code), Kagi (private search + summarizer)
- **Privacy note**: Use Kagi for sensitive topics; Exa does not keep queries confidential
- **Output format**: Request URLs as source identifiers for citation

### Documenting Research

After research, create a research summary in the skill directory:
- File: `references/research-notes.md` (or similar)
- Include: Sources consulted, key findings, URLs for citation
- Purpose: Enables future skill updates with source traceability
</research_phase>

## Citation Requirements

<citation_requirements>
**All third-party content must be attributed. Use formal ACM citations when the source adds value.**

### What Requires Attribution

<citation_scope>
**Distinguish attribution from formal citation:**
- **Attribution**: Acknowledging the source (always required for third-party content)
- **Formal ACM citation**: Full bibliographic reference with footnote (sometimes required)

**Must attribute:**
- Direct quotes from any source
- Specific claims attributed to sources
- Statistics, benchmarks, or empirical findings
- Code patterns adapted from specific sources
- Well-known concepts with identifiable originators

**Informal attribution is sufficient for:**
- Short quotes (single sentences) — use `"quote" — Author, Source Work`
- Well-known aphorisms where author is the key information
- Cases where the source work is widely known (e.g., SICP, "Simple Made Easy")

**Formal ACM citations are warranted when:**
- The source would be useful for Claude to look up (URLs, documentation)
- Fair-use concerns exist (substantial portions, not just short quotes)
- Content substantially paraphrases a source (cite the source being paraphrased)
- Statistics or empirical claims need verification
- Code or patterns are adapted from a specific source

**Does not require attribution:**
- General programming knowledge without an identifiable originator (e.g., "functions should do one thing")
- Claude's own analysis and synthesis
- Content the skill author created

**Judgment call:** When in doubt, attribute. Formal citation when the source adds value.
</citation_scope>

### Formal Citation Format

<citation_format>
**When formal citations are warranted, use ACM style with Markdown footnote syntax.**

**In-text citation:** Use Markdown footnote references: `[^1]`, `[^2]`

**Reference list format:**
```markdown
## Sources

<sources>
[^1]: Author Name. Year. Title. Publication venue. URL or DOI

[^2]: Organization. Year. Document Title. Retrieved [Date] from URL
</sources>
```

**Example citations:**
```markdown
Rich Hickey's "Simple Made Easy" talk[^1] distinguishes simplicity from ease...

## Sources

<sources>
[^1]: Rich Hickey. 2011. Simple Made Easy. Strange Loop Conference. Retrieved November 24, 2025 from https://www.infoq.com/presentations/Simple-Made-Easy/

[^2]: ACM. 2023. Reference Formatting. Retrieved November 24, 2025 from https://www.acm.org/publications/authors/reference-formatting
</sources>
```

**Why Markdown footnotes:** Footnote syntax (`[^1]`) renders properly in Markdown viewers, creates clickable links to sources, and distinguishes citations from array indexing or other bracket uses in technical content.
</citation_format>

### Citation Accuracy

<citation_accuracy>
**Never fabricate bibliographic details.**

- Verify DOIs resolve correctly before including
- Use actual access dates, not invented dates (when adding citations retroactively, use the date content was originally retrieved, not the current date)
- If uncertain about any field, omit it rather than guess
- Mark uncertain information as `[unverified]`
- Prefer incomplete but accurate over complete but fabricated
</citation_accuracy>

### Source Verification

<source_verification>
**Training data is not verification. Use tools to confirm sources before citing.**

Memories from training are hypotheses, not facts. Before adding any citation:

1. **Verify URLs exist** — Fetch the URL to confirm it resolves and contains relevant content
2. **Verify quotes are accurate** — Search for the exact quote; paraphrased memories often drift from originals
3. **Verify attributions** — Confirm who actually said something; community interpretations often get misattributed to authoritative sources (e.g., "Apple says..." when it's actually a blog post)
4. **Verify content matches claim** — Read the source to confirm it supports what you're citing it for

**When verification tools are available (WebFetch, WebSearch, Kagi, Exa), use them.** The cost of a few tool calls is trivial compared to publishing incorrect citations.

**Common verification failures:**
- Attributing secondary interpretations to primary sources (e.g., a blogger's synthesis cited as official documentation)
- URLs constructed from memory that return 404 or redirect elsewhere
- Quotes that are paraphrases or composites of what was actually said
- Version-specific claims stated as fact without verification

**Verification workflow:**
1. Draft citations based on memory
2. Before finalizing, verify each citation with appropriate tools
3. Correct or remove citations that don't verify
4. Note in commit message that sources were verified
</source_verification>

### Common Citation Mistakes

<citation_mistakes>
**Lessons learned from skill validation:**

- **"Unknown" attributions** — Verify before accepting. Quotes attributed to "Unknown" often have identifiable sources (e.g., "Time is a device..." is Ray Cummings, 1922)
- **Incomplete quotes without ellipses** — If quoting a sentence fragment, end with `...` to indicate incompleteness
- **Unsourced statistics** — Specific numbers (e.g., "58% adoption", "100x slower") require sources. If no source exists, either find one, remove the claim, or qualify it (e.g., "significant performance issues" instead of "100x slower")
- **Informal documentation references** — "From the X documentation" is insufficient. Cite formally: `[^1]: Author. Title. URL`
- **Paraphrased official guidance without disclosure** — If a skill substantially paraphrases official documentation (like style guides), add upfront disclosure: "This skill synthesizes and paraphrases the official X guidelines."
- **Assuming well-known means no attribution needed** — Named concepts (Liskov Substitution Principle, Test Pyramid) should acknowledge their originators. Informal attribution is fine when the name itself attributes (e.g., "Liskov Substitution Principle" names Liskov); formal citation when the source would be useful to look up.
</citation_mistakes>
</citation_requirements>

## Validation Phase

<validation_phase>
**Validate skill content before finalizing.**

### Content Validation Checklist

<content_validation>
Before completing a skill, verify:

**Structure:**
- [ ] YAML frontmatter has `name` and `description`
- [ ] Description includes WHAT and WHEN (max 1024 chars)
- [ ] Opens with `<skill_scope skill="skill-name">` containing related skills
- [ ] Major sections use XML tags with `snake_case` names
- [ ] Cross-references point to correct skill names

**Content Quality:**
- [ ] Focuses on judgment frameworks, not basic mechanics
- [ ] Includes decision tables for context-dependent guidance
- [ ] Has common mistakes section organized by background
- [ ] Safety constraints are explicitly stated
- [ ] Directive language uses calm, direct framing (see `<directive_language>`)
- [ ] Resources are machine-readable (no videos)

**Attribution and Citations:**
- [ ] All third-party content is attributed (author + source work)
- [ ] Formal ACM citations used where warranted (see `<citation_scope>`)
- [ ] Sources verified with tools, not just memory (see `<source_verification>`)
- [ ] URLs fetched to confirm they exist and contain claimed content
- [ ] Quotes verified against original source (not paraphrased from memory)
- [ ] Attributions confirmed (e.g., "Apple says" actually comes from Apple)
- [ ] Sources section uses proper format
- [ ] No probable plagiarism
- [ ] Incomplete quotes end with ellipses
- [ ] No "Unknown" attributions (verify or remove)
- [ ] Quantitative claims have sources (or are qualified)
- [ ] Substantial paraphrasing cites the source

**Consistency:**
- [ ] No conflicts with related skills
- [ ] Cross-references align with target skill content
- [ ] Terminology is consistent throughout
</content_validation>

### Empirical Validation

<empirical_validation>
**Skills are iteratively refined based on actual usage.** Walk the user through the process of validating a skill.

After creating a skill:
1. Test in a clean context window
2. Observe whether the skill triggers appropriately
3. Note where Claude struggles or over-constrains
4. Refine based on observations

**Evaluation questions:**
- Does the skill trigger when expected?
- Does Claude apply the guidance correctly?
- Are there gaps where Claude lacks needed information?
- Are there constraints that hurt more than help?
- Does the skill behave consistently across Opus and Sonnet? A directive that works well on one tier may overtrigger or underperform on the other (see `<directive_language>`).
</empirical_validation>

### Plagiarism and Citation Validation

<plagiarism_validation>
**For skills intended for publication, run systematic plagiarism checks.**

**Parallel agent validation:** Launch multiple agents simultaneously to check each skill file. Each agent should:
1. Read the skill file
2. Identify passages that sound copied (unusual phrasing, tone shifts)
3. Flag quotes or claims lacking citations
4. Check for specific statistics or unique phrases without sources
5. Report assessment: clean / needs-review / likely-plagiarized

**Example prompt for validation agent:**
```
Read [skill file] and check for potential plagiarism. Look for:
1. Text that sounds copied from external sources
2. Quotes or specific claims lacking citations
3. Statistics or unique phrases without sources
Report: File path, suspicious passages with line numbers, assessment.
```

**Post-validation:** Address all flagged issues before publication. Even "clean" files may have minor citation improvements identified.
</plagiarism_validation>

### Related Skill Consistency

<consistency_validation>
When creating or updating a skill, check for conflicts with related skills:

1. **Identify related skills** that might contain similar guidance
2. **Read full sections**, not just grep for keywords (conflicts may be conceptual)
3. **Check for principle conflicts**, not just terminology differences
4. **Update all related skills** when refining a principle
</consistency_validation>
</validation_phase>

## Skill Creation Process

<creation_process>
Follow this process in order, skipping steps only with clear justification.

### Step 1: Understand the Skill Purpose

<step_understand>
**Goal:** Clearly define what the skill does and when it should be used.

**Activities:**
1. Identify concrete examples of how the skill will be used
2. Determine what triggers should invoke this skill
3. Clarify what related skills exist and how this differs
4. Establish the skill's scope boundaries

**Questions to answer:**
- What problem does this skill solve?
- What would a user say that should trigger this skill?
- What existing skills are related, and how does this differ?
- What is explicitly OUT of scope?

**Complete when:** Clear purpose statement and scope boundaries established.
</step_understand>

### Step 2: Research Content

<step_research>
**Goal:** Gather authoritative information for skill content.

**Activities:**
1. Identify what content requires research (vs. existing knowledge)
2. Use `opinionated-research:research-specialist-basic` (or `opinionated-research:research-specialist-complex` for deep topics) for unfamiliar domains
3. Collect URLs and sources for citation
4. Document research findings for future reference

**Skip when:** Creating a skill for a domain you're already expert in, with no post-cutoff content.

**Complete when:** All necessary information gathered with source attribution.
</step_research>

### Step 3: Plan Skill Architecture

<step_plan>
**Goal:** Design the skill's structure and identify reusable components.

**Activities:**
1. Outline major sections with XML tag names
2. Identify what belongs in SKILL.md vs. references/
3. Determine if scripts or assets are needed
4. Plan cross-references to related skills

**Architectural questions:**
- What decision frameworks are needed?
- What common mistakes should be documented?
- What safety constraints are critical?
- What content can Claude retrieve from training vs. needs explicit inclusion?

**Complete when:** Clear outline with section structure and resource allocation.
</step_plan>

### Step 4: Initialize the Skill

<step_initialize>
**Goal:** Create the skill directory structure.

**For new skills**, use the init script in Anthropic's `skill-creator:skill-creator` skill if available:
```bash
scripts/init_skill.py <skill_name> --path <output_directory>
```

**Manual initialization:**
```bash
mkdir -p skill-name/{scripts,references,assets}
touch skill-name/SKILL.md
```

**Skip when:** Iterating on an existing skill.

**Complete when:** Directory structure exists with SKILL.md template.
</step_initialize>

### Step 5: Write the Skill

<step_write>
**Goal:** Create the skill content following quality guidelines.

**Writing principles:**
- Use imperative/infinitive form ("To accomplish X, do Y")
- Apply XML tags to major sections
- Focus on judgment frameworks over mechanics
- Include decision tables for context-dependent guidance
- Organize common mistakes by background
- Add cross-references with brief principle restatement

**Order of writing:**
1. YAML frontmatter (name, description)
2. `<skill_scope skill="skill-name">` with related skills and purpose
3. When to use section
4. Core content sections with XML tags
5. Common mistakes section
6. Resources section
7. Sources section (citations)

**Complete when:** All content written with proper structure.
</step_write>

### Step 6: Validate the Skill

<step_validate>
**Goal:** Ensure skill meets quality standards.

**Activities:**
1. Run through content validation checklist
2. Verify all citations
3. Check for conflicts with related skills
4. Test in clean context window if possible

**Complete when:** All validation checks pass.
</step_validate>

### Step 7: Iterate Based on Usage

<step_iterate>
**Goal:** Refine skill based on actual performance.

**Iteration triggers:**
- Skill doesn't trigger when expected
- Claude applies guidance incorrectly
- Gaps where Claude lacks information
- Over-constraints that hurt performance

**Iteration process:**
1. Observe skill in use
2. Identify specific problems
3. Determine root cause (content, structure, or description)
4. Make targeted changes
5. Re-validate

**Note:** Skill refinement is ongoing. Document observations for future improvements.
</step_iterate>
</creation_process>

## Skill Tiers and Relationships

<skill_tiers>
**Skills exist in a hierarchy with fallback behavior.**

| Tier | Purpose | Example |
|------|---------|---------|
| Meta-skill | Universal principles | `opinionated-software-engineering:software-engineer` |
| Paradigm skills | Fallback for language families | `functional-programmer`, `object-oriented-programmer` |
| Language skills | Specific language guidance | `java-programmer`, `clojure-programmer` |
| Process skills | Situation-specific | `opinionated-software-engineering:test-driven-development`, `opinionated-software-engineering:git-version-control` |

**Invocation behavior:**
- Language-specific skills supersede paradigm skills (no redundant loading)
- Meta-skill (`opinionated-software-engineering:software-engineer`) invoked for all coding tasks
- Process skills invoked based on activity (testing, committing, etc.)

**Content placement:**
- System-level patterns (hexagonal architecture) → `opinionated-software-engineering:software-engineer`
- Paradigm-specific patterns (FP composition) → paradigm skills
- Language-specific syntax/tooling → language skills
- Universal processes (TDD, Git) → process skills
</skill_tiers>

## Anti-Patterns

<anti_patterns>
**Patterns that reduce skill effectiveness:**

### Content Anti-Patterns

- **Teaching basics**: Explaining concepts (e.g., map/filter/reduce) when Claude knows them from training
- **Aggressive directives**: Using "CRITICAL", "MUST", "ALWAYS" to force behaviors — causes overtriggering on Opus and adds no value on current Sonnet models (see `<directive_language>`)
- **Over-constraining**: So much detail that Claude can't apply judgment
- **Duplicate content**: Same information in multiple skills
- **Missing safety**: Not including critical guardrails because "Claude knows"

### Structure Anti-Patterns

- **No XML tags**: Unstructured content that's hard to navigate
- **Flat organization**: No hierarchy or progressive disclosure
- **Missing cross-references**: Island skills with no connection to ecosystem
- **Vague description**: Description that doesn't enable discovery

### Process Anti-Patterns

- **No research**: Creating skills for unfamiliar domains without investigation
- **No validation**: Shipping skills without verification
- **No iteration**: Treating skills as write-once artifacts
- **No citations**: Including third-party content without attribution
- **Memory as verification**: Treating training data memories as verified facts; citing URLs, quotes, or attributions without using tools to confirm accuracy
</anti_patterns>

## Resources

<resources>
**Official documentation:**
- Claude Code Skills: https://code.claude.com/docs/en/skills.md
- Claude Code Subagents: https://code.claude.com/docs/en/sub-agents.md
- Prompting Best Practices: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- XML Tagging Best Practices: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags

**Related skills:**
- `opinionated-software-engineering:software-engineer` - Design principles informing skill architecture
</resources>

## Sources

<sources>
[^1]: Anthropic. 2025. Use XML tags to structure your prompts. Retrieved November 24, 2025 from https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags.md

[^2]: Anthropic. 2025. Skills Documentation. Claude Code. Retrieved November 24, 2025 from https://code.claude.com/docs/en/skills.md

[^3]: Anthropic. 2026. Prompting best practices. Claude API Documentation. Retrieved March 1, 2026 from https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
</sources>
