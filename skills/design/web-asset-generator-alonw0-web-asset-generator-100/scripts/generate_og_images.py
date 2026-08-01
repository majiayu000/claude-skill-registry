#!/usr/bin/env python3
"""
Generate social media meta images (Open Graph images) for Facebook, Twitter, WhatsApp, etc.
Can work with a logo/image or text-based content.
"""

import sys
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Import validation utilities
try:
    from lib.validators import validate_all, print_validation_results, hex_to_rgb, validate_contrast
except ImportError:
    # If running from a different directory, try alternative import
    sys.path.insert(0, str(Path(__file__).parent))
    from lib.validators import validate_all, print_validation_results, hex_to_rgb, validate_contrast

# Standard Open Graph image sizes
OG_SIZES = {
    'og-image.png': (1200, 630),  # Facebook, LinkedIn, WhatsApp
    'twitter-image.png': (1200, 675),  # Twitter (16:9 ratio)
    'og-square.png': (1200, 1200),  # Square variant for some platforms
}

def calculate_font_size(text, base_size=120):
    """
    Calculate optimal font size based on text length.

    Args:
        text: The text to be displayed
        base_size: Base font size (default: 120)

    Returns:
        int: Calculated font size
    """
    text_length = len(text)

    if text_length <= 20:
        # Short text: use larger font for impact
        return int(base_size * 1.2)  # 144px
    elif text_length <= 40:
        # Medium text: use base size
        return base_size  # 120px
    elif text_length <= 60:
        # Long text: reduce slightly
        return int(base_size * 0.85)  # 102px
    else:
        # Very long text: reduce more
        return int(base_size * 0.7)  # 84px

def create_text_image(text, size, bg_color='#4F46E5', text_color='white', 
                     font_size=80, logo_path=None):
    """
    Create an image with text and optional logo.
    
    Args:
        text: Main text to display
        size: Tuple of (width, height)
        bg_color: Background color (hex or color name)
        text_color: Text color
        font_size: Font size for text
        logo_path: Optional path to logo image to include
    """
    # Create image
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice font, fall back to default
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", int(font_size * 0.5))
    except:
        font = ImageFont.load_default()
        font_small = font
    
    # Add logo if provided
    logo_height = 0
    if logo_path and Path(logo_path).exists():
        logo = Image.open(logo_path)
        # Resize logo to fit (max 20% of image height - gives more space for text)
        max_logo_height = int(size[1] * 0.20)
        if logo.height > max_logo_height:
            ratio = max_logo_height / logo.height
            new_size = (int(logo.width * ratio), max_logo_height)
            logo = logo.resize(new_size, Image.Resampling.LANCZOS)
        
        # Convert to RGBA if needed
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        
        # Center logo at top
        logo_x = (size[0] - logo.width) // 2
        logo_y = int(size[1] * 0.15)
        img.paste(logo, (logo_x, logo_y), logo)
        logo_height = logo.height + int(size[1] * 0.1)
    
    # Wrap text to fit width
    max_width = int(size[0] * 0.85)  # 85% of image width
    wrapped_lines = []
    
    # Split text into words and wrap
    words = text.split()
    current_line = []
    
    for word in words:
        current_line.append(word)
        line_text = ' '.join(current_line)
        bbox = draw.textbbox((0, 0), line_text, font=font)
        line_width = bbox[2] - bbox[0]
        
        if line_width > max_width:
            if len(current_line) > 1:
                current_line.pop()
                wrapped_lines.append(' '.join(current_line))
                current_line = [word]
            else:
                wrapped_lines.append(word)
                current_line = []
    
    if current_line:
        wrapped_lines.append(' '.join(current_line))
    
    # Calculate total text height
    total_text_height = 0
    for line in wrapped_lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        total_text_height += (bbox[3] - bbox[1]) + 10
    
    # Start position for text (centered vertically)
    available_height = size[1] - logo_height
    y = logo_height + (available_height - total_text_height) // 2
    
    # Draw each line centered
    for line in wrapped_lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        line_height = bbox[3] - bbox[1]
        x = (size[0] - line_width) // 2
        draw.text((x, y), line, fill=text_color, font=font)
        y += line_height + 10
    
    return img

def resize_image_for_og(source_path, size, fit_mode='cover'):
    """
    Resize an existing image for Open Graph specs.
    
    Args:
        source_path: Path to source image
        size: Target size tuple (width, height)
        fit_mode: 'cover' (fill, may crop) or 'contain' (fit, may have borders)
    """
    img = Image.open(source_path)
    
    if fit_mode == 'cover':
        # Calculate aspect ratios
        img_ratio = img.width / img.height
        target_ratio = size[0] / size[1]
        
        if img_ratio > target_ratio:
            # Image is wider, fit to height
            new_height = size[1]
            new_width = int(new_height * img_ratio)
        else:
            # Image is taller, fit to width
            new_width = size[0]
            new_height = int(new_width / img_ratio)
        
        # Resize and crop to center
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Crop to target size
        left = (new_width - size[0]) // 2
        top = (new_height - size[1]) // 2
        img = img.crop((left, top, left + size[0], top + size[1]))
    else:  # contain
        # Fit image within target size, add borders if needed
        img.thumbnail(size, Image.Resampling.LANCZOS)
        
        # Create new image with target size and paste resized image centered
        new_img = Image.new('RGB', size, 'white')
        x = (size[0] - img.width) // 2
        y = (size[1] - img.height) // 2
        new_img.paste(img, (x, y))
        img = new_img
    
    return img

def generate_og_images(output_dir, text=None, source_image=None, logo_path=None,
                       bg_color='#4F46E5', text_color='white', platforms='all',
                       validate=False):
    """
    Generate Open Graph images for social media.

    Args:
        output_dir: Directory to save images
        text: Text to display (if creating text-based image)
        source_image: Path to existing image to resize
        logo_path: Path to logo to include with text
        bg_color: Background color for text-based images
        text_color: Text color for text-based images
        platforms: 'facebook', 'twitter', 'square', or 'all'
        validate: If True, run validation checks on generated images

    Returns:
        Dictionary with 'files' and optional 'validation_results'
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Determine which sizes to generate
    sizes_to_generate = {}
    if platforms == 'all':
        sizes_to_generate = OG_SIZES
    elif platforms == 'facebook':
        sizes_to_generate = {'og-image.png': OG_SIZES['og-image.png']}
    elif platforms == 'twitter':
        sizes_to_generate = {'twitter-image.png': OG_SIZES['twitter-image.png']}
    elif platforms == 'square':
        sizes_to_generate = {'og-square.png': OG_SIZES['og-square.png']}

    generated_files = []

    for filename, size in sizes_to_generate.items():
        if text:
            # Generate text-based image with dynamic font sizing
            # Base size: 120px for 1200px images, 90px for smaller
            base_font_size = 120 if size[0] >= 1200 else 90
            optimal_font_size = calculate_font_size(text, base_font_size)
            img = create_text_image(text, size, bg_color, text_color,
                                   font_size=optimal_font_size,
                                   logo_path=logo_path)
        elif source_image:
            # Resize existing image
            img = resize_image_for_og(source_image, size)
        else:
            raise ValueError("Must provide either text or source_image")

        # Save
        output_path = output_dir / filename
        img.save(output_path, 'PNG', optimize=True)
        generated_files.append(str(output_path))
        print(f"✓ Generated {filename} ({size[0]}x{size[1]})")

    result = {'files': generated_files}

    # Run validation if requested
    if validate and generated_files:
        print("\n" + "=" * 70)
        print("Running validation checks...")
        print("=" * 70)

        validation_results = {}

        # Validate each generated file
        for file_path in generated_files:
            filename = Path(file_path).name

            # Determine platform(s) for this file
            if 'twitter' in filename:
                platforms_to_check = ['twitter']
            elif 'square' in filename:
                platforms_to_check = ['facebook', 'twitter']  # Square works for both
            else:
                platforms_to_check = ['facebook', 'linkedin', 'whatsapp']

            file_results = validate_all(file_path, platforms_to_check)
            validation_results[filename] = file_results

            # Print results for this file
            print(f"\n{filename}:")
            print_validation_results(file_results, verbose=True)

        # If text-based, also validate contrast ratio
        if text:
            print("\n" + "=" * 70)
            print("Accessibility Checks:")
            print("=" * 70)

            try:
                # Convert colors to RGB tuples
                if bg_color.startswith('#'):
                    bg_rgb = hex_to_rgb(bg_color)
                else:
                    # For named colors, we'd need a mapping - for now just skip
                    bg_rgb = None

                if text_color.startswith('#'):
                    text_rgb = hex_to_rgb(text_color)
                elif text_color.lower() == 'white':
                    text_rgb = (255, 255, 255)
                elif text_color.lower() == 'black':
                    text_rgb = (0, 0, 0)
                else:
                    text_rgb = None

                if bg_rgb and text_rgb:
                    # Calculate font size in pixels (use the optimal font size calculated earlier)
                    base_font_size = 120 if list(sizes_to_generate.values())[0][0] >= 1200 else 90
                    optimal_font_size = calculate_font_size(text, base_font_size)

                    contrast_result = validate_contrast(
                        text_rgb,
                        bg_rgb,
                        font_size=optimal_font_size,
                        is_bold=True  # Social images typically use bold text
                    )
                    print(f"  {contrast_result}")
                    validation_results['contrast'] = contrast_result
            except Exception as e:
                print(f"  ⚠ Could not validate contrast: {e}")

        result['validation_results'] = validation_results

    return result

def generate_og_html_tags():
    """Generate HTML meta tags for Open Graph images."""
    return """<!-- Open Graph / Facebook -->
<meta property="og:image" content="/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Your description here">

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="/twitter-image.png">
<meta name="twitter:image:alt" content="Your description here">"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate social media meta images (Open Graph images)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Text-based image
  python generate_og_images.py output/ --text "Welcome to my site"

  # Text with logo
  python generate_og_images.py output/ --text "My App" --logo logo.png

  # Text with custom colors
  python generate_og_images.py output/ --text "Hello" --bg-color "#FF5733" --text-color "#FFFFFF"

  # Resize existing image
  python generate_og_images.py output/ --image photo.jpg

  # Generate with validation
  python generate_og_images.py output/ --text "My Site" --validate
        """
    )

    parser.add_argument('output_dir', help='Directory to save generated images')

    # Source options (mutually exclusive)
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument('--text', help='Text to display in the image')
    source_group.add_argument('--image', dest='source_image', help='Path to existing image to resize')

    # Optional arguments
    parser.add_argument('--logo', dest='logo_path', help='Path to logo image to include with text')
    parser.add_argument('--bg-color', dest='bg_color', default='#4F46E5',
                       help='Background color (hex or name, default: #4F46E5)')
    parser.add_argument('--text-color', dest='text_color', default='white',
                       help='Text color (hex or name, default: white)')
    parser.add_argument('--platforms', choices=['all', 'facebook', 'twitter', 'square'],
                       default='all', help='Which platforms to generate for (default: all)')
    parser.add_argument('--validate', action='store_true',
                       help='Run validation checks on generated images (file size, dimensions, contrast)')

    args = parser.parse_args()

    print("Generating Open Graph images...")
    result = generate_og_images(
        args.output_dir,
        text=args.text,
        source_image=args.source_image,
        logo_path=args.logo_path,
        bg_color=args.bg_color,
        text_color=args.text_color,
        platforms=args.platforms,
        validate=args.validate
    )

    files = result['files']
    print(f"\n✅ Generated {len(files)} Open Graph images in {args.output_dir}/")

    if not args.validate:
        print("\n💡 Tip: Use --validate to check file sizes, dimensions, and accessibility")

    print("\nHTML meta tags to include in your <head>:")
    print(generate_og_html_tags())
