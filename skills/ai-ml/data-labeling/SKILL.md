---
name: data-labeling
description: Set up and manage data labeling workflows using manual annotation tools, semi-automated pipelines, active learning, and programmatic weak supervision. Use when the user requests data labeling or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: AI Agent Skills
  version: 1.0.0
---

# Data Labeling

This skill enables an AI agent to design and execute data labeling workflows for machine learning projects. It covers manual annotation with tools like Label Studio, semi-automated labeling with model-assisted pre-annotation, active learning loops that prioritize the most informative samples, and programmatic weak supervision using labeling functions. The agent handles label schema design, annotator guidelines, quality control through inter-annotator agreement, and export to ML-ready formats.

## Workflow

1. **Define the labeling schema and guidelines:** Design the label taxonomy — classes for classification, entity types for NER, bounding box categories for object detection, or segment labels for semantic segmentation. Write clear annotator guidelines with positive and negative examples for each label, covering boundary cases and ambiguous scenarios.

2. **Set up the labeling environment:** Configure a labeling tool (Label Studio, Labelbox, or Prodigy) with the schema, import the raw data, and set up user accounts with appropriate permissions. Define the labeling interface template that matches the task type — text classification, span annotation, image bounding boxes, or multi-turn dialogue tagging.

3. **Pre-annotate with model predictions:** Use existing models or heuristic rules to generate preliminary labels for the dataset. Annotators then review and correct these predictions rather than labeling from scratch, which can reduce annotation time by 40-60%. This is especially valuable for tasks where a decent baseline model already exists.

4. **Execute labeling with quality control:** Assign labeling tasks to annotators with built-in redundancy — have 2-3 annotators label the same items to measure inter-annotator agreement (Cohen's kappa or Fleiss' kappa). Flag items with low agreement for review by a senior annotator. Track annotator accuracy against a gold-standard set embedded in the task queue.

5. **Run active learning iterations:** After an initial labeled set is created, train a model and use uncertainty sampling or query-by-committee to select the most informative unlabeled examples for the next round of annotation. This maximizes model improvement per labeled sample and is critical when labeling budgets are limited.

6. **Export and validate:** Export labeled data in the format required by the training pipeline (JSONL, COCO, CoNLL, CSV). Run validation checks to ensure label consistency, check for missing annotations, and verify that the class distribution meets requirements. Document the labeling process and dataset statistics for reproducibility.

## Supported Technologies

- **Annotation tools:** Label Studio, Labelbox, Prodigy (spaCy), Amazon SageMaker Ground Truth, CVAT
- **Weak supervision:** Snorkel, Flyingsquid, Skweak
- **Active learning:** modAL, ALiPy, Prodigy active learning recipes
- **Agreement metrics:** Cohen's kappa, Fleiss' kappa, Krippendorff's alpha
- **Export formats:** COCO JSON, Pascal VOC XML, CoNLL, JSONL, Hugging Face Datasets

## Usage

Provide the agent with the raw dataset, the task type (classification, NER, object detection, etc.), and the label categories. Optionally specify the labeling tool preference and quality requirements (minimum inter-annotator agreement). The agent will configure the labeling environment, set up quality control, and manage the annotation workflow.

## Examples

### Example 1: Label Studio Pipeline for Text Classification

**Label Studio labeling interface configuration (`config.xml`):**

```xml
<View>
  <Header value="Classify the customer review sentiment:" />
  <Text name="text" value="$text" />
  <Choices name="sentiment" toName="text" choice="single-column" showInline="true">
    <Choice value="positive" />
    <Choice value="negative" />
    <Choice value="neutral" />
  </Choices>
  <Textarea name="notes" toName="text" placeholder="Optional: explain ambiguous cases"
            maxSubmissions="1" editable="true" />
</View>
```

**Python script to set up the project and import data:**

```python
from label_studio_sdk import Client

ls = Client(url="http://localhost:8080", api_key="your-api-key")

project = ls.start_project(
    title="Customer Review Sentiment",
    label_config=open("config.xml").read(),
    description="Label customer reviews as positive, negative, or neutral.",
)

# Import tasks from a CSV file
import csv
tasks = []
with open("reviews.csv") as f:
    for row in csv.DictReader(f):
        tasks.append({"data": {"text": row["review_text"]}, "meta": {"source_id": row["id"]}})

project.import_tasks(tasks)

# Configure inter-annotator overlap: each task gets 2 annotators
project.set_params(maximum_annotations=2, overlap_cohort_percentage=100)
print(f"Created project with {len(tasks)} tasks, 2 annotators per task")

# After annotation, export results
annotations = project.export_tasks(export_type="JSON")
# Compute agreement
from sklearn.metrics import cohen_kappa_score
labels_a1 = [a["annotations"][0]["result"][0]["value"]["choices"][0] for a in annotations if len(a["annotations"]) >= 2]
labels_a2 = [a["annotations"][1]["result"][0]["value"]["choices"][0] for a in annotations if len(a["annotations"]) >= 2]
print(f"Cohen's kappa: {cohen_kappa_score(labels_a1, labels_a2):.3f}")
```

### Example 2: Weak Supervision with Snorkel Labeling Functions

```python
import pandas as pd
import numpy as np
from snorkel.labeling import labeling_function, PandasLFApplier, LFAnalysis
from snorkel.labeling.model import LabelModel

SPAM = 1
HAM = 0
ABSTAIN = -1

df = pd.DataFrame({
    "text": [
        "Congratulations! You've won a free iPhone!", "Meeting at 3pm tomorrow",
        "URGENT: claim your prize now!!!", "Can you review the Q3 report?",
        "Buy cheap meds online fast", "Lunch plans for Thursday?",
        "Click here for a free vacation", "Project deadline is next Friday",
    ]
})

@labeling_function()
def lf_contains_free(x):
    return SPAM if "free" in x.text.lower() else ABSTAIN

@labeling_function()
def lf_contains_urgent(x):
    return SPAM if "urgent" in x.text.lower() else ABSTAIN

@labeling_function()
def lf_contains_click(x):
    return SPAM if "click" in x.text.lower() else ABSTAIN

@labeling_function()
def lf_excessive_punctuation(x):
    return SPAM if x.text.count("!") >= 3 else ABSTAIN

@labeling_function()
def lf_contains_meeting(x):
    return HAM if any(w in x.text.lower() for w in ["meeting", "project", "report", "deadline"]) else ABSTAIN

@labeling_function()
def lf_short_and_casual(x):
    return HAM if len(x.text.split()) < 8 and "?" in x.text else ABSTAIN

lfs = [lf_contains_free, lf_contains_urgent, lf_contains_click,
       lf_excessive_punctuation, lf_contains_meeting, lf_short_and_casual]

applier = PandasLFApplier(lfs=lfs)
L_train = applier.apply(df=df)

print(LFAnalysis(L=L_train, lfs=lfs).lf_summary())

# Train the label model to combine noisy labeling functions
label_model = LabelModel(cardinality=2, verbose=True)
label_model.fit(L_train=L_train, n_epochs=500, log_freq=100, seed=42)

# Get probabilistic labels
probs = label_model.predict_proba(L=L_train)
df["label"] = label_model.predict(L=L_train)
df["confidence"] = np.max(probs, axis=1)

# Filter out low-confidence samples for manual review
confident = df[df["confidence"] > 0.8]
needs_review = df[df["confidence"] <= 0.8]
print(f"Confidently labeled: {len(confident)}, needs manual review: {len(needs_review)}")
```

## Best Practices

- **Write detailed annotation guidelines** with at least 3 positive and 3 negative examples per label, covering edge cases. Update guidelines as annotators surface ambiguous cases during labeling.
- **Embed gold-standard items** (5-10% of tasks) with known correct labels into the annotation queue to continuously monitor annotator quality and catch fatigue or confusion.
- **Measure inter-annotator agreement** with Cohen's kappa (2 annotators) or Fleiss' kappa (3+). A kappa below 0.6 indicates the guidelines or schema need revision before proceeding.
- **Use active learning** when the labeling budget is limited — it can achieve the same model performance with 30-50% fewer labeled examples by focusing annotation effort on the most uncertain or informative samples.
- **Version your labeled datasets** with clear metadata (annotator IDs, timestamps, guideline version) so you can trace labels back to specific annotation campaigns and reproduce results.
- **Start with a pilot round** of 50-100 samples before scaling up. Use the pilot to calibrate guidelines, estimate annotation speed, and identify schema issues early.

## Edge Cases

- **High annotator disagreement:** When kappa drops below 0.4, the task definition is likely ambiguous. Split the problematic label into more specific sub-labels, add more examples to guidelines, or hold a calibration session with annotators to align understanding.
- **Severe class imbalance in the raw data:** If the target class is rare (< 5%), random sampling will produce few positive examples. Use keyword filtering, model-based pre-selection, or stratified sampling to enrich the annotation queue with likely positive examples.
- **Labeling function conflicts in weak supervision:** When multiple labeling functions disagree on the same sample, the label model may produce low-confidence predictions. Increase labeling function coverage by writing more specific functions, or route conflicting samples to manual annotation.
- **Annotator fatigue on large batches:** Quality degrades after 2-3 hours of continuous labeling. Break work into sessions of 100-200 items, randomize task order, and track per-session accuracy against gold standards to detect quality drops.
- **Schema evolution mid-project:** If new label categories are added after annotation has started, all previously labeled data must be reviewed for the new categories. Use versioned schemas and re-annotation queues rather than retroactively editing existing annotations.
