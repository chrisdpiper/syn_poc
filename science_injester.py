
from db_class import db_class
from langchain.embeddings import GPT4AllEmbeddings
import time
import os

CHROMA_PATH = os.getenv('CHROMA_PATH', 'science')

print("chroma path:" + CHROMA_PATH)


embedder = GPT4AllEmbeddings()
db = db_class(embedder)
db.set_chroma_path("science")


script_start_time = time.time()

execution_times = []

#IM Attract Actual Page Content.pdf
#IM Attractions.pptx
#Intermolecular Attractions Worksheet.pdf
db.load("./science_docs/IM Attract Actual Page Content.pdf")
db.load("./science_docs/Intermolecular Attractions Worksheet.pdf")
db.load("./science_docs/IM Attractions.pptx")





      

       


