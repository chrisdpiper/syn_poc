
from db_class import db_class
from langchain.embeddings import GPT4AllEmbeddings
import time
import os

CHROMA_PATH = os.getenv('CHROMA_PATH', 'science')

print("chroma path:" + CHROMA_PATH)


embedder = GPT4AllEmbeddings()
db = db_class(embedder)



script_start_time = time.time()

execution_times = []






      

       


