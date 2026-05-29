---
name: github-stars-analyzer
description: Analyzes GitHub repository data to generate comprehensive research reports about stars, popularity trends, and comparative insights
---

# GitHub Stars Research Analyzer

This skill provides in-depth analysis of GitHub repositories, tracking star growth, comparing popularity metrics, and generating research reports for open source projects and developer tools.

## Capabilities

- **Repository Analysis**: Extract and analyze key metrics (stars, forks, issues, contributors, activity)
- **Star Growth Tracking**: Calculate daily, weekly, and monthly star growth rates and trends
- **Comparative Analysis**: Compare multiple repositories across various metrics
- **Research Report Generation**: Create comprehensive reports with insights and recommendations
- **Data Visualization**: Generate charts and graphs for trend analysis
- **Export Formats**: Output reports in Markdown, PDF, and JSON formats

## Input Requirements

GitHub repository data can be provided in multiple formats:

- **Repository URLs**: Direct GitHub repository links
- **Owner/Repo Names**: GitHub owner and repository names
- **JSON Input**: Structured data with repository information
- **CSV Lists**: Multiple repositories in CSV format

Required fields:
- Repository owner (username or organization)
- Repository name
- Optional: Time period for analysis (default: last 30 days)

## Output Formats

Results include:

- **Metrics Summary**: Key statistics and calculations
- **Growth Analysis**: Star growth rates and trends
- **Comparative Insights**: Multi-repository comparisons
- **Visualizations**: Charts and graphs (when applicable)
- **Recommendations**: Actionable insights for project maintainers
- **Export Options**: Markdown, PDF, and JSON reports

## How to Use

"Analyze the GitHub repository claude-code-skills-factory and generate a star growth report"
"Compare the popularity of these three repositories over the last 90 days"
"Track star growth trends for the Anthropic organization's repositories"
"Generate a comprehensive research report on React's star growth patterns"

## Scripts

- `github_api.py`: Handles GitHub API interactions and data fetching
- `analyze_repository.py`: Core analysis engine for repository metrics
- `generate_reports.py`: Creates research reports in multiple formats
- `visualize_data.py`: Generates charts and visualizations

## Best Practices

1. **Respect Rate Limits**: Always handle GitHub API rate limits gracefully
2. **Data Validation**: Verify repository existence and accessibility
3. **Time Period Selection**: Use appropriate time windows for meaningful analysis
4. **Comparative Context**: Always provide industry/ecosystem context for metrics
5. **Privacy Considerations**: Respect private repositories and user privacy

## Limitations

- **API Rate Limits**: GitHub API has strict rate limits (60 requests/hour unauthenticated)
- **Historical Data**: Limited historical data availability through API
- **Private Repositories**: Cannot access private repositories without proper authentication
- **Data Freshness**: Real-time data depends on GitHub API updates
- **Repository Age**: New repositories may not have sufficient historical data