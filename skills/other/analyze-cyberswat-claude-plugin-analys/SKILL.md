---
name: analyze
description: Use this skill when the user wants to analyze something and needs help choosing the right approach, persona, and command sequence. Suggests whether to use the full framework or lightweight /quick mode.
allowed-tools: [Read]
---

# Analyze

I need to analyze something. Help me figure out the right approach.

## Steps

1. **Identify the domains** What expertise areas are relevant to this subject?
   - **Primary domain**: The core expertise needed to analyze this topic
   - **Adjacent domains**: Other areas that could surface blind spots, such as security, legal, financial, operational, or UX

   If adjacent domains are relevant, note them for use in the critique cross domain flag.

2. **Generate rich personas** Create two to three fully formed personas. Each persona must include:
   - Specific role and seniority level
   - Years and type of experience
   - Industry or organizational context
   - Formative experiences that shape their perspective, such as projects shipped, failures witnessed, and lessons learned
   - What they prioritize and what they are skeptical of

   Mark one as recommended with rationale. The personas should be meaningfully different, not variations on the same viewpoint.

   **Persona anti pattern guidance**: Personas that differ only in tone or vocabulary are not meaningfully different. Each must arrive at a genuinely different prioritization. A "cautious CTO" and a "risk averse VP of Engineering" are the same persona wearing different titles. Test: if two personas would rank the same three concerns in the same order, collapse them into one and generate a genuinely distinct alternative.

3. **Assess complexity** Is this a full framework situation or would `analysis:quick` suffice?

   **Standard tier**: Use quick mode when:
   - Decision is easily reversible
   - Stakes are contained to one project or area
   - User has direct experience with this type of decision
   - Time constrained

   **Extended tier**: Use full framework when:
   - Decision is hard to reverse
   - Multiple stakeholders or domains affected
   - Operating outside familiar territory
   - The "obvious" answer feels too easy

4. **Identify the Key Question** What is the single most important question this analysis needs to answer? This becomes the through line for every subsequent step.

5. **Recommend the sequence** Which commands, in what order?

## Output

First, state the Key Question:

```
## Key Question
[The single most important question this analysis needs to answer]
```

Then present the personas in a clear format:

```
## Suggested Personas

### 1. [Role Title] ★ Recommended
[Full persona description: three to four sentences covering experience, context,
formative experiences, and what shapes their judgment]

**Why this lens:** [1 sentence on why this perspective fits the subject]

### 2. [Role Title]
[Full persona description]

**Why this lens:** [1 sentence]

### 3. [Role Title] if warranted
[Full persona description]

**Why this lens:** [1 sentence]
```

Then output the exact commands with the full recommended persona embedded.

**If adjacent domains were identified**, include a cross domain flag on the critique command:

```
/analysis:research [topic]. Approach as [full persona description].
/analysis:evaluate [topic]. Approach as [full persona description].
/analysis:critique [topic]. Approach as [full persona description]. Also flag concerns from a [adjacent domain expert].
/analysis:synthesize
/analysis:decide
```

**If no significant adjacent domains**, use standard critique:

```
/analysis:research [topic]. Approach as [full persona description].
/analysis:evaluate [topic]. Approach as [full persona description].
/analysis:critique [topic]. Approach as [full persona description].
/analysis:synthesize
/analysis:decide
```

**If using quick mode:**
```
/analysis:quick [topic]. Approach as [full persona description].
```

The user can copy these directly or substitute an alternative persona from the list.

Do not run anything yet. Just give me the plan and the commands.

## Available Commands

- `analysis:research` Gather external context, industry trends, evidence base
- `analysis:evaluate` Five perspectives: Informed, Steelman, Skeptic, Practical, Contrarian
- `analysis:critique` Adversarial: find fatal flaws, assumptions, failure modes. Supports optional cross domain flag: "Also flag concerns from a [domain expert]"
- `analysis:synthesize` Structured output: summary, recommendation, tradeoffs, open questions
- `analysis:decide` Decision landscape, type detection, commitment with reversal triggers and next action
- `analysis:quick` Lightweight mode: compressed analysis in a single pass

Subject: $ARGUMENTS
