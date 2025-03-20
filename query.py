
from db_class import db_class
from langchain.embeddings import GPT4AllEmbeddings

embedder = GPT4AllEmbeddings()
db = db_class(embedder)

import os
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOllama
from langchain.embeddings import GPT4AllEmbeddings

embedder = GPT4AllEmbeddings()
retriever = db.get_retriever(embedder)
LLM_MODEL = os.getenv('LLM_MODEL', 'mistral')
llm = ChatOllama(model=LLM_MODEL)

qa_chain = RetrievalQA.from_chain_type(
    llm = llm,
    chain_type='stuff',
    retriever=retriever,
    return_source_documents=True, verbose=True
)
print("type:" + retriever.search_type)
#print("type:" + retriever.)




while True:
    query = input("What's on your mind: ")
    if query == '':
        break
    result = qa_chain(query)
    answer, docs = result['result'], result['source_documents']

    print(answer)

    print("#"* 30, "Sources", "#"* 30)
    for document in docs:
        print("\n> SOURCE: " + document.metadata["source"] + ":")
        #print(document.page_content)
    print("#"* 30, "Sources", "#"* 30)