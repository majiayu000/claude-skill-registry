---
name: Sentiment Analysis
description: Classify text sentiment using NLP techniques, lexicon-based analysis, and machine learning for opinion mining, brand monitoring, and customer feedback analysis
---

# Sentiment Analysis

## Overview

Sentiment analysis determines emotional tone and opinions in text, enabling understanding of customer satisfaction, brand perception, and feedback analysis.

## Approaches

- **Lexicon-based**: Using sentiment dictionaries
- **Machine Learning**: Training classifiers on labeled data
- **Deep Learning**: Neural networks for complex patterns
- **Aspect-based**: Sentiment about specific features
- **Multilingual**: Non-English text analysis

## Sentiment Types

- **Positive**: Favorable, satisfied
- **Negative**: Unfavorable, dissatisfied
- **Neutral**: Factual, no clear sentiment
- **Mixed**: Combination of sentiments

## Implementation with Python

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import re
from collections import Counter

# Sample review data
reviews_data = [
    "This product is amazing! I love it so much.",
    "Terrible quality, very disappointed.",
    "It's okay, nothing special.",
    "Best purchase ever! Highly recommend.",
    "Worst product I've ever bought.",
    "Pretty good, satisfied with the purchase.",
    "Excellent service and fast delivery.",
    "Poor quality and bad customer support.",
    "Not bad, does what it's supposed to.",
    "Absolutely fantastic! Five stars!",
    "Mediocre product, expected better.",
    "Love everything about this!",
    "Complete waste of money.",
    "Good value for the price.",
    "Very satisfied, will buy again!",
    "Horrible experience from start to finish.",
    "It works as described.",
    "Outstanding quality and design!",
    "Disappointed with the results.",
    "Perfect! Exactly what I wanted.",
]

sentiments = [
    'Positive', 'Negative', 'Neutral', 'Positive', 'Negative',
    'Positive', 'Positive', 'Negative', 'Neutral', 'Positive',
    'Negative', 'Positive', 'Negative', 'Positive', 'Positive',
    'Negative', 'Neutral', 'Positive', 'Negative', 'Positive'
]

df = pd.DataFrame({'review': reviews_data, 'sentiment': sentiments})

print("Sample Reviews:")
print(df.head(10))

# 1. Lexicon-based Sentiment Analysis
from nltk.sentiment import SentimentIntensityAnalyzer
try:
    import nltk
    nltk.download('vader_lexicon', quiet=True)
    sia = SentimentIntensityAnalyzer()

    df['vader_scores'] = df['review'].apply(lambda x: sia.polarity_scores(x))
    df['vader_compound'] = df['vader_scores'].apply(lambda x: x['compound'])
    df['vader_sentiment'] = df['vader_compound'].apply(
        lambda x: 'Positive' if x > 0.05 else ('Negative' if x < -0.05 else 'Neutral')
    )

    print("\n1. VADER Sentiment Scores:")
    print(df[['review', 'vader_compound', 'vader_sentiment']].head())
except:
    print("NLTK not available, skipping VADER analysis")

# 2. Textblob Sentiment (alternative)
try:
    from textblob import TextBlob

    df['textblob_polarity'] = df['review'].apply(lambda x: TextBlob(x).sentiment.polarity)
    df['textblob_sentiment'] = df['textblob_polarity'].apply(
        lambda x: 'Positive' if x > 0.1 else ('Negative' if x < -0.1 else 'Neutral')
    )

    print("\n2. TextBlob Sentiment Scores:")
    print(df[['review', 'textblob_polarity', 'textblob_sentiment']].head())
except:
    print("TextBlob not available")

# 3. Feature Extraction for ML
vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
X = vectorizer.fit_transform(df['review'])
y = df['sentiment']

print(f"\n3. Feature Matrix Shape: {X.shape}")
print(f"Features extracted: {len(vectorizer.get_feature_names_out())}")

# 4. Machine Learning Model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Naive Bayes classifier
nb_model = MultinomialNB()
nb_model.fit(X_train, y_train)
y_pred = nb_model.predict(X_test)

print("\n4. Machine Learning Results:")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# 5. Sentiment Distribution
fig, axes = plt.subplots(2, 2, figsize=(14, 8))

# Distribution of sentiments
sentiment_counts = df['sentiment'].value_counts()
axes[0, 0].bar(sentiment_counts.index, sentiment_counts.values, color=['green', 'red', 'gray'], alpha=0.7, edgecolor='black')
axes[0, 0].set_title('Sentiment Distribution')
axes[0, 0].set_ylabel('Count')
axes[0, 0].grid(True, alpha=0.3, axis='y')

# Pie chart
axes[0, 1].pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%',
               colors=['green', 'red', 'gray'], startangle=90)
axes[0, 1].set_title('Sentiment Proportion')

# VADER compound scores distribution
if 'vader_compound' in df.columns:
    axes[1, 0].hist(df['vader_compound'], bins=20, color='steelblue', edgecolor='black', alpha=0.7)
    axes[1, 0].axvline(x=0.05, color='green', linestyle='--', label='Positive threshold')
    axes[1, 0].axvline(x=-0.05, color='red', linestyle='--', label='Negative threshold')
    axes[1, 0].set_xlabel('VADER Compound Score')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].set_title('VADER Score Distribution')
    axes[1, 0].legend()

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[1, 1],
            xticklabels=np.unique(y_test), yticklabels=np.unique(y_test))
axes[1, 1].set_title('Classification Confusion Matrix')
axes[1, 1].set_ylabel('True Label')
axes[1, 1].set_xlabel('Predicted Label')

plt.tight_layout()
plt.show()

# 6. Most Informative Features
feature_names = vectorizer.get_feature_names_out()

# Get feature importance from Naive Bayes
for sentiment_class, idx in enumerate(np.unique(y)):
    class_idx = list(np.unique(y)).index(idx)
    top_features_idx = np.argsort(nb_model.feature_log_prob_[class_idx])[-5:]

    print(f"\nTop features for '{idx}':")
    for feature_idx in reversed(top_features_idx):
        print(f"  {feature_names[feature_idx]}")

# 7. Word frequency analysis
positive_words = ' '.join(df[df['sentiment'] == 'Positive']['review'].values).lower()
negative_words = ' '.join(df[df['sentiment'] == 'Negative']['review'].values).lower()

# Clean and tokenize
def get_words(text):
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()
    return [w for w in words if len(w) > 2]

pos_word_freq = Counter(get_words(positive_words))
neg_word_freq = Counter(get_words(negative_words))

# Visualization
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Positive words
top_pos_words = dict(pos_word_freq.most_common(10))
axes[0].barh(list(top_pos_words.keys()), list(top_pos_words.values()), color='green', alpha=0.7, edgecolor='black')
axes[0].set_xlabel('Frequency')
axes[0].set_title('Top Words in Positive Reviews')
axes[0].invert_yaxis()

# Negative words
top_neg_words = dict(neg_word_freq.most_common(10))
axes[1].barh(list(top_neg_words.keys()), list(top_neg_words.values()), color='red', alpha=0.7, edgecolor='black')
axes[1].set_xlabel('Frequency')
axes[1].set_title('Top Words in Negative Reviews')
axes[1].invert_yaxis()

plt.tight_layout()
plt.show()

# 8. Trend analysis (simulated over time)
dates = pd.date_range('2023-01-01', periods=len(df))
df['date'] = dates
df['rolling_sentiment_score'] = df['vader_compound'].rolling(window=3, center=True).mean()

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df['date'], df['rolling_sentiment_score'], marker='o', linewidth=2, label='Rolling Avg (3-day)')
ax.scatter(df['date'], df['vader_compound'], alpha=0.5, s=30, label='Daily Score')
ax.axhline(y=0, color='black', linestyle='--', alpha=0.3)
ax.fill_between(df['date'], df['rolling_sentiment_score'], 0,
                where=(df['rolling_sentiment_score'] > 0), alpha=0.3, color='green', label='Positive')
ax.fill_between(df['date'], df['rolling_sentiment_score'], 0,
                where=(df['rolling_sentiment_score'] <= 0), alpha=0.3, color='red', label='Negative')
ax.set_xlabel('Date')
ax.set_ylabel('Sentiment Score')
ax.set_title('Sentiment Trend Over Time')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# 9. Aspect-based sentiment (simulated)
aspects = ['Quality', 'Price', 'Delivery', 'Customer Service']
aspect_sentiments = []

for aspect in aspects:
    keywords = {
        'Quality': ['quality', 'product', 'design', 'material'],
        'Price': ['price', 'cost', 'expensive', 'value'],
        'Delivery': ['delivery', 'fast', 'shipping', 'arrived'],
        'Customer Service': ['service', 'support', 'customer', 'help']
    }

    # Count mentions and associated sentiment
    aspect_reviews = df[df['review'].str.contains('|'.join(keywords[aspect]), case=False)]
    if len(aspect_reviews) > 0:
        avg_sentiment = aspect_reviews['vader_compound'].mean()
        aspect_sentiments.append({
            'Aspect': aspect,
            'Avg Sentiment': avg_sentiment,
            'Count': len(aspect_reviews)
        })

aspect_df = pd.DataFrame(aspect_sentiments)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Aspect sentiment scores
colors_aspect = ['green' if x > 0 else 'red' for x in aspect_df['Avg Sentiment']]
axes[0].barh(aspect_df['Aspect'], aspect_df['Avg Sentiment'], color=colors_aspect, alpha=0.7, edgecolor='black')
axes[0].set_xlabel('Average Sentiment Score')
axes[0].set_title('Sentiment by Aspect')
axes[0].axvline(x=0, color='black', linestyle='-', linewidth=0.8)
axes[0].grid(True, alpha=0.3, axis='x')

# Mention count
axes[1].bar(aspect_df['Aspect'], aspect_df['Count'], color='steelblue', alpha=0.7, edgecolor='black')
axes[1].set_ylabel('Number of Mentions')
axes[1].set_title('Aspect Mention Frequency')
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

# 10. Summary report
print("\n" + "="*50)
print("SENTIMENT ANALYSIS SUMMARY")
print("="*50)
print(f"Total Reviews: {len(df)}")
print(f"Positive: {len(df[df['sentiment'] == 'Positive'])} ({len(df[df['sentiment'] == 'Positive'])/len(df)*100:.1f}%)")
print(f"Negative: {len(df[df['sentiment'] == 'Negative'])} ({len(df[df['sentiment'] == 'Negative'])/len(df)*100:.1f}%)")
print(f"Neutral: {len(df[df['sentiment'] == 'Neutral'])} ({len(df[df['sentiment'] == 'Neutral'])/len(df)*100:.1f}%)")
if 'vader_compound' in df.columns:
    print(f"\nAverage VADER Score: {df['vader_compound'].mean():.3f}")
    print(f"Model Accuracy: {accuracy_score(y_test, y_pred):.2%}")
print("="*50)
```

## Methods Comparison

- **Lexicon-based**: Fast, interpretable, limited context
- **Machine Learning**: Requires training data, good accuracy
- **Deep Learning**: Complex patterns, needs large dataset
- **Hybrid**: Combines multiple approaches

## Applications

- Customer feedback analysis
- Product reviews monitoring
- Social media sentiment
- Brand perception tracking
- Chatbot sentiment detection

## Deliverables

- Sentiment distribution analysis
- Classified sentiments for all texts
- Confidence scores
- Feature importance for classification
- Trend analysis visualizations
- Aspect-based sentiment breakdown
- Executive summary with insights
