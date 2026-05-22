---
name: pytorch-model-cli
description: Guidance for implementing CLI tools that perform inference using PyTorch models in native languages (C/C++/Rust). This skill should be used when tasks involve extracting weights from PyTorch .pth files, implementing neural network forward passes in C/C++, or creating standalone inference tools without Python dependencies.
---

# PyTorch Model CLI Implementation

## Overview

This skill provides procedural guidance for creating command-line tools that perform inference using PyTorch models without Python dependencies. These tasks typically involve extracting weights from `.pth` files, implementing forward passes in C/C++, and handling image preprocessing correctly.

## Workflow

### Phase 1: Analysis and Planning

1. **Examine the PyTorch model architecture**
   - Load the `.pth` file in Python to understand the model structure
   - Print layer names, weight shapes, and activation functions
   - Document the expected input dimensions and preprocessing requirements

2. **Inspect input data format**
   - Check image dimensions, color format (grayscale/RGB/RGBA), and bit depth
   - Determine expected normalization (0-1, -1 to 1, ImageNet stats, etc.)
   - Verify input matches model expectations (e.g., MNIST expects 28x28 grayscale)

3. **Plan weight extraction format**
   - Decide on intermediate format (JSON, binary, etc.)
   - Note that PyTorch stores linear layer weights as `[out_features, in_features]`
   - Account for any transposition needed during matrix multiplication

### Phase 2: Weight Extraction

1. **Create a weight extraction script**
   - Load model using `torch.load()` with appropriate `map_location`
   - Extract state dict and iterate through named parameters
   - Save weights in a format readable by target language

2. **Verify extracted weights**
   - Print weight statistics (min, max, mean, shape) during extraction
   - Compare shapes against expected model architecture
   - Keep the extraction script for debugging until task is fully verified

3. **Document weight ordering**
   - Record which dimension corresponds to input vs output features
   - Note any required transposition for target language implementation

### Phase 3: Native Implementation

1. **Handle image loading and preprocessing**
   - Convert color images to grayscale if required
   - Handle alpha channels appropriately (PNG files may have RGBA)
   - Resize images to expected dimensions if necessary
   - Apply correct normalization matching training preprocessing

2. **Implement forward pass**
   - Load weights from extracted format
   - Implement matrix multiplication with correct dimension ordering
   - Apply activation functions (ReLU, softmax, etc.) between layers
   - Implement argmax or appropriate output processing

3. **Add comprehensive error handling**
   - Validate input file existence before processing
   - Check image dimensions match model expectations
   - Verify weight file loads correctly with expected dimensions
   - Handle command-line argument validation

### Phase 4: Verification

1. **Compare outputs with PyTorch reference**
   - Run inference in Python and record exact output values
   - Run native implementation on same input
   - Compare numerical outputs (not just predicted class)
   - Acceptable tolerance: typically 1e-5 for float32

2. **Test edge cases**
   - Images with different color formats
   - Images with alpha channels
   - Images with incorrect dimensions
   - Missing or malformed weight files

3. **Read back written files**
   - After writing C/C++ source, read it back to verify completeness
   - Check for truncation or incomplete writes
   - Verify all functions are properly closed

## Common Pitfalls

### Weight Dimension Confusion
PyTorch linear layers store weights as `[out_features, in_features]`. When implementing matrix multiplication in C/C++:
- For input vector `x` of shape `[in_features]`
- Output is `W @ x` where `W` is `[out_features, in_features]`
- Result has shape `[out_features]`

### Image Preprocessing Errors
- PNG files may have 3 channels (RGB) or 4 channels (RGBA) even for grayscale content
- MNIST models expect single-channel input normalized to specific range
- Conversion to grayscale: `gray = 0.299*R + 0.587*G + 0.114*B`

### Premature Cleanup
- Do not delete helper scripts (weight extraction, verification) until task is confirmed working
- Keep intermediate outputs for debugging
- Maintain ability to re-run any step independently

### Incomplete File Writes
- Always verify written source files are complete
- Check that all braces/brackets are closed
- Read back the file after writing to confirm content

## Verification Checklist

Before considering the task complete:

- [ ] Model architecture documented (layers, activations, shapes)
- [ ] Input format verified (dimensions, color space, normalization)
- [ ] Weights extracted with verified shapes
- [ ] Native implementation compiles without warnings
- [ ] Output compared numerically with PyTorch reference
- [ ] Edge cases tested (wrong dimensions, missing files)
- [ ] Source files read back and verified complete
- [ ] Helper scripts retained until full verification

## Resources

### references/

- `weight_extraction_patterns.md` - Common patterns for extracting weights from different PyTorch model types
- `verification_strategies.md` - Detailed strategies for verifying native implementations against PyTorch

### scripts/

Scripts directory available for reusable extraction or verification utilities if needed.
