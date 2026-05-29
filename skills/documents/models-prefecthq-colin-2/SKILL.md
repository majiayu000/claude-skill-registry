---
name: Onboarding Skill
description: Agent skill compiled from company onboarding docs in Notion
---

# Company Onboarding Guide

This skill contains onboarding information compiled from Notion.

{% for page in colin.notion.search("onboarding") %}
## {{ page.title }}

{{ page.content }}

---
{% endfor %}
