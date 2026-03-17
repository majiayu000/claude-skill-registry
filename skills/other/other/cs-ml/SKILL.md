---
name: cs-ml
cluster: computer-science
description: "ML: supervised/unsupervised/RL, CNN/RNN/Transformer, training, evaluation, MLOps, LLM fine-tuning"
tags: ["ml","deep-learning","neural-networks","transformers","cs"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "machine learning neural network transformer training model deployment llm"
---

# cs-ml

## Purpose
This skill handles machine learning tasks, including supervised/unsupervised learning, reinforcement learning, CNN/RNN/Transformer models, training pipelines, evaluation metrics, MLOps workflows, and LLM fine-tuning. It integrates with OpenClaw to automate code generation and execution for ML projects.

## When to Use
Use this skill when building ML models from scratch, fine-tuning pre-trained models like BERT, deploying models via MLOps, or evaluating performance. Apply it for tasks involving large datasets, neural networks, or production pipelines, such as image recognition with CNNs or text generation with Transformers.

## Key Capabilities
- Train supervised models using algorithms like linear regression or decision trees via scikit-learn integration.
- Implement unsupervised learning with K-means clustering or PCA for dimensionality reduction.
- Build and train deep learning models: CNNs for images (e.g., using Keras), RNNs for sequences, or Transformers for NLP tasks.
- Handle RL environments with libraries like Stable Baselines, including Q-learning loops.
- Evaluate models with metrics like accuracy, F1-score, or ROC curves, and generate confusion matrices.
- Manage MLOps: model deployment to containers, monitoring with MLflow, and CI/CD integration.
- Fine-tune LLMs like GPT variants using Hugging Face Transformers, with techniques like LoRA for efficiency.

## Usage Patterns
Invoke this skill via OpenClaw's CLI or API to generate code snippets. For training, specify model type and data source; for evaluation, provide a trained model path. Always set environment variables for authentication, e.g., export $OPENCLAW_API_KEY=your_key. Patterns include: 
- Pipeline mode: Chain training and evaluation in a single command.
- Interactive mode: Use for iterative fine-tuning, querying the skill for code adjustments.
- Example 1: Train a CNN for image classification – Call the skill with data path, then run the generated script.
- Example 2: Fine-tune an LLM – Provide a base model and dataset, get a fine-tuning script, and execute it with specified hyperparameters.

## Common Commands/API
Use OpenClaw's CLI for direct execution or API for programmatic access. Authentication requires $OPENCLAW_API_KEY in your environment.

- CLI Command for training a CNN:  
  `openclaw cs-ml train --model cnn --data /path/to/images --epochs 10 --batch-size 32`  
  This generates a Python script using TensorFlow:  
  ```python
  from tensorflow import keras
  model = keras.Sequential([keras.layers.Conv2D(32, 3, activation='relu')])
  model.fit(train_data, epochs=10)
  ```

- CLI Command for LLM fine-tuning:  
  `openclaw cs-ml fine-tune --model bert --dataset /path/to/text.json --learning-rate 5e-5`  
  Output script example:  
  ```python
  from transformers import BertForSequenceClassification
  model = BertForSequenceClassification.from_pretrained('bert-base')
  trainer = Trainer(model=model, train_dataset=dataset)
  trainer.train()
  ```

- API Endpoint for evaluation:  
  POST to `https://api.openclaw.com/cs-ml/evaluate` with JSON body:  
  `{ "model_path": "/path/to/model.h5", "data_path": "/path/to/test.csv", "metrics": ["accuracy", "f1"] }`  
  Response includes metrics output.

- Config Format: Use YAML for hyperparameters, e.g.:  
  ```yaml
  model: transformer
  params:
    layers: 12
    hidden_size: 768
  ```

## Integration Notes
Integrate this skill with other OpenClaw skills by chaining commands, e.g., use "data-processing" skill first for data cleaning, then pass output to cs-ml for training. For external tools, set up dependencies like installing TensorFlow via `pip install tensorflow` in your generated scripts. Use $OPENCLAW_API_KEY for API calls in custom code. For MLOps, link with cloud services: export model to S3 with AWS CLI, then deploy via cs-ml command. Ensure compatibility by specifying library versions, e.g., Transformers 4.20+.

## Error Handling
Common errors include data mismatches, authentication failures, or library version conflicts. Handle them as follows:
- Data errors: Check for shape issues in training commands, e.g., if `openclaw cs-ml train` fails with "Input shape mismatch", verify data with `--validate-data` flag.
- Authentication: If API calls fail with 401, ensure $OPENCLAW_API_KEY is set and not expired; retry with `openclaw cs-ml --retry-auth`.
- Runtime errors: For GPU issues in deep learning, add `--device cuda` and handle with try-except in generated code:  
  ```python
  try:
      model.fit(data)
  except RuntimeError as e:
      print(f"Error: {e}, falling back to CPU")
  ```
- General: Log outputs with `--verbose` flag and debug generated scripts line-by-line.

## Graph Relationships
- Related to cluster: computer-science
- Connected tags: ml, deep-learning, neural-networks, transformers, cs
- Links to other skills: depends on "data-processing" for preprocessing; enhances "deployment" for MLOps pipelines; integrates with "nlp" for Transformer-based tasks
