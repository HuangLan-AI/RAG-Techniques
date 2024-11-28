import os
from dotenv import load_dotenv
from openai import OpenAI
from src.utilities import (
    load_pdf_texts,
    split_text_character_based,
    split_text_token_based,
    create_chroma_collection,
    add_documents_to_collection,
    generate_hallucinated_answer,
    generate_related_queries,
    generate_final_answer
)
from src.rag_techniques import (
    naive_rag,
    expansion_answer_rag,
    expansion_queries_rag
)

def main():
    # Load environment variables from .env file
    load_dotenv()
    my_openai_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=my_openai_key)

    # Read texts from PDF file
    file_name = "The Goldfish Story.pdf"
    pdf_texts = load_pdf_texts(file_name)

    # Split texts into chunks
    character_chunks = split_text_character_based(pdf_texts)
    token_chunks = split_text_token_based(character_chunks)

    # Create Embeddings and Store in Chromadb
    collection_name = "goldfish_collection"
    collection = create_chroma_collection(collection_name=collection_name)
    add_documents_to_collection(collection, token_chunks)

    # Set the original query
    original_query = "How the goldfish die?"

    # Performe naive RAG
    res_naive = naive_rag(collection, original_query, client, generate_final_answer)

    # Performe expansion answer technique
    res_exp_ans = expansion_answer_rag(collection, original_query, client, generate_hallucinated_answer, generate_final_answer)

    # Performe expansion queries technique
    res_exp_que = expansion_queries_rag(collection, original_query, client, generate_related_queries, generate_final_answer)

    print("Final Answer of Navive RAG:")
    print(res_naive)
    print("=================================")
    print("Final Answer of Expansion Answer:")
    print(res_exp_ans)
    print("=================================")
    print("Final Answer of Expansion Queries:")
    print(res_exp_que)


if __name__ == "__main__":
    main()