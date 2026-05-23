---
name: gcp-batch-inference
description: Running batch inference on Google Cloud (also known as Vertex AI)
license: MIT
---

# Overview

Get asynchronous, high-throughput, and cost-effective inference for your large-scale data processing needs with Gemini's batch inference (formerly known as batch prediction). This guide will walk you through the value of batch inference, how it works, its limitations, and best practices for optimal results.

## Why use batch inference?

In many real-world scenarios, you don't need an immediate response from a language model. Instead, you might have a large dataset of prompts that you need to process efficiently and affordably. This is where batch inference shines.

## Key benefits include

- **Cost-Effectiveness** Batch processing is offered at a 50% discounted rate compared to real-time inference, making it ideal for large-scale, non-urgent tasks. Implicit caching is enabled by default for Gemini 2.5 Pro, Gemini 2.5 Flash, and Gemini 2.5 Flash-Lite. Implicit caching provides a 90% discount on cached tokens compared to standard input tokens. However, the discounts for cache and batch don't stack. The 90% cache hit discount takes precedence over the batch discount.
- **High rate limits** Process hundreds of thousands of requests in a single batch with a higher rate limit compared to the real time Gemini API.
- **Simplified Workflow** Instead of managing a complex pipeline of individual real-time requests, you can submit a single batch job and retrieve the results once the processing is complete. The service will handle format validation, parallelize requests for concurrent processing, and automatically retry to strive for a high completion rate with 24 hours turnaround time.

## Optimal for tasks

Batch inference is optimized for large-scale processing tasks like:
- **Content Generation** Generate product descriptions, social media posts, or other creative text in bulk.
- **Data Annotation and Classification** Classify user reviews, categorize documents, or perform sentiment analysis on a large corpus of text.
- **Offline Analysis** Summarize articles, extract key information from reports, or translate documents at scale.

# Google Cloud Documentation Links

Review these documentation pages when you need it for the task at hand:
- [Overview](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/batch-prediction-gemini) - See the up-to-date list of supported AI models here.
- [Batch inference from Cloud Storage](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/batch-prediction-from-cloud-storage) - Batch inference from JSONL blobs in a GCS bucket
  - [Creating a batch from GCS using the Python SDK](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/batch-prediction-from-cloud-storage#create-batch-job-python_genai_sdk) 
- [Batch inference for BigQuery](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/batch-prediction-from-bigquery) - Batch inference from table rows in BigQuery
  - [Creating a batch from BigQuery using the Python SDK](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/batch-prediction-from-bigquery#create-batch-job-python_genai_sdk) 
- [Resume an incomplete batch inference job](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/batch-prediction-resume)
- [Context caching](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview) - Implicit caching is simpler, but always store and double-check the inference metrics to ensure that prefix caching is actually effective.

# Abbreviations

- GCP: [Google Cloud Platform](https://cloud.google.com/)
- GCS: [Google Cloud Storage](https://cloud.google.com/storage)
