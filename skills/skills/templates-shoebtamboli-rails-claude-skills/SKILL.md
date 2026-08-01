---
name: templates
description: <%= templatesections %>
---

---
name: <%= file_name %>
description: <%= skill_description %>
version: 1.0.0
rails_version: ">= 7.0"
tags:
<% skill_tags.each do |tag| -%>
  - <%= tag %>
<% end -%>
---

# <%= file_name.titleize %>

<%= template_sections %>

## Troubleshooting

Add common issues and solutions here.

## References

- [Add external documentation links]
- [Add related resources]

---

*Generated with rails_claude_skills v<%= RailsClaudeSkills::VERSION %>*
