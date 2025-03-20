from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from langchain.embeddings import GPT4AllEmbeddings
from langchain_community.embeddings import OllamaEmbeddings


embedder = GPT4AllEmbeddings()
#embedder = OllamaEmbeddings(model="nomic-embed-text")



while True:
    query = input("What's on your mind: ")
    if query == '':
        break
    query_vector = embedder.embed_query(query)
    fig = plt.figure()
    print("len:" + str(len(query_vector)))
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
     #   print(str(i) + " : " + str(query_vector[i]))
     #   array = np.array([[float(query_vector[i]), float(query_vector[i+1]),float(query_vector[1+3]),float(query_vector[i+4]), float(query_vector[i+5]), float(query_vector[i+6])],
      #                    [query_vector[i+7], [query_vector[i+8],query_vector[1+9],query_vector[i+10], query_vector[i+11], query_vector[i+12]]]] )


        print(str(last_x) + " : " + str(last_y) + " : " +str(last_z))
        x.append(last_x)
        y.append(last_y)
        z.append(last_z)
        u.append(query_vector[i])
        v.append(query_vector[i+1])
        w.append(query_vector[i+2])
        last_x = last_x + query_vector[i]
        last_y = last_y + query_vector[i+1]
        last_z = last_z + query_vector[i+2]
        


    #    array = np.array([[0, 0, 0, 0, 0, 1], [-1, -1, -1, 0, 0, 1],
     #           [1, 1, 1, 0, 0, 1], [2, 2, 2, 0, 0, 1]])
        
      #  array = np.array([0, 0, 0, 0, 0, 1], [-1, -1, -1, 0, 0, 1])
                
     #   print(query_vector)
     #       soa = np.array([[0, 0, 1, 1, -2, 0], [0, 0, 2, 1, 1, 0],
      #          [0, 0, 3, 2, 1, 0], [0, 0, 4, 0.5, 0.7, 0]])
        #, Y, Z, U, V, W = 
        



    ax = fig.add_subplot(111, projection='3d')
    scale = 100
    ax.quiver(x,y,z,u,v,w, color='r')

    plt.show()    