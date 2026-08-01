---
name: detailed
description: Claude Code Skills and Agent Architecture in DiPeO
---

Claude Code Skills and Agent Architecture in DiPeO


Doc-Lookup Skill – Implementation and Configuration


The doc-lookup skill in DiPeO is a specialized documentation retrieval tool defined under .claude/skills/doc-lookup. It is configured via a SKILL.md file with YAML frontmatter specifying its name, description, and allowed tools. For example, the skill’s description notes that it “locate[s] and retrieve[s] specific documentation sections”, returning “minimal, targeted excerpts instead of full files”, and it is permitted to use the Read, Grep, Glob, and Bash tools. These permissions let the skill search file contents and execute a script in a sandboxed shell.


In implementation, doc-lookup relies on a Python helper script (section_search.py) to do the heavy lifting. When invoked (via a Bash tool call), this script parses the Markdown files in the docs/ directory and extracts sections by heading level (e.g. ##, ###). It then matches the query against documentation anchors or content and ranks the results by relevance. The matching logic prioritizes explicit anchor IDs (defined in the docs as {#anchor-id}) and implicit anchors (auto-generated from headings), then falls back to fuzzy heading text matches or keyword matches in the content. By using this deterministic script, the skill can reliably return the top 1–3 documentation sections relevant to a query (including the file path, section heading, anchor, and snippet content) without loading entire files into context. This design ensures the AI gets just the needed excerpt. For example, the router skills demonstrate usage like:


Skill(doc-lookup) --query "cli-commands" --paths docs/agents/backend-development.md --top 1



which under the hood runs:


python .claude/skills/doc-lookup/scripts/section_search.py --query "cli-commands" --paths docs/agents/backend-development.md --top 1



to fetch the “CLI Commands” section from the specified doc. The skill’s configuration thus consists of the SKILL.md (which educates Claude on when/how to use the skill) and the associated script and resources that actually perform the lookup.


Agent–Skill Architecture (“Thin Wrapper” System)


DiPeO employs a multi-tier agent and skill architecture to modularize the AI’s knowledge and tool use. At the core are several domain-specific agents (sub-agents) defined under .claude/agents/ (e.g. dipeo-backend.md, dipeo-frontend-dev.md, etc.). Each agent file specifies that agent’s role, scope, and persona (often including sections like what code areas “YOU OWN” vs “YOU DO NOT OWN” to delineate responsibilities). These agents are “full” problem solvers for their domain (e.g. backend, frontend, codegen), configured with a model (Claude variant) and given extensive context or documentation in their prompts. For instance, the dipeo-backend agent focuses on the FastAPI server, CLI, database, etc., and explicitly does not cover execution engine or codegen (those belong to other agents). If a task falls outside its domain, the agent knows to defer or escalate accordingly.


Complementing each full agent is a “router” skill for that domain – essentially a thin wrapper around the agent’s expertise. These router skills (found under .claude/skills/) are lightweight (on the order of 50–100 lines) and provide decision logic and quick reference anchors for documentation. For example, the dipeo-backend router skill’s SKILL.md lists criteria for when a backend task is simple enough to handle within the skill versus when to escalate to the full agent. Simple tasks (e.g. minor code changes under ~20 lines or single-file inquiries) are handled directly by the skill with minimal context, whereas complex tasks (multi-file features, architectural changes, cross-cutting concerns) trigger an escalation. The escalation is done by invoking the full agent through a special directive (e.g. Task(dipeo-backend, "Detailed task description")), effectively handing off to the larger agent with a fresh prompt focused on that task.


The router skills act as the first-line triage: they load quickly and cheaply to interpret the user’s request and either solve it or route it. They are integrated with the documentation system by referencing key doc sections via anchors. In practice, a router skill will often suggest using the doc-lookup skill for specific context. For instance, the dipeo-backend skill includes a list of documentation anchors (like #core-responsibilities, #common-patterns) and explicitly tells the assistant to use Skill(doc-lookup) to retrieve those sections on-demand. The router skill itself is allowed to call other skills (its frontmatter includes allowed-tools: ..., Skill enabling nested skill calls). This means the skill can dynamically pull in documentation or even defer to another skill/agent as needed.


Overall, the structure is hierarchical: user queries → router skill (domain decision & quick info) → optional doc-lookup skill (for detailed docs) → possibly escalate to full agent. This is all facilitated by Claude’s agent runtime. Claude’s Skill mechanism allows the AI to load a skill by name when it deems it relevant, and the Task mechanism allows spawning a sub-agent for complex tasks. The DiPeO repository’s .claude directory is organized exactly to leverage these capabilities of Claude’s code agent SDK. The integration is “thin” in the sense that there isn’t a lot of custom orchestration code – the agent skills framework itself orchestrates the behavior. The metadata (skill/agent definitions) is pre-loaded into Claude’s system prompt at session start, and Claude autonomously decides to load a skill or agent file when the situation matches its description. The DiPeO team only had to provide well-structured prompts and scripts; the Claude agent (especially when running via the Claude Code environment or Anthropic’s SDK) handles discovering and executing these skills.


Design Motivations and Goals


Why build this modular agent-skill system? The design appears driven by goals of modularity, efficiency, and maintainability, tightly aligned with Anthropic’s Claude capabilities. One major motivation is token economy. Rather than dumping all relevant project documentation or code context into every AI prompt, DiPeO uses progressive disclosure: the agent loads detailed information only when needed. According to the project docs, this yields a “80-90% token reduction vs. automatic injection” of docs. For example, a focused lookup of a CLI section might cost ~1.5K tokens with the skill, versus ~15K tokens if the entire backend guide were in context. This efficiency is crucial given large context windows and costly operations. It also keeps the model’s attention focused on the task at hand, reducing distraction from irrelevant content.


Another motivation is modularity and reuse of expertise. By packaging domain knowledge into independent agents and skills, each component can be updated or extended without affecting the others. Skills act like pluggable “expertise packages.” For instance, the doc-lookup skill is a reusable utility that any agent can invoke for documentation help, rather than duplicating doc-parsing logic in multiple agents. Likewise, the “router” logic (what to do or who should handle what) is kept separate from the detailed problem-solving. This separation of concerns makes the system more maintainable and transparent. It’s clear which agent is responsible for which aspect of the project (e.g. backend vs. frontend), and the decision criteria are explicitly documented in the router skill for that domain. If the project grows a new domain, a new agent and a thin router skill can be added in parallel, following the same pattern.


The design also leverages Anthropic Claude’s strengths and tooling. Claude’s Agent Skills feature is explicitly about allowing on-demand loading of instructions and code tools from files. DiPeO’s .claude/skills directory follows this pattern: each skill has a SKILL.md (for high-level guidance and trigger metadata) and can include scripts or reference files for detailed or procedural tasks. This suggests a deliberate intent to be compatible with Claude’s ecosystem – e.g. using the Bash tool to run Python scripts for deterministic operations like documentation search, which is exactly how Anthropic envisions mixing code with LLM reasoning. The rationale is that certain tasks (like searching text, parsing docs, or applying code transformations) are better done by code for accuracy and efficiency. By providing those as scripts (the doc lookup, code formatting, etc.), the agent doesn’t waste time or context tokens doing them via pure language prediction. This yields more reliability (the skill will return precise results from the actual repository docs, avoiding hallucinations) and ensures a single source of truth – the bot’s answers about DiPeO are grounded in the actual documentation content. It also prevents content drift: if documentation is updated, the skill will retrieve the updated info, rather than relying on stale hard-coded prompts.


In summary, the motivations include: saving tokens by loading context on demand, maintaining clear module boundaries between different knowledge areas, reusing tooling across tasks, and aligning with Claude’s agent skill interface for a more native, scalable AI integration. The result is an agent system that behaves more like a team of specialists that consult a library of knowledge when needed, rather than a monolithic prompt stuffed with everything.


Patterns, Best Practices, and Trade-offs


DiPeO’s implementation showcases several emerging best practices for AI agent design using skills:






Router + Specialist Pattern: They use a two-stage pattern where a lightweight router skill decides how to handle a user query, and either solves it directly or delegates it. This is explicitly documented in their workflow examples. For instance, “Pattern 2: Router → Doc-Lookup → Solve” shows the agent first loading a router skill for decision support, then using doc-lookup to fetch a specific ~50-line doc excerpt, and then proceeding to solve the problem. Only if necessary does it escalate to a full agent (Pattern 3). This progressive approach is a best practice for keeping interactions efficient and targeted, and DiPeO’s docs highlight its benefits (e.g. 80-90% token savings and more focused answers).






Stable Documentation Anchors: A notable practice is the use of stable, human-curated anchors in documentation for key topics. Each agent’s guide in docs/agents/ contains predefined heading IDs for important sections (for example, backend docs have anchors like #cli-implementation, #mcp-server, #database-schema). The skills reference these anchors when doing lookups. This system ensures that the agent can reliably pull the exact section it needs. It avoids ambiguity in searches and prevents the model from grabbing too much or too little context. The team even established conventions to only use Markdown heading IDs (and not HTML <a> tags) so that the doc-lookup parser catches everything. The trade-off here is some up-front effort to maintain those anchors and keep them updated as docs evolve, but it pays off in consistency. In effect, the documentation and the AI’s retrieval skill are co-designed for each other.






Minimal Prompt Wrappers (“Thin Skills”): The router skills themselves are kept concise – essentially playbooks around 50 lines as noted. They contain just the essential logic: what falls under this domain, when to use this skill vs. when to call in a bigger agent, and references to documentation. By keeping them thin, they introduce very little token overhead and minimize the chance of conflicting or outdated info. They serve as decision aides rather than full knowledge dumps. This modular, minimal style reduces complexity. A potential trade-off is that the AI (Claude) needs to correctly interpret when to load these skills; however, because Claude pre-loads each skill’s name and short description in the system prompt, it has a high-level index of when each skill is applicable. DiPeO’s skill descriptions are written clearly to aid this (for example, the doc-lookup skill’s description explicitly says when to use it, and the router skills describe the domain triggers in their frontmatter).






Use of Tools and Code: The integration of actual code execution as part of skills is a best practice exemplified by doc-lookup (and likely others like a testing or formatting skill). By granting the Bash tool and writing a Python snippet for complex operations, the DiPeO agents offload work that would be tedious or error-prone for an LLM to do in pure natural language. This pattern (LLM deciding to run a script) is encouraged by Anthropic for reliability. The DiPeO setup demonstrates the trade-off here: increased system complexity (you need to write and maintain the script, ensure the environment allows it, and secure it) in exchange for far greater accuracy and efficiency on that task. For doc lookups, this means the answer is guaranteed to come from real docs, and for other skills (e.g. code generation or maintenance scripts) it can enforce deterministic outcomes.






One trade-off of adopting Claude’s agent/skill system is coupling to that ecosystem. The .claude directory and Skill/Task syntax are specific to Claude’s code assistant. DiPeO’s approach is clearly optimized for Anthropic’s platform (e.g. using a Claude “Sonnet” model and Claude Code SDK). This yields great synergy (since Claude was designed to use these skills natively), but it means the solution is less immediately portable to other LLM providers. However, given Claude’s large context and advanced tooling, the benefits appear to outweigh this, especially for a complex project like DiPeO. The design choices illustrate a conscious alignment with Claude’s philosophy of agent development – using “composable resources” (skills) and on-demand expertise to scale up what the AI can do.


In conclusion, DiPeO’s Claude integration showcases a forward-thinking agent architecture: modular skills for each need, minimal wrapper prompts, and delegating to code when appropriate. This yields a system that is efficient in token usage, easier to update (each skill/agent can be edited in isolation), and powerful in capability (thanks to direct code execution and targeted knowledge retrieval). The clear patterns (router skills, progressive loading, and anchored docs) serve as a template for best practices in building AI agents that are both specialized and flexible, while the only notable trade-offs are the added initial complexity in setup and a reliance on Claude’s tooling – both of which are justified by the significant gains in performance and maintainability.


