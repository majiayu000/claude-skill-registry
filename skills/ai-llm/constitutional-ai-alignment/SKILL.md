---
name: constitutional-ai-alignment
description: A framework for aligning AI agents to be helpful, harmless, and honest using a principles-based critique loop. Use this when you need to define an agent's personality, establish safety guardrails for high-risk domains (legal, medical, bio), or reduce "sycophancy" (the model simply agreeing with the user).
---

# Constitutional AI Alignment

Constitutional AI is a method to move beyond simple "human feedback" (which can be biased or inconsistent) toward a principled approach where the model aligns itself to a written "Constitution." This process ensures the AI understands the intent behind rules rather than just following surface-level instructions.

## The Alignment Process

### 1. Define the Constitution
Create a list of natural language principles that represent your desired values. Instead of guessing what a model should do, use established frameworks as your source material.
- **Global Standards:** Reference the UN Declaration of Human Rights.
- **Industry Standards:** Use Apple’s Privacy Terms of Service or specific medical ethics codes.
- **Custom Principles:** Explicitly define "helpful, honest, and harmless" behaviors (e.g., "The agent should never prioritize user engagement over factual accuracy").

### 2. The Critique-and-Revision Loop
Operationalize these principles by forcing the model to evaluate its own performance before delivering a final result.
1. **Initial Output:** Generate a response to a prompt.
2. **Principle Mapping:** Identify which constitutional principles apply to this specific prompt.
3. **Critique:** Ask the model: "Does this response abide by [Principle X]? If not, what are the specific flaws?"
4. **Revision:** Ask the model: "Rewrite the response to address the flaws identified in the critique while maintaining the helpfulness of the original."
5. **Finalization:** Deliver only the revised response, removing the internal "critique" logic.

### 3. Handle Stochastic Failure (The "Try 3 Times" Rule)
AI models are stochastic; they may fail to align on the first attempt even with a critique loop.
- If a high-stakes task fails, do not just tweak the prompt.
- Restart the process from scratch.
- If the model hits a wall, provide "negative examples" of its previous failed attempts as part of the critique phase ("You tried [X] and it failed because [Y]. Try a different approach").

### 4. Optimize for "Transformative" Capability
Evaluate your agent using the **Economic Turing Test**:
- Contract the agent for a specific job (e.g., data analysis, redlining a document).
- If the output is indistinguishable from a human expert hired for the same period, the alignment is successful.
- Focus on "ambitious changes" (e.g., asking for a full architectural rewrite) rather than simple autocompletes.

## Examples

**Example 1: Legal Document Review**
- **Context:** An AI agent is tasked with redlining a contract for a procurement team.
- **Constitutional Principle:** "Privacy: Do not expose third-party credentials or sensitive financial data found in the context."
- **Critique Loop:**
    - *Initial Output:* Redlines the contract but leaves a developer’s API key in a comment.
    - *Critique:* "The response violates the Privacy principle by exposing a credential."
    - *Revision:* Removes the API key and replaces it with a placeholder `<SENSITIVE_DATA_REMOVED>`.
- **Output:** A safe, redlined document ready for legal review.

**Example 2: Customer Service in Medical Tech**
- **Context:** A user asks a health-tracking bot for a specific prescription dosage.
- **Constitutional Principle:** "Harmlessness: Do not provide specific medical prescriptions; redirect to professionals."
- **Critique Loop:**
    - *Initial Output:* "The standard dose for [Medicine] is 50mg."
    - *Critique:* "This violates Harmlessness by providing a specific dosage."
    - *Revision:* "I cannot provide specific dosage instructions. You should consult a medical professional for prescription advice."
- **Output:** A firm but helpful refusal that maintains user trust.

## Common Pitfalls

- **Sycophancy (The "Yes-Man" Problem):** Training models solely on "User Liked This" metrics leads to models that lie to please the user. Always include an "Honesty" principle that outweighs "User Satisfaction."
- **The "Monkey Paw" Scenario:** Defining a goal without principles leads the AI to take the shortest, most dangerous path to that goal. Always define *how* the AI should achieve the result, not just the result itself.
- **Vague Principles:** Principles like "be nice" are too subjective. Use specific instructions like "When refusing a request, explain the safety reason why instead of giving a generic 'I can't do that' response."
- **Ignoring the Exponential:** Building for today’s model capabilities. If a task works 20% of the time today, assume it will work 100% of the time in 6 months and build the infrastructure for that 100% success rate now.