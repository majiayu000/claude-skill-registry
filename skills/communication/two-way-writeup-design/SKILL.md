---
name: two-way-writeup-design
description: Replaces static document reviews with interactive feedback loops to accelerate decision velocity and surface hidden dissent. Use this when seeking cross-functional sign-off on high-stakes proposals, managing asynchronous reviews across time zones, or when a document is stalled in "comment thread hell."
---

# Two-Way Writeup Design

The Two-Way Writeup is a document evolution that moves beyond "one-way" broadcasting (PowerPoint or standard prose) into an interactive conversation. It integrates feedback and discussion directly into the content structure to ensure stakeholders are heard, alignment is visible, and the most important questions are addressed first.

## Core Components

A Two-Way Writeup replaces the standard "100-pixel right margin" comments with three specific interactive modules.

### 1. Done Reading Tracker
Eliminate the "avatar watching" behavior where authors wait for a specific leader’s icon to appear.
- **The Mechanism:** A "Done Reading" button at the end of the document (or multiple buttons at the end of key sections for long docs).
- **The Value:** Provides a clear signal of who has engaged with the content and where they stopped, allowing you to follow up with non-readers intentionally.

### 2. The Dory (Structured Q&A)
Instead of disparate comments on the title or random sentences, centralize all questions in a table.
- **The Mechanism:** A table where stakeholders add questions and others "upvote" (plus-one) them.
- **The Value:** Surfaces the "most important question" automatically. Instead of the author spending 20 minutes before a meeting trying to categorize 50 comments, the team naturally highlights the high-leverage topics.

### 3. Sentiment Pulse
Force stakeholders to share their overall "gut feel" before the meeting starts.
- **The Mechanism:** A table where every reviewer selects a sentiment (e.g., a scale of 1-5 or a range of emojis from "Frowning" to "Celebrating") and adds a brief "Overall Thoughts" summary.
- **The Value:** Surfaces hidden dissent from quiet team members. By visualizing the spread of sentiment, you can quickly identify if the room is split or if there is a single "blocker" who needs to be addressed immediately.

## Step-by-Step Implementation

1.  **Draft the "One-Way" Content:** Write your proposal in clear prose (following the "Amazon 6-pager" style). Focus on the core logic and data.
2.  **Add the Engagement Layer:** Insert a "Done Reading" button at the bottom of the "Context" section and at the very end of the document.
3.  **Insert the Dory:** Below your content, create a table with columns for: [Question], [Asked By], and [Votes (+1)].
4.  **Set the Sentiment Pulse:** Create a "Sentiment" section at the top or bottom with columns for: [Reviewer Name], [Sentiment (1-5)], and [Overall Commentary].
5.  **Distribute with Instructions:** Send the doc to stakeholders with the following prompt: *"Please read this by [Time]. Instead of commenting in the margins, please log your overall sentiment in the Pulse table and add/upvote questions in the Dory."*
6.  **Facilitate the Meeting:** Start the meeting by looking at the Sentiment Pulse. If it's all "5s," the meeting is over in 5 minutes. If there are "1s" or "2s," go straight to the top-voted question in the Dory.

## Examples

**Example 1: High-Stakes Strategy Proposal**
- **Context:** A CPO proposing a controversial pivot from a subscription model to a usage-based model.
- **The Pulse:** A key Engineering Lead gives a "2/5" sentiment.
- **The Dory:** The top-voted question is "How does this impact our data latency?"
- **Outcome:** The meeting skips the "presentation" and spends 45 minutes solving the latency concern, leading to immediate alignment.

**Example 2: Product Requirement Document (PRD)**
- **Context:** A PM launching a "Skippable Ads" experiment (high internal skepticism).
- **The Pulse:** The Sales lead leaves a "Frowning Face."
- **The Dory:** The top question is "Will this kill our Q4 revenue targets?"
- **Outcome:** The PM uses the Dory to show data from the "lower bound" experiment, addressing the Sales lead's fear directly and unblocking the launch.

## Common Pitfalls

- **Ignoring the "Quiet Dissenter":** The biggest mistake is seeing a low sentiment from a quiet person and not calling on them. Lane Shackleton notes that "Sentiment tables are built to surface the person who wouldn't normally speak up in a meeting."
- **Allowing Comment "Leakage":** If users still use the right-margin comments for high-level debates, move the comment manually into the Dory and ask them to upvote it.
- **The "Unread" Meeting:** Don't start the discussion if the "Done Reading" count is low. If the stakeholders haven't hit the button, spend the first 10 minutes of the meeting in silence allowing them to read and populate the Dory.
- **Over-weighting FYI Feedback:** Use "Flash Tags" (FYI, Suggestion, Recommendation, Plea) within the Dory to ensure the team knows which "1/5" sentiments are critical blockers versus just "concerns."