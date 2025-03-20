import os
from langchain.chains import RetrievalQA
from db_class import db_class
from langchain.embeddings import GPT4AllEmbeddings

embeddings = GPT4AllEmbeddings()
embedder = GPT4AllEmbeddings()
chroma_db = db_class(embedder)
db = chroma_db.get_db()



print("\nEmbedding keys:", db.get().keys())
print("\nNumber of embedded docs:", len(db.get()["ids"]))
    

    
file_list = set()
length = len(db.get()["ids"])
print
for x in range(len(db.get()["ids"])):
    print("id:"+ str(x) + "/" + str(length))
    doc = db.get()["metadatas"][x]
    source = doc["source"]
     # print(source)
    file_list.add(source)
        
### Set only stores a value once even if it is inserted more than once.
list_set = set(file_list)
unique_list = (list(list_set))

print("\nNumber of unique files in db:" + str(len(unique_list)))
print("\nList of unique files in db:\n")
for unique_file in unique_list:
    print(unique_file)