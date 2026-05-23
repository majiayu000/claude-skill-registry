---
name: content-analysis
description: Analyze text content using both traditional NLP and LLM-enhanced methods. Extract sentiment, topics, keywords, and insights from various content types including social media posts, articles, reviews, and video content. Use when working with text analysis, sentiment detection, topic modeling, or content optimization.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Content Analysis Skill

Analyze text content using advanced NLP techniques and LLM-powered insights to extract sentiment, topics, and actionable intelligence from various content sources.

## Quick Start

This skill helps you:
1. **Analyze sentiment** using both traditional NLP and LLM methods
2. **Extract topics and keywords** from large text datasets
3. **Classify and cluster content** automatically
4. **Identify viral content** patterns and characteristics
5. **Generate content insights** and recommendations
6. **Support multiple languages** and content formats

## When to Use

- **Social Media Analysis**: Facebook, Twitter, Instagram, Weibo posts
- **Content Marketing**: Blog posts, articles, marketing copy analysis
- **Video Content**: YouTube titles, descriptions, comments analysis
- **Product Reviews**: Amazon, e-commerce customer feedback
- **News Analysis**: Article categorization, sentiment tracking
- **Customer Feedback**: Support tickets, surveys, reviews analysis

## Key Requirements

### Traditional NLP Analysis
```bash
pip install pandas numpy matplotlib seaborn nltk scikit-learn wordcloud
```

### LLM-Enhanced Analysis (Optional)
```bash
pip install openai dashscope  # For OpenAI and Qwen API access
```

### Setup NLTK Data
```python
import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')
```

## Core Workflow

### 1. Data Preparation
Your data should include:
- **Text Content**: Main text to analyze (titles, descriptions, comments, etc.)
- **Metadata**: Optional (author, date, category, engagement metrics)
- **Multiple Languages**: Support for English, Chinese, and other languages

### 2. Analysis Process
1. **Text Preprocessing**: Clean, tokenize, and normalize text
2. **Sentiment Analysis**: Traditional VADER + LLM-enhanced analysis
3. **Topic Extraction**: TF-IDF keywords + LLM semantic topics
4. **Content Classification**: Automated categorization and clustering
5. **Pattern Recognition**: Identify viral content characteristics
6. **Insight Generation**: Actionable recommendations

### 3. Output Deliverables
- Sentiment analysis reports with confidence scores
- Topic models and keyword extractions
- Content classification results
- Viral content pattern analysis
- Optimization recommendations

## Example Usage Scenarios

### Social Media Content Analysis
```python
# Analyze Twitter posts for brand sentiment
# Identify trending topics and hashtags
# Measure engagement patterns
```

### YouTube Video Analysis
```python
# Analyze video titles and descriptions
# Extract topics from comments
# Identify viral content patterns
```

### Product Review Analysis
```python
# Analyze customer feedback sentiment
# Extract product feature mentions
# Identify improvement opportunities
```

## Key Analysis Methods

### Traditional NLP Techniques
- **VADER Sentiment Analysis**: Rule-based sentiment scoring
- **TF-IDF Keyword Extraction**: Statistical term importance
- **Text Clustering**: K-means and hierarchical clustering
- **Word Frequency Analysis**: Term frequency and co-occurrence
- **Language Detection**: Automatic language identification

### LLM-Enhanced Analysis
- **Context-Aware Sentiment**: Nuanced emotion understanding
- **Semantic Topic Extraction**: Meaning-based topic identification
- **Content Summarization**: Automatic text summarization
- **Multi-Language Support**: Cross-lingual analysis
- **Zero-Shot Classification**: Categorization without training data

### Advanced Analytics
- **Time Series Analysis**: Content trends over time
- **Engagement Prediction**: Predict viral potential
- **Competitive Analysis**: Compare content performance
- **Audience Insights**: Demographic and preference analysis

## Common Business Questions Answered

1. **What is the overall sentiment toward our brand?**
2. **Which topics are trending in our industry?**
3. **What makes content go viral?**
4. **How does sentiment vary by demographic or region?**
5. **What are customers saying about our products?**
6. **Which content formats perform best?**

## Integration Examples

See [examples/](examples/) directory for:
- `basic_content_analysis.py` - Traditional NLP analysis
- `llm_enhanced_analysis.py` - LLM-powered analysis
- `social_media_analysis.py` - Social media specific analysis
- Sample datasets for testing

## LLM Configuration

### Supported LLM Providers
- **OpenAI**: GPT-3.5, GPT-4 models
- **Qwen (通义千问)**: Chinese-optimized models
- **Open Source**: Local models via HuggingFace

### API Setup Examples
```python
# OpenAI Configuration
import openai
openai.api_key = 'your-api-key'

# Qwen Configuration
import dashscope
dashscope.api_key = 'your-api-key'
```

## Best Practices

1. **Data Quality**: Ensure clean, consistent text data
2. **Sampling Strategy**: Use representative samples for LLM analysis
3. **Cost Management**: Balance traditional NLP with LLM calls
4. **Language Handling**: Configure appropriate language models
5. **Validation**: Cross-validate sentiment analysis results
6. **Privacy**: Ensure compliance with data protection regulations

## Performance Optimization

### For Large Datasets
- Use data sampling for LLM analysis
- Implement batch processing
- Cache LLM responses when possible
- Use traditional NLP for initial filtering

### Cost Management
- Prioritize important content for LLM analysis
- Use traditional NLP for bulk processing
- Implement smart sampling strategies
- Monitor API usage and costs

## Advanced Features

- **Real-time Analysis**: Stream processing for live content
- **Multi-modal Analysis**: Text + image + video content
- **Custom Models**: Fine-tune models for specific domains
- **Integration APIs**: Connect with content management systems
- **Automated Reporting**: Scheduled analysis and reporting

## Troubleshooting

### Common Issues
1. **Low Sentiment Accuracy**: Check language settings and text preprocessing
2. **High API Costs**: Optimize sampling and caching strategies
3. **Slow Processing**: Implement parallel processing and batching
4. **Language Support**: Ensure appropriate models for non-English content

### Performance Tips
- Pre-process text data effectively
- Use appropriate model sizes for tasks
- Implement result caching
- Monitor resource usage and optimize