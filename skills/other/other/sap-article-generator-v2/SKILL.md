---
name: sap-article-generator
description: Generate comprehensive, fact-checked SAP technical articles and configuration guides with embedded images, flowcharts, and references. Use when users request SAP documentation, how-to guides, configuration tutorials, process explanations, or technical articles on SAP topics (ECC, S/4HANA, modules like SD, MM, FI, PP, ABAP, OData APIs, archiving, etc.). Creates professional Word documents with proper formatting and web-sourced visual aids with built-in image downloading.
---

# SAP Article Generator

Generate optimized, fact-checked SAP technical articles as professional Word documents with embedded images, flowcharts, and references.

## Overview

This skill is **self-contained** and includes:
- Web research and fact-checking capabilities
- Built-in image downloading from the web
- Professional Word document creation with docx
- Proper SAP formatting and terminology
- Embedded screenshots and diagrams
- Reference citations

## Article Generation Workflow

Follow these steps in sequence for every article:

### 0. PREREQUISITE: Read docx Skill (MANDATORY)
```bash
# REQUIRED before creating any Word document
cat /mnt/skills/public/docx/SKILL.md
```

### 1. Topic Analysis and Planning (2-3 minutes)
- Identify the SAP module, process, or topic
- Determine scope: configuration guide, conceptual overview, or troubleshooting
- Define target audience: beginner, intermediate, or advanced users
- Plan article structure based on topic type

### 2. Research and Fact-Checking (5-10 minutes)
**CRITICAL: Always search before writing to ensure current, accurate information**

Use web_search tool to verify:
- Latest SAP transaction codes and menu paths
- Current best practices and SAP Notes
- Version-specific differences (ECC vs S/4HANA)
- Official SAP documentation

**Minimum 2-3 searches** for any article.

**Search query examples:**
- "SAP [transaction code] [module] configuration"
- "SAP [process name] step by step guide"
- "SAP S/4HANA [topic] best practices"

### 3. Content Structure Planning

**Configuration Guides:**
1. Introduction and business context
2. Prerequisites and system requirements
3. Configuration overview
4. Step-by-step configuration with transaction codes
5. IMG menu paths and settings
6. Testing and validation
7. Troubleshooting
8. Best practices
9. References

**Conceptual Articles:**
1. Introduction and business context
2. Key concepts and terminology
3. Process flow and architecture
4. Technical implementation
5. Integration points
6. Use cases and examples
7. Best practices
8. References

**Troubleshooting Guides:**
1. Problem overview and symptoms
2. Root cause analysis
3. Diagnostic steps
4. Solution steps
5. Prevention strategies
6. Related SAP Notes
7. References

### 4. Visual Content Integration (CRITICAL - MUST DO THIS!)

**Images significantly improve article quality. Every article MUST have 2-3+ embedded images.**

#### Step 4.1: Search for Images
Use web_search to find relevant SAP images:
```
web_search("SAP [transaction] screenshot")
web_search("SAP [process] flow diagram")
web_search("SAP [module] configuration screen")
```

**Image types to include:**
- Transaction screen screenshots
- Process flow diagrams
- System architecture diagrams
- Configuration examples
- Data flow illustrations

#### Step 4.2: Extract Image URLs
From the web_search results, identify direct image URLs. Look for:
- .png, .jpg, .jpeg, .gif, .svg, .webp URLs
- Image URLs in search results snippets
- URLs from SAP blogs, tutorials, help portal

#### Step 4.3: Download Images Using Built-in Script

**Install dependencies first (if not already installed):**
```bash
pip install requests Pillow --break-system-packages
```

**Create temp directory:**
```bash
mkdir -p /home/claude/temp_images
```

**Download images:**

**Option A - Single Image:**
```bash
python scripts/fetch_image.py \
  "https://example.com/sap-screenshot.png" \
  /home/claude/temp_images
```

**Option B - Multiple Images (Recommended):**
```bash
# Create URL list
cat > /home/claude/image_urls.txt << 'EOF'
https://example.com/sap-vov8.png
https://example.com/sales-flow.jpg
https://example.com/config-screen.png
EOF

# Download all at once
python scripts/fetch_images_batch.py \
  /home/claude/image_urls.txt \
  /home/claude/temp_images
```

#### Step 4.4: Verify Downloads
```bash
ls -lh /home/claude/temp_images/
```

You should see the downloaded images with file sizes.

### 5. Document Creation with Embedded Images

**Follow the docx skill guidelines to create a professional Word document.**

**Key requirements for images in the document:**

1. **Embed images using the docx library** according to the docx skill instructions
2. **Use the downloaded image paths** from `/home/claude/temp_images/`
3. **Add figure captions** below each image:
   - Format: "Figure X: [Description]"
   - Example: "Figure 1: SAP Transaction VOV8 - Sales Document Type Configuration"
4. **Center-align images**
5. **Resize to appropriate width** (typically 600px for full-width images)

**Example embedding pattern (following docx skill):**
```python
# After creating document according to docx skill
# Add image paragraph with the downloaded image
# See docx SKILL.md for exact syntax
```

### 6. Document Formatting Standards

**Title Page:**
- Article title (Heading 1, SAP blue #0070AD)
- Subtitle
- Date and version

**Content Formatting:**
- **Headings**: Hierarchical (H1: 16pt SAP blue, H2: 14pt, H3: 12pt)
- **Paragraphs**: 11pt Calibri, 1.15 line spacing
- **Transaction codes**: Monospace font (Courier New), light gray background
- **Tables**: Professional borders, header row with SAP blue background
- **Lists**: Bullet points or numbered lists as appropriate

**Images:**
- 600px width for full-width images
- Figure captions below each image
- Center-aligned
- Minimum 2-3 images per article

**References Section:**
- Numbered list of all sources
- Format: [1] Source Title, URL, Accessed: YYYY-MM-DD

### 7. Quality Assurance Checklist

Before delivering, verify:
- [ ] Read docx SKILL.md completely
- [ ] Performed 2-3+ web searches for fact-checking
- [ ] Downloaded 2-3+ relevant images
- [ ] Images properly embedded with captions
- [ ] All transaction codes verified
- [ ] Table of contents generated (if applicable)
- [ ] References section complete
- [ ] Professional formatting throughout
- [ ] Saved to /mnt/user-data/outputs/

### 8. Delivery
```bash
# Save document to outputs
# Filename: [Topic]_SAP_Guide.docx
mv /home/claude/article.docx /mnt/user-data/outputs/SAP_[Topic]_Guide.docx
```

Provide user with:
- Computer link: `computer:///mnt/user-data/outputs/SAP_[Topic]_Guide.docx`
- Brief summary of included content

## Built-in Image Fetching Scripts

This skill includes two Python scripts for downloading images:

### scripts/fetch_image.py
Downloads a single image from a URL.

**Usage:**
```bash
python scripts/fetch_image.py <image_url> [output_dir] [filename]
```

**Examples:**
```bash
# Download to current directory
python scripts/fetch_image.py https://example.com/image.jpg

# Download to specific directory
python scripts/fetch_image.py https://example.com/image.jpg /home/claude/temp_images

# Download with custom filename
python scripts/fetch_image.py https://example.com/image.jpg /home/claude/temp_images sap_screenshot.jpg
```

### scripts/fetch_images_batch.py
Downloads multiple images from a list.

**Usage:**
```bash
python scripts/fetch_images_batch.py <urls_file> [output_dir]
```

**Input file:** Text file with one URL per line, or JSON array

**Example:**
```bash
python scripts/fetch_images_batch.py urls.txt /home/claude/temp_images
```

## Common SAP Topics

This skill handles articles on:
- **SD**: Sales orders, pricing, delivery, billing, consignment
- **MM**: Procurement, inventory, material master, consignment
- **FI**: General ledger, accounts payable/receivable, asset accounting
- **CO**: Cost centers, profit centers, internal orders
- **PP**: Production planning, work centers, BOMs, confirmations
- **WM**: Warehouse management, storage bins, transfers
- **Technical**: ABAP, OData APIs, IDocs, BAPIs, RFCs, CDS views
- **Basis**: Data archiving (SARA), transports, system administration
- **S/4HANA**: Fiori apps, embedded analytics, simplifications

## Complete Example Workflow

**User Request:** "Create an article on SAP sales order type configuration"

**Step-by-step execution:**

1. **Read docx skill:**
   ```bash
   cat /mnt/skills/public/docx/SKILL.md
   ```

2. **Research** (3 web searches):
   ```
   web_search("SAP SD sales order type configuration VOV8")
   web_search("SAP sales document types customizing")
   web_search("SAP S/4HANA order type setup")
   ```

3. **Find images** (2 web searches):
   ```
   web_search("SAP transaction VOV8 screenshot")
   web_search("SAP sales order flow diagram")
   ```

4. **Download images:**
   ```bash
   mkdir -p /home/claude/temp_images
   
   cat > /home/claude/urls.txt << 'EOF'
   https://sap-blog.com/vov8-screenshot.png
   https://sap-tutorial.com/sales-flow.jpg
   EOF
   
   python scripts/fetch_images_batch.py /home/claude/urls.txt /home/claude/temp_images
   
   ls -lh /home/claude/temp_images/
   ```

5. **Create Word document** following docx skill with:
   - Title page
   - Table of contents
   - Introduction
   - Configuration steps
   - **Embedded images** from /home/claude/temp_images/
   - Testing procedures
   - References section

6. **Save and deliver:**
   ```bash
   # Document saved during creation to:
   /mnt/user-data/outputs/SAP_Sales_Order_Types_Configuration_Guide.docx
   ```

## Troubleshooting

**Issue: Images not downloading**
- Check URLs are direct image links
- Verify network connectivity
- Try alternative image sources
- Some sites block automated downloads

**Issue: Image format not supported**
- Script supports: JPG, PNG, GIF, WebP, BMP, SVG, TIFF
- Auto-detects format from content-type header

**Issue: Images not embedding in Word**
- Verify image files exist in /home/claude/temp_images/
- Check file paths are correct
- Follow docx skill instructions exactly for embedding

**Issue: Python dependencies missing**
```bash
pip install requests Pillow --break-system-packages
```

## Critical Reminders

1. **ALWAYS read docx SKILL.md first** before creating any Word document
2. **ALWAYS fact-check** with 2-3+ web searches
3. **ALWAYS download and embed 2-3+ images** - this is not optional
4. **ALWAYS cite sources** in the references section
5. **ALWAYS use proper SAP formatting** (transaction codes in monospace)
6. **ALWAYS save to /mnt/user-data/outputs/** for user access
7. **ALWAYS verify** image downloads before embedding

## Success Criteria

A successful SAP article includes:
✅ 2000-4000 words of fact-checked content  
✅ 2-3+ embedded images with captions  
✅ Professional Word document formatting  
✅ SAP-specific styling (blue headers, monospace codes)  
✅ Step-by-step instructions with transaction codes  
✅ References section with 3-5+ sources  
✅ Saved to /mnt/user-data/outputs/ with proper filename
