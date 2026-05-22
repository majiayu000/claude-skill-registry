---
name: ai-product-strategy-mapping
description: A framework to assess and integrate AI into your product strategy by mapping core customer problems to AI capabilities. Use this when your industry is facing a major technology shift, when prioritizing an AI roadmap, or when deciding between augmenting existing features vs. building new AI-first solutions.
---

# AI Product Strategy Mapping

The "Meteor Framework" is a method for radically rethinking your product in the face of the AI shift. Rather than treating AI as a "bolt-on" feature, this framework forces you to evaluate whether your core value proposition is in the path of the "AI meteor" and determine if your product should be augmented or entirely replaced by AI-driven workflows.

## The Strategy Workflow

### 1. Define the Core Premise
Before looking at the technology, return to first principles. Strip away your current UI and features.
*   Identify the core problem your product solves.
*   Define why people use it and what specific value they derive.
*   Ask: "What is the job the customer is hiring us to do?"

### 2. Map AI Capabilities to the Problem
Evaluate your core premise against the specific technical strengths of Large Language Models (LLMs). Determine if AI can perform the following tasks better than your current manual or rule-based workflows:
*   **Synthesis:** Summarizing text, scanning images, or parsing data.
*   **Generation:** Writing text, code, or creating multimedia.
*   **Reasoning:** Answering complex queries or making deductions based on data.
*   **Action:** Taking real-world steps (e.g., "Change my flight," "Refund this customer").

### 3. Determine the Integration Model
Decide how the AI will interact with your existing product structure.
*   **Replacement:** The AI does the job entirely (e.g., an AI bot answering a support ticket instead of a human).
*   **Augmentation:** The AI acts as a "copilot" or assistant to the user (e.g., suggesting a reply for a support agent to edit).
*   **Vertical Specialization:** Determine if you need a specialized LLM for your specific industry data or if building on top of general models (OpenAI, Anthropic) is sufficient.

### 4. Implement via Generalist Teams
Avoid creating a siloed "AI Team." Instead:
*   Embed machine learning experts into existing product squads.
*   Train generalist PMs and Designers to understand AI capabilities.
*   Focus on the user experience of AI interjections (e.g., "How and when should the assistant suggest an answer?").

## Examples

**Example 1: Customer Support (Intercom's "Fin")**
*   **Core Premise:** Customers need fast, accurate answers to support questions.
*   **AI Mapping:** LLMs can scan a knowledge base and reason through a solution.
*   **Application:** Transition from "Conversational Support" (human-to-human) to "AI-First Support" where the bot is the first line of defense.
*   **Output:** An AI chatbot that resolves 50-70% of inbound queries without human intervention.

**Example 2: Data Reporting & Visualization**
*   **Core Premise:** Users need to understand their business performance data to make decisions.
*   **AI Mapping:** LLMs can query databases and summarize trends using natural language.
*   **Application:** Move away from complex dashboard-building UIs (Tableau-style) to a "Single Box" interface.
*   **Output:** A natural language interface where a user asks, "Who was our top salesman in January?" and receives an immediate answer instead of a chart.

## Common Pitfalls to Avoid

*   **The "Bolt-On" Mistake:** Adding a "summarize" button to an old workflow rather than rethinking if the workflow is still necessary. AI should be foundational, not an accessory.
*   **The Sunk Cost Trap:** Protecting old "Table Stakes" features (like complex manual reporting) that AI has rendered obsolete. If AI can do it better, be willing to "bet the farm" on the new version.
*   **Waiting for Certainty:** Treating AI like a hype cycle (e.g., Crypto/Web3). AI is a "before/after" technology shift; waiting for the market to settle will leave you behind.
*   **Over-specializing the Team:** Hiring only ML specialists and keeping them separate from the product. This prevents the "product sense" from being applied to the AI's capabilities.
*   **Ignoring the "Story":** Building great AI tech but failing to explain *why* it’s better for the customer. Ensure your "Product-Market-Story Fit" accounts for the AI’s value.