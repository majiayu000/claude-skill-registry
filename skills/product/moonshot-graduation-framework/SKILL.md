---
name: moonshot-graduation-framework
description: A framework for transitioning high-ambiguity R&D projects (Horizon 3) into operational product squads (Horizon 1). Use this when moving an experimental prototype to a permanent product team or when scaling a "moonshot" lab project into a commercial business line.
---

# Moonshot Graduation Framework

Innovation often dies during the handoff between R&D "labs" and the core product organization. This framework provides a structured process for ring-fencing experimental projects and successfully graduating them into production-grade products without losing the original vision or compromising operational excellence.

## 1. The Portfolio Allocation Model
Before starting a moonshot, establish clear resource boundaries to prevent "innovation theater" or resource starvation. Use the **5-30-60 Rule** for team capacity:

*   **5–10% Research (Horizon 3):** High-ambiguity, low-confidence moonshots with a 3–5 year payoff.
*   **25–30% Operations:** Maintaining current in-market products (security, privacy, uptime, accessibility).
*   **60% Incremental (Horizon 1):** Iterative improvements to existing products to realize ROI on previous bets.

## 2. The Graduation Trigger
Do not move a project out of R&D based on a calendar date. Transition only when these three signals are present:
1.  **Representative Signal:** A clear set of target customers has identified a genuine, recurring problem.
2.  **Novel Solution:** The prototype solves the problem in a way the customer could not achieve on their own.
3.  **Medium Confidence:** There is enough validation to justify "productizing" (investing in scale, security, and monetization).

## 3. The Transition Process (The "Seed" Model)
Avoid a "throw it over the wall" handoff. Follow this knowledge-transfer sequence:

### Step 1: Create the Hybrid Squad
Move the core researchers/innovators into a new "EPD" (Engineering, Product, Design) squad for a finite period. They provide the "seed" of expertise for the new product.

### Step 2: Establish the Persona
Define a metaphor for the product to guide ethical and UI decisions.
*   *Example:* GitHub framed Copilot as an "AI Pair Programmer." 
*   *Application:* If the AI behaves in a way a human pair programmer wouldn't (e.g., being offensive or distracting), the feature fails the persona test and must be filtered.

### Step 3: Backfill with Operators
Hire or transfer engineers who specialize in "fundamentals" (Uptime, Scale, Privacy). These operators build the "insulation" around the researchers, allowing the researchers to focus on vision while the product stabilizes.

### Step 4: Skill-Based Exit
Researchers should only return to the R&D team once their specific "seat" has been replaced by a permanent team member who has fully acquired the necessary domain expertise.

## Examples

**Example 1: Technical Infrastructure Transition**
*   **Context:** An R&D team creates an AI-powered code completion tool.
*   **Application:** Instead of asking the existing "Editor" team to build it, leadership creates a dedicated "Copilot Squad." They move 3 researchers to this squad and hire 4 production engineers to handle the 200ms latency requirements and GPU supply chain issues. 
*   **Output:** The researchers stay long enough to ensure the "AI logic" is sound, but the production engineers ensure the service doesn't crash at scale.

**Example 2: Ethics and Content Filtering**
*   **Context:** The AI model occasionally suggests offensive language or "toxic" code.
*   **Application:** Using the "Pair Programmer" persona, the team realizes a real human wouldn't shout slurs at a colleague. They implement a "Responsible AI" filter that detects sentiment and blocks offensive outputs, treating the AI as a professional teammate rather than just a text generator.

## Common Pitfalls

*   **Calendar-Based Handoffs:** Moving a project because "it’s been six months" rather than because the team has been successfully backfilled. 
    *   *Correction:* Base exits on "replacement in seat" status.
*   **Outsourcing Innovation:** Letting the R&D team continue to own the roadmap after graduation.
    *   *Correction:* The permanent EPD squad must own and control the roadmap to feel accountability for customer outcomes.
*   **Ignoring Fundamentals Early:** Treating security and privacy as "later" problems.
    *   *Correction:* Graduation requires a "Fundamentals Contract" where the team agrees to meet corporate standards for uptime and safety before the public launch.