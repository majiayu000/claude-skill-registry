---
name: weibo-trends-analyzer
description: Analyzes Weibo (微博) trending topics and generates creative product ideas based on hot search keywords. Fetches real-time trending data from Weibo API, researches background information and user insights, evaluates product development potential using a 100-point scoring system, and creates an interactive HTML dashboard. Use when analyzing Chinese social media trends, identifying product opportunities from trending topics, or generating market-driven creative product concepts.
---

# Weibo Trends Analyzer - 微博热搜创意产品分析

## Overview

This skill helps you identify creative product opportunities from Weibo trending topics. It fetches real-time hot search data, researches comprehensive background information, evaluates product development potential, and presents findings in an interactive dashboard.

**Keywords**: Weibo, 微博, trending topics, hot search, 热搜, product ideas, creative products, market analysis, social media trends, Chinese market

## Workflow

### 1. Fetch Weibo Trending Topics

**Default API**: https://apis.tianapi.com/weibohot/index?key=4dfdf794141101d7bb8ece0294dbbc02

When the user requests Weibo trending analysis, fetch the current hot search list:

```bash
curl -s "https://apis.tianapi.com/weibohot/index?key=4dfdf794141101d7bb8ece0294dbbc02"
```

**API Response Processing**:

The API returns data in this format:
```json
{
  "code": 200,
  "msg": "success",
  "result": {
    "list": [
      {
        "hotword": "trending keyword",
        "hotwordnum": "1234567",
        "hottag": "新/热/荐"
      }
    ]
  }
}
```

**Field Mapping**:
- `hotword` → Trending keyword (热搜关键词)
- `hotwordnum` → Heat value (热度值), may contain category prefix like "综艺 587870"
- `hottag` → Tag (标签): "新"(new), "热"(hot), "荐"(recommended), or empty
- Ranking position → Inferred from array index (1-based)

**Parsing Instructions**:
1. Check if `code == 200` to confirm success
2. Extract the `result.list` array
3. For each item in the list:
   - Rank = array index + 1
   - Keyword = `hotword`
   - Heat value = extract numeric value from `hotwordnum` (remove category prefix if present)
   - Tag = `hottag`
   - Category = extract from `hotwordnum` prefix if exists (e.g., "综艺", "剧集", "盛典", "演出")
4. Limit analysis to top 10-15 items to manage processing time

**Error Handling**:

If API fetch fails, follow this fallback strategy:

1. **API Returns Error Code (code ≠ 200)**:
   - Log the error message from API response
   - Inform user: "API returned error: {msg}. Would you like to use mock data instead?"
   - Suggest checking API key or quota limits
   - If user agrees, use `.claude/skills/weibo-trends-analyzer/weibo-mock-data.json`

2. **Network/Connection Failure**:
   - Inform user: "Unable to connect to API. Possible network issue."
   - Offer to use mock data: `.claude/skills/weibo-trends-analyzer/weibo-mock-data.json`
   - Suggest verifying internet connection

3. **Invalid JSON Response**:
   - Log the response received
   - Inform user: "API returned invalid data format"
   - Recommend checking if API endpoint has changed
   - Fall back to mock data if available

4. **Empty or Malformed Data**:
   - If `result.list` is empty or missing
   - Inform user: "No trending topics found in API response"
   - Use mock data as fallback

### 2. Deep Research Each Trending Topic

For EACH trending topic, perform **2 focused web searches** to gather essential background:

**Search Strategy (2 searches per topic)**:

**Search 1: Context & Background**
Combine social media discussions and news background in one search:
- Search query examples:
  - "{keyword} 微博 新闻背景"
  - "{keyword} 热搜原因 讨论"
  - "{keyword} latest news 用户看法"

Goal: Understand WHAT the trend is about and WHY it's trending

**Search 2: User Insights & Market Potential**
Focus on consumer perspective and product opportunities:
- Search query examples:
  - "{keyword} 用户需求 产品"
  - "{keyword} 消费者痛点"
  - "{keyword} 产品创意 市场"

Goal: Identify user needs, pain points, and product development opportunities

**Information to Extract**:
From the 2 searches, gather:
- ✅ Social media sentiment and discussion volume (社交媒体讨论)
- ✅ News background and event context (新闻背景)
- ✅ Target demographics and audience size (目标人群)
- ✅ User pain points and unmet needs (用户痛点)
- ✅ Existing products or market gaps (市场机会)
- ✅ Cultural/social significance (文化意义)

**Error Handling for Web Searches**:

1. **Search Returns No Results**:
   - Log: "No search results for: {keyword}"
   - Mark research as "Limited data available"
   - Proceed with analysis using keyword itself and general market knowledge
   - Note in dashboard: "⚠️ 背景研究受限"

2. **Search Timeout or Failure**:
   - Retry once with simplified query (just keyword without additional terms)
   - If retry fails, mark as "Search unavailable"
   - Continue analysis with available data
   - Note limitation in product analysis

3. **Irrelevant Search Results**:
   - If results don't match trending topic context:
   - Try alternative search query with different keywords
   - Use general industry knowledge for analysis
   - Document: "Based on general market analysis"

4. **Partial Search Success (1 of 2 succeeds)**:
   - Proceed with available search data
   - Note which aspect is missing (context vs. user insights)
   - Make conservative estimates for missing information
   - Mark in dashboard with: "⚠️ 部分数据"

### 3. AI-Powered Product Ideation & Scoring

For each trending topic, analyze and generate creative product ideas using this scoring framework:

**Scoring System (Total: 100 Points)**

1. **Product Development Potential (可发展度)**: 40 points
   - Market size and scalability (15 points)
   - Technical feasibility (10 points)
   - Trend longevity vs. fleeting fad (10 points)
   - Competitive landscape (5 points)

2. **Interest Level (有趣度)**: 20 points
   - Creative uniqueness (10 points)
   - Emotional appeal (5 points)
   - Share-ability/viral potential (5 points)

3. **Practical Life Utility (生活有用度)**: 20 points
   - Daily life integration (10 points)
   - Problem-solving capability (5 points)
   - Target audience size (5 points)

4. **Small-Scale Production Ease (小规模生产容易程度)**: 20 points
   - Manufacturing complexity (10 points)
   - Material accessibility (5 points)
   - Cost efficiency for small batches (5 points)

**Product Concept Requirements**:

For each trend, generate 1-3 creative product concepts including:

- **Market Category (市场赛道)**: Which product category (e.g., home decor, fashion accessories, stationery, tech gadgets, lifestyle products, toys, etc.)
- **Product Name (产品名称)**: Catchy, memorable name
- **Target Audience (销售对象人群)**: Specific demographic (age, interests, income level, lifestyle)
- **Manufacturing Characteristics (工厂批量生产特点)**:
  - Production method (e.g., 3D printing, injection molding, screen printing, laser cutting)
  - Material requirements
  - Minimum order quantity (MOQ) feasibility
  - Lead time estimates
  - Cost structure (per unit at different volumes)
- **Detailed Description (详细描述)**: How the product relates to the trending topic
- **Total Score (总分)**: Sum of all four scoring dimensions
- **Score Breakdown (评分分析)**: Brief justification for each score component

**Scoring Guidelines**:
- Be objective and realistic
- Consider Chinese market context
- Factor in current manufacturing capabilities
- Account for trend cycle timing

### 4. Generate Interactive HTML Dashboard

Create a comprehensive, visually appealing HTML dashboard with the following structure:

**Dashboard Components**:

**A. Header Section**
```html
- Title: "微博热搜创意产品分析报告 - Weibo Trends Product Analysis"
- Generation timestamp
- Total trends analyzed count
- Summary statistics (average score, top categories, etc.)
```

**B. Highlight Section - Top Performers**
Display products by score tiers:

- **🏆 Outstanding (优秀) - Score ≥ 80**:
  - Prominent display with gold/premium styling
  - Enlarged cards with detailed breakdown
  - Recommended action: "优先开发推荐"

- **⭐ Good (良好) - Score 60-79**:
  - Standard card layout with highlighted borders
  - Recommended action: "可考虑开发"

- **📋 Other Products - Score < 60**:
  - Compact list view
  - Recommended action: "观望或需优化"

**C. Product Cards**

Each product card should display:
```html
<div class="product-card score-tier-{excellent/good/other}">
  <div class="trend-info">
    <h3>{Trending Keyword}</h3>
    <span class="rank">热搜排名: #{rank}</span>
    <span class="heat">热度: {heat_value}</span>
  </div>

  <div class="product-concept">
    <h4>{Product Name}</h4>
    <div class="total-score">{Total Score}/100</div>
    <div class="score-badge">{优秀/良好/其他}</div>

    <div class="details">
      <p><strong>市场赛道:</strong> {market_category}</p>
      <p><strong>目标人群:</strong> {target_audience}</p>
      <p><strong>产品描述:</strong> {description}</p>
      <p><strong>生产特点:</strong> {manufacturing_details}</p>
    </div>

    <div class="score-breakdown">
      <h5>评分详情</h5>
      <div class="score-bar">
        <span>可发展度</span>
        <progress value="{score}" max="40"></progress>
        <span>{score}/40</span>
      </div>
      <div class="score-bar">
        <span>有趣度</span>
        <progress value="{score}" max="20"></progress>
        <span>{score}/20</span>
      </div>
      <div class="score-bar">
        <span>生活有用度</span>
        <progress value="{score}" max="20"></progress>
        <span>{score}/20</span>
      </div>
      <div class="score-bar">
        <span>生产容易度</span>
        <progress value="{score}" max="20"></progress>
        <span>{score}/20</span>
      </div>
    </div>

    <div class="analysis">
      <h5>分数分析</h5>
      <p>{score_justification}</p>
    </div>
  </div>

  <div class="research-summary">
    <h5>背景研究</h5>
    <ul>
      <li><strong>社交媒体:</strong> {social_media_insights}</li>
      <li><strong>新闻背景:</strong> {news_background}</li>
      <li><strong>用户洞察:</strong> {user_insights}</li>
    </ul>
  </div>
</div>
```

**D. Dashboard Styling Requirements**

```css
/* Color Scheme */
- Excellent products (≥80): Gold/amber theme (#FFD700, #FFA500)
- Good products (60-79): Blue/cyan theme (#4A90E2, #50C8E8)
- Other products (<60): Gray/neutral theme (#95A5A6, #BDC3C7)

/* Design Guidelines */
- Responsive layout (grid or flexbox)
- Clean, modern aesthetics
- Clear visual hierarchy
- Easy-to-read typography (Chinese + English support)
- Interactive hover effects
- Sortable/filterable options
- Progress bars for score visualization
- Badge system for quick identification
```

**E. Interactive Features**

Include JavaScript for:
- Sort by score (highest to lowest, lowest to highest)
- Filter by score tier (优秀/良好/其他)
- Filter by market category
- Search functionality for keywords
- Expandable/collapsible detailed sections
- Export to PDF option (bonus)

**F. Footer Section**
```html
- Disclaimer about trend volatility
- Recommendation to conduct further market research
- Generation metadata (API source, analysis timestamp)
- Skill version information
```

### 5. File Output

Generate the following files:

1. **`weibo-trends-analysis-{YYYY-MM-DD}.html`**: Complete interactive dashboard
2. **`weibo-trends-data-{YYYY-MM-DD}.json`**: Raw structured data for further processing (optional)

**Error Handling for File Generation**:

1. **File Write Permission Denied**:
   - Try alternative filename with timestamp: `weibo-trends-analysis-{YYYY-MM-DD-HHmmss}.html`
   - If still fails, inform user: "Unable to write files. Please check directory permissions."
   - Suggest user-provided output path

2. **HTML Generation Error**:
   - If template rendering fails, create simplified HTML version with basic table layout
   - Ensure at minimum: product names, scores, and basic descriptions are included
   - Log error details for troubleshooting

3. **Data Validation Before Output**:
   - Verify at least 1 product concept was generated
   - Check all scores are within valid ranges (0-40, 0-20, etc.)
   - Ensure required fields are present (product name, score, description)
   - If validation fails, inform user which topics had issues

4. **Large File Handling**:
   - If analyzing >20 topics, warn user about large file size
   - Consider generating paginated HTML or summary + detailed sections
   - Ensure browser compatibility for large datasets

## Best Practices

**Research Quality**:
- Perform 2 focused web searches per trending topic (optimized for efficiency)
- Synthesize information from multiple sources within each search
- Verify factual accuracy
- Note information freshness
- Prioritize quality over quantity in search results

**Product Ideation**:
- Think beyond obvious connections
- Consider cultural context and Chinese consumer behavior
- Evaluate both short-term trend exploitation and long-term product viability
- Be creative but realistic

**Scoring Objectivity**:
- Use consistent criteria across all products
- Justify scores with specific evidence
- Avoid bias toward certain product categories
- Consider manufacturing realities in China

**Dashboard Quality**:
- Ensure all Chinese characters display correctly (UTF-8 encoding)
- Test responsiveness on different screen sizes
- Validate HTML/CSS/JS syntax
- Include fallback fonts for Chinese text
- Make data visualizations clear and intuitive

## Example Usage Flow

```
User: "分析微博热搜"
或
User: "分析今日微博热搜并生成产品创意"

Claude:
1. Fetches trending data from default API (https://apis.tianapi.com/weibohot/index?key=...)
   - If API fails, offers to use mock data
2. Parses the result.list array and extracts top 10-15 trending topics
3. For each topic:
   - Performs 2 focused web searches for background research
   - Handles search failures gracefully with fallback strategies
   - Analyzes market potential and user needs
   - Generates creative product concepts
   - Calculates detailed scores
4. Validates all generated data
5. Compiles all data into structured format
6. Generates interactive HTML dashboard with error indicators if needed
7. Saves output files

Output:
- weibo-trends-analysis-2026-01-11.html
- weibo-trends-data-2026-01-11.json (optional)
```

## Limitations and Considerations

**API Dependencies**:
- Requires valid Weibo API endpoint provided by user
- API rate limits may affect number of trends that can be analyzed
- API response format may vary - adapt parsing as needed

**Web Search Constraints**:
- Search results quality depends on keyword specificity
- Chinese language content may require specific search strategies
- Information recency is critical for trend analysis

**Scoring Subjectivity**:
- Despite structured framework, some scoring involves judgment
- Market conditions change rapidly
- Manufacturing feasibility requires domain expertise validation

**Dashboard Limitations**:
- Static HTML file (not a live web application)
- Requires modern browser for best experience
- Large datasets (>50 products) may impact page performance

## Technical Requirements

**Tools Available**:
- Bash: For API calls using curl
- WebSearch: For researching trending topics (REQUIRED)
- Write: For generating HTML and JSON output files

**Dependencies**:
- No external libraries required for basic functionality
- Modern web browser for viewing dashboard
- Internet connection for API and web searches

## Quality Checklist

Before finalizing output, verify:
- [ ] All trending topics have been researched (2 focused searches each)
- [ ] Search failures handled gracefully with appropriate fallbacks
- [ ] Every product concept includes all required fields
- [ ] Scores are calculated correctly and sum to totals
- [ ] Data limitations marked clearly (⚠️ indicators where applicable)
- [ ] HTML renders correctly with proper UTF-8 encoding
- [ ] Chinese characters display properly
- [ ] Interactive features (sort, filter, search) work
- [ ] Styling differentiates score tiers clearly
- [ ] All links and references are functional
- [ ] Dashboard is responsive on different screen sizes
- [ ] Data accuracy has been verified

## Advanced Features (Optional)

If time and context allow, consider adding:

**Trend Tracking**:
- Compare with previous analyses to identify rising/falling trends
- Track keyword position changes over time
- Identify recurring themes or patterns

**Competitive Analysis**:
- Check for existing similar products on Taobao/Tmall/JD
- Analyze pricing strategies
- Identify market gaps

**Visual Enhancements**:
- Charts and graphs for score distributions
- Trend heat maps
- Category breakdowns (pie charts)
- Timeline visualizations

**Export Options**:
- CSV export for spreadsheet analysis
- PDF generation for presentations
- API-ready JSON for integration with other systems

## Version History

- v1.2 (2026-01-17): Error handling & performance optimization
  - Comprehensive error handling for API, web searches, and file generation
  - Optimized web searches from 3-5 to 2 focused searches per topic
  - Improved reliability with graceful fallbacks
  - 33-40% faster processing time
- v1.1 (2026-01-11): API integration with TianAPI
  - Built-in Weibo trending API
  - Updated data parsing for real API format
- v1.0 (2026-01-11): Initial skill creation
  - Core workflow: API fetch → Research → Scoring → Dashboard
  - 100-point scoring system
  - Interactive HTML dashboard with tier-based highlighting

## References and Resources

**Weibo Trending Data**:
- Official Weibo Hot Search: https://s.weibo.com/top/summary
- Alternative APIs may provide different data structures

**Product Development Resources**:
- Alibaba 1688: For manufacturing partner research
- Taobao/Tmall: For market research and competitive analysis
- Pinduoduo: For trending product categories

**Design Inspiration**:
- Product Hunt: For creative product naming and positioning
- Xiaohongshu (小红书): For lifestyle product trends
- Douyin (抖音): For viral product concepts

## Support and Troubleshooting

**Common Issues**:

1. **API Returns Empty Data**:
   - Verify API endpoint is correct and accessible
   - Check API authentication if required
   - Try alternative Weibo trending API sources

2. **Web Search Not Finding Relevant Information**:
   - Refine search queries to be more specific
   - Try different keyword combinations (Chinese + English)
   - Use site-specific searches (site:weibo.com, site:baidu.com)

3. **HTML Dashboard Not Displaying Correctly**:
   - Ensure file uses UTF-8 encoding
   - Check for JavaScript errors in browser console
   - Verify all HTML tags are properly closed

4. **Scores Seem Inconsistent**:
   - Review scoring guidelines in Section 3
   - Ensure all criteria are evaluated objectively
   - Document reasoning for borderline scores

**Getting Help**:
- Review official Claude Code skills documentation
- Check example skills for similar patterns
- Validate JSON data structure before generating HTML

---

**License**: MIT License - Free to use and modify
**Author**: Claude Code Skills Framework
**Last Updated**: 2026-01-17
**Version**: 1.2