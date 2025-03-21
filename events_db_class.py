import os
from langchain_chroma import Chroma
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema.document import Document
from langchain.document_loaders import TextLoader
from langchain_community.document_loaders import JSONLoader

CHROMA_PATH = os.getenv('CHROMA_PATH', 'events')

TARGET_SOURCE_CHUNKS=1
CHUNK_SIZE=500
CHUNK_OVERLAP=50
HIDE_SOURCE_DOCUMENTS=False


class db_class:
    def __init__(self, embedder) -> None:
            self.embedder = embedder
            self.loaded_files = []
            self.vector_db = Chroma(
                persist_directory=CHROMA_PATH,
                embedding_function=self.embedder
            )

    def load_text(self, text):
        print("4"*40)
        print("loading text:" + str(text))
        text_splitter = CharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        self.chunks = [Document(page_content=x) for x in text_splitter.split_text(str(text))]

        print("=>  loading and chunking done.")
        
        self.vector_db.add_documents(self.chunks)

        
    def load(self, path):
        fileExt =  os.path.splitext(path)
        #print("preping:"+path)
        if "http" in path:
            urls = []
            urls.append(path)
            loader = UnstructuredURLLoader(urls=urls)
            print("loading url:" + path)
            self.loaded_files = loader.load()
             
        elif "txt" in fileExt[1]:
            loader = TextLoader(file_path=path)
            print("loading txt doc:" + path)
            self.loaded_files = loader.load()

        elif "doc" in fileExt[1]:
            # dont forget pip install "unstructured[all-docs]"
            loader = UnstructuredWordDocumentLoader(file_path=path)
            print("loading word doc:" + path)
            self.loaded_files = loader.load()

        elif "pdf" in fileExt[1]:
            loader = UnstructuredPDFLoader(file_path=path)
            print("loading pdf:" + path)
            self.loaded_files = loader.load()

        #todo: need to check doc existence
        self.split_documents()
        
        print("=>  loading and chunking done.")
        
        self.vector_db.add_documents(self.chunks)
        

        print("doc added to vector db.")

    def load_file_dir(self,folder_path):
        
        self.folder_path = folder_path
        loader = DirectoryLoader(
            self.folder_path
        )
        self.loaded_files = loader.load()
        return self.loaded_files 
    
    def split_documents(self):
        if len(self.loaded_files)==0:
               print("need better error checking no loaded files")
               exit()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )
        self.chunks = splitter.split_documents(self.loaded_files )
        return self.chunks
    

    def embed(self):
        vector_db = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=self.embedder
        )

        vector_db.add_documents(self.chunks)
    
    def get_retriever(self,embedder):
        if not os.path.isdir(CHROMA_PATH):
            raise NotADirectoryError(
                "chroma db not found at " + str(CHROMA_PATH)
            )
        
        vector_db = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embedder
        )

        return vector_db.as_retriever(
            search_kwargs={"k": TARGET_SOURCE_CHUNKS}
        )

    def get_db(self):
         return(self.vector_db)
    
    def reset(self):
        client = Chroma(persist_directory=CHROMA_PATH)
        client.reset_collection()
        