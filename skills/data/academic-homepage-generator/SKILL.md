---
name: academic-homepage-generator
description: When the user requests to create or customize an academic personal website from a GitHub template repository. This skill handles the complete workflow of forking academic template repositories (like academicpages.github.io), extracting structured personal information from memory or provided data, and systematically updating configuration files (_config.yml), navigation menus (_data/navigation.yml), content pages (_pages/about.md), and publication listings (_publications/). It specifically handles academic profiles including personal details, education background, research experience, publications, skills, and contact information. Triggers include requests to 'fork and customize academic homepage', 'build personal academic website', 'create research portfolio', or 'set up GitHub pages with academic template'.
---
# Skill: Academic Homepage Generator

## Primary Objective
Fork a specified academic GitHub Pages template repository, rename it, and populate it with a user's personal academic information extracted from memory or provided data. The final output is a fully configured, personalized academic homepage ready to be hosted on GitHub Pages.

## Core Workflow
The skill follows a strict, sequential workflow to ensure a successful deployment. Deviations may cause errors.

1.  **Retrieve Personal Data**: Extract the user's structured academic profile from memory using `memory-read_graph`. This data is the single source of truth for all content updates.
2.  **Fork Template Repository**: Use `github-fork_repository` on the target template (e.g., `academicpages/academicpages.github.io`).
3.  **Identify User Account**: Use `github-get_me` to get the forking user's GitHub username.
4.  **Rename Repository**: Use `github-rename_repository` to give the fork a user-specified name (e.g., `LJT-Homepage`).
5.  **Analyze Repository Structure**: Examine key directories (`_pages/`, `_publications/`, `_data/`, `_config.yml`) to understand the template's layout.
6.  **Update Core Configuration Files**:
    *   `_config.yml`: Update site title, description, URL, and most importantly, the `author` section with personal details (name, bio, location, employer, email, social links).
    *   `_data/navigation.yml`: Simplify the site's main navigation menu. Typically, reduce it to only essential links like "Publications" as per user instruction.
    *   `_pages/about.md`: Completely replace the default content with a structured personal profile containing: Introduction, Research Interests, Education, Research Experience, Publications (listed in-text), Skills, and Contact Information.
7.  **Manage Publication Files**:
    *   Delete all existing sample files in the `_publications/` directory.
    *   Create new Markdown files for each of the user's publications, using a consistent naming convention (e.g., `YYYY-MM-DD-short-title.md`). Each file must contain valid YAML frontmatter (`title`, `collection`, `date`, `venue`, `citation`).
8.  **Final Verification**: Check that all key files (`_config.yml`, `_pages/about.md`, `_data/navigation.yml`) and publication entries have been correctly created and contain no placeholder data.

## Critical Constraints & Guardrails
*   **Data Fidelity**: Do not add, modify, or hallucinate any personal information. Use **only** the data provided in the memory graph. If information is missing (e.g., a specific social media link not in memory), leave the field blank in the configuration.
*   **Publication Inclusion**: List **all** publications from memory in the `about.md` page, clearly distinguishing between first-author and co-authored works. Also create individual publication Markdown files for each.
*   **Navigation Simplification**: Adhere to the user's request regarding the navigation menu. If asked to show only specific pages, remove all other links from `_data/navigation.yml`.
*   **No Extra Pages**: Do not create, enable, or modify pages beyond those explicitly mentioned in the workflow (e.g., do not activate blog, teaching, or portfolio sections unless specified).

## Required Tools
This skill requires sequential use of the following tools. Ensure all necessary permissions/scopes are available.
1.  `memory-read_graph`
2.  `github-fork_repository`
3.  `github-get_me`
4.  `github-rename_repository`
5.  `github-get_file_contents`
6.  `github-create_or_update_file`
7.  `github-delete_file`

## Failure Recovery
*   **Concurrent Write Conflicts**: If `github-create_or_update_file` or `github-delete_file` fails with a "409 conflict" error, fetch the latest repository state (`github-get_file_contents` on the root) to get the new `sha`, then retry the operation with the updated `sha`.
*   **Missing Data**: If a required field from the memory graph is empty, log a clear note and proceed, leaving the corresponding website field blank. Do not invent data.

## Output
The skill is complete when the user's forked GitHub repository contains all personalized files and the commit history shows successful updates. Provide the user with the URL to their new repository (e.g., `https://github.com/<username>/<repo-name>`).
