---
name: bookstrap-init
description: Initialize a new book project by creating a Book Requirements Document (BRD) through guided questions
argument-hint: <book concept>
allowed-tools:
  - Bash(*)
  - Read
  - Write
  - AskUserQuestion
  - TaskCreate
---

# Initialize Book Project

Set up a new book project by creating a comprehensive Book Requirements Document (BRD).

## Book Concept

The user wants to write: **$ARGUMENTS**

## Workflow

This command delegates to the `brd-creator` agent to guide the user through BRD creation via structured questions.

### Step 1: Check Prerequisites

First, verify that SurrealDB is running and accessible:

```bash
# Check if SurrealDB container is running
if docker ps | grep -q bookstrap-db; then
  echo "SurrealDB is running"
else
  echo "SurrealDB_NOT_RUNNING"
fi
```

If SurrealDB is not running, start it:

```bash
# Start SurrealDB via docker-compose
docker-compose up -d
```

Wait a few seconds for the database to be ready:

```bash
sleep 3
```

### Step 2: Initialize Schema

Run the schema initialization script:

```bash
./scripts/init-schema.sh
```

This creates all necessary tables, fields, and indexes in SurrealDB.

### Step 3: Delegate to BRD Creator

The `brd-creator` agent will guide the user through creating the BRD by asking structured questions about:

1. **Core Details**: Title, genre, word count target, audience
2. **Thesis/Premise**: One-sentence summary, core argument, reader takeaway
3. **Structure**: Format, POV, tense, timeline approach
4. **Voice**: Tone, comparable titles, sample passage
5. **Characters/Concepts**: Key figures with descriptions and relationships
6. **Research Sources**: Primary sources, secondary sources, URLs for ingestion
7. **Constraints**: Must include, must avoid, sensitivity considerations

The agent will:
- Ask one question at a time
- Wait for user responses
- Generate a comprehensive `BRD.md` file
- Store the BRD content in the SurrealDB `brd` table

### Step 4: Create Project Structure

After the BRD is created, set up the initial project structure:

```bash
# Create directories
mkdir -p manuscript
mkdir -p research
mkdir -p logs
mkdir -p data

# Create .gitignore if it doesn't exist
if [ ! -f .gitignore ]; then
  cat > .gitignore << 'EOF'
# Environment
.env

# Database
data/

# Logs
logs/

# OS
.DS_Store
Thumbs.db

# Editor
.vscode/
.idea/
EOF
fi
```

### Step 5: Create Configuration

If `bookstrap.config.json` doesn't exist, copy from template:

```bash
if [ ! -f bookstrap.config.json ]; then
  cp templates/bookstrap.config.json bookstrap.config.json
fi
```

### Step 6: Verify Environment

Check that required environment variables are set:

```bash
# Check for embedding provider API key
if [ -f .env ]; then
  source .env
  if [ -z "$GEMINI_API_KEY" ] && [ -z "$OPENAI_API_KEY" ]; then
    echo "WARNING: No embedding API key found. Set GEMINI_API_KEY or OPENAI_API_KEY in .env"
  fi
else
  echo "NOTE: Create a .env file and add your API keys (see .env.example)"
fi
```

## After Initialization

Return a summary including:
- BRD location and version
- Database status (running, schema initialized)
- Project directories created
- Configuration file status
- Next steps: `/bookstrap-ingest` to load research materials

## Notes

- The BRD can be edited later and re-ingested into the database
- The initial book concept can be as simple or detailed as desired
- The agent will ask clarifying questions to fill in any gaps
- All answers can be refined during the question process
