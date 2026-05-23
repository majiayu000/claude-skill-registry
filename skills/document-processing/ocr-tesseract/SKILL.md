---
name: OCR with Tesseract
description: Comprehensive guide to Optical Character Recognition (OCR) using Tesseract OCR engine with Python
---

# OCR with Tesseract

## Overview

Comprehensive guide to Optical Character Recognition (OCR) using Tesseract OCR engine with Python.

## Prerequisites

- **Python 3.7+**: Required for pytesseract and related libraries
- **Tesseract OCR Engine**: Must be installed on the system (separate from Python package)
- **OpenCV**: For image preprocessing and manipulation
- **PIL/Pillow**: For image loading and conversion
- **NumPy**: For array operations
- **Image Preprocessing**: Understanding of image enhancement techniques
- **Regular Expressions**: For text extraction and pattern matching

## Key Concepts

- **Tesseract Engine**: Open-source OCR engine developed by Google
- **Page Segmentation Modes (PSM)**: Different modes for handling various document layouts
- **OCR Engine Modes (OEM)**: Choice between legacy and LSTM neural network engines
- **Language Support**: Multi-language OCR with language-specific trained data
- **Image Preprocessing**: Grayscale conversion, denoising, binarization, deskewing
- **Confidence Scores**: Reliability metrics for OCR output
- **Region of Interest (ROI)**: Focused OCR on specific image regions
- **Post-processing**: Text cleaning, spell correction, and validation

## Table of Contents

1. [Tesseract Installation](#tesseract-installation)
2. [Basic Usage](#basic-usage)
3. [Language Support](#language-support)
4. [Image Preprocessing](#image-preprocessing)
5. [OCR Configuration](#ocr-configuration)
6. [OCR Optimization](#ocr-optimization)
7. [Post-processing](#post-processing)
8. [Handling Different Document Types](#handling-different-document-types)
9. [Batch Processing](#batch-processing)
10. [Error Handling](#error-handling)
11. [Production Tips](#production-tips)

---

## Tesseract Installation

### Windows Installation

```powershell
# Using Chocolatey
choco install tesseract

# Or download installer from:
# https://github.com/UB-Mannheim/tesseract/wiki
```

### macOS Installation

```bash
# Using Homebrew
brew install tesseract

# Install additional language data
brew install tesseract-lang
```

### Linux Installation

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-all  # All languages

# CentOS/RHEL
sudo yum install tesseract
```

### Python Installation

```bash
# Install pytesseract wrapper
pip install pytesseract

# Install image processing libraries
pip install Pillow opencv-python-headless
```

---

## Basic Usage

### Python (pytesseract)

```python
import pytesseract
from PIL import Image

# Set Tesseract path (Windows only)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Basic OCR
def extract_text(image_path: str) -> str:
    """Extract text from an image"""
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

# Example
text = extract_text('document.png')
print(text)
```

### Command Line

```bash
# Basic OCR
tesseract image.png output

# OCR with language
tesseract image.png output -l eng

# OCR with multiple languages
tesseract image.png output -l eng+tha

# OCR with specific output format
tesseract image.png output -l eng hocr  # HTML output
tesseract image.png output -l eng pdf   # PDF output
tesseract image.png output -l eng tsv   # TSV output
```

### Get Detailed Information

```python
import pytesseract
from PIL import Image

def get_ocr_details(image_path: str):
    """Get detailed OCR information"""
    image = Image.open(image_path)
    
    # Get bounding boxes
    boxes = pytesseract.image_to_boxes(image)
    
    # Get data with confidence scores
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    
    # Get bounding boxes for words
    words = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    
    return {
        'text': pytesseract.image_to_string(image),
        'boxes': boxes,
        'data': data,
        'confidence': data['conf']
    }

# Print confidence scores
details = get_ocr_details('document.png')
for i, conf in enumerate(details['confidence']):
    if conf > 0:
        print(f"Word: {details['text'][i]}, Confidence: {conf}%")
```

---

## Language Support

### Available Languages

```python
import pytesseract

# Get list of available languages
languages = pytesseract.get_languages(config='')
print(languages)
# Output: ['eng', 'tha', 'chi_sim', 'chi_tra', 'jpn', 'kor', ...]
```

### Multi-Language OCR

```python
import pytesseract
from PIL import Image

def ocr_multi_language(image_path: str, languages: list) -> str:
    """OCR with multiple languages"""
    lang_string = '+'.join(languages)
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang=lang_string)
    return text

# Example: English + Thai
text = ocr_multi_language('document.png', ['eng', 'tha'])
print(text)
```

### Language-Specific Configuration

```python
# Thai language with specific settings
config = r'--oem 3 --psm 6 -l tha+eng'
text = pytesseract.image_to_string(image, config=config)

# Chinese (Simplified)
config = r'--oem 3 --psm 6 -l chi_sim'
text = pytesseract.image_to_string(image, config=config)

# Japanese
config = r'--oem 3 --psm 6 -l jpn'
text = pytesseract.image_to_string(image, config=config)
```

---

## Image Preprocessing

### Grayscale Conversion

```python
import cv2
import numpy as np
from PIL import Image

def to_grayscale(image_path: str) -> np.ndarray:
    """Convert image to grayscale"""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray

# Using PIL
def to_grayscale_pil(image_path: str) -> Image.Image:
    """Convert to grayscale using PIL"""
    image = Image.open(image_path)
    return image.convert('L')
```

### Noise Removal

```python
import cv2
import numpy as np

def remove_noise(image: np.ndarray) -> np.ndarray:
    """Remove noise from image"""
    # Apply median blur
    denoised = cv2.medianBlur(image, 3)
    return denoised

def bilateral_filter(image: np.ndarray) -> np.ndarray:
    """Apply bilateral filter for edge-preserving denoising"""
    denoised = cv2.bilateralFilter(image, 9, 75, 75)
    return denoised

def gaussian_blur(image: np.ndarray) -> np.ndarray:
    """Apply Gaussian blur"""
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    return blurred
```

### Deskewing

```python
import cv2
import numpy as np

def deskew(image: np.ndarray) -> np.ndarray:
    """Correct skewed images"""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    
    # Threshold
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    
    # Get coordinates
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    
    # Adjust angle
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    
    # Rotate image
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    
    return rotated
```

### Binarization (Thresholding)

```python
import cv2
import numpy as np

def binarize_otsu(image: np.ndarray) -> np.ndarray:
    """Otsu's binarization"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return binary

def binarize_adaptive(image: np.ndarray) -> np.ndarray:
    """Adaptive thresholding"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    return binary

def binarize_manual(image: np.ndarray, threshold: int = 127) -> np.ndarray:
    """Manual thresholding"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    return binary
```

### Complete Preprocessing Pipeline

```python
import cv2
import numpy as np

def preprocess_image(image_path: str) -> np.ndarray:
    """Complete preprocessing pipeline for OCR"""
    # Load image
    image = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Denoise
    denoised = cv2.medianBlur(gray, 3)
    
    # Threshold
    binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    
    # Dilate to connect text
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(binary, kernel, iterations=1)
    
    return dilated

# Usage
processed = preprocess_image('document.png')
cv2.imwrite('processed.png', processed)
```

---

## OCR Configuration

### PSM (Page Segmentation Mode)

```python
import pytesseract

# PSM modes
PSM_MODES = {
    0: 'Orientation and script detection (OSD) only',
    1: 'Automatic page segmentation with OSD',
    2: 'Automatic page segmentation, but no OSD, or OCR',
    3: 'Fully automatic page segmentation, but no OSD (Default)',
    4: 'Assume a single column of text of variable sizes',
    5: 'Assume a single uniform block of vertically aligned text',
    6: 'Assume a single uniform block of text',
    7: 'Treat the image as a single text line',
    8: 'Treat the image as a single word',
    9: 'Treat the image as a single word in a circle',
    10: 'Treat the image as a single character',
    11: 'Sparse text. Find as much text as possible in no particular order',
    12: 'Sparse text with OSD',
    13: 'Raw line. Treat the image as a single text line'
}

def ocr_with_psm(image_path: str, psm: int, lang: str = 'eng') -> str:
    """OCR with specific PSM mode"""
    config = f'--psm {psm}'
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang=lang, config=config)
    return text

# Examples
# Single line text
text_line = ocr_with_psm('line.png', psm=7)

# Single word
text_word = ocr_with_psm('word.png', psm=8)

# Single character
text_char = ocr_with_psm('char.png', psm=10)

# Sparse text
text_sparse = ocr_with_psm('sparse.png', psm=11)
```

### OEM (OCR Engine Mode)

```python
# OEM modes
OEM_MODES = {
    0: 'Legacy engine only',
    1: 'Neural nets LSTM engine only',
    2: 'Legacy + LSTM engines',
    3: 'Default, based on what is available (Default)'
}

def ocr_with_oem(image_path: str, oem: int, psm: int = 3) -> str:
    """OCR with specific OEM mode"""
    config = f'--oem {oem} --psm {psm}'
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, config=config)
    return text

# Use LSTM engine only (recommended for better accuracy)
text = ocr_with_oem('document.png', oem=1)
```

### Custom Configuration

```python
def ocr_custom_config(image_path: str) -> str:
    """OCR with custom configuration"""
    config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, config=config)
    return text

# Whitelist specific characters (e.g., numbers only)
config_numbers = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'

# Blacklist specific characters
config_blacklist = r'--oem 3 --psm 6 -c tessedit_char_blacklist=|'

# DPI setting (for high-DPI images)
config_dpi = r'--oem 3 --psm 6 --dpi 300'
```

---

## OCR Optimization

### DPI Optimization

```python
import cv2

def optimize_dpi(image_path: str, target_dpi: int = 300) -> np.ndarray:
    """Optimize image DPI for better OCR"""
    image = cv2.imread(image_path)
    
    # Calculate scale factor
    current_dpi = 96  # Default screen DPI
    scale = target_dpi / current_dpi
    
    # Resize image
    height, width = image.shape[:2]
    new_height = int(height * scale)
    new_width = int(width * scale)
    
    resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
    
    return resized
```

### Region of Interest (ROI)

```python
def ocr_roi(image_path: str, x: int, y: int, w: int, h: int) -> str:
    """OCR on specific region of interest"""
    image = cv2.imread(image_path)
    roi = image[y:y+h, x:x+w]
    
    # Convert to PIL for pytesseract
    roi_pil = Image.fromarray(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))
    text = pytesseract.image_to_string(roi_pil)
    
    return text

# Usage: Extract text from a specific area
text = ocr_roi('document.png', x=100, y=50, w=400, h=100)
```

### Multiple ROI Extraction

```python
def extract_multiple_regions(image_path: str, regions: list) -> dict:
    """Extract text from multiple regions"""
    image = cv2.imread(image_path)
    results = {}
    
    for i, region in enumerate(regions):
        x, y, w, h = region
        roi = image[y:y+h, x:x+w]
        roi_pil = Image.fromarray(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))
        text = pytesseract.image_to_string(roi_pil)
        results[f'region_{i}'] = text
    
    return results

# Example: Extract from multiple form fields
regions = [
    (100, 50, 200, 30),   # Name field
    (100, 100, 200, 30),  # Address field
    (100, 150, 100, 30),  # Zip code field
]
results = extract_multiple_regions('form.png', regions)
```

---

## Post-processing

### Text Cleaning

```python
import re

def clean_ocr_text(text: str) -> str:
    """Clean OCR output"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Fix common OCR errors
    text = text.replace('|', 'I')
    text = text.replace('0', 'O')  # Context-dependent
    
    # Remove non-printable characters
    text = ''.join(char for char in text if char.isprintable() or char == '\n')
    
    return text.strip()

# Usage
raw_text = pytesseract.image_to_string(image)
cleaned = clean_ocr_text(raw_text)
```

### Confidence Filtering

```python
def extract_with_confidence(image_path: str, min_confidence: float = 60.0) -> list:
    """Extract text with confidence filtering"""
    image = Image.open(image_path)
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    
    results = []
    for i, conf in enumerate(data['conf']):
        if conf > min_confidence:
            results.append({
                'text': data['text'][i],
                'confidence': conf,
                'bbox': (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            })
    
    return results

# Usage
high_confidence_words = extract_with_confidence('document.png', min_confidence=80)
```

### Spell Correction

```python
from textblob import TextBlob

def correct_spelling(text: str) -> str:
    """Correct spelling errors in OCR output"""
    blob = TextBlob(text)
    corrected = str(blob.correct())
    return corrected

# Usage
corrected = correct_spelling(cleaned_text)
```

---

## Handling Different Document Types

### Receipts

```python
def extract_receipt_info(image_path: str) -> dict:
    """Extract information from receipts"""
    image = preprocess_image(image_path)
    
    # Extract text
    text = pytesseract.image_to_string(image)
    
    # Extract common receipt fields using regex
    receipt_info = {
        'date': extract_date(text),
        'total': extract_total(text),
        'items': extract_items(text)
    }
    
    return receipt_info

def extract_date(text: str) -> str:
    """Extract date from receipt text"""
    date_pattern = r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}'
    match = re.search(date_pattern, text)
    return match.group() if match else None

def extract_total(text: str) -> float:
    """Extract total amount from receipt"""
    # Look for patterns like "Total: $12.34"
    total_pattern = r'(?:total|amount|sum)[:\s]*[$]?\s*([\d,]+\.\d{2})'
    match = re.search(total_pattern, text, re.IGNORECASE)
    return float(match.group(1).replace(',', '')) if match else None
```

### Invoices

```python
def extract_invoice_info(image_path: str) -> dict:
    """Extract information from invoices"""
    image = preprocess_image(image_path)
    text = pytesseract.image_to_string(image)
    
    invoice_info = {
        'invoice_number': extract_invoice_number(text),
        'date': extract_date(text),
        'due_date': extract_due_date(text),
        'vendor': extract_vendor(text),
        'total': extract_total(text)
    }
    
    return invoice_info

def extract_invoice_number(text: str) -> str:
    """Extract invoice number"""
    pattern = r'(?:invoice|inv)[#:\s]*([A-Z0-9-]+)'
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1) if match else None
```

### Forms

```python
def extract_form_fields(image_path: str, field_definitions: dict) -> dict:
    """Extract form fields using defined regions"""
    image = cv2.imread(image_path)
    results = {}
    
    for field_name, region in field_definitions.items():
        x, y, w, h = region
        roi = image[y:y+h, x:x+w]
        roi_pil = Image.fromarray(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))
        text = pytesseract.image_to_string(roi_pil, config='--psm 7')
        results[field_name] = text.strip()
    
    return results

# Example field definitions
form_fields = {
    'first_name': (100, 50, 200, 30),
    'last_name': (100, 100, 200, 30),
    'email': (100, 150, 300, 30),
    'phone': (100, 200, 150, 30)
}

results = extract_form_fields('form.png', form_fields)
```

### ID Cards

```python
def extract_id_card(image_path: str) -> dict:
    """Extract information from ID cards"""
    image = preprocess_image(image_path)
    text = pytesseract.image_to_string(image, lang='eng+tha')
    
    # Extract common ID card fields
    id_info = {
        'name': extract_name(text),
        'id_number': extract_id_number(text),
        'dob': extract_dob(text)
    }
    
    return id_info

def extract_id_number(text: str) -> str:
    """Extract ID number"""
    # Thai ID pattern: 13 digits
    pattern = r'\b\d{13}\b'
    match = re.search(pattern, text)
    return match.group() if match else None
```

---

## Batch Processing

### Process Multiple Files

```python
import os
from pathlib import Path

def batch_ocr(input_dir: str, output_dir: str, lang: str = 'eng') -> dict:
    """Process multiple images in a directory"""
    results = {}
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Process each image
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f'{Path(filename).stem}.txt')
            
            # Extract text
            text = pytesseract.image_to_string(
                Image.open(input_path),
                lang=lang
            )
            
            # Save to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            
            results[filename] = output_path
    
    return results

# Usage
results = batch_ocr('input_images/', 'output_texts/', lang='eng+tha')
```

### Parallel Processing

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

def process_single_image(image_path: str, output_dir: str) -> tuple:
    """Process a single image"""
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        output_path = os.path.join(output_dir, f'{Path(image_path).stem}.txt')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        return (image_path, output_path, None)
    except Exception as e:
        return (image_path, None, str(e))

def batch_ocr_parallel(input_dir: str, output_dir: str, max_workers: int = 4) -> dict:
    """Batch process images in parallel"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    image_files = [
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp'))
    ]
    
    results = {}
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(process_single_image, img, output_dir): img
            for img in image_files
        }
        
        for future in as_completed(futures):
            input_path, output_path, error = future.result()
            if error:
                results[input_path] = {'error': error}
            else:
                results[input_path] = {'output': output_path}
    
    return results
```

### Progress Tracking

```python
from tqdm import tqdm

def batch_ocr_with_progress(input_dir: str, output_dir: str) -> dict:
    """Batch process with progress bar"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    image_files = [
        f for f in os.listdir(input_dir)
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp'))
    ]
    
    results = {}
    
    for filename in tqdm(image_files, desc="Processing images"):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, f'{Path(filename).stem}.txt')
        
        try:
            text = pytesseract.image_to_string(Image.open(input_path))
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            results[filename] = output_path
        except Exception as e:
            results[filename] = {'error': str(e)}
    
    return results
```

---

## Error Handling

### Robust OCR Function

```python
def robust_ocr(image_path: str, max_retries: int = 3) -> dict:
    """Robust OCR with error handling and retries"""
    result = {
        'success': False,
        'text': None,
        'error': None,
        'attempts': 0
    }
    
    for attempt in range(max_retries):
        result['attempts'] = attempt + 1
        
        try:
            # Preprocess image
            processed = preprocess_image(image_path)
            
            # Extract text
            text = pytesseract.image_to_string(
                Image.fromarray(processed),
                config='--oem 3 --psm 6'
            )
            
            result['success'] = True
            result['text'] = text
            break
            
        except pytesseract.TesseractError as e:
            result['error'] = f"Tesseract error: {str(e)}"
        except Exception as e:
            result['error'] = f"Unexpected error: {str(e)}"
    
    return result

# Usage
result = robust_ocr('document.png')
if result['success']:
    print(result['text'])
else:
    print(f"Failed after {result['attempts']} attempts: {result['error']}")
```

### Validation

```python
def validate_ocr_output(text: str, min_length: int = 10) -> bool:
    """Validate OCR output"""
    if not text or len(text.strip()) < min_length:
        return False
    
    # Check if output is mostly whitespace
    if len(text.strip()) / len(text) < 0.1:
        return False
    
    # Check for common error patterns
    error_patterns = [
        r'^[^\w\s]*$',  # Only special characters
        r'^(.)\1+$',     # Repeated characters
    ]
    
    for pattern in error_patterns:
        if re.match(pattern, text.strip()):
            return False
    
    return True
```

---

## Production Tips

### Performance Optimization

```python
# 1. Use appropriate image size
def resize_for_ocr(image_path: str, max_width: int = 2000) -> np.ndarray:
    """Resize image for optimal OCR performance"""
    image = cv2.imread(image_path)
    height, width = image.shape[:2]
    
    if width > max_width:
        scale = max_width / width
        new_height = int(height * scale)
        image = cv2.resize(image, (max_width, new_height), interpolation=cv2.INTER_AREA)
    
    return image

# 2. Cache preprocessed images
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def get_cached_preprocessing(image_path: str) -> np.ndarray:
    """Cache preprocessed images"""
    return preprocess_image(image_path)

# 3. Use threading for concurrent processing
from concurrent.futures import ThreadPoolExecutor

def process_images_concurrent(image_paths: list, max_workers: int = 4) -> list:
    """Process multiple images concurrently"""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(robust_ocr, image_paths))
    return results
```

### Memory Management

```python
import gc

def batch_ocr_memory_efficient(input_dir: str, output_dir: str, batch_size: int = 10):
    """Batch process with memory management"""
    image_files = [
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]
    
    # Process in batches
    for i in range(0, len(image_files), batch_size):
        batch = image_files[i:i + batch_size]
        
        for img_path in batch:
            try:
                text = pytesseract.image_to_string(Image.open(img_path))
                # Save immediately
                output_path = os.path.join(output_dir, f'{Path(img_path).stem}.txt')
                with open(output_path, 'w') as f:
                    f.write(text)
            except Exception as e:
                print(f"Error processing {img_path}: {e}")
        
        # Clear memory
        gc.collect()
```

### Quality Assurance

```python
def quality_assurance(image_path: str, expected_patterns: list = None) -> dict:
    """Perform quality assurance on OCR output"""
    result = robust_ocr(image_path)
    
    if not result['success']:
        return result
    
    qa_result = {
        'success': True,
        'text': result['text'],
        'confidence': calculate_confidence(result['text']),
        'pattern_match': None
    }
    
    # Check for expected patterns
    if expected_patterns:
        for pattern in expected_patterns:
            if re.search(pattern, result['text']):
                qa_result['pattern_match'] = pattern
                break
    
    return qa_result

def calculate_confidence(text: str) -> float:
    """Calculate confidence score based on text characteristics"""
    score = 0.0
    
    # Length score
    score += min(len(text) / 100, 1.0) * 0.3
    
    # Alphanumeric ratio
    alnum_ratio = sum(c.isalnum() for c in text) / len(text) if text else 0
    score += alnum_ratio * 0.4
    
    # Dictionary word ratio (simplified)
    words = text.split()
    valid_words = sum(word.isalpha() for word in words)
    word_ratio = valid_words / len(words) if words else 0
    score += word_ratio * 0.3
    
    return min(score, 1.0)
```

---

## Related Skills

- [Image Preprocessing](../07-document-processing/image-preprocessing/SKILL.md) - Image enhancement for better OCR accuracy
- [Document Parsing](../07-document-processing/document-parsing/SKILL.md) - Structured data extraction from documents
- [OCR with PaddleOCR](../07-document-processing/ocr-paddleocr/SKILL.md) - Alternative OCR engine with deep learning
- [PDF Processing](../07-document-processing/pdf-processing/SKILL.md) - PDF-specific processing techniques
- [Document Ingestion Pipeline](../07-document-processing/document-ingestion-pipeline/SKILL.md) - Document loading workflows
- [RAG Implementation](../06-ai-ml-production/rag-implementation/SKILL.md) - Retrieval-Augmented Generation patterns

## Additional Resources

- [Tesseract OCR Documentation](https://tesseract-ocr.github.io/)
- [pytesseract Documentation](https://pypi.org/project/pytesseract/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Tesseract Training](https://github.com/tesseract-ocr/tesseract/wiki/TrainingTesseract)
