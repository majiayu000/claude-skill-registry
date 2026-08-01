---
name: ai-agent-skills
description: Here’s a complete breakdown of how to configure and set up the Scoring
  Skill in raiaAI’s Launch Pad. This skill allows your AI agent to evaluate the quality
  of its conversations and assign a Conversation Score ranging from 0 to 10—helping
  you measure effectiveness, identify issues, and improve agent performance.
---

# Scoring Skill

Here’s a complete breakdown of how to **configure and set up the Scoring Skill** in raiaAI’s Launch Pad. This skill allows your AI agent to **evaluate the quality of its conversations** and assign a **Conversation Score** ranging from 0 to 10—helping you measure effectiveness, identify issues, and improve agent performance.

***

####

<figure><img src="../.gitbook/assets/Screenshot 2025-04-17 at 10.15.18 AM.png" alt=""><figcaption></figcaption></figure>

#### 🧠 **Scoring Skill Setup Guide**

***

#### 🔍 **What the Scoring Skill Does**

* Automatically **scores conversations** based on:
  * Engagement
  * Response relevance
  * Issue resolution
  * Tone and flow
* Scores are displayed as **color-coded ratings**:
  * **Grey (0):** No meaningful interaction
  * **Red (1–3):** Poor interaction
  * **Yellow (4–6):** Average interaction
  * **Green (7–10):** High-quality, helpful interaction

***

#### ⚙️ **Configuration Steps**

**1. Enable the Skill**

* Go to your agent’s **Skills tab**
* Click **“Add Skill”** → Select **Scoring Skill**
* Toggle the status to **Active**

***

**2. (Optional) Customize Scoring Prompts**

* Define what metrics or questions the agent should reflect on after each conversation:
  *   Example prompt:

      > “On a scale of 1-10, how helpful and complete was this conversation in addressing the user's question?”
* These prompts can be added into the backend or used via your OpenAI Assistant function tool (if enabled).

***

**3. Review Scoring Behavior**

* After setup, all threads processed by the agent will be scored automatically.
* Scores appear in **thread metadata** and in **Mission Control** dashboards (if deployed in a campaign).

***

**4. Monitor and Analyze Scores**

You can monitor performance across channels (SMS, Email, Chat, Copilot) by:

* Viewing **average score per agent**
* Filtering **low-score conversations** for review
* Exporting data for **performance tracking**

***

#### 🎯 **Business Use Cases**

* **Customer Support QA:** Flag low-quality interactions for team review.
* **Sales Coaching:** Track if sales agents are providing clear and engaging information.
* **Training Feedback Loop:** Use scores to identify which instructions or knowledge sources need refinement.

***

#### ✅ **Best Practices**

| Tip                                       | Why It Matters                                           |
| ----------------------------------------- | -------------------------------------------------------- |
| Use clear rating prompts                  | Helps the AI agent assess conversations more accurately  |
| Cross-reference scores with user feedback | Pinpoint gaps in training or tone                        |
| Set benchmarks by use case                | A "6" may be fine for FAQs, but low for high-touch sales |
| Use human review for low-score threads    | Improve the assistant’s performance through retraining   |

## [Scoring Video Setup](https://www.youtube.com/watch?v=qj-quHneNlg)

{% embed url="https://www.youtube.com/watch?v=qj-quHneNlg" %}
