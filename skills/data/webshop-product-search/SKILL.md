---
name: webshop-product-search
description: This skill performs an initial product search using a web interface by generating appropriate search keywords based on interpreted query criteria. It is triggered when starting a product discovery task or when returning to search results. The skill inputs structured search parameters and outputs a list of candidate products from the search results page.
---
# Skill: WebShop Product Search

## Primary Function
Generate a targeted search query and execute it on a web shopping interface to retrieve a list of candidate products that match the user's criteria.

## Core Workflow
1.  **Interpret Criteria:** Analyze the user's instruction to identify key product attributes (e.g., "long clip-in hair extension", "natural looking", "price lower than 40.00 dollars").
2.  **Formulate Query:** Construct a concise, effective search string that prioritizes the most critical attributes. The primary goal is to balance specificity with recall.
3.  **Execute Search:** Use the `search[keywords]` action to submit the query.
4.  **Parse Results:** The skill's success is marked by the system returning a "Page 1" observation containing a list of products (ASINs, titles, prices).

## Key Decision Logic
*   **Query Formulation:** Start with a broad query containing the core product type. If the initial results are poor, the skill may be re-invoked with a more refined query (e.g., adding "synthetic" or "human hair" based on observed results).
*   **Trigger Condition:** This skill is the entry point for a new product discovery task. It is also the correct action when the observation contains "[SEP] Search" or "[SEP] Back to Search", indicating the agent is on a search page.
*   **Output Handoff:** The output of this skill is the search results page. Subsequent skills (e.g., `product-evaluation`) should be used to analyze individual items from this list.

## Error Handling / Edge Cases
*   If no search action is available in the current state, this skill is not applicable.
*   If the observation does not contain a clear search interface prompt, do not use this skill.
*   The search keywords must be a single string enclosed in brackets after `search[`. Do not include multiple actions or extra formatting.

## Example from Trajectory
**Instruction:** "i need a long clip-in hair extension which is natural looking, and price lower than 40.00 dollars"
**Skill Execution:**
1.  Criteria identified: `product_type="clip-in hair extension"`, `attribute="long"`, `attribute="natural looking"`, `budget="<40.00"`.
2.  Query formulated: Prioritizes core product type and key attribute -> `"long clip-in hair extension"`.
3.  Action: `search[long clip-in hair extension]`
