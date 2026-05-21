#!/usr/bin/env python3
"""
Validation utilities for web assets.
Validates file sizes, dimensions, formats, and accessibility requirements.
"""

import os
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from PIL import Image
import colorsys


# Platform-specific requirements
PLATFORM_REQUIREMENTS = {
    'facebook': {
        'max_file_size': 8 * 1024 * 1024,  # 8MB
        'recommended_size': (1200, 630),
        'min_size': (600, 315),
        'aspect_ratio': 1.91,
        'formats': ['png', 'jpg', 'jpeg'],
    },
    'twitter': {
        'max_file_size': 5 * 1024 * 1024,  # 5MB
        'recommended_size': (1200, 675),
        'min_size': (300, 157),
        'aspect_ratio': 16/9,
        'formats': ['png', 'jpg', 'jpeg', 'webp'],
    },
    'linkedin': {
        'max_file_size': 5 * 1024 * 1024,  # 5MB
        'recommended_size': (1200, 627),
        'min_size': (1200, 628),
        'aspect_ratio': 1.91,
        'formats': ['png', 'jpg', 'jpeg'],
    },
    'whatsapp': {
        'max_file_size': 8 * 1024 * 1024,  # 8MB (same as Facebook)
        'recommended_size': (1200, 630),
        'min_size': (600, 315),
        'aspect_ratio': 1.91,
        'formats': ['png', 'jpg', 'jpeg'],
    },
}

# WCAG contrast ratio requirements
WCAG_AA_NORMAL = 4.5
WCAG_AA_LARGE = 3.0
WCAG_AAA_NORMAL = 7.0
WCAG_AAA_LARGE = 4.5


class ValidationResult:
    """Represents the result of a validation check."""

    def __init__(self, passed: bool, message: str, level: str = 'info'):
        """
        Initialize validation result.

        Args:
            passed: Whether the validation passed
            message: Description of the result
            level: 'success', 'warning', 'error', 'info'
        """
        self.passed = passed
        self.message = message
        self.level = level

    def __str__(self):
        icon = {
            'success': '✓',
            'warning': '⚠',
            'error': '❌',
            'info': 'ℹ',
        }.get(self.level, '•')

        return f"{icon} {self.message}"

    def __repr__(self):
        return f"ValidationResult(passed={self.passed}, level='{self.level}', message='{self.message}')"


def validate_file_size(file_path: str, platform: str = 'facebook') -> ValidationResult:
    """
    Validate file size against platform requirements.

    Args:
        file_path: Path to the image file
        platform: Platform name (facebook, twitter, linkedin, whatsapp)

    Returns:
        ValidationResult with pass/fail and message
    """
    if platform not in PLATFORM_REQUIREMENTS:
        return ValidationResult(
            False,
            f"Unknown platform: {platform}",
            'error'
        )

    file_path = Path(file_path)
    if not file_path.exists():
        return ValidationResult(
            False,
            f"File not found: {file_path}",
            'error'
        )

    file_size = os.path.getsize(file_path)
    max_size = PLATFORM_REQUIREMENTS[platform]['max_file_size']

    # Convert to MB for display
    file_size_mb = file_size / (1024 * 1024)
    max_size_mb = max_size / (1024 * 1024)

    if file_size > max_size:
        return ValidationResult(
            False,
            f"File size {file_size_mb:.1f}MB exceeds {platform.title()} limit of {max_size_mb:.0f}MB",
            'error'
        )
    elif file_size > max_size * 0.8:  # Warn if within 80% of limit
        return ValidationResult(
            True,
            f"File size {file_size_mb:.1f}MB is close to {platform.title()} limit ({max_size_mb:.0f}MB)",
            'warning'
        )
    else:
        return ValidationResult(
            True,
            f"File size {file_size_mb:.1f}MB is within {platform.title()} limits",
            'success'
        )


def validate_dimensions(file_path: str, platform: str = 'facebook') -> ValidationResult:
    """
    Validate image dimensions against platform requirements.

    Args:
        file_path: Path to the image file
        platform: Platform name

    Returns:
        ValidationResult with pass/fail and message
    """
    if platform not in PLATFORM_REQUIREMENTS:
        return ValidationResult(
            False,
            f"Unknown platform: {platform}",
            'error'
        )

    file_path = Path(file_path)
    if not file_path.exists():
        return ValidationResult(
            False,
            f"File not found: {file_path}",
            'error'
        )

    try:
        with Image.open(file_path) as img:
            width, height = img.size
    except Exception as e:
        return ValidationResult(
            False,
            f"Could not read image dimensions: {e}",
            'error'
        )

    requirements = PLATFORM_REQUIREMENTS[platform]
    rec_width, rec_height = requirements['recommended_size']
    min_width, min_height = requirements['min_size']

    # Check if dimensions match recommended size
    if (width, height) == (rec_width, rec_height):
        return ValidationResult(
            True,
            f"Dimensions {width}x{height} match {platform.title()} recommended size",
            'success'
        )

    # Check if dimensions meet minimum requirements
    if width < min_width or height < min_height:
        return ValidationResult(
            False,
            f"Dimensions {width}x{height} below {platform.title()} minimum ({min_width}x{min_height})",
            'error'
        )

    # Check aspect ratio
    actual_ratio = width / height
    expected_ratio = requirements['aspect_ratio']
    ratio_diff = abs(actual_ratio - expected_ratio)

    if ratio_diff > 0.1:  # Allow 10% variance
        return ValidationResult(
            True,
            f"Dimensions {width}x{height} have non-standard aspect ratio (expected {expected_ratio:.2f}:1, got {actual_ratio:.2f}:1)",
            'warning'
        )

    return ValidationResult(
        True,
        f"Dimensions {width}x{height} meet {platform.title()} requirements",
        'success'
    )


def validate_format(file_path: str, platform: str = 'facebook') -> ValidationResult:
    """
    Validate image format against platform requirements.

    Args:
        file_path: Path to the image file
        platform: Platform name

    Returns:
        ValidationResult with pass/fail and message
    """
    if platform not in PLATFORM_REQUIREMENTS:
        return ValidationResult(
            False,
            f"Unknown platform: {platform}",
            'error'
        )

    file_path = Path(file_path)
    if not file_path.exists():
        return ValidationResult(
            False,
            f"File not found: {file_path}",
            'error'
        )

    try:
        with Image.open(file_path) as img:
            format_name = img.format.lower() if img.format else None
    except Exception as e:
        return ValidationResult(
            False,
            f"Could not read image format: {e}",
            'error'
        )

    allowed_formats = PLATFORM_REQUIREMENTS[platform]['formats']

    if format_name in allowed_formats:
        return ValidationResult(
            True,
            f"Format {format_name.upper()} is supported by {platform.title()}",
            'success'
        )
    else:
        return ValidationResult(
            False,
            f"Format {format_name.upper()} not supported by {platform.title()} (use {', '.join(allowed_formats).upper()})",
            'error'
        )


def calculate_contrast_ratio(color1: Tuple[int, int, int], color2: Tuple[int, int, int]) -> float:
    """
    Calculate contrast ratio between two RGB colors.
    Based on WCAG 2.0 formula.

    Args:
        color1: RGB tuple (r, g, b) 0-255
        color2: RGB tuple (r, g, b) 0-255

    Returns:
        Contrast ratio (1.0 to 21.0)
    """
    def relative_luminance(rgb):
        """Calculate relative luminance of an RGB color."""
        r, g, b = [c / 255.0 for c in rgb]

        # Apply gamma correction
        r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
        g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
        b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4

        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    lum1 = relative_luminance(color1)
    lum2 = relative_luminance(color2)

    # Ensure lighter color is in numerator
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)

    return (lighter + 0.05) / (darker + 0.05)


def validate_contrast(
    text_color: Tuple[int, int, int],
    bg_color: Tuple[int, int, int],
    font_size: int = 16,
    is_bold: bool = False
) -> ValidationResult:
    """
    Validate contrast ratio meets WCAG requirements.

    Args:
        text_color: RGB tuple for text
        bg_color: RGB tuple for background
        font_size: Font size in pixels
        is_bold: Whether text is bold

    Returns:
        ValidationResult with WCAG compliance level
    """
    ratio = calculate_contrast_ratio(text_color, bg_color)

    # Determine if text is "large" (18pt+ or 14pt+ bold)
    # Assuming 16px = 12pt, so 1px = 0.75pt
    pt_size = font_size * 0.75
    is_large = pt_size >= 18 or (pt_size >= 14 and is_bold)

    # Check WCAG levels
    if is_large:
        min_aa = WCAG_AA_LARGE
        min_aaa = WCAG_AAA_LARGE
    else:
        min_aa = WCAG_AA_NORMAL
        min_aaa = WCAG_AAA_NORMAL

    if ratio >= min_aaa:
        return ValidationResult(
            True,
            f"Contrast ratio {ratio:.1f}:1 meets WCAG AAA standards ({min_aaa:.1f}:1 required)",
            'success'
        )
    elif ratio >= min_aa:
        return ValidationResult(
            True,
            f"Contrast ratio {ratio:.1f}:1 meets WCAG AA standards ({min_aa:.1f}:1 required)",
            'success'
        )
    else:
        return ValidationResult(
            False,
            f"Contrast ratio {ratio:.1f}:1 fails WCAG AA standards ({min_aa:.1f}:1 required)",
            'error'
        )


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """
    Convert hex color to RGB tuple.

    Args:
        hex_color: Hex color string (e.g., "#4F46E5" or "4F46E5")

    Returns:
        RGB tuple (r, g, b)
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def validate_all(file_path: str, platforms: List[str] = None) -> Dict[str, List[ValidationResult]]:
    """
    Run all validations on an image file for specified platforms.

    Args:
        file_path: Path to the image file
        platforms: List of platforms to validate against (default: ['facebook', 'twitter'])

    Returns:
        Dictionary of platform -> list of ValidationResults
    """
    if platforms is None:
        platforms = ['facebook', 'twitter']

    results = {}

    for platform in platforms:
        if platform not in PLATFORM_REQUIREMENTS:
            results[platform] = [
                ValidationResult(False, f"Unknown platform: {platform}", 'error')
            ]
            continue

        platform_results = [
            validate_file_size(file_path, platform),
            validate_dimensions(file_path, platform),
            validate_format(file_path, platform),
        ]

        results[platform] = platform_results

    return results


def print_validation_results(results: Dict[str, List[ValidationResult]], verbose: bool = True):
    """
    Print validation results in a formatted way.

    Args:
        results: Dictionary of platform -> list of ValidationResults
        verbose: If True, show all results; if False, only show warnings/errors
    """
    for platform, checks in results.items():
        print(f"\n{platform.title()} Validation:")
        print("=" * 70)

        for result in checks:
            if verbose or result.level in ['warning', 'error']:
                print(f"  {result}")

    # Summary
    total_checks = sum(len(checks) for checks in results.values())
    passed_checks = sum(1 for checks in results.values() for r in checks if r.passed)
    failed_checks = total_checks - passed_checks

    print(f"\n{'=' * 70}")
    print(f"Summary: {passed_checks}/{total_checks} checks passed")

    if failed_checks > 0:
        print(f"⚠ {failed_checks} issue(s) need attention")
    else:
        print("✓ All validations passed!")


if __name__ == '__main__':
    # Test the validators
    import sys

    if len(sys.argv) < 2:
        print("Usage: python validators.py <image_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    print(f"Validating: {file_path}")
    results = validate_all(file_path, platforms=['facebook', 'twitter', 'linkedin'])
    print_validation_results(results)

    # Test contrast validation
    print(f"\n{'=' * 70}")
    print("Contrast Ratio Tests:")
    print("=" * 70)

    # Test cases
    test_cases = [
        ("White on Black", (255, 255, 255), (0, 0, 0), 16, False),
        ("Black on White", (0, 0, 0), (255, 255, 255), 16, False),
        ("Gray on White", (128, 128, 128), (255, 255, 255), 16, False),
        ("Purple on White", hex_to_rgb("#4F46E5"), (255, 255, 255), 16, False),
        ("White on Purple", (255, 255, 255), hex_to_rgb("#4F46E5"), 80, True),
    ]

    for name, text_color, bg_color, size, bold in test_cases:
        result = validate_contrast(text_color, bg_color, size, bold)
        print(f"  {name} ({size}px{'bold' if bold else ''}): {result}")
