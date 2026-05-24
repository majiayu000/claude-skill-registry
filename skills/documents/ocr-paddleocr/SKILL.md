---
name: OCR with PaddleOCR
description: Comprehensive guide to PaddleOCR implementation for multi-language text recognition, table extraction, and document layout analysis
---

# OCR with PaddleOCR

## Overview

PaddleOCR is a powerful, open-source OCR toolkit that supports multi-language text recognition, table recognition, and document layout analysis. This skill covers implementation patterns for various document processing scenarios.

## Prerequisites

- **Python 3.8+**: Required for PaddlePaddle and PaddleOCR
- **PaddlePaddle**: Deep learning framework (CPU or GPU version)
- **OpenCV**: For image preprocessing and manipulation
- **NumPy**: For array operations
- **Image Preprocessing**: Understanding of image enhancement techniques
- **Deep Learning Basics**: Knowledge of neural networks and model inference

## Key Concepts

- **Detection Model**: Locates text regions in images using DBNet
- **Recognition Model**: Identifies text content using CRNN
- **Direction Classifier**: Determines text orientation (0°, 90°, 180°, 270°)
- **Multi-language Support**: Supports 80+ languages with specific models
- **Table Recognition**: Specialized models for extracting structured table data
- **Document Layout Analysis**: Identifies document structure (headers, paragraphs, tables, images)
- **GPU Acceleration**: CUDA support for faster inference
- **Model Quantization**: INT8 quantization for deployment on edge devices

## Implementation Guide

### Installation

```bash
# CPU version
pip install paddlepaddle paddleocr

# GPU version (CUDA 11.2)
pip install paddlepaddle-gpu paddleocr

# GPU version (CUDA 11.8)
pip install paddlepaddle-gpu==2.5.2.post118 -f https://www.paddlepaddle.org.cn/whl/linux/mkl/avx/stable.html
```

### Basic Text Recognition

```python
from paddleocr import PaddleOCR
import cv2

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Read image
image_path = 'document.png'
image = cv2.imread(image_path)

# Perform OCR
result = ocr.ocr(image, cls=True)

# Extract text
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        print(line[1][0])  # Text content
```

### Multi-language OCR

```python
from paddleocr import PaddleOCR

# Supported languages: 'ch', 'en', 'korean', 'japan', 'chinese_cht', 'ta', 'te', 'ka', 'ca', 'hi'

# English
ocr_en = PaddleOCR(use_angle_cls=True, lang='en')

# Chinese
ocr_ch = PaddleOCR(use_angle_cls=True, lang='ch')

# Thai
ocr_th = PaddleOCR(use_angle_cls=True, lang='th')

# Korean
ocr_kr = PaddleOCR(use_angle_cls=True, lang='korean')

# Custom language model
ocr_custom = PaddleOCR(
    use_angle_cls=True,
    lang='en',
    det_model_dir='./custom_det/',
    rec_model_dir='./custom_rec/',
    cls_model_dir='./custom_cls/'
)
```

### Table Recognition

```python
from paddleocr import PaddleOCR
import cv2

# Initialize with table recognition
ocr = PaddleOCR(
    use_angle_cls=True,
    lang='en',
    table=True,  # Enable table recognition
    show_log=True
)

# Read image with table
image = cv2.imread('table.png')

# Perform table OCR
result = ocr.ocr(image, cls=True)

# Extract table data
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        bbox, (text, confidence) = line
        print(f"Text: {text}, Confidence: {confidence:.2f}")
```

### Document Layout Analysis

```python
from paddleocr import PPStructure

# Initialize structure analysis
table_engine = PPStructure(show_log=True)

# Analyze document layout
image_path = 'document.png'
result = table_engine(image_path)

# Process layout results
for region in result:
    print(f"Type: {region['type']}")
    print(f"Confidence: {region['score']:.2f}")
    
    if region['type'] == 'table':
        # Extract table HTML
        html = region['res']['html']
        print(f"Table HTML: {html}")
    elif region['type'] == 'text':
        # Extract text
        for text_line in region['res']:
            print(f"Text: {text_line['text']}")
```

### Batch Processing

```python
from paddleocr import PaddleOCR
import os
import glob

# Initialize OCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Process multiple images
image_dir = 'documents/'
image_files = glob.glob(os.path.join(image_dir, '*.png'))

results = []
for image_file in image_files:
    image = cv2.imread(image_file)
    result = ocr.ocr(image, cls=True)
    results.append({
        'file': image_file,
        'result': result
    })

# Save results
import json
with open('ocr_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
```

### GPU Acceleration

```python
from paddleocr import PaddleOCR

# Initialize with GPU support
ocr = PaddleOCR(
    use_angle_cls=True,
    lang='en',
    use_gpu=True,  # Enable GPU
    gpu_mem=500,  # GPU memory in MB
    enable_mkldnn=True  # Enable MKLDNN acceleration
)
```

### Custom Model Training

```python
# Prepare training data
# Data format: image_path, text_content

# Train custom detection model
!python tools/train.py -c configs/det/ch_PP-OCRv4/ch_PP-OCRv4_det.yml -o Global.pretrained_model=./your_model/best_accuracy

# Train custom recognition model
!python tools/train.py -c configs/rec/ch_PP-OCRv4/ch_PP-OCRv4_rec.yml -o Global.pretrained_model=./your_model/best_accuracy

# Export model for inference
!python tools/export_model.py -c configs/det/ch_PP-OCRv4/ch_PP-OCRv4_det.yml -o Global.pretrained_model=./your_model/best_accuracy Global.save_inference_dir=./inference/det
```

### Result Processing

```python
from paddleocr import PaddleOCR
import cv2

ocr = PaddleOCR(use_angle_cls=True, lang='en')
image = cv2.imread('document.png')
result = ocr.ocr(image, cls=True)

# Extract structured results
def extract_text_results(result):
    """Extract and structure OCR results"""
    extracted = []
    
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            bbox, (text, confidence) = line
            
            # Calculate bounding box
            x1 = min([point[0] for point in bbox])
            y1 = min([point[1] for point in bbox])
            x2 = max([point[0] for point in bbox])
            y2 = max([point[1] for point in bbox])
            
            extracted.append({
                'text': text,
                'confidence': confidence,
                'bbox': {
                    'x1': x1,
                    'y1': y1,
                    'x2': x2,
                    'y2': y2
                },
                'points': bbox
            })
    
    return extracted

# Get structured results
structured_results = extract_text_results(result)

# Sort by Y position (top to bottom)
sorted_results = sorted(structured_results, key=lambda x: x['bbox']['y1'])

# Print results
for item in sorted_results:
    print(f"{item['text']} (confidence: {item['confidence']:.2f})")
```

### Visualization

```python
import cv2
import numpy as np
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='en')
image = cv2.imread('document.png')
result = ocr.ocr(image, cls=True)

# Draw bounding boxes
def draw_ocr_results(image, result):
    """Draw OCR results on image"""
    image_copy = image.copy()
    
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            bbox, (text, confidence) = line
            
            # Convert to numpy array
            points = np.array(bbox, dtype=np.int32)
            
            # Draw bounding box
            color = (0, 255, 0) if confidence > 0.9 else (0, 165, 255)
            cv2.polylines(image_copy, [points], True, color, 2)
            
            # Draw text
            x, y = bbox[0]
            cv2.putText(
                image_copy,
                f"{text} ({confidence:.2f})",
                (int(x), int(y - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                1
            )
    
    return image_copy

# Visualize
result_image = draw_ocr_results(image, result)
cv2.imwrite('ocr_result.png', result_image)
```

## Best Practices

### Performance Optimization

```python
# Use appropriate model size
# PP-OCRv4: Best accuracy, slower
# PP-OCRv4-mobile: Good accuracy, faster
# PP-OCRv4-server: Best accuracy for server deployment

ocr = PaddleOCR(
    use_angle_cls=True,
    lang='en',
    det_algorithm='DB',  # Detection algorithm
    rec_algorithm='CRNN',  # Recognition algorithm
    use_tensorrt=True,  # Enable TensorRT for faster inference
    precision='fp16'  # Use FP16 for faster inference
)
```

### Image Preprocessing

```python
import cv2
import numpy as np
from paddleocr import PaddleOCR

def preprocess_image(image_path):
    """Preprocess image for better OCR results"""
    image = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply denoising
    denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    
    # Apply adaptive thresholding
    binary = cv2.adaptiveThreshold(
        denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    
    return binary

# Use preprocessed image
ocr = PaddleOCR(use_angle_cls=True, lang='en')
processed_image = preprocess_image('document.png')
result = ocr.ocr(processed_image, cls=True)
```

### Error Handling

```python
from paddleocr import PaddleOCR
import cv2

def safe_ocr(image_path, ocr):
    """Safe OCR with error handling"""
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Failed to load image: {image_path}")
        
        result = ocr.ocr(image, cls=True)
        return result
    
    except Exception as e:
        print(f"OCR error: {e}")
        return None

# Initialize OCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Process with error handling
result = safe_ocr('document.png', ocr)
if result:
    # Process results
    pass
```

### Confidence Thresholding

```python
def filter_by_confidence(result, threshold=0.8):
    """Filter OCR results by confidence threshold"""
    filtered = []
    
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            bbox, (text, confidence) = line
            
            if confidence >= threshold:
                filtered.append({
                    'text': text,
                    'confidence': confidence,
                    'bbox': bbox
                })
    
    return filtered

# Filter low-confidence results
high_confidence_results = filter_by_confidence(result, threshold=0.8)
```

## Related Skills

- [Image Preprocessing](../07-document-processing/image-preprocessing/SKILL.md) - Image enhancement for better OCR accuracy
- [Document Parsing](../07-document-processing/document-parsing/SKILL.md) - Structured data extraction from documents
- [OCR with Tesseract](../07-document-processing/ocr-tesseract/SKILL.md) - Alternative OCR engine
- [PDF Processing](../07-document-processing/pdf-processing/SKILL.md) - PDF-specific processing techniques
- [Document Ingestion Pipeline](../07-document-processing/document-ingestion-pipeline/SKILL.md) - Document loading workflows

## Additional Resources

- [PaddleOCR GitHub](https://github.com/PaddlePaddle/PaddleOCR)
- [PaddleOCR Documentation](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.7/README_en.md)
- [PaddlePaddle Documentation](https://www.paddlepaddle.org.cn/documentation/docs/en/index.html)
- [Model Zoo](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.7/doc/doc_en/models_list_en.md)
