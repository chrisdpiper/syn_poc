from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_core.tools import tool
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from get_vector_db import get_vector_db

import os
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever


#from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.runnables import RunnableParallel
import json



def get_prompt():
    QUERY_PROMPT = PromptTemplate(
        input_variables=["question"],
        template="""You are an AI language model assistant. Your task is to generate five
        different versions of the given user question to retrieve relevant documents from
        a vector database. By generating multiple perspectives on the user question, your
        goal is to help the user overcome some of the limitations of the distance-based
        similarity search. Provide these alternative questions separated by newlines.
        Original question: {question}""",
    )

    template = """Answer the question based ONLY on the following context:
    {context}
    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    return QUERY_PROMPT, prompt

LLM_MODEL = os.getenv('LLM_MODEL', 'mistral')
llm = ChatOllama(model=LLM_MODEL)
db = get_vector_db()
        # Get the prompt templates
QUERY_PROMPT, prompt = get_prompt()

  # Set up the retriever to generate multiple queries using the language model and the query prompt
retriever = MultiQueryRetriever.from_llm(
    db.as_retriever(), 
    llm,
    prompt=QUERY_PROMPT
)

# Define the processing chain to retrieve context, generate the answer, and parse the output
#chain = (
#    {"context": retriever, "question": RunnablePassthrough()}
#    | prompt
#    | llm
#    | StrOutputParser()
#)
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
# Define the processing chain to retrieve context, generate the answer, and parse the output
rag_chain_from_docs = (
    RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
    | prompt
    | llm
    | StrOutputParser()
)
rag_chain_with_source = RunnableParallel(
    {"context": retriever, "question": RunnablePassthrough()}
).assign(answer=rag_chain_from_docs)



#response = chain.invoke(input)

def ask( input):
    response = rag_chain_with_source.invoke(input)
#results = (retriever.get_relevant_documents(input)) gets actual data



#    s = response["context"]
#    j = json.dumps(str(s[0]))
#    start = j.find('metadata={\'source\': ') + 21
#    end = j.find('}', start)
#    s = j[start:end-1]

    print("question:" + input)
##    print("answer:"+ response["answer"] + "\nsource:"+ s)

   # docs = retriever.get_relevant_documents(input)
    print("answer:"+ response["answer"] ) #+ "\nsource:"+ str(response["context"]))




#ask("what type of game is checkers")"
done = False
while(done!=True):
    question = input("ask away:")
    if question == "":
        done = True
    else:
        ask(question)





#print("Keys and Values:")
#for key, value in response.items():
#    if key == "answer":
#        print(f"{key}: {value}")
###
#query = input

#tool(response_format="content_and_artifact")
#ef retrieve(query: str):
#   """Retrieve information related to a query."""
#   retrieved_docs = vector_store.similarity_search(query, k=2)
#   serialized = "\n\n".join(
#       (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
#       for doc in retrieved_docs
#   )
#   return serialized, retrieved_docs
