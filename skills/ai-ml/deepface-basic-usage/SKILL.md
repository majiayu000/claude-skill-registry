---
description: Basic usage guide for the DeepFace library (face recognition, verification, analysis).
---

# Skill: DeepFace Basic Usage

This skill provides a quick reference and guide for using the `deepface` library for face recognition tasks.

## Overview

DeepFace is a hybrid face recognition framework for Python that wraps state-of-the-art models (VGG-Face, FaceNet, ArcFace, etc.) and detectors (RetinaFace, MtCNN, YOLO, etc.).

## Installation

```bash
pip install deepface
# Or with pixi
pixi add deepface
```

## Core Functions

Import:
```python
from deepface import DeepFace
```

### 1. Face Verification (1:1)

Determines if two images belong to the same person.

```python
result = DeepFace.verify(
    img1_path = "img1.jpg",
    img2_path = "img2.jpg",
    model_name = "VGG-Face", # Optional: see Model Selection below
    detector_backend = "opencv", # Optional: see Detector Selection below
    distance_metric = "cosine", # Optional: cosine, euclidean, euclidean_l2
    align = True, # Optional: Align faces before verification
)

# result is a dict:
# {
#   "verified": True,
#   "distance": 0.256,
#   "threshold": 0.40,
#   "model": "VGG-Face",
#   "detector_backend": "opencv",
#   "similarity_metric": "cosine",
#   "facial_areas": {"img1": {...}, "img2": {...}},
#   "time": 1.23
# }
```

### 2. Face Recognition / Search (1:N)

Finds identity of an input image in a database (folder of images).

**Directory-based (`find`)**:
```python
dfs = DeepFace.find(
    img_path = "img.jpg",
    db_path = "/path/to/images_folder",
    model_name = "VGG-Face",
    detector_backend = "opencv"
)
# Returns a list of pandas DataFrames (one per face detected in input)
```

**Database-backed (`search`)**:
Supports backends like Postgres (pgvector), Pinecone, Milvus, Weaviate, etc.
```python
# Register
DeepFace.register(img="img1.jpg")
# Search
dfs = DeepFace.search(img="target.jpg")
```

### 3. Facial Attribute Analysis

Predicts age, gender, race, and emotion.

```python
objs = DeepFace.analyze(
    img_path = "img.jpg",
    actions = ['age', 'gender', 'race', 'emotion'],
    detector_backend = "opencv"
)
# Returns a list of dicts (one per face)
```

### 4. Embeddings (Representation)

Get the vector representation of a face.

```python
embedding_objs = DeepFace.represent(
    img_path = "img.jpg",
    model_name = "VGG-Face",
    detector_backend = "opencv"
)
# Returns list of dicts:
# [
#   {
#     "embedding": [0.1, 0.5, ...],
#     "facial_area": {...}
#   }
# ]
```

## Configuration Options

### Available Models
`VGG-Face` (default), `Facenet`, `Facenet512`, `OpenFace`, `DeepFace`, `DeepID`, `ArcFace`, `Dlib`, `SFace`, `GhostFaceNet`.

*Recommendation:*
- **Accuracy**: `ArcFace`, `Facenet512`, `VGG-Face`
- **Legacy/Lower Accuracy**: `DeepFace`, `OpenFace`

### Available Detectors
`opencv` (default, fast), `ssd`, `dlib`, `mtcnn`, `retinaface` (highly accurate), `mediapipe`, `yolov8`, `centerface`.

*Recommendation:*
- **Speed**: `opencv`, `ssd`
- **Accuracy**: `retinaface`, `mtcnn`

### Distance Metrics
`cosine` (default), `euclidean`, `euclidean_l2`.

## Common Issues & Tips

1.  **Dependencies**: DeepFace installs many dependencies (tensorflow/keras or pytorch depending on model). Ensure your environment is set up correctly.
2.  **Weights Download**: First run will download model weights to `~/.deepface/weights`.
3.  **Face Not Found**: If no face is detected, functions may raise `ValueError`. Set `enforce_detection=False` to skip detection (treats whole image as face) or handle the exception.
    ```python
    DeepFace.verify(..., enforce_detection=False)
    ```
4.  **Backend Compatibility**: If using specialized detectors (like `retinaface` or `dlib`), ensure their specific pip packages are installed.

