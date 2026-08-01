---
name: ai-agent-skills-raia-ai-raia-v2-docs
description: The retriever skill is a mechanism that allows the system (an agent)
  to fetch contextual information from an external vector database, such as Pinecone,
  in real time. The retrieved data is then passed to OpenAI's models as additional
  context, enhancing the accuracy and specificity of the AI's responses.
---

# Retrieval Skill

### 🧠 What Is the Retriever Skill?

The **retriever skill** is a mechanism that allows the system (an agent) to fetch contextual information from an **external vector database**, such as Pinecone, in real time. The retrieved data is then passed to OpenAI's models as **additional context**, enhancing the accuracy and specificity of the AI's responses.

Illya describes this as an industry-standard approach for augmenting language models with external knowledge.

***

### 🔄 Retrieval Flow

1. **Agent Sends Message**
   * When a user sends a message to an agent, the system checks whether the agent has any external retrievers configured.
2. **Query External Vector DB**
   * If retrievers are present, the system makes a **search query** to the external database (e.g., Pinecone), using the user's message as the query.
3. **Attach Retrieved Content**
   * The system retrieves relevant documents or embeddings from the vector DB and **attaches them as context** for the OpenAI API call.
4. **Generate Answer**
   * OpenAI uses both the user's query and the attached context to generate a more accurate response.

***

### 🧩 Key Fields and Configurations

When a user adds a retriever skill, they go through a configuration form with the following fields:

#### 1. **Retriever Type**

* Currently supports **Pinecone**, but is designed to support others (e.g., Weaviate, PostgreSQL with pgvector, APIs).
* Future plans include support for **non-vector retrievers** (e.g., SQL-based or API-based lookups).

#### 2. **Name**

* A label for the retriever setup (e.g., “Sales Docs Retriever”).

#### 3. **API Key**

* The user's Pinecone API key is required to fetch data.
* Used to call Pinecone’s API and list all available **indexes**.

#### 4. **Index Selection**

* The system auto-fetches available **indexes** once the API key is verified.
* An **index** in Pinecone is equivalent to a **vector database**.

#### 5. **Namespace**

* Namespaces act like **tables** within the vector DB.
* Each namespace is isolated and must be explicitly selected.
* Required for querying Pinecone.

#### 6. **Field Name**

* Used to configure how data is chunked or presented (may relate to how metadata is tagged or retrieved).

#### 7. **Top-K**

* The number of top results (most relevant chunks) to return from the query.
* Controls the depth of context fed to OpenAI.

***

### 🗂 Data Hierarchy in Pinecone (as explained)

| Concept   | Pinecone Equivalent |
| --------- | ------------------- |
| Index     | Database            |
| Namespace | Table               |
| Embedding | Row/document        |

Multiple namespaces can exist within a single index, and multiple indexes can be used by a single customer, depending on use cases (e.g., file search vs text search with different embedding dimensions).

***

### 🛠 Feedback Management + Vector Store Upload Logic

In parallel, the team also updated how **feedback data** is managed and used in vector stores:

* **Daily Generation**: A feedback file is created daily per agent if new feedback exists.
* **Skip Re-upload Logic**: If a file is deleted from the vector store manually, it’s marked as such and **not re-uploaded** automatically.
* **Goal**: Avoid polluting the vector DB with unwanted feedback and give admins fine control over what training data is stored.

#### Future Plan:

* A **skill UI** is planned to show all feedbacks.
* Admins will be able to **view, edit, delete**, or **flag to ignore** feedback directly—rather than navigating Copilot manually.

***

### ✅ Key Benefits of the Retriever Skill

* Supports **external knowledge injection** dynamically.
* Enables **flexible customer-specific indexing** (multi-index and multi-namespace setups).
* Integrates seamlessly with OpenAI for contextual grounding.
* Future extensible to support API retrievers and traditional databases.
