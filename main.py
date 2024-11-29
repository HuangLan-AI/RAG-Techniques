import os
from datetime import datetime
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
    expansion_queries_rag,
    reranking_rag
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
    res_exp_ans, hypothetical_answer = expansion_answer_rag(collection, original_query, client, generate_hallucinated_answer, generate_final_answer)

    # Performe expansion queries technique
    res_exp_que, related_queries = expansion_queries_rag(collection, original_query, client, generate_related_queries, generate_final_answer)

    # Performe reranking & expansion queries technique
    res_rerank, top_documents = reranking_rag(collection, original_query, related_queries, client, generate_final_answer)

    # Generate timestamp for the file name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file_path = os.path.join("results", f"result_{timestamp}.txt")

    # Write results to the text file
    with open(results_file_path, "w", encoding="utf-8") as file:
        file.write("Original Query:\n")
        file.write(original_query)
        file.write("\n\n")

        file.write("Final Answer of Naive RAG:\n")
        file.write("\n".join(res_naive))
        file.write("\n\n")

        file.write("Final Answer of Expansion Answer:\n")
        file.write("\n".join(res_exp_ans))
        file.write("\n\n")

        file.write("Final Answer of Expansion Queries:\n")
        file.write("\n".join(res_exp_que))
        file.write("\n\n")

        file.write("Hypothetical Answer:\n")
        file.write("".join(hypothetical_answer))
        file.write("\n\n")

        file.write("Related Queries:\n")
        file.write("\n".join(related_queries))
        file.write("\n\n")

        file.write("Top Documents (Reranked):\n")
        file.write("\n".join(top_documents))

    # Print a success message
    print(f"Results have been saved to {results_file_path}")


if __name__ == "__main__":
    main()