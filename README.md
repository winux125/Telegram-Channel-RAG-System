# Durov RAG System

This project is a Retrieval-Augmented Generation (RAG) application that allows you to semantically search and interact with messages from Pavel Durov's Telegram channel. 

It uses **Qdrant** as the vector database, **SentenceTransformers** (`BAAI/bge-m3`) for local message embeddings, and an OpenAI-compatible API to generate in-context answers based on the retrieved Telegram posts.

---

## Features

- **Semantic Search**: Uses the powerful BGE-M3 model to embed and search Telegram messages.
- **Vector Database**: Connects to a local Qdrant instance for fast and scalable vector retrieval.
- **RAG Generation**: passes context to an LLM using an OpenAI-compatible endpoint.
- **JSON Data Processing**: Automatically reads Telegram chat histories exported to a formatted `result.json` file.

## Prerequisites

To run this project, you need:
- **Python 3.12+**
- **Docker** (to run the local Qdrant container)
- An exported Telegram chat history saved as `result.json` in the root folder.
- An API Key from an LLM provider compatible with the OpenAi Python Client.

## Setup & Installation

**1. Clone the repository**

```bash
git clone https://github.com/winux125/Telegram-Channel-RAG-System
cd Telegram-Channel-RAG-System
```

**2. Install Dependencies**

Since this project uses `uv` for package management, simply run:

```bash
uv sync
```

Alternatively, use `pip`:

```bash
pip install python-dotenv openai qdrant-client sentence-transformers torch
```

**3. Configure Environment Variables**

Create a `.env` file in the root of your directory with the following variables:

```env
API_KEY_LLM=your_api_key_here
BASE_URL_LLM=https://api.your-provider.com/v1
```

By default, the script targets the model `z-ai/glm-4.5-air:free`. Make sure your LLM provider supports this model name, or modify the `main.py` script to use a different model.

**4. Start Qdrant Database**

Spin up a local Qdrant instance via Docker:

```bash
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```

**5. Add your Data**

Export the Telegram channel chat history (in JSON format) and name it `result.json`. Place it in the root directory.

## Usage

Simply run the main script. If the Qdrant collection doesn't exist, it will automatically embed all the messages from `result.json` and upload them to your Qdrant instance.

```bash
python main.py
```

Currently, the script performs a test search and query: `"telegram is the most downloaded"`. You can modify the `main()` function in `main.py` to prompt the LLM with your custom queries.

## Project Structure

- `main.py`: The entrypoint of the application. Contains the RAG pipeline, embedding pipeline, and the vector storage configurations.
- `pyproject.toml` / `uv.lock`: Dependency definitions and locks.
- `.env`: (Not tracked) Holds confidential API keys entirely locally.
- `result.json`: (Not tracked) Holds the exported message chunks to feed into the Qdrant database.
