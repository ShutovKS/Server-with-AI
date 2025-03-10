# Server with AI Agent

[Русский](./README.md) | [English](./README.en.md)

## Description

Server with an AI agent powered by a LLM (Large Language Model).  
The models have access to various tools:

- Internet search
- Wikipedia search
- RAG with database access

## Installation

Clone the repository and install the dependencies:

```bash
git clone <repo>
cd <repo>
pip install -r requirements.txt
```

Place your .txt files containing texts for the RAG knowledge base into the `data` folder.

## Running

To start the server, execute:

```bash
python main.py
```

To rebuild the database, run:

```bash
python ./app/engine/generate.py
```

## Usage

After starting the server, send POST requests to `http://127.0.0.1:8000/api/`

Request the AI in chat format, with access to the database and tools:

```bash
curl -X POST "http://127.0.0.1:8000/api/chat/request" -H "accept: application/json" -H "Content-Type: application/json" -d '{"messages":[{"role":"user","content":"What are the consequences for someone who steals intellectual property?"}]}'
```

Request the AI:

```bash
curl -X POST "http://127.0.0.1:8000/api/query/complete" -H "Content-Type: application/json" -d '{"query": "What are the consequences for someone who steals intellectual property?"}'
```

Request the AI with database access:

```bash
curl -X POST "http://127.0.0.1:8000/api/query/request-to-stored-index" -H "Content-Type: application/json" -d '{"query": "What are the consequences for someone who steals intellectual property?"}'
```

Request the AI with database and tools access:

```bash
curl -X POST "http://127.0.0.1:8000/api/query/request-agent" -H "Content-Type: application/json" -d '{"query": "What are the consequences for someone who steals intellectual property?"}'
```