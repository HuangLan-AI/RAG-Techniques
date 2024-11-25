from helper_utils import word_wrap, project_embeddings
from pypdf import PdfReader
import os
from openai import OpenAI
from dotenv import load_dotenv

import numpy as np
import umap


# Load environment variables from .env file
load_dotenv()

my_openai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=my_openai_key)


###########################################
# Read Data
###########################################

# Read texts from PDF file
file_name = "The Goldfish Story.pdf"
file_path = os.path.join("data", file_name)
reader = PdfReader("data/" + file_name)
pdf_texts = [p.extract_text().strip() for p in reader.pages]

# Filter the empty strings
pdf_texts = [text for text in pdf_texts if text]
# print(len(pdf_texts), pdf_texts[0])


###########################################
# Split the text into smaller chunks
###########################################
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    SentenceTransformersTokenTextSplitter,
)

# Character-based splitting
character_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", ". ", " ", ""], chunk_size=1000, chunk_overlap=0
)
character_split_texts = character_splitter.split_text("\n\n".join(pdf_texts))
# print(word_wrap(character_split_texts[0]))
# print(f"\nTotal chunks: {len(character_split_texts)}")

# Token-based splitting
token_splitter = SentenceTransformersTokenTextSplitter(
    chunk_overlap=0, tokens_per_chunk=256
)
token_split_texts = []
for text in character_split_texts:
    token_split_texts += token_splitter.split_text(text)
# print(word_wrap(token_split_texts[0]))
# print(f"\nTotal chunks: {len(token_split_texts)}")


###########################################
# Create Embeddings and Store in Chromadb
###########################################
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

embedding_function = SentenceTransformerEmbeddingFunction()
# print(embedding_function([token_split_texts[0]]))

# Instantiate the Chroma client and create a collection called "goldfish"
chroma_client = chromadb.Client()
chroma_collection = chroma_client.create_collection("goldfish", embedding_function=embedding_function)

# Add embedings
ids = [str(i) for i in range(len(token_split_texts))]
chroma_collection.add(ids=ids, documents=token_split_texts)
# print(chroma_collection.count())


###########################################
# Naive RAG
###########################################
query = "How the goldfish die?"

results = chroma_collection.query(query_texts=[query], n_results=5)
retrieved_documents_naive = results["documents"][0]

# print(len(retrieved_documents_naive))
# for document in retrieved_documents_naive:
#     print(document)
#     print("\n")


###########################################
# Generate Hallucinated Answers
###########################################
# Create a answer generating model using base model gpt-3.5-turbo
def augment_query_generated(query, model="gpt-3.5-turbo"):
    prompt = """You are an experienced and helpful academic researcher. 
   Provide an example answer to the given question, that might be found in a document of story."""
    messages = [
        {
            "role": "system",
            "content": prompt,
        },
        {"role": "user", "content": query},
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    content = response.choices[0].message.content
    return content

# Generate the hallucinated answer
original_query = "How the goldfish die?"
hypothetical_answer = augment_query_generated(original_query)
joint_query = f"{original_query} {hypothetical_answer}"
# print(word_wrap(joint_query))


###########################################
# Get answers from chunks
###########################################
# Pass both original query and hallucinated answer to chromabd
results = chroma_collection.query(
    query_texts=joint_query, n_results=5, include=["documents", "embeddings"]
)
retrieved_documents_exp_ans = results["documents"][0]

# for doc in retrieved_documents:
#     print(word_wrap(doc))
#     print("")

# Generate the final answer using the OpenAI model
def generate_answer(query, context, model="gpt-3.5-turbo"):

    prompt = f"""
    You are a knowledgeable academic researcher. 
    Your users are inquiring about a story. 
    """

    messages = [
        {
            "role": "system",
            "content": prompt,
        },
        {
            "role": "user",
            "content": f"based on the following context:\n\n{context}\n\nAnswer the query: '{query}'",
        },
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    content = response.choices[0].message.content
    content = content.split("\n")
    return content

context_naive = "\n\n".join(retrieved_documents_naive)
context_exp_ans = "\n\n".join(retrieved_documents_exp_ans)

res_naive = generate_answer(query=original_query, context=context_naive)
res_exp_answer = generate_answer(query=original_query, context=context_exp_ans)
print("Final Answer of Navive RAG:")
print(res_naive)
print("Final Answer of Expansion Answer:")
print(res_exp_answer)
