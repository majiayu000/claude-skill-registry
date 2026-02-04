---
name: web-form-autofiller
description: When the user needs to fill out web forms with data from memory or structured sources, this skill automates the entire workflow reads form links from files, navigates to web forms, analyzes form structure and fields, extracts relevant data from memory or knowledge bases, maps data to form fields, fills text inputs, selects checkboxes and radio buttons, handles multi-page forms with navigation, and submits forms. It's triggered when users mention filling forms, questionnaires, surveys, or registration forms, especially when combined with data from memory systems or structured files.
---
# Skill: Web Form Autofiller

## Purpose
Automate the process of filling web forms by extracting data from memory/knowledge bases and mapping it to form fields. Handles complex forms with multiple field types (text, radio, checkbox, date) and multi-page navigation.

## Core Workflow
1.  **Parse Request:** Identify the form URL source (file path, direct link) and the data subjects (people, entities) to fill the form for.
2.  **Acquire Data:** Read the form link and fetch relevant entity data from memory/knowledge graphs.
3.  **Navigate & Analyze:** Load the form in a browser and analyze its structure to identify all required and optional fields.
4.  **Map & Fill:** For each data subject, map their attributes to the corresponding form fields, applying default rules for missing information.
5.  **Submit & Repeat:** Submit the form and repeat the process for additional subjects if needed.

## Detailed Instructions

### 1. Initial Setup & Data Acquisition
-   **Locate Form Link:** If the user provides a file path (e.g., `form_link_for_public.txt`), read the URL from that file using `filesystem-read_file`.
-   **Extract Entity Data:** Query the memory/knowledge graph (`memory-read_graph`) to get structured data for all entities mentioned in the request (e.g., "MCP Wang" and "Alex Wang"). Pay close attention to `observations` arrays for attributes.

### 2. Form Analysis & Field Mapping
-   **Navigate to Form:** Use `playwright_with_chunk-browser_navigate` to load the form URL.
-   **Inspect Structure:** Use the snapshot navigation tools (`browser_snapshot_navigate_to_next_span`, `browser_snapshot_navigate_to_first_span`) to view the entire form. Create a mental map of all fields:
    -   **Text Inputs:** Name, Email, Address, Phone, Student ID, Birthday (date).
    -   **Checkboxes:** Session selection (Morning, Afternoon). Multiple can be selected.
    -   **Radio Groups:** Dietary Restrictions, Anxiety Level (1-5), Activities, Highest Degree. Only one selection allowed per group.
    -   Note which fields are marked as required.
-   **Define Data Mapping Logic:** Based on the form analysis and available entity data, define rules:
    -   **Session:** If "participate for the whole day" is requested, select *both* Morning and Afternoon checkboxes.
    -   **Defaults:** For fields not mentioned in memory (e.g., anxiety level), default to the most negative/lowest option (e.g., "1" for anxiety).
    -   **Single Selection Logic:** For radio groups where multiple entity attributes could apply (e.g., hobbies: Programming, Basketball, Swimming), you must choose **only one**. Prioritize based on context or explicit mentions (e.g., "cannot swim" implies not selecting swimming).

### 3. Filling the Form (Per Person)
-   **Text Fields:** Use `playwright_with_chunk-browser_type` to fill textboxes. Reference elements by their `ref` ID or accessible role/name from the snapshot.
-   **Checkboxes:** Use `playwright_with_chunk-browser_click` on the checkbox element.
-   **Radio Buttons:** Use `playwright_with_chunk-browser_click` on the specific radio button element.
-   **Navigation:** If the form is long, use snapshot navigation between spans to access all fields.
-   **Submit:** Click the "Submit" button using `playwright_with_chunk-browser_click`.

### 4. Handling Multiple Submissions
-   After successful submission, the page will show a confirmation. If another submission is needed for a different person, click the "Submit another response" link.
-   **Important:** The form will reset. Repeat the entire filling process for the next person with their specific data.

## Key Decision Rules & Defaults
-   **Missing Data:** Any attribute not explicitly found in the memory entity's `observations` should be considered "not mentioned" and defaulted to a negative or empty state.
-   **Dietary Restrictions:** Map explicitly mentioned restrictions (e.g., "cannot eat seafood") to the corresponding option ("No Seafood"). If "Dietary restrictions: None" is stated, select "None".
-   **Highest Degree Earned:** Select the degree that has been *earned* (e.g., "Bachelor's"), not what is "currently pursuing".
-   **Activities:** Choose only one activity from the radio group. Select the one most strongly associated with the person's hobbies or explicitly mentioned capabilities.

## Error Handling & Validation
-   If the form link is invalid or the page fails to load, report the error and stop.
-   If a required field cannot be mapped from memory and has no sensible default, ask the user for clarification.
-   After submission, verify the success message ("Your response has been recorded") appears.

## Finalization
-   Once all forms are submitted, provide a clear summary of what was submitted for each person.
-   Use `local-claim_done` to signal task completion.
