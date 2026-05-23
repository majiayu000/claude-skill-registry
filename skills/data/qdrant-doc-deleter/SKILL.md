---
name: qdrant-doc-deleter
description: Deletes specific PDF documents from Qdrant vector database collection. Use when user wants to remove, delete, or clean up PDF documents from the vector database, Qdrant collection, or needs to manage document versions.
---

# Qdrant Document Deleter

This skill helps users delete specific PDF documents from the Qdrant vector database collection using the existing `UTIL/delete_documents.py` script.

## When to Use This Skill

Activate this skill automatically when the user:
- Wants to delete/remove PDF documents from Qdrant
- Needs to clean up old document versions (e.g., 2024 vs 2025)
- Asks to remove specific documents from the vector database
- Wants to manage or prune the Qdrant collection
- Uses keywords like "delete documents", "remove from Qdrant", "clean up PDFs"

## How to Use

### Step 1: Identify Documents to Delete

Ask the user which documents they want to delete. Documents should be specified by their PDF filename (e.g., `document-name.pdf`).

### Step 2: Review the Script

Read `UTIL/delete_documents.py` to check the current `DOCUMENTS_TO_DELETE` list:

```python
DOCUMENTS_TO_DELETE = [
    'file1.pdf',
    'file2.pdf',
    # ...
]
```

### Step 3: Update the Document List

Edit the `DOCUMENTS_TO_DELETE` list in the script to include the documents the user wants to delete:

```python
from Edit import Edit

Edit(
    file_path='/home/tromanow/COHORT/TX/UTIL/delete_documents.py',
    old_string='DOCUMENTS_TO_DELETE = [\n    # Current list...\n]',
    new_string='DOCUMENTS_TO_DELETE = [\n    # Documents to delete\n    "document1.pdf",\n    "document2.pdf",\n]'
)
```

### Step 4: Explain the Process to the User

Before running, explain:
- How many documents will be deleted
- What the script does (searches for chunks with matching filename)
- That it requires confirmation (user must type "yes")
- That deletion is permanent

### Step 5: Run the Script

Execute the deletion script:

```bash
cd UTIL
python delete_documents.py
```

The script will:
1. Display the documents to be deleted
2. Ask for confirmation ("yes" to proceed)
3. Scroll through all chunks in the collection
4. Delete chunks where `filename` matches the document names
5. Show deletion statistics

### Step 6: Report Results

After execution, summarize:
- Number of documents processed
- Number of chunks deleted per document
- Any errors or warnings
- Total chunks removed from the collection

## Key Features of the Script

### Safety Features
- **Confirmation required**: User must type "yes" to proceed
- **Detailed logging**: Shows progress for each document
- **Error handling**: Continues processing even if one document fails
- **Statistics**: Reports exact number of chunks deleted

### How It Works
1. **Scroll through collection**: Uses Qdrant's scroll API to iterate through all points
2. **Filter by filename**: Checks each chunk's `filename` field in payload
3. **Batch delete**: Collects all matching point IDs and deletes them
4. **No reloading needed**: Surgically removes specific documents without affecting others

### Configuration
The script uses settings from `LOAD_DB/config.py`:
- `QDRANT_COLLECTION_NAME_CONTEXTUAL`: The collection to delete from
- `QDRANT_API_URL`: Qdrant server URL
- `QDRANT_API_KEY`: API key for authentication

## Example Workflow

### Example 1: Delete Outdated 2024 Documents

```
User: "I need to delete the 2024 versions of the payment rate PDFs"

Claude: I'll help you delete the 2024 payment rate documents from Qdrant.

Based on the existing script, I can see there are 2024 documents listed. Let me update the script to delete:
- wd-24-23-att1-twc.pdf
- acf-218-qpr-ffy-2024-for-texas.pdf
- texas-early-learning-strategic-plan-2024-2026-final-accessible.pdf

[Updates DOCUMENTS_TO_DELETE list]

Now I'll run the deletion script. You'll need to confirm by typing "yes" when prompted.

[Runs script]

✓ Deleted 3 documents:
  - wd-24-23-att1-twc.pdf: 45 chunks
  - acf-218-qpr-ffy-2024-for-texas.pdf: 32 chunks
  - texas-early-learning-strategic-plan-2024-2026-final-accessible.pdf: 78 chunks

Total: 155 chunks removed from the collection.
```

### Example 2: Delete Specific Document

```
User: "Remove tx-ccdf-state-plan-ffy2025-2027-approved.pdf from the database"

Claude: I'll delete tx-ccdf-state-plan-ffy2025-2027-approved.pdf from the Qdrant collection.

[Updates script with single document]

Running deletion script...

✓ Deleted tx-ccdf-state-plan-ffy2025-2027-approved.pdf: 124 chunks removed
```

## Error Handling

### Document Not Found
If a document has 0 chunks deleted:
- Explain that the document wasn't found in the collection
- Suggest checking the filename spelling
- Offer to verify collection contents with `verify_qdrant.py`

### Deletion Errors
If deletion fails for a document:
- Report the error message
- Continue with remaining documents
- Suggest checking Qdrant connection/credentials

### No Confirmation
If user doesn't type "yes":
- Script exits safely
- No changes made to collection

## Advanced Usage

### Verify Before Deleting

Before deletion, check if documents exist:

```bash
cd LOAD_DB
python verify_qdrant.py
```

This shows all documents and chunk counts in the collection.

### Check Specific Document

To find chunks for a specific document before deleting, you can use the retriever:

```python
# Search for chunks from a specific document
from chatbot.retriever import Retriever
retriever = Retriever()
# Use scroll API to filter by filename
```

## Notes

- **Permanent deletion**: There's no undo - chunks are permanently removed
- **Collection name**: Defaults to `QDRANT_COLLECTION_NAME_CONTEXTUAL` from config
- **Filename matching**: Exact match on the `filename` field in chunk payload
- **Batch processing**: Processes in batches of 100 for efficiency
- **Independent operation**: Doesn't affect other documents in the collection

## Related Tools

- `load_pdf_qdrant.py`: Load new documents to Qdrant
- `verify_qdrant.py`: Verify collection contents and statistics
- `reload_single_pdf.py`: Reload a single PDF (delete + re-add)
