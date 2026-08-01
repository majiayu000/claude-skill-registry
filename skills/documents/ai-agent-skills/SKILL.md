---
name: ai-agent-skills
description: The Web Search Skill enables AI agents on the Raia platform to access
  real-time information from the internet, allowing them to provide up-to-date, relevant,
  and context-aware answers. This dynamic capability helps bridge gaps in static training
  data and ensures more responsive and informed conversations across a variety of
  use cases.
---

# Web Search Skill



***

## 🌐 Raia Web Search Skill Documentation

The **Web Search Skill** enables AI agents on the Raia platform to access real-time information from the internet, allowing them to provide up-to-date, relevant, and context-aware answers. This dynamic capability helps bridge gaps in static training data and ensures more responsive and informed conversations across a variety of use cases.

***

### 🧠 Purpose

Use the Web Search Skill when agents need to:

* Retrieve **live or recent data** not found in internal sources
* **Fact-check** statements or verify details
* Answer **time-sensitive** questions (e.g. news, pricing, events)
* Reference **public information** to supplement domain-specific knowledge

***

### 🔍 Key Capabilities

| Feature                            | Description                                                              |
| ---------------------------------- | ------------------------------------------------------------------------ |
| **Live Web Lookup**                | Real-time querying via OpenAI’s Web Search integration                   |
| **Contextual Inference**           | Automatically determines if a search is necessary based on the prompt    |
| **Integrated Response Generation** | Blends search results with model knowledge for seamless, natural answers |
| **Trusted Source Ranking**         | Prioritizes reliable and high-authority sources                          |

***

### ⚙️ How It Works

The Web Search Skill uses OpenAI’s **Web Search tool**, which is intelligently invoked by the AI agent when needed—**no manual trigger required**.

1. **Autonomous Triggering**\
   When a user asks a question, the agent evaluates whether it can confidently answer using its internal training or previously provided documents. If not, it **autonomously performs a web search**.
2. **Query Execution**\
   The agent sends the query through OpenAI’s Web Search tool, retrieving **real-time results** from the public internet.
3. **Integrated Reasoning**\
   Instead of quoting web results directly, the AI blends them **into its working context**, alongside its trained knowledge and your custom system instructions. This creates a **holistic understanding** that powers a highly accurate and fluent answer.
4. **Final Output**\
   The agent returns a response that is **informative, timely, and conversational**, seamlessly enriched with insights from the web—without disrupting the tone or logic of the overall interaction.

> ✅ Users don’t need to know when a search happens—it’s fully automated and invisible unless explicitly requested.

***

### ✅ Best Practices

* **Use cases that benefit from Web Search:**
  * Current events, financial updates, market trends
  * Business operating hours, availability, or weather
  * Product reviews, Reddit discussions, social buzz
  * Verifying claims or identifying breaking changes
* **When NOT to rely on it:**
  * Secure/internal-only knowledge
  * Complex topics requiring proprietary documents
  * Questions where exact citations are mandatory (use scraping or static sources instead)

***

### 🧪 Example Use Cases

| User Prompt                                          | What the Agent Does                                                 |
| ---------------------------------------------------- | ------------------------------------------------------------------- |
| “What’s the latest on the AI copyright lawsuit?”     | Searches news sites for updates and summarizes current events       |
| “Are there any delays at TPA airport today?”         | Checks public travel alerts and news feeds for live status          |
| “What are people saying about Apple’s new headset?”  | Aggregates sentiment and highlights key Reddit or blog discussions  |
| “Is Google Cloud still offering their AI free tier?” | Looks up the most recent product/pricing page from official sources |

***

### 🧰 Integration Notes (for Developers)

* Web Search is **baked into the Raia agent runtime** and does not require custom API setup.
* It plays well with other skills like **Scraping**, **Document Retrieval**, and **Memory**.
* Developers can encourage or suppress Web Search through agent instructions if finer control is needed.
