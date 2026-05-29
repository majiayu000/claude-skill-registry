---
name: gemini-video
description: Invoke Google Gemini for video understanding and analysis using the Python google-genai SDK. Supports gemini-3-pro-preview and gemini-2.5-flash for video analysis, transcription, and content extraction.
---

# Gemini Video Skill

Invoke Google Gemini models for video understanding, analysis, transcription, and content extraction using the Python `google-genai` SDK.

## Available Models

| Model ID | Description | Best For |
|----------|-------------|----------|
| `gemini-3-pro-preview` | Best multimodal understanding | Complex video analysis, detailed descriptions |
| `gemini-2.5-pro` | Advanced reasoning | Deep video analysis with reasoning |
| `gemini-2.5-flash` | Fast processing | Quick video summaries, high throughput |

## Configuration

**API Key**: Use environment variable `GEMINI_API_KEY`

## Usage

### Video Analysis (Local File)

For local video files, use the File API to upload first:

```bash
python -c "
from google import genai
from google.genai import types
import time

client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

# Upload video file
video_file = client.files.upload(file='VIDEO_PATH')
print(f'Uploaded file: {video_file.name}')

# Wait for processing
while video_file.state.name == 'PROCESSING':
    print('Processing video...')
    time.sleep(5)
    video_file = client.files.get(name=video_file.name)

if video_file.state.name == 'FAILED':
    raise ValueError('Video processing failed')

# Analyze video
response = client.models.generate_content(
    model='gemini-3-pro-preview',
    contents=[
        types.Content(parts=[
            types.Part(text='Describe what happens in this video'),
            types.Part(file_data=types.FileData(file_uri=video_file.uri, mime_type=video_file.mime_type))
        ])
    ]
)
print(response.text)
"
```

### Video Analysis (From URL)

```bash
python -c "
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

# For publicly accessible video URLs
video_url = 'VIDEO_URL_HERE'

response = client.models.generate_content(
    model='gemini-3-pro-preview',
    contents=[
        types.Content(parts=[
            types.Part(text='Analyze this video and provide a detailed summary'),
            types.Part(file_data=types.FileData(file_uri=video_url, mime_type='video/mp4'))
        ])
    ]
)
print(response.text)
"
```

### Video Transcription

```bash
python -c "
from google import genai
from google.genai import types
import time

client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

# Upload video
video_file = client.files.upload(file='VIDEO_PATH')
while video_file.state.name == 'PROCESSING':
    time.sleep(5)
    video_file = client.files.get(name=video_file.name)

# Transcribe
response = client.models.generate_content(
    model='gemini-3-pro-preview',
    contents=[
        types.Content(parts=[
            types.Part(text='Transcribe all spoken words in this video. Include timestamps if possible.'),
            types.Part(file_data=types.FileData(file_uri=video_file.uri, mime_type=video_file.mime_type))
        ])
    ]
)
print(response.text)
"
```

## Workflow

When this skill is invoked:

1. **Determine the task type**:
   - **Video Summary**: Generate overview of video content
   - **Transcription**: Extract spoken words
   - **Visual Analysis**: Describe visual elements, scenes, actions
   - **Content Extraction**: Pull specific information from video
   - **Q&A**: Answer questions about video content

2. **Prepare the video**:
   - Local file → Upload via File API
   - Remote URL → Use directly (if publicly accessible)
   - Wait for processing if needed

3. **Select the appropriate model**:
   - Complex analysis → `gemini-3-pro-preview`
   - Quick summaries → `gemini-2.5-flash`

4. **Execute and return results**

## Example Invocations

### Summarize Meeting Recording
```bash
python -c "
from google import genai
from google.genai import types
import time

client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

video_file = client.files.upload(file='meeting_recording.mp4')
while video_file.state.name == 'PROCESSING':
    time.sleep(5)
    video_file = client.files.get(name=video_file.name)

response = client.models.generate_content(
    model='gemini-3-pro-preview',
    contents=[
        types.Content(parts=[
            types.Part(text='''Summarize this meeting recording:
1. List all participants mentioned
2. Key discussion points
3. Action items and decisions made
4. Any deadlines mentioned'''),
            types.Part(file_data=types.FileData(file_uri=video_file.uri, mime_type=video_file.mime_type))
        ])
    ]
)
print(response.text)
"
```

### Analyze Tutorial Video
```bash
python -c "
from google import genai
from google.genai import types
import time

client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

video_file = client.files.upload(file='tutorial.mp4')
while video_file.state.name == 'PROCESSING':
    time.sleep(5)
    video_file = client.files.get(name=video_file.name)

response = client.models.generate_content(
    model='gemini-3-pro-preview',
    contents=[
        types.Content(parts=[
            types.Part(text='''Analyze this tutorial video and create:
1. A step-by-step guide based on the content
2. Key concepts explained
3. Any tips or best practices mentioned
4. Prerequisites needed to follow along'''),
            types.Part(file_data=types.FileData(file_uri=video_file.uri, mime_type=video_file.mime_type))
        ])
    ]
)
print(response.text)
"
```

### Extract Code from Coding Video
```bash
python -c "
from google import genai
from google.genai import types
import time

client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

video_file = client.files.upload(file='coding_session.mp4')
while video_file.state.name == 'PROCESSING':
    time.sleep(5)
    video_file = client.files.get(name=video_file.name)

response = client.models.generate_content(
    model='gemini-3-pro-preview',
    contents=[
        types.Content(parts=[
            types.Part(text='''Extract all code shown in this video:
1. Identify the programming language
2. Capture the complete code snippets
3. Note any explanations given for the code
4. List any libraries or dependencies mentioned'''),
            types.Part(file_data=types.FileData(file_uri=video_file.uri, mime_type=video_file.mime_type))
        ])
    ]
)
print(response.text)
"
```

### Timestamp-Based Analysis
```bash
python -c "
from google import genai
from google.genai import types
import time

client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

video_file = client.files.upload(file='presentation.mp4')
while video_file.state.name == 'PROCESSING':
    time.sleep(5)
    video_file = client.files.get(name=video_file.name)

response = client.models.generate_content(
    model='gemini-3-pro-preview',
    contents=[
        types.Content(parts=[
            types.Part(text='''Create a timestamped outline of this video:
Format: [MM:SS] - Topic/Event
Include major topic changes, key points, and notable moments.'''),
            types.Part(file_data=types.FileData(file_uri=video_file.uri, mime_type=video_file.mime_type))
        ])
    ]
)
print(response.text)
"
```

### Q&A About Video
```bash
python -c "
from google import genai
from google.genai import types
import time

client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

video_file = client.files.upload(file='lecture.mp4')
while video_file.state.name == 'PROCESSING':
    time.sleep(5)
    video_file = client.files.get(name=video_file.name)

response = client.models.generate_content(
    model='gemini-3-pro-preview',
    contents=[
        types.Content(parts=[
            types.Part(text='YOUR_QUESTION_ABOUT_VIDEO_HERE'),
            types.Part(file_data=types.FileData(file_uri=video_file.uri, mime_type=video_file.mime_type))
        ])
    ]
)
print(response.text)
"
```

## File Management

### List Uploaded Files
```bash
python -c "
from google import genai

client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

for f in client.files.list():
    print(f'{f.name}: {f.state.name} ({f.mime_type})')
"
```

### Delete Uploaded File
```bash
python -c "
from google import genai

client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
client.files.delete(name='files/FILE_ID_HERE')
print('File deleted')
"
```

## Supported Video Formats

- MP4 (`video/mp4`)
- MOV (`video/quicktime`)
- AVI (`video/x-msvideo`)
- FLV (`video/x-flv`)
- MKV (`video/x-matroska`)
- WebM (`video/webm`)
- WMV (`video/x-ms-wmv`)
- 3GPP (`video/3gpp`)

## Video Limitations

- **Maximum file size**: Check current API limits (typically 2GB)
- **Maximum duration**: Varies by model (typically up to 1 hour)
- **Processing time**: Longer videos take more time to process
- **Quota**: Video analysis consumes more tokens than text

## Error Handling

Common errors and solutions:
- **PROCESSING state stuck**: Video may be too large or corrupted
- **FAILED state**: Unsupported format or processing error
- **File not found**: Upload before analysis
- **Rate limiting**: Implement retry with exponential backoff

## Notes

- Videos must be uploaded via File API before analysis (no inline data like images)
- Processing time depends on video length and complexity
- Uploaded files are automatically deleted after 48 hours
- For very long videos, consider chunking or asking specific timestamp questions
- Gemini 3 Pro provides the most detailed video analysis

## Tools to Use

- **Bash**: Execute Python commands
- **Read**: Load local video file paths
- **Write**: Save transcriptions or analysis to files
- **Glob**: Find video files in directories
