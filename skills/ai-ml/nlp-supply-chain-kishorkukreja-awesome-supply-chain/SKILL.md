---
name: nlp-supply-chain
description: When the user wants to apply NLP to supply chain, extract information from documents, analyze supplier communications, classify items, or process unstructured text. Also use when the user mentions "natural language processing," "NLP," "text mining," "document extraction," "supplier sentiment analysis," "product classification from text," "BERT," "transformers for text," or "chatbots for supply chain." For general ML, see ml-supply-chain.
---

# Natural Language Processing for Supply Chain

You are an expert in applying NLP to supply chain problems. Your goal is to extract insights from unstructured text, automate document processing, analyze supplier communications, and classify products using modern NLP techniques.

## Applications

1. **Document Processing**: Purchase orders, invoices, contracts
2. **Product Classification**: Categorize items from descriptions
3. **Supplier Risk Analysis**: Analyze news, reports, sentiment
4. **Demand Sensing**: Social media, reviews, trends
5. **Chatbots**: Customer service, internal queries

---

## Product Classification with BERT

```python
from transformers import BertTokenizer, BertForSequenceClassification
import torch

class ProductClassifier:
    """
    Classify products from text descriptions using BERT
    """
    
    def __init__(self, num_classes):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertForSequenceClassification.from_pretrained(
            'bert-base-uncased',
            num_labels=num_classes
        )
    
    def classify(self, product_description):
        """Classify product from description"""
        
        # Tokenize
        inputs = self.tokenizer(
            product_description,
            return_tensors='pt',
            truncation=True,
            padding=True,
            max_length=128
        )
        
        # Predict
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            predicted_class = torch.argmax(logits, dim=1).item()
        
        return predicted_class
```

---

## Named Entity Recognition (NER) for Invoices

```python
from transformers import pipeline

class InvoiceExtractor:
    """
    Extract entities from invoices using NER
    """
    
    def __init__(self):
        self.ner = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")
    
    def extract_entities(self, invoice_text):
        """Extract company names, dates, amounts"""
        
        entities = self.ner(invoice_text)
        
        extracted = {
            'companies': [],
            'dates': [],
            'amounts': []
        }
        
        for ent in entities:
            if ent['entity'].startswith('B-ORG') or ent['entity'].startswith('I-ORG'):
                extracted['companies'].append(ent['word'])
            elif ent['entity'].startswith('B-DATE'):
                extracted['dates'].append(ent['word'])
        
        return extracted
```

---

## Supplier Risk Sentiment Analysis

```python
from transformers import pipeline

class SupplierRiskAnalyzer:
    """
    Analyze supplier risk from news and reports
    """
    
    def __init__(self):
        self.sentiment_analyzer = pipeline("sentiment-analysis")
    
    def analyze_news(self, articles):
        """Analyze sentiment of news about supplier"""
        
        sentiments = []
        for article in articles:
            result = self.sentiment_analyzer(article['text'])[0]
            sentiments.append({
                'article': article['title'],
                'sentiment': result['label'],
                'score': result['score']
            })
        
        # Aggregate risk
        negative_count = sum(1 for s in sentiments if s['sentiment'] == 'NEGATIVE')
        risk_score = negative_count / len(sentiments)
        
        return {
            'risk_score': risk_score,
            'sentiments': sentiments
        }
```

---

## Chatbot for Supply Chain Queries

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

class SupplyChainChatbot:
    """
    Chatbot for internal supply chain queries
    """
    
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
    
    def respond(self, user_input, chat_history):
        """Generate response to user query"""
        
        # Encode input
        new_input_ids = self.tokenizer.encode(
            user_input + self.tokenizer.eos_token,
            return_tensors='pt'
        )
        
        # Generate response
        chat_history_ids = torch.cat([chat_history, new_input_ids], dim=-1)                           if chat_history is not None else new_input_ids
        
        response_ids = self.model.generate(
            chat_history_ids,
            max_length=1000,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        response = self.tokenizer.decode(
            response_ids[:, chat_history_ids.shape[-1]:][0],
            skip_special_tokens=True
        )
        
        return response, response_ids
```

---

## Tools & Libraries

- `transformers (Hugging Face)`: BERT, GPT, T5
- `spaCy`: industrial NLP
- `NLTK`: text processing
- `Gensim`: topic modeling
- `OpenAI API`: GPT-4 integration

---

## Related Skills

- **ml-supply-chain**: general ML
- **supplier-risk-management`: risk analysis
- **demand-forecasting**: demand sensing from text
