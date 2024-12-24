from itertools import count

from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
import os
from pinecone import Pinecone
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX")
pc = Pinecone(api_key=api_key)

embeddings = OpenAIEmbeddings()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
temp = """다음 블로그 글을 요약해줘. 마크다운 포맷은 모두 제거하고, 내용을 간결하게 정리해줘. 요약은 원본 내용의 약 50% 정도로 축약해줘.\n내용 : {content}"""

prompt = PromptTemplate(template=temp, input_variables=['content'])

chain = prompt | llm | StrOutputParser()

pinecone_index = pc.Index(index_name)

vector_store = PineconeVectorStore(index_name=index_name, embedding=embeddings)

def vec_store(postid, title, content):
    text = f"Title: {title}, Content: {content}"
    print(text)
    summary = chain.invoke({"content": text})
    print("요약 : " + summary)
    vector_store.add_texts(
        texts=[summary],
        metadatas=[{"postid": int(postid)}],
        ids=[str(postid)]
    )

def vec_search(query_text):
    query_vecter = embeddings.embed_query(query_text)
    results = pinecone_index.query(vector=query_vecter, top_k=3, include_metadata=True)
    metasets = []
    if "matches" in results:
        print(results)
        for match in results['matches']:
            if match['score'] > 0.75:
                metasets.append(int(match['id']))
    print(query_text)
    print(metasets)
    return metasets

def vec_delete(postid):
    pinecone_index.delete(ids=[str(postid)])

def vec_update(postid, title, content):
     pinecone_index.delete(ids=[str(postid)])
     text = f"Title: {title}, Content: {content}"
     summary =  chain.invoke({"content": text})
     print("요약 : " + summary)
     vector_store.add_texts(
        texts=[summary],
        metadatas=[{"postid": int(postid)}],
        ids=[str(postid)]
    )