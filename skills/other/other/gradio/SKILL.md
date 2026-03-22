---
name: gradio
description: |
  Python library for building ML demo UIs with minimal code. Create interactive web interfaces
  for models with text, image, audio, and video inputs/outputs. Share demos via public links
  or deploy to Hugging Face Spaces.
license: Apache-2.0
compatibility: 'python 3.8+, gradio 4.0+, Linux/macOS/Windows'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: data-ai
  tags:
    - ml-demos
    - web-ui
    - huggingface-spaces
    - interactive
    - prototyping
---

# Gradio

## Installation

```bash
# Install Gradio
pip install gradio
```

## Quick Start — Simple Interface

```python
# hello.py — Minimal Gradio app with a text interface
import gradio as gr

def greet(name: str, intensity: int) -> str:
    return "Hello, " + name + "!" * intensity

demo = gr.Interface(
    fn=greet,
    inputs=["text", gr.Slider(1, 10, value=1, label="Excitement")],
    outputs="text",
    title="Greeting Generator",
    description="Enter your name and excitement level.",
)

demo.launch()  # Opens http://localhost:7860
```

## Chat Interface

```python
# chatbot.py — Build a chatbot UI with streaming responses
import gradio as gr
from openai import OpenAI

client = OpenAI()

def chat(message: str, history: list) -> str:
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for h in history:
        messages.append({"role": "user", "content": h[0]})
        if h[1]:
            messages.append({"role": "assistant", "content": h[1]})
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        stream=True,
    )

    partial = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            partial += chunk.choices[0].delta.content
            yield partial

demo = gr.ChatInterface(
    fn=chat,
    title="AI Chat",
    description="Chat with GPT-4",
    examples=["Tell me a joke", "Explain quantum computing"],
)
demo.launch()
```

## Image Classification

```python
# image_classifier.py — Image classification demo with a pre-trained model
import gradio as gr
from transformers import pipeline

classifier = pipeline("image-classification", model="google/vit-base-patch16-224")

def classify(image):
    results = classifier(image)
    return {r["label"]: r["score"] for r in results}

demo = gr.Interface(
    fn=classify,
    inputs=gr.Image(type="pil"),
    outputs=gr.Label(num_top_classes=5),
    title="Image Classifier",
    examples=["cat.jpg", "dog.jpg"],
)
demo.launch()
```

## Blocks API (Custom Layouts)

```python
# blocks_app.py — Build complex layouts with the Blocks API
import gradio as gr

def process_text(text: str, operation: str) -> str:
    if operation == "Uppercase":
        return text.upper()
    elif operation == "Lowercase":
        return text.lower()
    elif operation == "Word Count":
        return f"Word count: {len(text.split())}"
    return text

with gr.Blocks(title="Text Processor", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Text Processing Tool")

    with gr.Row():
        with gr.Column(scale=2):
            text_input = gr.Textbox(label="Input Text", lines=5, placeholder="Enter text here...")
            operation = gr.Radio(
                choices=["Uppercase", "Lowercase", "Word Count"],
                label="Operation",
                value="Uppercase",
            )
            submit_btn = gr.Button("Process", variant="primary")
        with gr.Column(scale=1):
            output = gr.Textbox(label="Result", lines=5)

    submit_btn.click(fn=process_text, inputs=[text_input, operation], outputs=output)

demo.launch()
```

## File Upload and Download

```python
# file_processing.py — Handle file uploads and provide downloadable outputs
import gradio as gr
import pandas as pd

def analyze_csv(file) -> tuple[str, str]:
    df = pd.read_csv(file.name)
    summary = f"Rows: {len(df)}, Columns: {len(df.columns)}\n\n"
    summary += f"Columns: {', '.join(df.columns)}\n\n"
    summary += df.describe().to_string()

    output_path = "/tmp/summary.csv"
    df.describe().to_csv(output_path)
    return summary, output_path

demo = gr.Interface(
    fn=analyze_csv,
    inputs=gr.File(label="Upload CSV"),
    outputs=[gr.Textbox(label="Summary"), gr.File(label="Download Summary")],
)
demo.launch()
```

## Authentication and Sharing

```python
# auth_and_share.py — Add authentication and create a public share link
import gradio as gr

def secret_fn(text):
    return f"Secret processed: {text}"

demo = gr.Interface(fn=secret_fn, inputs="text", outputs="text")

# Launch with auth and public link
demo.launch(
    auth=("admin", "password123"),  # Simple auth
    share=True,                      # Creates a public URL (72h)
    server_port=7860,
)
```

## Deploy to Hugging Face Spaces

```bash
# Create a Space on Hugging Face
pip install huggingface_hub
huggingface-cli repo create my-demo --type space --space-sdk gradio

# Clone and push
git clone https://huggingface.co/spaces/username/my-demo
cd my-demo
# Add app.py and requirements.txt, then push
git add . && git commit -m "Initial demo" && git push
```

```txt
# requirements.txt — Dependencies for Hugging Face Spaces deployment
gradio==4.44.0
transformers
torch
```

## API Access

```python
# api_client.py — Use any Gradio app as an API
from gradio_client import Client

client = Client("username/my-demo")  # Or local URL
result = client.predict(
    "Hello world",     # Input text
    api_name="/predict",
)
print(result)
```

## Key Concepts

- **`gr.Interface`**: Simple function-to-UI mapping — one function, inputs, outputs
- **`gr.Blocks`**: Flexible layout system for complex multi-step applications
- **`gr.ChatInterface`**: Purpose-built chatbot UI with history management
- **Sharing**: `share=True` creates a temporary public URL; Spaces for permanent hosting
- **Components**: 30+ built-in components — Image, Audio, Video, File, DataFrame, Plot, etc.
- **API**: Every Gradio app automatically gets a REST API at `/api/`
- **Queuing**: Built-in request queuing for handling concurrent users
