from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from langchain.embeddings import GPT4AllEmbeddings
from langchain_community.embeddings import OllamaEmbeddings

embedders = []


embedder = GPT4AllEmbeddings()
embedders.append(embedder)
embedder = OllamaEmbeddings(model="nomic-embed-text")
embedders.append(embedder)

def encode(query, embedder,ax,col):
    print("mbedding with " + str(col))
    query_vector = embedder.embed_query(query)
    x = []
    y = []
    z  = []
    u = []
    v = []
    w = []
    last_x = 0
    last_y = 0
    last_z = 0
    for i in range(0,len(query_vector),3):
        x.append(last_x)
        y.append(last_y)
        z.append(last_z)
        u.append(query_vector[i])
        v.append(query_vector[i+1])
        w.append(query_vector[i+2])
        last_x = last_x + query_vector[i]
        last_y = last_y + query_vector[i+1]
        last_z = last_z + query_vector[i+2]
    
    ax.quiver(x,y,z,u,v,w, color=col)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
    

while True:
    col = ['r','b','g']
    i=0
    query = input("phrase to draw: ")
    if query == '':
        break
    encode(query,embedders[0],ax, col[0])
    encode(query,embedders[1],ax, col[1])


    plt.show()    
   
        


    #    array = np.array([[0, 0, 0, 0, 0, 1], [-1, -1, -1, 0, 0, 1],
     #           [1, 1, 1, 0, 0, 1], [2, 2, 2, 0, 0, 1]])
        
      #  array = np.array([0, 0, 0, 0, 0, 1], [-1, -1, -1, 0, 0, 1])
                
     #   print(query_vector)
     #       soa = np.array([[0, 0, 1, 1, -2, 0], [0, 0, 2, 1, 1, 0],
      #          [0, 0, 3, 2, 1, 0], [0, 0, 4, 0.5, 0.7, 0]])
        #, Y, Z, U, V, W = 
        

   