---
name: webshop-product-detail-check
description: This skill examines a specific product's detailed page to verify it matches the user's requirements, checking price, description, features, and reviews. Trigger when a candidate product is selected from search results. It confirms alignment with constraints and provides a final suitability assessment before purchase.
---
# Skill: Product Detail Verification

## Trigger
Activate this skill when the agent has navigated to a specific product's detailed page from a search results list. The agent should have a user query containing specific requirements (e.g., product type, attributes, price constraints).

## Core Objective
Analyze the product detail page to confirm if the product meets all user-specified constraints. Provide a clear "Proceed" or "Reject" recommendation.

## Execution Workflow

1.  **Parse User Requirements:** Extract key constraints from the user's instruction. Primary constraints are typically **Price** and **Key Attributes** (e.g., "long", "clip-in", "natural looking"). Store these in a structured format.

2.  **Scrape Product Page Data:** Systematically extract the following information from the current page observation:
    *   **Product Title**
    *   **Price**
    *   **Key Description Snippets** (from Description/Features sections)
    *   **Rating** (if available)
    *   **Availability of "Buy Now"** action.

3.  **Constraint Verification:** Compare the scraped data against the user's requirements.
    *   **Price Check:** Is the product price strictly less than the user's maximum? (e.g., < $40.00).
    *   **Attribute Check:** Do the title and description contain terms matching the user's key attributes? (e.g., confirm "clip-in" and "natural looking" are present).
    *   **Suitability Flag:** Product is suitable only if **ALL** hard constraints (price, mandatory attributes) are satisfied.

4.  **Decision & Action:**
    *   **If SUITABLE:** Conclude the product matches requirements. The recommended action is `click[buy now]`.
    *   **If NOT SUITABLE:** Conclude the product fails one or more constraints. The recommended action is to return to search (`click[back to search]`) to find another candidate.

## Output Format
Your response must use the following format:

**Thought:** [Your reasoning, summarizing the user's constraints, the product details found, and the result of the verification check.]
**Action:** [The single, valid action to take: `click[buy now]` or `click[back to search]`]

## Notes
*   Prioritize information explicitly on the product page. Assume missing information (like a Rating of "N.A.") does not disqualify a product unless specified by the user.
*   The "Buy Now" button must be present in the available actions list for the purchase action to be valid.
