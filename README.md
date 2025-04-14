# RAG Web Scraper

A Retrieval-Augmented Generation (RAG) web scraper built with Streamlit, LangChain, and Ollama that allows you to:

1. Enter any URL to crawl a webpage
2. Extract content and convert it to markdown
3. Split text into chunks and create embeddings
4. Ask questions about the webpage content
5. Get AI-generated answers based on the relevant context

## Features

- Simple web interface built with Streamlit
- Converts HTML to Markdown for better processing
- Uses LangChain with Ollama for local LLM integration
- In-memory vector store for quick retrieval
- Chat interface for questions and answers
- Context-aware responses from the AI

## Requirements

- Python 3.11+
- Ollama running locally with llama3.2 model installed

## Installation

```bash
# Install dependencies with Poetry
poetry install

# Or with pip
pip install -r requirements.txt
```

## Usage

1. Make sure Ollama is running locally with the llama3.2 model
2. Run the application:

```bash
poetry run streamlit run main.py
```

3. Enter a URL to crawl
4. Ask questions about the content
5. Clear chat history and reset index as needed

## How It Works

1. The application loads a webpage and converts HTML to markdown
2. Text is split into smaller chunks for processing
3. Chunks are embedded and stored in an in-memory vector store
4. When you ask a question, the system retrieves relevant chunks
5. The LLM generates an answer based on the retrieved context

## Credits

Created by Sascha Corti (sascha@corti.com)