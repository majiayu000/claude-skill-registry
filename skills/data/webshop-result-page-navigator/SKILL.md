---
name: webshop-result-page-navigator
description: Navigates through paginated search results by moving to the next or previous page. Use this skill when the current page of product listings does not contain a suitable match and you need to review more options. It identifies and clicks the appropriate pagination controls (e.g., 'next >' or '< prev') to load additional result pages for evaluation.
---
# Skill: WebShop Result Page Navigator

## Purpose
This skill enables systematic navigation through paginated product search results in a WebShop environment. It is triggered when the current page of results does not contain an item matching the user's criteria, allowing the agent to access more options.

## Core Logic
1.  **Trigger Condition:** The agent has reviewed the current page of product listings and determined that no item satisfies the user's requirements (e.g., price, features).
2.  **Action Selection:** The skill identifies the correct pagination control to click:
    *   `click[next >]` to load the subsequent page of results.
    *   `click[< prev]` to return to the previous page of results.
3.  **Post-Action:** After navigation, the agent should resume its primary task of evaluating the newly loaded product listings against the user's instruction.

## Usage in Trajectory
The skill was demonstrated when the agent, searching for a pendant light under $120 with a dimmer switch, found no suitable options on Page 1. It correctly executed `click[next >]` to access Page 2, and repeated the action to access Page 3, where a potential match was found.

## Key Principle
This skill handles the deterministic, repetitive task of page navigation, freeing the agent's reasoning capacity for the higher-freedom task of evaluating product features and making purchase decisions.
