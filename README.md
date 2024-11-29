# RAG Techniques
A Python-based project that implements Retrieval-Augmented Generation (RAG) techniques using multiple PDFs as knowledge sources. The project demonstrates and compares various RAG strategies, including Naive RAG, Expansion Answer, Expansion Queries, and Reranking Queries, leveraging LangChain, ChromaDB, and OpenAI APIs.

## Features
- **Naive RAG**: Retrieves relevant document chunks and answers queries using embeddings.
- **Expansion Answer**: Expands the query with a hypothetical answer to improve retrieval.
- **Expansion Queries**: Generates multiple related queries to enhance document retrieval.
- **Reranking**: Ranks retrieved documents using a cross-encoder for more accurate results.
- Supports processing multiple PDFs from a specified directory.

