from itertools import count

from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
import os
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX")
pc = Pinecone(api_key=api_key)

embeddings = OpenAIEmbeddings()

pinecone_index = pc.Index(index_name)

vector_store = PineconeVectorStore(index_name=index_name, embedding=embeddings)

def vec_store(postid, title, content):
    text = f"Title: {title}, Content: {content}"
    vector_store.add_texts(
        texts=[text],
        metadatas=[{"postid": int(postid)}],
        ids=[str(postid)]
    )

def vec_search(query_text):
    results = vector_store.similarity_search(query_text, k=3)

    metasets = []
    if results:
        print(results)
        for match in results:
            metasets.append(int(match.metadata['postid']))
    return metasets

def vec_delete(postid):
    pinecone_index.delete(ids=[str(postid)])

def vec_update(postid, title, content):
    pinecone_index.delete(ids=[str(postid)])
    text = f"Title: {title}, Content: {content}"
    vector_store.add_texts(
        texts=[text],
        metadatas=[{"postid": int(postid)}],
        ids=[str(postid)]
    )