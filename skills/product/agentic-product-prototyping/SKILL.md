---
name: agentic-product-prototyping
description: Build functional software prototypes and MVPs without deep technical skills by using AI agents as "developers in your pocket." Use this skill when you need to validate a new product concept, build custom back-office tools (e.g., a real estate data manager), or create high-fidelity demos to unblock engineering roadmaps.
---

# Agentic Product Prototyping

This skill allows product managers and founders to bypass the traditional "design-to-engineering" bottleneck by acting as a "generative lead" who directs AI agents to build, deploy, and maintain software. By focusing on "AI-native coding"—understanding system components and debugging rather than syntax—you can reduce the cost of software creation to near zero.

## The Prototyping Workflow

### 1. Draft the "Super-Prompt" (The PRD)
Instead of a vague request, provide a structured prompt that mimics a Product Requirement Document. Define the stack and core functionality immediately.
- **Define the Stack:** Specify Node.js, React, or Python (or tell the agent to "choose the best modern stack for a web app").
- **List Core Features:** Use bullet points for specific functionality (e.g., "Voting system," "Kanban board for status tracking," "Admin dashboard").
- **Set Design Constraints:** Specify "Modern UI," "Responsive mobile view," or "User-friendly dashboard."
- **Define Data Persistence:** Explicitly ask for a database (e.g., Postgres) to ensure the app saves user data.

### 2. Monitor the "Multiplayer" Session
Observe the agent as it builds. Treat the agent as another user in your workspace.
- **Watch the Progress Pane:** Monitor the installation of packages and database schema creation.
- **Check for Proactive Fixes:** Agents often spot their own errors. Wait for the agent to attempt a self-repair before intervening.
- **Verify via Screenshots:** Ask the agent to take a screenshot of the homepage to verify the UI is rendering correctly before you even open the app.

### 3. Apply "AI-Native" Debugging
When the agent gets stuck (the "Gap"), your role is to unblock it.
- **Ask for the Admin Path:** If the agent builds an admin panel but you can't find it, ask: "How do I log into the admin panel?" or "Create an admin account for me using a SQL query."
- **Iterate on UI Pixels:** Use an assistant-style tool for small adjustments. Example: "Move this button 3 pixels to the left" or "Change the header color to match this hex code."
- **Unblock Migrations:** If a feature requires a database change, ask the agent to "Write the migration script" or use a side-chat (like Claude or ChatGPT) to help you understand the error and feed the solution back to the agent.

### 4. Deploy and Scale
- **One-Click Deployment:** Use integrated cloud services (e.g., Replit's Google Cloud abstraction) to get a live URL immediately.
- **Maintenance:** Use the agent to run periodic SQL queries or update packages.
- **Human-in-the-Loop:** If the agent reaches a fundamental architectural limit (like complex database sharding), use the prototype as a "live PRD" to hand off to a professional engineer.

## Core Principles: "Amjad's Law"
- **ROI on Learning to Code:** The return on investment for learning to *read* and *debug* code (not write it from scratch) doubles every six months as AI agents become more powerful.
- **Generative over Executional:** Your value shifts from "managing a process" to "generating ideas." The faster you can generate and test ideas, the more successful the product.
- **AI-Computer Interface (ACI):** Treat the environment as a computer designed for an AI. Give the agent tools (Shell access, SQL access, File editor) rather than just a chat box.

## Examples

**Example 1: Internal Feature Request Dashboard**
- **Context:** A PM needs a way for users to vote on upcoming features to help prioritize the roadmap.
- **Input:** A prompt specifying: "Build a Node.js web app where users can submit feature requests, upvote them, and I can move them from 'Planned' to 'In Progress' via an admin login."
- **Application:** The agent builds the Postgres schema for votes, the React front-end, and the auth for the PM.
- **Output:** A live URL the PM shares with the community to collect real data in 10 minutes.

**Example 2: Marketing Competitive Pricing Tool**
- **Context:** A Marketing Lead wants to monitor a competitor's pricing daily without manual checks.
- **Input:** "Build a Python app that scrapes [Competitor URL] daily, saves the price of 'Product X' to a database, and alerts me via Slack if it drops below $50."
- **Application:** The agent sets up a cron job (scheduled task), handles the web scraping logic, and integrates the Slack API.
- **Output:** A background tool that runs indefinitely, providing the team with a competitive edge.

## Common Pitfalls
- **The "Git" Trap:** Don't waste time learning low-level version control (Git) or environment configuration. Let the agent manage the "nonsense" and focus only on the app's logic and UI.
- **Vague Iteration:** Avoid saying "Make it better." Instead, say "Add a comment thread to the feature request page" or "Change the font to Inter."
- **Migration Errors:** AI agents can struggle with changing existing database structures. If an error occurs after adding a feature, ask the agent to "Show me the current database schema and tell me why the last change failed."
- **Over-Siloing:** Don't wait for a "final design" to start building. Use the agent to build the functional prototype first, then use a Figma-to-Code extension to clean up the pixels.