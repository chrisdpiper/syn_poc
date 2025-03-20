
from db_class import db_class
from langchain.embeddings import GPT4AllEmbeddings
import time
 

def get_all_urls(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses 
        soup = BeautifulSoup(response.content, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a') if a.get('href')]
        return links
    except requests.exceptions.RequestException as e:
         print(f"Request error: {e}")
         return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def load_and_parse_text(file_path):
    try:
        with open(file_path, 'r') as file:
            text = file.read()
            lines = text.splitlines()
            return lines
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"An error occurred: {e}"

embedder = GPT4AllEmbeddings()
db = db_class(embedder)

import requests
from bs4 import BeautifulSoup

script_start_time = time.time()


#db.load("https://www.linkedin.com/pulse/daniels-law-enough-case-enforceable-data-privacy-b%25C3%25A1rtfai-walcott-yfodc")

#exit()
execution_times = []
url = "https://en.wikipedia.org/wiki/Outline_of_chemistry"
#db.load(url)
data_urls = get_all_urls(url)
if data_urls:
    for url in data_urls:
        if "/wiki/" in url and "https" not in url and "file" not in url and ":" not in url and "Main" not in url:
            start_time = time.time()
            url = url.replace("/wiki/", "https://en.wikipedia.org/wiki/")
            print(url)
            db.load(url)
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"url load time: {execution_time} seconds")
            execution_times.append(execution_time)


file_path = 'katalin_doc_links.txt'
parsed_data = load_and_parse_text(file_path)

for file in parsed_data:
         start_time = time.time()
         print(file)
         db.load(file)
         end_time = time.time()
         execution_time = end_time - start_time
         print(f"url load time: {execution_time} seconds")
         execution_times.append(execution_time)










db.load("https://en.wikipedia.org/wiki/Tree_frog")
db.load("https://en.wikipedia.org/wiki/Desert_rain_frog")
db.load("https://en.wikipedia.org/wiki/Platymantis")
db.load("https://en.wikipedia.org/wiki/Pseudopaludicola")


end_time = time.time()
execution_time = end_time - script_start_time
print(f"full Execution time: {execution_time} seconds")
load_time_taken = 0
for time in execution_times:
    load_time_taken = load_time_taken + time

average_time = str(load_time_taken / len(execution_times))

print("average load time "+ average_time + " " + str(len(execution_times))+ " docs loaded")
      

       


