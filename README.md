# RAG Techniques
A Python-based project that implements Retrieval-Augmented Generation (RAG) techniques using multiple PDFs as knowledge sources. The project demonstrates and compares various RAG strategies, including Naive RAG, Expansion Answer, Expansion Queries, and Reranking Queries, leveraging LangChain, ChromaDB, and OpenAI APIs.

## Features
- **Naive RAG**: Retrieves relevant document chunks and answers queries using embeddings.
- **Expansion Answer**: Expands the query with a hypothetical answer to improve retrieval.
- **Expansion Queries**: Generates multiple related queries to enhance document retrieval.
- **Reranking**: Ranks retrieved documents using a cross-encoder for more accurate results.
- Supports processing multiple PDFs from a specified directory.

## Installation
### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- OpenAI API key

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/HuangLan-AI/RAG-Techniques.git
    cd RAG-Techniques
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv rag-venv
    source rag-venv/bin/activate  # On Windows: rag-venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your `.env` file: 
    Create a `.env` file in the project root with the following variables:
    ```bash
    OPENAI_API_KEY=<your_openai_api_key>
    PDF_DIRECTORY=data/goldfish
    COLLECTION_NAME=goldfish_collection
    ORIGINAL_QUERY="How the goldfish die?"
    ```

## Usage
1. Place your PDFs in the directory specified in the `.env` file (`PDF_DIRECTORY`).
2. Run the project:
    ```bash
    python main.py
    ```
3. Results will be saved in the `results/` directory with a timestamped file.

## License
This project is licensed under the MIT License. See the LICENSE file for details.


