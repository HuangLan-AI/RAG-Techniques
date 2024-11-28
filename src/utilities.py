import os
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from textwrap import dedent


# ------------------------------------
# Data Loading Functions
# ------------------------------------
def load_pdf_texts(file_name, directory="data"):
    """
    Reads and extracts text from a PDF file.

    Args:
        file_name (str): The name of the PDF file.
        directory (str): The directory containing the PDF file.

    Returns:
        list: A list of text strings, one for each page of the PDF.
    """
    file_path = os.path.join(directory, file_name)
    reader = PdfReader(file_path)
    pdf_texts = [page.extract_text().strip() for page in reader.pages]
    # Filter out empty strings
    return [text for text in pdf_texts if text]


# ------------------------------------
# Text Splitting Functions
# ------------------------------------
def split_text_character_based(texts, chunk_size=1000, chunk_overlap=0):
    """
    Splits texts into chunks using character-based splitting.
    """
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ". ", " ", ""], chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return splitter.split_text("\n\n".join(texts))


def split_text_token_based(texts, tokens_per_chunk=256, chunk_overlap=0):
    """
    Splits texts into chunks using token-based splitting.
    """
    splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=chunk_overlap, tokens_per_chunk=tokens_per_chunk)
    chunks = []
    for text in texts:
        chunks.extend(splitter.split_text(text))
    return chunks


# ------------------------------------
# Embedding Functions
# ------------------------------------
def create_chroma_collection(collection_name, embedding_model="all-MiniLM-L6-v2"):
    """
    Creates a ChromaDB collection for storing embeddings.
    """
    embedding_function = SentenceTransformerEmbeddingFunction(model_name=embedding_model)
    client = chromadb.Client()
    return client.create_collection(name=collection_name, embedding_function=embedding_function)


def add_documents_to_collection(collection, documents):
    """
    Adds documents to a ChromaDB collection.
    """
    ids = [str(i) for i in range(len(documents))]
    collection.add(ids=ids, documents=documents)


# ------------------------------------
# LLM Response Generation Functions
# ------------------------------------
def generate_hallucinated_answer(query, client, model="gpt-3.5-turbo"):
    """
    Generates a hallucinated answer for the given query using an LLM.
    """
    prompt = dedent("""
        You are an experienced and helpful academic researcher.
        Provide an example answer to the given question based on common sense in life,
        that might be found in a document or story. Keep your answer to one paragraph.
    """)
    messages = [{"role": "system", "content": prompt}, {"role": "user", "content": query}]
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content


def generate_related_queries(query, client, model="gpt-3.5-turbo"):
    """
    Generates related queries for the given query.
    """
    prompt = dedent("""
        You are a knowledgeable academic researcher.
        For the given question, propose up to five related questions to assist in finding relevant information.
        List each question on a separate line without numbering.
    """)
    messages = [{"role": "system", "content": prompt}, {"role": "user", "content": query}]
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content.split("\n")


def generate_final_answer(query, client, context, model="gpt-3.5-turbo"):
    """
    Generates the final answer based on the given query and context using an LLM.

    Args:
        query (str): The user query.
        client: The OpenAI client instance.
        context (str): The context to base the answer on.
        model (str): The name of the LLM model to use (default is "gpt-3.5-turbo").

    Returns:
        str or list: The final answer as a single string or a list of strings if split is True.
    """

    prompt = dedent("""
        You are a knowledgeable academic researcher.
        Your users are inquiring about a story. 
    """)

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"Based on the following context:\n\n{context}\n\nAnswer the query: '{query}'"},
    ]

    response = client.chat.completions.create(model=model, messages=messages)
    content = response.choices[0].message.content
    content = content.split("\n")
    return content