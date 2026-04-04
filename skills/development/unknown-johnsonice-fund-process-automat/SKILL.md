---
name: process_resume_skill
description: Process candidate resume PDFs to extract Name, Gender, Nationality and URR status
---

# Process Candidate Resumes

This skill processes candidate resume PDFs and extracts key information using an LLM.

## What it does:
- Processes PDF resumes directly using Gemini API (handles both text-based and image-based PDFs)
- Uses Gemini 2.0 Flash to extract: Name, Gender, Country of Nationality, and URR status
- Saves results to a CSV file

## Usage:

### Basic Usage
Run the process script with default settings:
```bash
python .claude/skills/process_resume_skill/scripts/process_resume.py
```

### With Custom Options
```bash
conda activate agent
python .claude/skills/process_resume_skill/scripts/process_resume.py \
  --pdf_folder /path/to/resume/folder \
  --output_file /path/to/output.csv \
  --model gemini-2.0-flash-exp \
  --skip_test
```

### Command-line Arguments:
- `--pdf_folder`: Path to folder containing PDF resumes (default: `/ephemeral/home/xiong/data/Fund/Resumes/current`)
- `--output_file`: Path to output CSV file (default: `candidates_info.csv` in pdf_folder)
- `--model`: Gemini model to use (default: `gemini-2.0-flash-exp`)
- `--skip_test`: Skip the Gemini API connection unit test

## Key Functions:

The script provides several functions that can be used programmatically:

- `process_single_resume(pdf_path: str, client: genai.Client, model: str) -> Dict[str, str]`: Process a single resume and extract candidate information using Gemini API
- `process_resumes(pdf_folder: str, client: genai.Client, model: str) -> pd.DataFrame`: Process all resumes in a folder and return a DataFrame
- `parse_json_response(response_text: str) -> Dict[str, str]`: Parse JSON from Gemini response, handling markdown code blocks
- `print_statistics(df: pd.DataFrame) -> None`: Print summary statistics about processed candidates
- `unit_test(client: genai.Client, model: str) -> bool`: Test the Gemini API connection
- `get_extraction_prompt() -> str`: Get the prompt for information extraction

## Configuration:
- Requires `.env` file in project root with `GOOGLE_API_KEY`
- Uses Google Gemini API with direct PDF processing (no text extraction needed)
- Handles both text-based and image-based (scanned) PDFs automatically
- Handles errors gracefully by marking them as "error" in the output CSV

## Output:
The script generates a CSV file with the following columns:
- **Name**: Candidate's full name
- **Gender**: Male/Female (inferred from name and experience)
- **Nationality**: Country of nationality
- **URR**: "yes" or "no" indicating if from Under-Represented Region

## URR Countries:
The script identifies candidates from Under-Represented Regions (URR) based on a predefined list including: Afghanistan, Algeria, Angola, Bahrain, Benin, Botswana, Brunei Darussalam, Burkina Faso, Cabo Verde, Cambodia, Cameroon, Central African Republic, Chad, China, Comoros, Côte d'Ivoire, Democratic Republic of the Congo, Djibouti, Egypt, and many others (see full list in process_resume.py:33-40).

## Statistics:
After processing, the script displays:
- Total candidates processed
- Gender distribution (Female/Male counts and percentages)
- URR vs Non-URR distribution
- Processing errors (if any)
