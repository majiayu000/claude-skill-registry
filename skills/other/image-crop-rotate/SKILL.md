---
name: image-crop-rotate
description: Image processing skill for cropping images to 50% from center and rotating them 90 degrees clockwise. This skill should be used when users request image cropping to center, image rotation, or both operations combined on image files.
---

# Image Crop and Rotate

## Overview

This skill provides functionality to crop images to 50% of their original size from the center and rotate them 90 degrees clockwise. It uses a reliable Python script with PIL/Pillow for consistent, high-quality image processing.

## When to Use This Skill

Use this skill when the user requests:
- Cropping an image to 50% from the center
- Rotating an image 90 degrees (clockwise)
- Both cropping and rotating an image
- Image processing tasks that combine center cropping with rotation

## How to Use This Skill

### Overview

The skill provides a single script that performs both operations: cropping to 50% from center and rotating 90 degrees clockwise.

### Process

1. **Identify the input image**: Locate the user's uploaded image file in `/mnt/user-data/uploads/`

2. **Execute the script**: Run the `crop_and_rotate.py` script with input and output paths:
   ```bash
   python scripts/crop_and_rotate.py <input_path> <output_path>
   ```

3. **Provide the result**: Move the processed image to `/mnt/user-data/outputs/` and share it with the user

### Script Details

**`scripts/crop_and_rotate.py`**

This script performs two operations in sequence:
1. Crops the image to 50% of its original size, centered
2. Rotates the cropped image 90 degrees clockwise

**Usage:**
```bash
python scripts/crop_and_rotate.py input.jpg output.jpg
```

**Arguments:**
- First argument: Path to input image
- Second argument: Path to save processed image

**Supported formats:** Any format supported by PIL/Pillow (JPEG, PNG, GIF, BMP, TIFF, etc.)

**Output:** The script prints processing details including original size, cropped size, and final size

### Example Workflow

```bash
# Process an uploaded image
python /mnt/user-data/skills/image-crop-rotate/scripts/crop_and_rotate.py \
    /mnt/user-data/uploads/photo.jpg \
    /mnt/user-data/outputs/photo_processed.jpg
```

The script will:
1. Open the input image
2. Crop it to 50% from the center (e.g., 1000x800 → 500x400)
3. Rotate the cropped image 90° clockwise (e.g., 500x400 → 400x500)
4. Save the result to the output path
