
from db_class import db_class
from langchain.embeddings import GPT4AllEmbeddings
import time

start_time = time.time()
embedder = GPT4AllEmbeddings()
db = db_class(embedder)

#db.load("../docs/fakeresume.docx")
db.load("https://www.linkedin.com/pulse/daniels-law-enough-case-enforceable-data-privacy-b%25C3%25A1rtfai-walcott-yfodc")
#db.load("https://www.linkedin.com/pulse/hidden-battle-your-health-data-katalin-b%25C3%25A1rtfai-walcott-uru5c")
#db.load("https://en.wikipedia.org/wiki/Tree_frog")
#db.load("https://en.wikipedia.org/wiki/Desert_rain_frog")
#db.load("https://en.wikipedia.org/wiki/Platymantis")
#db.load("https://en.wikipedia.org/wiki/Pseudopaludicola")

        
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")