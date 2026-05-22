---
name: Computer Vision Helper
slug: computer-vision-helper
description: Assist with image analysis, object detection, and visual AI tasks
category: ai-ml
complexity: intermediate
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "image analysis"
  - "computer vision"
  - "object detection"
  - "image classification"
  - "visual AI"
tags:
  - computer-vision
  - image-analysis
  - object-detection
  - visual-AI
  - deep-learning
---

# Computer Vision Helper

The Computer Vision Helper skill guides you through implementing image analysis and visual AI tasks. From basic image classification to complex object detection and segmentation, this skill helps you leverage modern computer vision techniques effectively.

Computer vision has been transformed by deep learning and now by vision-language models. This skill covers both traditional approaches (CNNs, pre-trained models) and cutting-edge techniques (CLIP, GPT-4V, Segment Anything). It helps you choose the right approach based on your accuracy requirements, available data, and deployment constraints.

Whether you are building product recognition, document analysis, medical imaging, or any visual AI application, this skill ensures you understand the landscape and implement solutions that work.

## Core Workflows

### Workflow 1: Select Computer Vision Approach
1. **Define** the task:
   - Classification: What category is this image?
   - Detection: Where are objects in this image?
   - Segmentation: Pixel-level object boundaries
   - OCR: Extract text from images
   - Similarity: Find similar images
   - Generation: Create or modify images
2. **Assess** available resources:
   - Training data quantity and quality
   - Compute budget (training and inference)
   - Latency requirements
   - Accuracy needs
3. **Choose** approach:
   | Task | No Training Data | Small Dataset | Large Dataset |
   |------|-----------------|---------------|---------------|
   | Classification | CLIP, GPT-4V | Transfer learning | Fine-tune/train |
   | Detection | GPT-4V, Grounding DINO | Fine-tune YOLO | Train custom |
   | Segmentation | SAM | Fine-tune SAM | Train custom |
   | OCR | Cloud APIs, Tesseract | Fine-tune | Train custom |
4. **Plan** implementation
5. **Document** approach rationale

### Workflow 2: Implement Image Classification
1. **Prepare** data:
   ```python
   # Data loading with augmentation
   transform = transforms.Compose([
       transforms.Resize(256),
       transforms.CenterCrop(224),
       transforms.RandomHorizontalFlip(),
       transforms.ColorJitter(brightness=0.2, contrast=0.2),
       transforms.ToTensor(),
       transforms.Normalize(mean=[0.485, 0.456, 0.406],
                          std=[0.229, 0.224, 0.225])
   ])

   dataset = ImageFolder(root='data/', transform=transform)
   dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
   ```
2. **Set up** model:
   ```python
   # Transfer learning from pretrained model
   model = models.resnet50(pretrained=True)

   # Freeze early layers
   for param in model.parameters():
       param.requires_grad = False

   # Replace classifier head
   model.fc = nn.Linear(model.fc.in_features, num_classes)
   ```
3. **Train** with validation
4. **Evaluate** on test set
5. **Optimize** for deployment

### Workflow 3: Deploy Vision Model
1. **Optimize** model:
   - Quantization (INT8)
   - Pruning
   - ONNX export
   - TensorRT optimization
2. **Set up** inference pipeline:
   ```python
   class VisionPipeline:
       def __init__(self, model_path):
           self.model = load_optimized_model(model_path)
           self.preprocessor = ImagePreprocessor()

       def predict(self, image):
           # Preprocess
           tensor = self.preprocessor.process(image)

           # Inference
           with torch.no_grad():
               output = self.model(tensor)

           # Postprocess
           return self.postprocess(output)

       def predict_batch(self, images):
           tensors = [self.preprocessor.process(img) for img in images]
           batch = torch.stack(tensors)

           with torch.no_grad():
               outputs = self.model(batch)

           return [self.postprocess(out) for out in outputs]
   ```
3. **Deploy** to target environment
4. **Monitor** performance

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Choose approach | "What CV approach for [task]" |
| Classify images | "Build image classifier" |
| Detect objects | "Object detection for [use case]" |
| Extract text | "OCR from images" |
| Zero-shot vision | "Classify images without training data" |
| Optimize model | "Speed up vision model" |

## Best Practices

- **Start with Pre-trained**: Don't train from scratch unless necessary
  - ImageNet pre-trained models for general vision
  - Domain-specific models when available
  - CLIP/GPT-4V for zero-shot capabilities

- **Data Quality Over Quantity**: Clean, balanced data matters
  - Remove mislabeled and duplicate images
  - Balance classes or use weighted training
  - Include edge cases in test set

- **Augment Thoughtfully**: Augmentation should reflect real variation
  - Use augmentations that mirror production conditions
  - Don't augment in ways that destroy task-relevant features
  - Test that augmentation helps, don't assume

- **Validate Correctly**: Image data leaks easily
  - Split by unique images, not by augmented versions
  - Consider subject-level splits (same person in different photos)
  - Test on truly held-out data

- **Optimize for Target Hardware**: Inference matters
  - Know your deployment constraints (edge vs cloud)
  - Profile and optimize bottlenecks
  - Consider batch size for throughput

- **Handle Edge Cases**: Real images are messy
  - Different lighting conditions
  - Rotation, blur, occlusion
  - Unusual aspect ratios
  - Out-of-distribution inputs

## Advanced Techniques

### Vision-Language Models for Zero-Shot
Use CLIP for classification without training:
```python
import clip

model, preprocess = clip.load("ViT-B/32")

def zero_shot_classify(image, labels):
    # Prepare image
    image_tensor = preprocess(image).unsqueeze(0)

    # Prepare text prompts
    text_prompts = [f"a photo of a {label}" for label in labels]
    text_tokens = clip.tokenize(text_prompts)

    # Get embeddings
    with torch.no_grad():
        image_features = model.encode_image(image_tensor)
        text_features = model.encode_text(text_tokens)

    # Compute similarities
    similarities = (image_features @ text_features.T).softmax(dim=-1)

    return {label: sim.item() for label, sim in zip(labels, similarities[0])}
```

### GPT-4V for Visual Analysis
Use multimodal LLMs for complex vision tasks:
```python
def analyze_image(image_path, question):
    import base64
    from openai import OpenAI

    # Encode image
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": question},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/jpeg;base64,{image_data}"
                }}
            ]
        }],
        max_tokens=500
    )

    return response.choices[0].message.content
```

### Object Detection with YOLO
Fast, accurate object detection:
```python
from ultralytics import YOLO

# Load pretrained model
model = YOLO("yolov8n.pt")

# Fine-tune on custom dataset
model.train(
    data="custom_dataset.yaml",
    epochs=100,
    imgsz=640,
    batch=16
)

# Inference
results = model.predict(source="image.jpg", conf=0.5)

for result in results:
    boxes = result.boxes
    for box in boxes:
        xyxy = box.xyxy[0].tolist()  # Bounding box
        conf = box.conf[0].item()     # Confidence
        cls = box.cls[0].item()       # Class ID
        print(f"Detected {cls} at {xyxy} with confidence {conf}")
```

### Segment Anything (SAM)
Universal segmentation:
```python
from segment_anything import sam_model_registry, SamPredictor

# Load SAM
sam = sam_model_registry["vit_h"](checkpoint="sam_vit_h.pth")
predictor = SamPredictor(sam)

# Set image
predictor.set_image(image)

# Segment with point prompt
masks, scores, logits = predictor.predict(
    point_coords=np.array([[500, 375]]),  # Click point
    point_labels=np.array([1]),            # 1 = foreground
    multimask_output=True
)

# Segment with box prompt
masks, scores, logits = predictor.predict(
    box=np.array([x1, y1, x2, y2])
)
```

### Model Optimization Pipeline
Prepare models for production:
```python
def optimize_for_deployment(model, sample_input):
    # Step 1: Export to ONNX
    torch.onnx.export(
        model,
        sample_input,
        "model.onnx",
        opset_version=13,
        dynamic_axes={"input": {0: "batch"}}
    )

    # Step 2: Quantize (INT8)
    from onnxruntime.quantization import quantize_dynamic
    quantize_dynamic(
        "model.onnx",
        "model_quantized.onnx",
        weight_type=QuantType.QInt8
    )

    # Step 3: Benchmark
    import onnxruntime as ort
    session = ort.InferenceSession("model_quantized.onnx")
    benchmark_inference(session, sample_input)

    return "model_quantized.onnx"
```

## Common Pitfalls to Avoid

- Training from scratch when transfer learning would work
- Not augmenting data appropriately for the task
- Data leakage through improper train/test splits
- Ignoring class imbalance in training data
- Overfitting to training data without regularization
- Not testing on diverse, real-world images
- Deploying without latency and throughput testing
- Assuming models work on all image types without testing
