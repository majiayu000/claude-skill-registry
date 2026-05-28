---
name: Label Studio Setup
description: Comprehensive guide for Label Studio setup and usage on local server for data labeling and annotation.
---

# Label Studio Setup

## Overview

Label Studio is an open-source data labeling platform that provides tools for image, text, audio, and video annotation. This skill covers Label Studio installation, project setup, data import/export, labeling interface customization, user management, quality control, ML backend integration, API usage, backup and migration, and production deployment.

## Prerequisites

- Understanding of Docker and containerization
- Knowledge of Python programming
- Familiarity with data annotation concepts
- Basic understanding of PostgreSQL and Redis
- Knowledge of web server configuration (Nginx)

## Key Concepts

### Label Studio Components

- **Web Application**: Django-based UI for labeling
- **Database**: PostgreSQL for data storage
- **Cache**: Redis for session management
- **ML Backend**: Optional ML model integration for pre-annotation
- **Storage**: File storage for media assets

### Annotation Types

- **Image Classification**: Single label per image
- **Object Detection**: Bounding box annotations
- **Semantic Segmentation**: Pixel-level annotations
- **Named Entity Recognition (NER)**: Text entity extraction
- **Video Annotation**: Frame-by-frame labeling
- **Audio Classification**: Labeling audio clips

### Quality Control

- **Review Workflow**: Multi-stage review process
- **Consensus**: Multiple annotators per task
- **Active Learning**: Uncertainty-based sampling
- **Inter-annotator Agreement**: Quality metrics

## Implementation Guide

### Installation

#### Docker Setup

```bash
# Pull Label Studio image
docker pull heartexlabs/label-studio:latest

# Create data directory
mkdir -p label-studio/data

# Run Label Studio
docker run -it \
  -p 8080:8080 \
  -v `pwd`/label-studio/data:/label-studio/data \
  heartexlabs/label-studio:latest
```

#### Docker Compose Setup

```yaml
# docker-compose.yml
version: '3.3'

services:
  app:
    image: heartexlabs/label-studio:latest
    container_name: label-studio
    ports:
      - 8080:8080
    volumes:
      - ./label-studio/data:/label-studio/data
    environment:
      - DJANGO_DB=default
      - POSTGRE_HOST=postgres
      - POSTGRE_USER=labelstudio
      - POSTGRE_PASSWORD=labelstudio
      - POSTGRE_DB=labelstudio
      - LABEL_STUDIO_USERNAME=admin
      - LABEL_STUDIO_PASSWORD=admin
      - LABEL_STUDIO_EMAIL=admin@example.com
    depends_on:
      - postgres

  postgres:
    image: postgres:13-alpine
    container_name: postgres
    volumes:
      - ./label-studio/postgres-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=labelstudio
      - POSTGRES_PASSWORD=labelstudio
      - POSTGRES_DB=labelstudio

  redis:
    image: redis:alpine
    container_name: redis
    ports:
      - 6379:6379

volumes:
  label-studio-postgres-data:
```

```bash
# Start with Docker Compose
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f app
```

#### Local Installation

```bash
# Install via pip
pip install label-studio

# Install with PostgreSQL support
pip install label-studio[postgresql]

# Install with all dependencies
pip install label-studio[all]

# Start Label Studio
label-studio start

# Start with custom port
label-studio start --port 9000

# Start with custom data directory
label-studio start --data-dir ./mydata

# Start with custom host
label-studio start --host 0.0.0.0
```

#### Configuration

```python
# label_studio_config.py
import os

# Database settings
DATABASE = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': os.getenv('POSTGRES_DB', 'labelstudio'),
    'USER': os.getenv('POSTGRES_USER', 'labelstudio'),
    'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'labelstudio'),
    'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
    'PORT': os.getenv('POSTGRES_PORT', '5432'),
}

# Redis settings
REDIS_LOCATION = os.getenv('REDIS_LOCATION', 'redis://localhost:6379/0')

# Storage settings
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'data', 'media')

# Security settings
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
ALLOWED_HOSTS = ['*']

# Email settings (for notifications)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# ML backend settings
ML_BACKEND_HOST = os.getenv('ML_BACKEND_HOST', 'http://localhost:9090')
ML_BACKEND_TIMEOUT = int(os.getenv('ML_BACKEND_TIMEOUT', '100'))
```

### Project Setup

#### Image Classification

```xml
<!-- Image Classification Config -->
<View>
  <Image name="image" value="$image"/>
  <Choices name="label" toName="image">
    <Choice value="Cat"/>
    <Choice value="Dog"/>
    <Choice value="Bird"/>
    <Choice value="Other"/>
  </Choices>
</View>

<Header value="Image Classification"/>
```

```python
# Create image classification project
from label_studio_sdk import Client

# Connect to Label Studio
LABEL_STUDIO_URL = 'http://localhost:8080'
API_KEY = 'your-api-key-here'

client = Client(url=LABEL_STUDIO_URL, api_key=API_KEY)

# Create project
project = client.create_project(
    title='Image Classification',
    description='Classify images into categories',
    label_config='''
    <View>
      <Image name="image" value="$image"/>
      <Choices name="label" toName="image">
        <Choice value="Cat"/>
        <Choice value="Dog"/>
        <Choice value="Bird"/>
        <Choice value="Other"/>
      </Choices>
    </View>
    '''
)
```

#### Object Detection

```xml
<!-- Object Detection Config -->
<View>
  <Image name="image" value="$image"/>
  <RectangleLabels name="label" toName="image" strokeWidth="3">
    <Label value="Person" background="#FF0000"/>
    <Label value="Car" background="#00FF00"/>
    <Label value="Bicycle" background="#0000FF"/>
    <Label value="Dog" background="#FFFF00"/>
  </RectangleLabels>
</View>

<Header value="Object Detection"/>
```

```python
# Create object detection project
project = client.create_project(
    title='Object Detection',
    description='Detect objects in images',
    label_config='''
    <View>
      <Image name="image" value="$image"/>
      <RectangleLabels name="label" toName="image" strokeWidth="3">
        <Label value="Person" background="#FF0000"/>
        <Label value="Car" background="#00FF00"/>
        <Label value="Bicycle" background="#0000FF"/>
        <Label value="Dog" background="#FFFF00"/>
      </RectangleLabels>
    </View>
    '''
)
```

#### Segmentation

```xml
<!-- Segmentation Config -->
<View>
  <Image name="image" value="$image"/>
  <PolygonLabels name="label" toName="image" strokeWidth="3">
    <Label value="Background" background="#000000"/>
    <Label value="Person" background="#FF0000"/>
    <Label value="Car" background="#00FF00"/>
    <Label value="Building" background="#0000FF"/>
  </PolygonLabels>
</View>

<Header value="Semantic Segmentation"/>
```

#### Named Entity Recognition (NER)

```xml
<!-- NER Config -->
<View>
  <Text name="text" value="$text"/>
  <Labels name="label" toName="text">
    <Label value="PERSON" background="#FF0000"/>
    <Label value="ORG" background="#00FF00"/>
    <Label value="LOC" background="#0000FF"/>
    <Label value="MISC" background="#FFFF00"/>
  </Labels>
</View>

<Header value="Named Entity Recognition"/>
```

```python
# Create NER project
project = client.create_project(
    title='Named Entity Recognition',
    description='Extract named entities from text',
    label_config='''
    <View>
      <Text name="text" value="$text"/>
      <Labels name="label" toName="text">
        <Label value="PERSON" background="#FF0000"/>
        <Label value="ORG" background="#00FF00"/>
        <Label value="LOC" background="#0000FF"/>
        <Label value="MISC" background="#FFFF00"/>
      </Labels>
    </View>
    '''
)
```

#### Custom Templates

```xml
<!-- Multi-Task Config (Classification + Bounding Box) -->
<View>
  <Image name="image" value="$image"/>

  <!-- Classification -->
  <Choices name="category" toName="image">
    <Choice value="Indoor"/>
    <Choice value="Outdoor"/>
    <Choice value="Mixed"/>
  </Choices>

  <!-- Object Detection -->
  <RectangleLabels name="objects" toName="image" strokeWidth="3">
    <Label value="Person" background="#FF0000"/>
    <Label value="Car" background="#00FF00"/>
  </RectangleLabels>

  <!-- Attributes -->
  <Taxonomy name="attributes" toName="objects">
    <Choice value="Occluded"/>
    <Choice value="Truncated"/>
    <Choice value="Crowded"/>
  </Taxonomy>
</View>

<Header value="Multi-Task Annotation"/>
```

```xml
<!-- Video Annotation Config -->
<View>
  <Video name="video" value="$video"/>
  <RectangleLabels name="label" toName="video" strokeWidth="3">
    <Label value="Person" background="#FF0000"/>
    <Label value="Car" background="#00FF00"/>
  </RectangleLabels>
  <Keyframe name="keyframe" toName="video"/>
</View>

<Header value="Video Annotation"/>
```

```xml
<!-- Audio Classification Config -->
<View>
  <Audio name="audio" value="$audio"/>
  <Choices name="label" toName="audio">
    <Choice value="Speech"/>
    <Choice value="Music"/>
    <Choice value="Noise"/>
    <Choice value="Other"/>
  </Choices>
</View>

<Header value="Audio Classification"/>
```

### Data Import/Export

#### Import Data

```python
# Import images
project.import_tasks(
    'path/to/images/',
    format='image_dir',
    label_config='label_config.xml'
)

# Import from JSON
tasks = [
    {
        'image': 'http://example.com/image1.jpg',
        'text': 'Sample text 1'
    },
    {
        'image': 'http://example.com/image2.jpg',
        'text': 'Sample text 2'
    }
]

project.import_tasks(tasks)

# Import from CSV
project.import_tasks(
    'data.csv',
    column_mapping={
        'image_url': 'image',
        'description': 'text'
    }
)

# Import with pre-annotations
tasks_with_predictions = [
    {
        'image': 'image1.jpg',
        'predictions': [
            {
                'result': [
                    {
                        'from_name': 'label',
                        'to_name': 'image',
                        'type': 'choices',
                        'value': {'choices': ['Cat']}
                    }
                ],
                'model_version': 'v1.0'
            }
        ]
    }
]

project.import_tasks(tasks_with_predictions)
```

#### Export Data

```python
# Export as JSON
export = project.export_tasks(
    export_type='JSON',
    download_all_tasks=True,
    download_resources=True
)

# Export as COCO format
export = project.export_tasks(
    export_type='COCO',
    download_all_tasks=True
)

# Export as YOLO format
export = project.export_tasks(
    export_type='YOLO',
    download_all_tasks=True
)

# Export as CSV
export = project.export_tasks(
    export_type='CSV',
    download_all_tasks=True
)

# Export only completed tasks
export = project.export_tasks(
    export_type='JSON',
    only_finished=True
)

# Save to file
import json
with open('export.json', 'w') as f:
    json.dump(export, f)
```

### Labeling Interface Customization

#### Custom CSS

```xml
<View style="background-color: #f0f0f0;">
  <Header value="Custom Styling" style="font-size: 24px; color: #333;"/>
  <Image name="image" value="$image" style="max-height: 600px;"/>
  <Choices name="label" toName="image" style="display: flex; gap: 10px;">
    <Choice value="Yes" style="background-color: #4CAF50; color: white; padding: 10px;"/>
    <Choice value="No" style="background-color: #f44336; color: white; padding: 10px;"/>
  </Choices>
</View>
```

#### Hotkeys

```xml
<View>
  <Header value="Use hotkeys: 1=Cat, 2=Dog, 3=Bird, 4=Other"/>
  <Image name="image" value="$image"/>
  <Choices name="label" toName="image">
    <Choice value="Cat" hotkey="1"/>
    <Choice value="Dog" hotkey="2"/>
    <Choice value="Bird" hotkey="3"/>
    <Choice value="Other" hotkey="4"/>
  </Choices>
</View>
```

#### Conditional Logic

```xml
<View>
  <Image name="image" value="$image"/>
  <Choices name="has_object" toName="image">
    <Choice value="Yes"/>
    <Choice value="No"/>
  </Choices>

  <Condition name="cond" when="has_object" equal="Yes">
    <RectangleLabels name="object_label" toName="image">
      <Label value="Person"/>
      <Label value="Car"/>
    </RectangleLabels>
  </Condition>
</View>
```

### User Management

```python
# Create user
user = client.create_user(
    email='user@example.com',
    username='newuser',
    password='password123',
    first_name='John',
    last_name='Doe'
)

# List users
users = client.get_users()
for user in users:
    print(f"{user.username}: {user.email}")

# Update user
user = client.update_user(
    user_id=1,
    first_name='Jane'
)

# Delete user
client.delete_user(user_id=1)

# Assign user to project
project.add_member(user_id=1, role='Annotator')

# Remove user from project
project.delete_member(user_id=1)
```

### Quality Control

#### Review Workflow

```python
# Enable review workflow
project.update_settings({
    'review_mode': True,
    'review_percentage': 0.1  # Review 10% of tasks
})

# Create review project
review_project = client.create_project(
    title='Review Project',
    description='Review annotations',
    source_project_id=project.id
)

# Get review tasks
review_tasks = review_project.get_tasks()

# Approve review
review_task = review_tasks[0]
review_task.update_annotations(
    {
        'result': review_task.annotations[0]['result'],
        'was_cancelled': False
    }
)
```

#### Consensus

```python
# Enable consensus
project.update_settings({
    'consensus_type': 'majority_vote',
    'consensus_number_of_annotators': 3  # 3 annotators per task
})

# Get consensus results
consensus_results = project.get_predictions(
    only_ground_truth=True
)
```

### ML Backend Integration

#### Pre-annotation Setup

```python
# ML backend server (Flask example)
from flask import Flask, request, jsonify
import torch
from transformers import pipeline

app = Flask(__name__)

# Load model
classifier = pipeline("image-classification", model="google/vit-base-patch16-224")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    image_url = data['data']['image']

    # Get prediction
    result = classifier(image_url)

    # Format for Label Studio
    predictions = [{
        'result': [{
            'from_name': 'label',
            'to_name': 'image',
            'type': 'choices',
            'value': {
                'choices': [result[0]['label']]
            },
            'score': result[0]['score']
        }],
        'model_version': 'v1.0'
    }]

    return jsonify(predictions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
```

```python
# Connect ML backend to project
project.connect_ml_backend(
    url='http://localhost:9090',
    model_version='v1.0'
)
```

#### Active Learning

```python
# Active learning with uncertainty sampling
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    image_url = data['data']['image']

    # Get prediction with probabilities
    result = classifier(image_url, top_k=5)

    # Calculate uncertainty (entropy)
    probs = [r['score'] for r in result]
    uncertainty = -sum(p * np.log(p) for p in probs if p > 0)

    predictions = [{
        'result': [{
            'from_name': 'label',
            'to_name': 'image',
            'type': 'choices',
            'value': {
                'choices': [result[0]['label']]
            },
            'score': result[0]['score']
        }],
        'model_version': 'v1.0',
        'score': uncertainty  # For active learning
    }]

    return jsonify(predictions)
```

### API Usage

#### Project Management

```python
from label_studio_sdk import Client

# Initialize client
client = Client(
    url='http://localhost:8080',
    api_key='your-api-key'
)

# Create project
project = client.create_project(
    title='My Project',
    description='Project description',
    label_config='<View>...</View>'
)

# Get project
project = client.get_project(project_id=1)

# List projects
projects = client.get_projects()

# Update project
project.update(
    title='Updated Title',
    description='Updated description'
)

# Delete project
client.delete_project(project_id=1)
```

#### Task Management

```python
# Create tasks
tasks = [
    {'data': {'image': 'http://example.com/image1.jpg'}},
    {'data': {'image': 'http://example.com/image2.jpg'}}
]
project.import_tasks(tasks)

# Get tasks
tasks = project.get_tasks()

# Get specific task
task = project.get_task(task_id=1)

# Update task
task.update({
    'data': {'image': 'http://example.com/new_image.jpg'}
})

# Delete task
task.delete()

# Search tasks
tasks = project.get_tasks(
    filter={
        'task': 'search query',
        'completion_percentage': 50
    }
)
```

#### Annotation Management

```python
# Get annotations for task
task = project.get_task(task_id=1)
annotations = task.get_annotations()

# Create annotation
annotation = task.create_annotation(
    result=[{
        'from_name': 'label',
        'to_name': 'image',
        'type': 'choices',
        'value': {'choices': ['Cat']}
    }]
)

# Update annotation
annotation.update(
    result=[{
        'from_name': 'label',
        'to_name': 'image',
        'type': 'choices',
        'value': {'choices': ['Dog']}
    }]
)

# Delete annotation
annotation.delete()
```

### Backup and Migration

#### Backup

```bash
# Backup database
docker exec label-studio pg_dump -U labelstudio labelstudio > backup.sql

# Backup media files
docker cp label-studio:/label-studio/data/media ./backup/media

# Backup with Docker Compose
docker-compose exec postgres pg_dump -U labelstudio labelstudio > backup.sql
```

```python
# Export all project data
projects = client.get_projects()

for project in projects:
    export = project.export_tasks(
        export_type='JSON',
        download_all_tasks=True,
        download_resources=True
    )

    # Save to file
    filename = f"backup_project_{project.id}.json"
    with open(filename, 'w') as f:
        json.dump(export, f)
```

#### Migration

```python
# Migrate to new instance
old_client = Client(url='http://old-server:8080', api_key='old-key')
new_client = Client(url='http://new-server:8080', api_key='new-key')

# Get projects from old instance
old_projects = old_client.get_projects()

# Migrate each project
for old_project in old_projects:
    # Create new project
    new_project = new_client.create_project(
        title=old_project.title,
        description=old_project.description,
        label_config=old_project.label_config
    )

    # Export tasks from old project
    tasks = old_project.get_tasks()
    task_data = [{'data': t.data} for t in tasks]

    # Import to new project
    new_project.import_tasks(task_data)
```

### Production Deployment

#### Nginx Reverse Proxy

```nginx
# /etc/nginx/sites-available/label-studio
server {
    listen 80;
    server_name label-studio.example.com;

    client_max_body_size 100M;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /label-studio/data/static/;
    }
}
```

#### SSL Configuration

```nginx
server {
    listen 443 ssl http2;
    server_name label-studio.example.com;

    ssl_certificate /etc/ssl/certs/label-studio.crt;
    ssl_certificate_key /etc/ssl/private/label-studio.key;

    client_max_body_size 100M;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    server {
        listen 80;
        server_name label-studio.example.com;
        return 301 https://$server_name$request_uri;
    }
}
```

#### Systemd Service

```ini
# /etc/systemd/system/label-studio.service
[Unit]
Description=Label Studio
After=network.target

[Service]
Type=simple
User=labelstudio
WorkingDirectory=/home/labelstudio
ExecStart=/home/labelstudio/venv/bin/label-studio start --port 8080
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable label-studio
sudo systemctl start label-studio
sudo systemctl status label-studio
```

## Best Practices

1. **Project Organization**
   - Use consistent naming conventions
   - Create descriptive project titles
   - Organize projects by task type
   - Use proper labeling guidelines

2. **Quality Assurance**
   - Enable review workflow for critical tasks
   - Use consensus for high-stakes annotations
   - Implement quality metrics
   - Provide clear annotation guidelines

3. **Performance Optimization**
   - Use pagination for large datasets
   - Implement async operations for imports
   - Optimize image loading and serving
   - Use CDN for media assets

4. **Security**
   - Use strong passwords and API keys
   - Enable SSL/TLS for production
   - Implement proper authentication
   - Regularly update dependencies

5. **Backup Strategy**
   - Regular database backups
   - Export project data periodically
   - Test restore procedures
   - Store backups securely

6. **User Management**
   - Create appropriate user roles
   - Assign users to relevant projects
   - Monitor user activity
   - Remove inactive users

7. **ML Integration**
   - Use pre-annotation to speed up labeling
   - Implement active learning for efficiency
   - Monitor model performance
   - Update models regularly

8. **Documentation**
   - Document labeling guidelines
   - Create annotation examples
   - Maintain project documentation
   - Share knowledge with team

9. **Monitoring**
   - Track annotation progress
   - Monitor system performance
   - Set up alerts for issues
   - Review quality metrics

10. **Scalability**
    - Use appropriate hardware
    - Implement load balancing
    - Optimize database queries
    - Plan for growth

## Related Skills

- [`05-ai-ml-core/data-augmentation`](05-ai-ml-core/data-augmentation/SKILL.md)
- [`05-ai-ml-core/data-preprocessing`](05-ai-ml-core/data-preprocessing/SKILL.md)
- [`05-ai-ml-core/model-training`](05-ai-ml-core/model-training/SKILL.md)
- [`07-document-processing/document-parsing`](07-document-processing/document-parsing/SKILL.md)
- [`06-ai-ml-production/llm-integration`](06-ai-ml-production/llm-integration/SKILL.md)
