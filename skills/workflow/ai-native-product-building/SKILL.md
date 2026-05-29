---
name: ai-native-product-building
description: Rapidly build, prototype, and deploy full-stack software using AI "text-to-app" tools. Use this when you need to create a greenfield application, build a high-fidelity working prototype for user testing, or bypass traditional engineering bottlenecks for internal tools.
---

AI-native product building shifts the Product Manager’s role from writing requirements for others to directly directing an AI agent to build the software. This approach reduces development time from months to weeks and costs by up to 99%.

## The "JIRA-Prompt" Framework
Treat every interaction with an AI agent (like Bolt) as if you are writing a high-quality ticket for a senior developer. 

### 1. Define the Technical Scope
Instead of general descriptions, provide the specific parameters the AI needs to spin up the environment:
*   **Identify the Core Functionality:** "Make a Spotify clone with streaming, playlists, and MP3 file support."
*   **Specify the Stack:** State the desired integrations (e.g., "Use Supabase for the database and Netlify for hosting").
*   **Provide Data Context:** Paste raw data (e.g., LinkedIn bio, CSV rows, or brand guidelines) directly into the prompt to give the AI context.

### 2. Balance Specification with "Vibes"
AI agents perform best when given a mix of rigid requirements and creative freedom.
*   **High Specificity:** Use this for business logic, data schemas, and user flows.
*   **The "Vibe" Prompt:** For UI/UX, use descriptive language rather than specific CSS. 
    *   *Example:* "Make it look like a high-end medical donation site—clean, professional, and trustworthy."
    *   *Example:* "Make it prettier and more modern."

### 3. Implement Iterative Debugging
When the AI gets stuck or produces an error:
*   **Screenshot Debugging:** Upload a screenshot of the UI issue or the error message and ask: "Fix this to match the intended design."
*   **The "Unstuck" Protocol:** If the AI fails after 3 attempts on a specific logic problem, move to a human-in-the-loop approach. Consult an expert or a developer to fix that specific "nook or cranny" while keeping the AI in charge of the broader codebase.

## Workflow: From Figma to Deployment

### Step 1: Design Extraction
Use the direct URL method to convert static designs into code:
*   Take your Figma design URL.
*   Prepend the AI tool's URL (e.g., `bolt.new/[FIGMA_URL]`).
*   Allow the agent to "suck in" the assets and layout to create the initial environment.

### Step 2: Live Prototyping
Instead of dragging frames in Figma, prompt the functional changes:
*   "Add a login page using Supabase Auth."
*   "Create a dashboard that pulls from the users table."
*   Test the app in real-time on your own device using QR code previews.

### Step 3: One-Click Deployment
Immediately move the app to a production URL:
*   Click "Deploy."
*   Connect to a hosting provider (Netlify/Vercel).
*   Attach a custom domain to transform the prototype into a live business.

## Examples

**Example 1: The "Zero-to-Market" CRM**
*   **Context:** An entrepreneur needs a custom CRM with Stripe billing but has no budget for a $30,000 agency.
*   **Input:** "Build a CRM for real estate agents. Include lead tracking, a Stripe integration for monthly subscriptions, and an AI-powered email drafter. Use a clean, blue-themed UI."
*   **Application:** Use Bolt to generate the base app. Iterate by saying "Add a column for 'Last Contacted Date'" and "Integrate the Stripe test key."
*   **Output:** A functional, revenue-generating SaaS product built in 3 weeks for ~$300 in inference costs.

**Example 2: Rapid Marketing Landing Page**
*   **Context:** A PM needs a landing page for a new feature experiment.
*   **Input:** [Paste LinkedIn Bio/Brand Specs] + "Create a personal portfolio site. Use a professional dark mode. Add a section for 'Current Projects' that I can edit easily."
*   **Application:** Generate the site, then prompt: "Add a contact form that sends entries to my email."
*   **Output:** A live, hosted URL ready for traffic in under 10 minutes.

## Common Pitfalls
*   **Legacy Code Migration:** Do not attempt to move a 20-year-old, thousand-file production codebase into a browser-based AI agent. Use these tools for greenfield projects or isolated "pods" like admin panels and marketing sites.
*   **Over-prompting the First Draft:** Avoid writing a 5-page prompt for the first version. Start with the "Spotify Clone" base and add features one-by-one to prevent the AI from getting confused.
*   **Ignoring Determinism:** Remember that code is deterministic—it either runs or it doesn't. If the AI produces a broken app, check if the environment (WebContainer) has finished booting before assuming the code is wrong.
*   **Treating it Like a Designer Only:** Don't just use it for UI. Leverage its ability to build "Full Stack" (databases, auth, APIs) to ensure the prototype is actually functional, not just a high-fidelity mockup.