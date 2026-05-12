# MCP Tools Reference

## Core Tools Used

- `wordpress_get_site_info`
- `wordpress_list_plugins`
- `wordpress_get_theme_info`
- `wordpress_list_pages`
- `wordpress_list_posts`
- `wordpress_detect_page_builder`
- `wordpress_get_database_stats`

## Notes

- All calls are read-only for audit mode.
- Builder detection is correlated with page/post scans for coverage estimates.
- Database stats are used for trend indicators, not destructive cleanup actions.
