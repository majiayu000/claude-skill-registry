---
name: wordpress
description: Operate connected WordPress sites through the NotFair MCP. Use for WordPress content, posts, pages, media, comments, terms, design, settings, plugins, themes, HTML files, or approved WordPress changes on a NotFair-connected site. Not the local Application-Password CMS setup used by SEO scripts.
argument-hint: "<site, content, plugin, or WordPress change>"
---

# Canonical NotFair workflow

Read [`../../wordpress/SKILL.md`](../../wordpress/SKILL.md) completely, then follow it as the active workflow. Normalize that path from the directory containing this wrapper: the canonical file is `<plugin-root>/wordpress/SKILL.md`, not `<plugin-root>/skills/wordpress/wordpress/SKILL.md`. Resolve every relative reference from the canonical file against `<plugin-root>/wordpress/`. If the canonical file cannot be read, stop and report the packaging error; never substitute a similarly named skill from another plugin.
