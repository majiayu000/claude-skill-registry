---
name: communication-style-preservation
version: 1.0.0
description: |
  Preserve and apply the user's unique bilingual French/English communication style. Use when drafting,
  editing, or refining communications to maintain casual-professional tone, code-switching patterns,
  and specific formulas. Key elements: (1) Bilingual structure (French base + English technical terms),
  (2) Casual but professional tone ("je suis preneur", "je capte pas", "ça devrait rouler"),
  (3) Structured flow (context → technical details → questions → sign-off), (4) Strategic emoji usage (🙏, 😅),
  (5) Direct mentions of @people and technical context
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Communication Style Preservation

You are tasked with preserving the user's unique bilingual French/English communication style while improving message structure and clarity.

## The User's Communication Style

The user communicates in a distinctive way that blends French and English naturally:

### Core Patterns

**1. Bilingual Code-Switching**
- Use French sentence structures and connectors
- Incorporate English technical terms naturally (code, PR, sprint, API, deployment)
- Keep casual French expressions: "je suis preneur", "je capte pas", "ça devrait rouler"
- Technical details in English, framing in French

**2. Casual-Professional Tone**
- Professional but approachable
- Avoid overly formal language
- Use natural, conversational French for context and questions
- Technical precision in English terms

**3. Message Structure**
1. **Context**: Brief situational setup in French
2. **Technical Details**: Specifics in English (code references, PR links, sprint info)
3. **Questions**: Clear, direct questions in French
4. **Sign-off**: Brief closing with appropriate emoji

**4. Emoji Usage**
- 🙏: Requests for help or feedback
- 😅: Self-deprecation or acknowledging confusion
- :prière: Urgent requests
- Use sparingly and strategically

**5. Context & Mentions**
- Always mention relevant @people
- Include specific technical context (ticket IDs, PR numbers, sprint names)
- Reference past conversations when relevant

## When to Use This Skill

Use this skill when:
- Drafting messages to the team
- Responding to technical discussions
- Asking questions about code or deployments
- Providing updates on work
- Requesting reviews or feedback

## Key Formulas to Apply

**Opening context:**
- "J'ai regardé pour [X]..."
- "Petit point sur [X]..."
- "Je suis en train de [X]..."

**Technical references:**
- Link to PRs: "PR #123"
- Ticket references: "RD-4450"
- Sprint context: "pour le sprint XYZ"

**Asking for help:**
- "Je suis preneur si tu peux regarder 🙏"
- "Tu captes ce que je veux dire ?"
- "Ça me semble bizarre"

**Acknowledging uncertainty:**
- "Je capte pas trop le comportement de..."
- "Y a un truc que je pige pas là 😅"

**Sign-offs:**
- "Ça devrait rouler"
- "Merci d'avance ! 🙏"
- "Dis-moi ce que tu en penses"

## Output Guidelines

1. **Structure first**: Always follow context → details → questions → sign-off
2. **Bilingual balance**: Mix French and English naturally based on content type
3. **Keep technical precision**: Don't translate technical terms
4. **Maintain tone**: Casual but never unprofessional
5. **Be specific**: Include PR numbers, ticket IDs, specific files when relevant

## Examples

See [examples.md](references/examples.md) for before/after comparisons showing style preservation.

For detailed pattern documentation, see [style-patterns.md](references/style-patterns.md).

## Common Mistakes to Avoid

- ❌ Translating technical terms into French (use "PR" not "demande de pull")
- ❌ Being too formal (avoid "Pourriez-vous s'il vous plaît")
- ❌ Losing the emoji (use 🙏 not nothing)
- ❌ Removing @mentions (always include relevant people)
- ❌ Forgetting to link specific technical context (PR #, ticket ID)
- ❌ Being too casual (avoid slang that's unprofessional)

## Process

1. Identify the communication type (question, update, request, etc.)
2. Choose appropriate formula from the patterns
3. Structure the message: context → details → questions → sign-off
4. Apply bilingual code-switching naturally
5. Add strategic emojis and @mentions
6. Verify technical precision (PR numbers, ticket IDs, files)
