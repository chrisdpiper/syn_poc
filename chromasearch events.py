
from events_db_class import db_class
from langchain.embeddings import GPT4AllEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
import chromadb
from langchain.schema.retriever import BaseRetriever
from langchain.schema import Document
from langchain.callbacks.manager import CallbackManagerForRetrieverRun, AsyncCallbackManagerForRetrieverRun
from typing import TYPE_CHECKING, Any, Dict, List, Optional 
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain


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
CHROMA_PATH = os.getenv('CHROMA_PATH', 'events')

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


       # print("\n ->documents that matched:")
        for i in range(len(metadatas)):
            formatted_distance = "{:.2f}".format(round(distances[i],2))
            formatted_source =  str(metadatas[i]).replace("{'source': ","")
            formatted_source = formatted_source.replace("'https://","")
            formatted_source = formatted_source.replace("'}","")
            formatted_source = formatted_source.replace("www.","")
            formatted_source = formatted_source.replace(".com.","")
  
          #  if len(metadatas)> 10:
        #        print(f"  index:{i:02d} " +"distance:" + formatted_distance + " " + formatted_source  )
           # else:
         #       print(f"  index:{i:01d} " +"distance:" + formatted_distance + " " + formatted_source  )

                 #       print("\ncontainer:" + str(type(d)) + " of len:" + str(len(d)))
      #      for i in d:
       #         print("\ncontains:" + str(i))
        choice = []
        num = 'a'

        if num=="a":
            for i in range(len(metadatas)):
                choice.append(i)
        else:
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
    return_source_documents=True, verbose=False
)

sum_chain = RetrievalQA.from_chain_type(
    llm = llm,
    chain_type='stuff',
    retriever=summaryRetriever,
    return_source_documents=True, verbose=True
)

last_querys_docs = []
doc_to_summarize = ""

system_prompt = (
    "Use the given context to answer the question. "
    "If you don't know the answer, say you don't know. "
 #   "Use three sentence maximum and keep the answer concise. "
    "Context: {context}"
)

sum_prompt = (
    "use the given context to give a summary."
    "please put each context paragraph in a numbered line."
    "Context: {context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

sumprompt = ChatPromptTemplate.from_messages(
    [
        ("system", sum_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
sum_answer_chain = create_stuff_documents_chain(llm, sumprompt)
chain = create_retrieval_chain(myRetriever, question_answer_chain)

sum_p_chain = create_retrieval_chain(summaryRetriever, question_answer_chain)


while True:
    
    
    query = input("\nWhat would you like to know?\n")
    if query == '':
        break

    if "e:" in query:
        query = query.replace("e:"," ")
        query = query.strip()
        print("\---\nexamining source:" + last_querys_docs[int(query)].metadata["source"]+"\n---")
        print(last_querys_docs[int(query)])
        print("\---")
    elif "s:" in query:
        query = query.replace("s:"," ")
    #    print (query)
        query = query.strip()
        if "a" in query:
            query = ""
            for i in range(len(last_querys_docs)):
                query  = query + str(i) + ","

        for index in query:
            if index == ",":
                continue
            doc_to_summarize = last_querys_docs[int(index)]
            query = "summarize" # this document" +  doc_to_summarize.metadata["source"]
          #  print ("summarizing: " + str(doc_to_summarize.metadata["source"]))
 
            #result = sum_chain(query)
            result = sum_p_chain.invoke({"input" : query})
            answer, docs = result['answer'], result['context']
            formatted_souce = str(doc_to_summarize.metadata["source"])
            formatted_souce = formatted_souce.replace("https://","")
            print("---\nsummarizing:\n" + formatted_souce)
            print("---\n" +answer + "\n---" )
          
#            
 #               print("  ->other sources to summarize")
  #              index = 0
   #             for document in last_querys_docs:
#
 #                   print("   "+ str(index) +":"  + document.metadata["source"] )
#
 #                   index=index+1
    else:
        result = chain.invoke({"input" : query})
   #     print("type:" + str(type(result)))
    #    for k in result:
     #       print(k)

        answer, docs = result['answer'], result['context']
        last_querys_docs = []
        index = 0
        for document in docs:
            formatted_souce = str(document.metadata["source"])
            formatted_souce = formatted_souce.replace("https://","")
            print("\n index: "+ str(index) +" " + formatted_souce)
            index = index + 1
            last_querys_docs.append(document)


        #query = input("chroma db search: ")
    # if query == '':
    #     break
    # docs = searchDataByVector(query)
        #for key in result:
        #   print("key:" + key)
        print("\n---\nquestion:" + query + "\n---\nanswer:\n---")
        print(answer)


  #      print("---\n  ->Sources")
        index = 0
        last_querys_docs = []
        for document in docs:
            formatted_souce = str(document.metadata["source"])
            formatted_souce = formatted_souce.replace("https://","")
   #         print("   "+ str(index) +":"  +  formatted_souce)
           
            last_querys_docs.append(document)
            index=index+1
            #print(document.page_content)
        #print("#"* 30, "Sources", "#"* 30)
    #    print("---")



