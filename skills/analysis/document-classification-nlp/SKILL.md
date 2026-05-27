---
name: document-classification-nlp
description: "Automatically classify and extract information from construction documents using NLP. Categorize RFIs, submittals, change orders, specifications, and contracts."
---

# Document Classification with NLP

## Overview

This skill implements NLP-based document classification and information extraction for construction projects. Automate document sorting, key term extraction, and content analysis.

**Document Types:**
- RFIs (Requests for Information)
- Submittals and shop drawings
- Change orders and variations
- Specifications and standards
- Contracts and agreements
- Safety reports and permits

## Quick Start

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pandas as pd

# Sample training data
documents = [
    ("Please clarify the steel reinforcement spacing for the foundation slab", "RFI"),
    ("Attached shop drawing for HVAC ductwork layout", "Submittal"),
    ("Additional cost for unforeseen soil conditions", "Change Order"),
    ("Fire-rated wall assembly specification Section 09 21 16", "Specification"),
]

texts, labels = zip(*documents)

# Train classifier
classifier = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=1000, ngram_range=(1, 2))),
    ('clf', MultinomialNB())
])

classifier.fit(texts, labels)

# Classify new document
new_doc = "Request to approve substitution of specified light fixtures"
prediction = classifier.predict([new_doc])[0]
print(f"Classification: {prediction}")  # Output: Submittal
```

## Advanced Classification System

### Document Classifier Class

```python
import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from typing import List, Dict, Tuple, Optional
import spacy
from dataclasses import dataclass

@dataclass
class ClassificationResult:
    document_id: str
    predicted_class: str
    confidence: float
    alternative_classes: List[Tuple[str, float]]
    extracted_entities: Dict[str, List[str]]
    keywords: List[str]

class ConstructionDocumentClassifier:
    """Classify and analyze construction documents"""

    # Document type patterns
    DOCUMENT_PATTERNS = {
        'RFI': [
            r'request\s+for\s+information',
            r'clarification\s+(needed|required|requested)',
            r'please\s+(clarify|confirm|advise)',
            r'question\s+(regarding|about)',
            r'rfi\s*#?\d*'
        ],
        'Submittal': [
            r'submittal',
            r'shop\s+drawing',
            r'product\s+data',
            r'sample\s+submission',
            r'approval\s+request',
            r'material\s+submission'
        ],
        'Change Order': [
            r'change\s+order',
            r'variation\s+order',
            r'cost\s+(increase|adjustment|addition)',
            r'scope\s+change',
            r'additional\s+work',
            r'unforeseen\s+conditions'
        ],
        'Specification': [
            r'section\s+\d{2}\s+\d{2}\s+\d{2}',
            r'specification',
            r'performance\s+requirement',
            r'material\s+standard',
            r'quality\s+standard'
        ],
        'Safety Report': [
            r'incident\s+report',
            r'safety\s+(inspection|violation|observation)',
            r'hazard\s+(identification|assessment)',
            r'near\s+miss',
            r'osha',
            r'jha|jsa'
        ],
        'Contract': [
            r'contract\s+agreement',
            r'terms\s+and\s+conditions',
            r'scope\s+of\s+work',
            r'payment\s+terms',
            r'warranty\s+provision'
        ]
    }

    def __init__(self, use_spacy: bool = True):
        self.classifier = None
        self.vectorizer = None
        self.label_encoder = LabelEncoder()

        if use_spacy:
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except:
                self.nlp = None
        else:
            self.nlp = None

    def train(self, documents: List[str], labels: List[str]) -> Dict:
        """Train the document classifier"""
        # Encode labels
        y = self.label_encoder.fit_transform(labels)

        # Create pipeline
        self.classifier = Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=5000,
                ngram_range=(1, 3),
                stop_words='english',
                sublinear_tf=True
            )),
            ('clf', LinearSVC(C=1.0, class_weight='balanced'))
        ])

        # Train
        self.classifier.fit(documents, y)

        # Cross-validation
        scores = cross_val_score(self.classifier, documents, y, cv=5)

        return {
            'accuracy_mean': scores.mean(),
            'accuracy_std': scores.std(),
            'classes': list(self.label_encoder.classes_)
        }

    def classify(self, document: str) -> ClassificationResult:
        """Classify a single document"""
        if self.classifier is None:
            # Use rule-based classification if no model trained
            return self._rule_based_classify(document)

        # Get prediction
        prediction = self.classifier.predict([document])[0]
        predicted_class = self.label_encoder.inverse_transform([prediction])[0]

        # Get confidence scores
        decision_scores = self.classifier.decision_function([document])[0]
        probs = self._softmax(decision_scores)

        alternatives = [
            (self.label_encoder.inverse_transform([i])[0], float(probs[i]))
            for i in np.argsort(probs)[::-1][1:4]
        ]

        # Extract entities and keywords
        entities = self._extract_entities(document)
        keywords = self._extract_keywords(document)

        return ClassificationResult(
            document_id="",
            predicted_class=predicted_class,
            confidence=float(probs[prediction]),
            alternative_classes=alternatives,
            extracted_entities=entities,
            keywords=keywords
        )

    def _rule_based_classify(self, document: str) -> ClassificationResult:
        """Rule-based classification using patterns"""
        doc_lower = document.lower()
        scores = {}

        for doc_type, patterns in self.DOCUMENT_PATTERNS.items():
            score = sum(
                1 for pattern in patterns
                if re.search(pattern, doc_lower)
            )
            scores[doc_type] = score

        if max(scores.values()) == 0:
            predicted = 'Other'
            confidence = 0.5
        else:
            predicted = max(scores, key=scores.get)
            confidence = scores[predicted] / len(self.DOCUMENT_PATTERNS[predicted])

        return ClassificationResult(
            document_id="",
            predicted_class=predicted,
            confidence=confidence,
            alternative_classes=[],
            extracted_entities=self._extract_entities(document),
            keywords=self._extract_keywords(document)
        )

    def _extract_entities(self, document: str) -> Dict[str, List[str]]:
        """Extract named entities from document"""
        entities = {
            'dates': [],
            'organizations': [],
            'people': [],
            'monetary': [],
            'references': []
        }

        # Date patterns
        date_pattern = r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}'
        entities['dates'] = re.findall(date_pattern, document)

        # Money patterns
        money_pattern = r'\$[\d,]+(?:\.\d{2})?'
        entities['monetary'] = re.findall(money_pattern, document)

        # Reference numbers
        ref_pattern = r'(?:RFI|CO|SI|PR)[-#]?\s*\d+'
        entities['references'] = re.findall(ref_pattern, document, re.IGNORECASE)

        # Use spaCy for NER if available
        if self.nlp:
            doc = self.nlp(document)
            for ent in doc.ents:
                if ent.label_ == 'ORG':
                    entities['organizations'].append(ent.text)
                elif ent.label_ == 'PERSON':
                    entities['people'].append(ent.text)

        return entities

    def _extract_keywords(self, document: str, top_n: int = 10) -> List[str]:
        """Extract key terms from document"""
        # Construction-specific terms
        construction_terms = [
            'concrete', 'steel', 'reinforcement', 'foundation', 'structural',
            'hvac', 'plumbing', 'electrical', 'mechanical', 'architectural',
            'specification', 'drawing', 'detail', 'schedule', 'submittals',
            'rfi', 'change order', 'delay', 'inspection', 'approval'
        ]

        doc_lower = document.lower()
        found_terms = [term for term in construction_terms if term in doc_lower]

        return found_terms[:top_n]

    def _softmax(self, x: np.ndarray) -> np.ndarray:
        """Convert decision scores to probabilities"""
        exp_x = np.exp(x - np.max(x))
        return exp_x / exp_x.sum()

    def batch_classify(self, documents: List[str]) -> pd.DataFrame:
        """Classify multiple documents"""
        results = [self.classify(doc) for doc in documents]

        return pd.DataFrame([{
            'Predicted_Class': r.predicted_class,
            'Confidence': r.confidence,
            'Keywords': ', '.join(r.keywords),
            'Dates_Found': ', '.join(r.extracted_entities['dates']),
            'References_Found': ', '.join(r.extracted_entities['references'])
        } for r in results])
```

## Information Extraction

### Key Information Extractor

```python
class ConstructionInfoExtractor:
    """Extract key information from construction documents"""

    def __init__(self):
        self.patterns = {
            'rfi_number': r'RFI\s*[-#]?\s*(\d+)',
            'submittal_number': r'(?:Submittal|SI)\s*[-#]?\s*(\d+)',
            'change_order_number': r'(?:Change Order|CO|PCO)\s*[-#]?\s*(\d+)',
            'spec_section': r'Section\s*(\d{2}\s*\d{2}\s*\d{2})',
            'cost_amount': r'\$\s*([\d,]+(?:\.\d{2})?)',
            'duration_days': r'(\d+)\s*(?:calendar\s+)?days?',
            'drawing_reference': r'(?:Drawing|Dwg|DWG)\s*[-#]?\s*([A-Z\d-]+)',
            'date': r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            'contractor_name': r'(?:Contractor|Subcontractor):\s*([^\n]+)',
            'project_name': r'Project:\s*([^\n]+)',
            'priority': r'(?:Priority|Urgency):\s*(Critical|High|Medium|Low)'
        }

    def extract_all(self, document: str) -> Dict:
        """Extract all available information"""
        results = {}

        for field, pattern in self.patterns.items():
            matches = re.findall(pattern, document, re.IGNORECASE)
            results[field] = matches if matches else None

        # Post-process
        if results.get('cost_amount'):
            results['cost_amount'] = [
                float(amt.replace(',', ''))
                for amt in results['cost_amount']
            ]

        return results

    def extract_rfi_details(self, document: str) -> Dict:
        """Extract RFI-specific information"""
        return {
            'rfi_number': self._find_first(document, self.patterns['rfi_number']),
            'date_submitted': self._find_first(document, self.patterns['date']),
            'spec_section': self._find_first(document, self.patterns['spec_section']),
            'drawing_ref': self._find_first(document, self.patterns['drawing_reference']),
            'question': self._extract_question(document),
            'priority': self._find_first(document, self.patterns['priority'])
        }

    def extract_change_order_details(self, document: str) -> Dict:
        """Extract change order specific information"""
        costs = re.findall(self.patterns['cost_amount'], document)
        total_cost = sum(float(c.replace(',', '')) for c in costs) if costs else None

        return {
            'co_number': self._find_first(document, self.patterns['change_order_number']),
            'date': self._find_first(document, self.patterns['date']),
            'cost_impact': total_cost,
            'duration_impact': self._find_first(document, self.patterns['duration_days']),
            'reason': self._extract_reason(document),
            'contractor': self._find_first(document, self.patterns['contractor_name'])
        }

    def _find_first(self, document: str, pattern: str) -> Optional[str]:
        match = re.search(pattern, document, re.IGNORECASE)
        return match.group(1) if match else None

    def _extract_question(self, document: str) -> Optional[str]:
        """Extract the question from an RFI"""
        # Look for question markers
        patterns = [
            r'Question:\s*(.+?)(?:\n\n|$)',
            r'(?:Please\s+)?(?:clarify|confirm|advise)(.+?)(?:\.|$)',
        ]
        for pattern in patterns:
            match = re.search(pattern, document, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:500]
        return None

    def _extract_reason(self, document: str) -> Optional[str]:
        """Extract reason for change order"""
        patterns = [
            r'Reason:\s*(.+?)(?:\n\n|$)',
            r'(?:Due to|Because of)\s*(.+?)(?:\.|$)',
        ]
        for pattern in patterns:
            match = re.search(pattern, document, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:500]
        return None
```

## Processing Pipeline

```python
def process_document_batch(documents: List[str], output_path: str):
    """Process and classify a batch of documents"""
    classifier = ConstructionDocumentClassifier()
    extractor = ConstructionInfoExtractor()

    results = []

    for i, doc in enumerate(documents):
        # Classify
        classification = classifier.classify(doc)

        # Extract info based on type
        if classification.predicted_class == 'RFI':
            extracted = extractor.extract_rfi_details(doc)
        elif classification.predicted_class == 'Change Order':
            extracted = extractor.extract_change_order_details(doc)
        else:
            extracted = extractor.extract_all(doc)

        results.append({
            'Document_ID': i + 1,
            'Classification': classification.predicted_class,
            'Confidence': classification.confidence,
            'Keywords': ', '.join(classification.keywords),
            **extracted
        })

    df = pd.DataFrame(results)
    df.to_excel(output_path, index=False)

    return df
```

## Quick Reference

| Document Type | Key Patterns | Extracted Info |
|--------------|--------------|----------------|
| RFI | "request for information", "clarify" | Number, spec section, question |
| Submittal | "shop drawing", "approval request" | Number, product, spec section |
| Change Order | "change order", "additional cost" | Number, cost, duration impact |
| Specification | "Section XX XX XX" | Section number, requirements |
| Safety Report | "incident", "hazard" | Date, type, severity |

## Resources

- **spaCy**: https://spacy.io
- **Scikit-learn**: https://scikit-learn.org
- **DDC Website**: https://datadrivenconstruction.io

## Next Steps

- See `vector-search` for semantic document search
- See `llm-data-automation` for advanced extraction
- See `pdf-to-structured` for PDF processing
