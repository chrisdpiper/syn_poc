
from db_class import db_class
from langchain.embeddings import GPT4AllEmbeddings
import os
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOllama
from langchain.embeddings import GPT4AllEmbeddings
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever



embedder = GPT4AllEmbeddings()
db = db_class(embedder)
vector_db = db.get_db()

#retriever = db.get_retriever(embedder)
LLM_MODEL = os.getenv('LLM_MODEL', 'mistral')
llm = ChatOllama(model=LLM_MODEL)

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
QUERY_PROMPT, prompt = get_prompt()

retriever = MultiQueryRetriever.from_llm(
    vector_db.as_retriever(), 
    llm,
    prompt=QUERY_PROMPT
)

qa_chain = RetrievalQA.from_chain_type(
    llm = llm,
    chain_type='stuff',
    retriever=retriever,
    return_source_documents=True, verbose=True
)




while True:
    query = input("What's on your mind: ")
    if query == '':
        break
    
    result = qa_chain(query)
    answer, docs = result['result'], result['source_documents']
    print("Question:" + query)
    print(answer)
    unique_docs = retriever.invoke(query)
    print("# docs" + str(len(unique_docs)))
    for document in unique_docs:
        print("\n> SOURCE: " + document.metadata["source"])
    #    #print(document.page_content)
      

    #print("#"* 30, "Sources", "#"* 30)
    #for document in docs:
    #    print("\n> SOURCE: " + document.metadata["source"] + ":")
    #    #print(document.page_content)
    #print("#"* 30, "Sources", "#"* 30)