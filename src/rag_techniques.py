import numpy as np
from sentence_transformers import CrossEncoder


def naive_rag(collection, query, client, generate_final_answer):
    """
    Performs the naive RAG technique.

    Args:
        collection: The ChromaDB collection instance.
        query (str): The original user query.
        client: The OpenAI client instance.
        generate_final_answer: Function to generate the final answer.

    Returns:
        str: The final answer using Naive RAG.
    """
    results = collection.query(query_texts=[query], n_results=5)
    retrieved_documents = results["documents"][0]
    context = "\n\n".join(retrieved_documents)
    response = generate_final_answer(query, client, context)
    return response


def expansion_answer_rag(collection, query, client, generate_hallucinated_answer, generate_final_answer):
    """
    Performs the expansion answer technique.

    Args:
        collection: The ChromaDB collection instance.
        query (str): The original user query.
        client: The OpenAI client instance.
        generate_hallucinated_answer: Function to generate a hallucinated answer.
        generate_final_answer: Function to generate the final answer.

    Returns:
        str: The final answer using expansion answer technique.
    """
    hypothetical_answer = generate_hallucinated_answer(query, client)
    joint_query = f"{query} {hypothetical_answer}"

    results = collection.query(query_texts=joint_query, n_results=5, include=["documents", "embeddings"])
    retrieved_documents = results["documents"][0]
    context = "\n\n".join(retrieved_documents)
    response = generate_final_answer(query, client, context)
    return response, hypothetical_answer


def expansion_queries_rag(collection, query, client, generate_related_queries, generate_final_answer):
    """
    Performs the expansion queries technique.

    Args:
        collection: The ChromaDB collection instance.
        query (str): The original user query.
        client: The OpenAI client instance.
        generate_related_queries: Function to generate related queries.
        generate_final_answer: Function to generate the final answer.

    Returns:
        str: The final answer using Expansion Queries.
    """
    related_queries = generate_related_queries(query, client)
    joint_query = [query] + related_queries

    results = collection.query(query_texts=joint_query, n_results=5, include=["documents", "embeddings"])
    retrieved_documents = results["documents"]

    # Deduplicate documents
    unique_documents = deduplicate_documents(retrieved_documents)

    context = "\n\n".join(unique_documents)
    response = generate_final_answer(query, client, context)

    return response, related_queries


def reranking_rag(collection, query, related_queries, client, generate_final_answer):
    """
    Performs the reranking and expansion queries techniques.

    Args:
        collection: The ChromaDB collection instance.
        query (str): The original user query.
        client: The OpenAI client instance.
        generate_related_queries: Function to generate related queries.
        generate_final_answer: Function to generate the final answer.

    Returns:
        str: The final answer using Expansion Queries.
    """
    joint_query = [query] + related_queries

    results = collection.query(query_texts=joint_query, n_results=10, include=["documents", "embeddings"])
    retrieved_documents = results["documents"]
    unique_documents = deduplicate_documents(retrieved_documents)

    pairs = []
    for doc in unique_documents:
        pairs.append([query, doc])

    cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    scores = cross_encoder.predict(pairs)

    # Take top 5 chunks with highest scores
    top_indices = np.argsort(scores)[::-1][:5]
    top_documents = [unique_documents[i] for i in top_indices]

    # Concatenate the top documents into a single context
    context = "\n\n".join(top_documents)

    # Generate final answer
    response = generate_final_answer(query, client, context)

    return response, top_documents


def deduplicate_documents(documents_list):
    """
    Deduplicates and flattens a list of document lists.

    Args:
        documents_list (list of lists): A list of lists of documents.

    Returns:
        list: A deduplicated, flattened list of documents.
    """
    unique_documents = set()
    for documents in documents_list:
        for document in documents:
            unique_documents.add(document)
    return list(unique_documents)