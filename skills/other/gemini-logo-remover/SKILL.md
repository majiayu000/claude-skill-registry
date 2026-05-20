---
name: gemini-logo-remover
description: Remove Gemini logos, watermarks, or AI-generated image markers using OpenCV inpainting. Use this skill when the user asks to remove Gemini logo, AI watermark, or any logo/watermark from images.
---

# Gemini Logo Remover

Remove Gemini logos and watermarks from AI-generated images using inpainting.

## Setup

```bash
pip install opencv-python numpy pillow --break-system-packages
```

## Usage

### By Coordinates

```python
import cv2
import numpy as np

def remove_region(input_path, output_path, x1, y1, x2, y2, radius=5):
    """Remove rectangular region using inpainting."""
    img = cv2.imread(input_path)
    h, w = img.shape[:2]
    
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)
    
    result = cv2.inpaint(img, mask, radius, cv2.INPAINT_TELEA)
    cv2.imwrite(output_path, result)

# Example: remove region at coordinates
remove_region('/mnt/user-data/uploads/img.png', 
              '/mnt/user-data/outputs/clean.png',
              x1=700, y1=650, x2=800, y2=720)
```

### By Corner

```python
def remove_corner_logo(input_path, output_path, corner='bottom_right', 
                       w_ratio=0.1, h_ratio=0.1, padding=10):
    """Remove logo from corner. corner: top_left, top_right, bottom_left, bottom_right"""
    img = cv2.imread(input_path)
    h, w = img.shape[:2]
    
    lw, lh = int(w * w_ratio), int(h * h_ratio)
    
    coords = {
        'bottom_right': (w - lw - padding, h - lh - padding, w - padding, h - padding),
        'bottom_left': (padding, h - lh - padding, lw + padding, h - padding),
        'top_right': (w - lw - padding, padding, w - padding, lh + padding),
        'top_left': (padding, padding, lw + padding, lh + padding)
    }
    x1, y1, x2, y2 = coords[corner]
    
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)
    
    result = cv2.inpaint(img, mask, 5, cv2.INPAINT_TELEA)
    cv2.imwrite(output_path, result)

# Example: remove bottom-right logo
remove_corner_logo('/mnt/user-data/uploads/img.png',
                   '/mnt/user-data/outputs/no_logo.png',
                   corner='bottom_right', w_ratio=0.08, h_ratio=0.08)
```

### Find Coordinates

```python
img = cv2.imread(input_path)
h, w = img.shape[:2]
print(f"Size: {w}x{h}")

# Gemini 별 로고는 보통 이미지 우하단 모서리에서 약간 안쪽에 위치
# 일반적인 좌표: x1=w-150, y1=h-100, x2=w-130, y2=h-55
# 정확한 위치는 이미지마다 다르므로 조정 필요
```

## Output

Always save to `/mnt/user-data/outputs/` and use `present_files` tool.

## Notes

- Inpainting works best for small areas with uniform backgrounds
- Gemini logo is typically in bottom-right corner
- Adjust coordinates/ratios based on actual logo position and size