
from db_class import db_class
from langchain.embeddings import GPT4AllEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
import chromadb
from langchain.schema.retriever import BaseRetriever
from langchain.schema import Document
from langchain.callbacks.manager import CallbackManagerForRetrieverRun, AsyncCallbackManagerForRetrieverRun
from typing import TYPE_CHECKING, Any, Dict, List, Optional 

embedder = GPT4AllEmbeddings()
db = db_class(embedder)

import os
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOllama
from langchain.embeddings import GPT4AllEmbeddings

from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt


embedder = GPT4AllEmbeddings()
retriever = db.get_retriever(embedder)
LLM_MODEL = os.getenv('LLM_MODEL', 'mistral')
llm = ChatOllama(model=LLM_MODEL)
CHROMA_PATH = os.getenv('CHROMA_PATH', 'chroma')

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_collection(name="langchain")


#collection.query(
#    query_embeddings=[[11.1, 12.1, 13.1],[1.1, 2.3, 3.2], ...],
#    n_results=10,
#    where={"metadata_field": "is_equal_to_this"},
#    where_document={"$contains":"search_string"}
#)

print(str(collection.metadata))



def searchDataByVector(query: str):
    try:

        query_vector = embedder.embed_query(query)





#        z = np.linspace(0,1,100)      
 #       x = z * np.sin(25*z)
  #      y = z * np.cos(25*z)
   #     ax.plot3D(x,y,z,'red')
        #plt.show()

     #   print("query_list type" + str(type(query_vector)))
      #  print("query len:" + str(len(query_vector)))
        #print("query_vector:" + str(query_vector))
 
        res = collection.query(
            query_embeddings=[query_vector],
            n_results=20,
            include=['distances','documents','embeddings', 'metadatas'],
        )
     #   print("****Query", "\n--------------")
      #  print(query)
    #    print("****Distances", "\n--------------")
    #    index = res["distances"]
    #    a = index[0]
     #   print("source documents:" + str(type(index[0])))
     #   for i in range(len(a)):
      #      print(str(i) + ":" + str(a[i]) + ":")#+ res['metadata'][0][i] )
        #print(res["distances"][0])
     #   print("****metadatas", "\n--------------")
    #    print(res['metadatas'][0])
    #    print("metadatas type:" + str(type(res['metadatas'])))
    #    print("metadatas len :"+ str(len(res['metadatas'])) )
    #    print("****Vector", "\n--------------")
      #  print(res['embeddings'][0][0])
  #      print("")
   #     keys = res.keys()
    #    for key in keys:
     #       print("key:" + key + "\nvalue type:" + str(type(res[key])) )
       # print(res)
        return res

    except Exception as e:
        print("Vector search failed : ", e)

class summaryRetriever(BaseRetriever):
    def __int__(self):
        pass
    def _get_relevant_documents(
            self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
            


        global doc_to_summarize
        result_docs = []
        result_docs.append(doc_to_summarize)
        return result_docs



class myRetriever(BaseRetriever):

    def __int__(self):
        pass

    def _get_relevant_documents(
            self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        # response = URAPI(request)
        # convert response (json or xml) in to langchain Document like  doc = Document(page_content="response docs")
        # dump all those result in array of docs and return below
        r = searchDataByVector(query)
       # print("*type:"+ str(type(r["documents"][0])))
       # print("*len:"+ str(len(r["documents"][0])))
        result_docs = []
        raw_docs = r["documents"]
        raw_metadatas = r["metadatas"]
        raw_distances = r["distances"]
        raw_embeddings = r["embeddings"]
# this is really inefficient
        docs = []
        metadatas = []
        distances = []
        embeddings = []
#remove duplicates and keep lowest values
        for i in range(len(raw_metadatas[0])):
            if raw_metadatas[0][i] in metadatas:
           #     print("       "+ str(raw_metadatas[0][i]) + "already in" )
                index = metadatas.index(raw_metadatas[0][i])
                if raw_distances[0][i] < distances[index]:
     #               print("updating " + str(metadatas[index]) +" to "  + raw_metadatas[0][i])
                    distances[index] = raw_metadatas[0][i]
        #        else:
      #              print("did not update " + str(metadatas[index])+ " as " + str(distances[index]) +" < " + str(raw_distances[0][i] ) )
            else:
       #         print("adding:" + str(raw_metadatas[0][i])  + " distance" + str(raw_distances[0][i]))
                metadatas.append(raw_metadatas[0][i])
                docs.append(raw_docs[0][i])
                distances.append(raw_distances[0][i])
                embeddings.append(raw_embeddings[0][i])


 
        for i in range(len(metadatas)):
            print("\n index: " + str(i) + str(metadatas[i]) + " importance:" + str(distances[i]))
     #       print("\ncontainer:" + str(type(d)) + " of len:" + str(len(d)))
      #      for i in d:
       #         print("\ncontains:" + str(i))
        choice = []
        num = input("keep what indexes?")

       
        for ch in num:
            choice.append(int(ch))

    
        for i in choice:
            doc = Document(page_content=docs[i])
            doc.metadata = metadatas[i]
            result_docs.append(doc)

 
        return result_docs

    async def _aget_relevant_documents(
            self,
            query: str,
            *,
            run_manager: AsyncCallbackManagerForRetrieverRun,
            **kwargs: any,
    ) -> List[Document]:
        raise NotImplementedError()
myRetriever = myRetriever()
summaryRetriever = summaryRetriever()
qa_chain = RetrievalQA.from_chain_type(
    llm = llm,
    chain_type='stuff',
    retriever=myRetriever,
    return_source_documents=True, verbose=True
)

sum_chain = RetrievalQA.from_chain_type(
    llm = llm,
    chain_type='stuff',
    retriever=summaryRetriever,
    return_source_documents=True, verbose=True
)

last_querys_docs = []
doc_to_summarize = ""

while True:
    
    
    query = input("What's on your mind: ")
    if query == '':
        break

    if "s:" in query:
        query = query.replace("s:"," ")
        print (query)
        query = query.strip()

        for index in query:
           
            print("index:" + index)
            doc_to_summarize = last_querys_docs[int(index)]
            query = "summarize this document"
          #  print ("summarizing: " + str(doc_to_summarize.metadata["source"]))
 
            result = sum_chain(query)
            answer, docs = result['result'], result['source_documents']
            print("summarizing:" + doc_to_summarize.metadata["source"])
            print(answer)
            print("  ->other sources to summarize")
        index = 0
        for document in last_querys_docs:
            print("\n index: "+ str(index) +" "  + document.metadata["source"] )

            index=index+1
    else:
        result = qa_chain(query)
        answer, docs = result['result'], result['source_documents']
        last_querys_docs = []
        index = 0
        for document in docs:
            print("\n index: "+ str(index) +" "  + document.metadata["source"] )
            index = index + 1
            last_querys_docs.append(document)


        #query = input("chroma db search: ")
    # if query == '':
    #     break
    # docs = searchDataByVector(query)
        #for key in result:
        #   print("key:" + key)
        print("question:" + query + "\n---\n\n")
        print(answer)


        print("  ->Sources")
        index = 0
        last_querys_docs = []
        for document in docs:
            print("\n index: "+ str(index) +" "  + document.metadata["source"] )
           
            last_querys_docs.append(document)
            index=index+1
            #print(document.page_content)
        #print("#"* 30, "Sources", "#"* 30)




