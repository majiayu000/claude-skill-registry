---
name: agentkit-seo-cv-ats
description: Optimize CV and resume content for recruiter readability and parser-safe ATS handling without making unsupported claims about exact vendor scoring. Use when the user asks about resumes, CVs, ATS formatting, keyword strategy, bullets, section order, achievement metrics, or job-targeted resume tailoring.
---

# AgentKit SEO CV ATS

## Overview

Use only the CV and ATS guidance relevant to the requested deliverable. Keep the advice conservative, parser-safe, and grounded in documented, durable constraints.

## Reference selection

- Layout, section order, file type, ATS-safe structure: [references/structure-and-formatting.md](references/structure-and-formatting.md)
- Summary, experience, skills, and education rewrites: [references/section-recipes.md](references/section-recipes.md)
- Job-description tailoring and bullet rewrites: [references/keywords-and-bullets.md](references/keywords-and-bullets.md)
- Parser-failure diagnosis, LaTeX/PDF post-build QA, or plain-text extraction: [references/parser-risks-and-agent-workflow.md](references/parser-risks-and-agent-workflow.md)
- Full-document review, consistency checks, maintenance: [references/cv-audit-and-maintenance.md](references/cv-audit-and-maintenance.md)

## Token discipline

- Do not load all references for a single bullet, section, or parser question.
- For long CVs, inspect contact, summary, target role, recent experience, and only sections relevant to the user's request first.
- Summarize missing inputs instead of asking for the whole career history when a narrow edit can proceed.
- Prefer text extraction, Markdown, LaTeX, or DOCX text before screenshots when parser behavior matters.
- When both an editable source file and rendered PDF are supplied, use the editable source as the primary content source and the PDF only for render or extraction sanity checks unless the user asks for PDF debugging.
- After creating or editing a LaTeX CV with a rendered PDF, run the compact post-build QA in the parser workflow; do not expand into a full visual redesign unless asked.
- For large context files, verify only CV-relevant hard anchors first: current role, education, dates, flagship projects, certifications, awards, and metrics that appear in the CV.
- Keep source ledgers compact: list input groups, not every bullet or section.
- Name next inspection if bounded.

## Depth contract

Use the smallest honest audit depth:

- `Quick scan`: contact block, summary, target role, recent experience, skills, and obvious parser risks.
- `Default audit`: quick scan plus core sections, target job description alignment when provided, and fact consistency against supplied context.
- `Deep audit`: full-document line edit, plain-text extraction/order check, job-by-job tailoring, every bullet, design/layout risks, and cross-platform consistency.

Default to `Default audit` for broad CV or resume reviews. Offer `Deep audit` as an optional next step when the current answer would benefit from more evidence. Do not choose `Deep audit` silently unless the user asks for a complete rewrite, exact file remediation, parser debugging, or every bullet reviewed.

## Intake workflow

- Ask for the current resume or CV, target role, and job description before doing role-specific optimization.
- If the user supplies only a resume, perform a general parser-safety and recruiter-readability pass and identify the missing target-role inputs.
- If the user supplies a context file, use it to verify facts before rewriting bullets, summaries, projects, or skills.
- If the user supplies a large context file, do not fully reconcile every section by default. Use targeted fact checks against claims visible in the CV, then offer a deeper consistency pass if conflicts or gaps remain.
- If the user has no context file and the CV conflicts with LinkedIn, GitHub, or portfolio facts, recommend creating or repairing the context file first.
- Do not fetch or infer LinkedIn, GitHub, portfolio, or public-profile facts unless the user supplies them or explicitly asks for lookup.
- Accept source material as pasted text, PDF text extraction, LaTeX, Markdown, DOCX text, screenshots when supported, or local files.
- Never add keywords, tools, metrics, employers, dates, or credentials that are not supported by the supplied material.

## Rules

- Do not claim guaranteed ATS success or exact ranking behavior.
- Separate facts visible in the CV, facts supplied by the user's context material, job-description requirements, and recommendations inferred from those inputs.
- Avoid absolute alignment claims such as "perfectly aligned" unless every relevant claim was checked. Prefer "no conflict found in the inspected inputs" for bounded audits.
- Prefer simple structure, plain section names, and measurable outcomes.
- Tailor wording to the target role, but do not fabricate tools, metrics, or employers.
- If the user supplies a job description, align terminology to that role while preserving the user's real experience.
- Optimize for reliable parsing first, recruiter readability second, and visual polish third.
- Preserve factual alignment with the user's context file, LinkedIn, and public portfolio.
- For rewrites, improve section clarity and evidence density before changing the user's positioning strategy.

## Response shape

Return only requested-relevant sections. For full CV audits or broad tailoring passes, return:

1. inputs used and target role assumptions
2. parser and structure issues
3. rewritten sections or bullet changes
4. keyword alignment notes tied to the job description
5. missing facts or evidence needed before stronger claims

For audits, use concise labels such as `Verified`, `From context`, `From job description`, `Inference`, and `Inaccessible` when a claim could otherwise be ambiguous. Include a `Depth note` for full-document audits, parser debugging, or intentionally bounded reviews; omit it for narrow bullet or section rewrites unless more input is needed.
