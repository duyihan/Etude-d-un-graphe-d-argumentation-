# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 17:01:56 2017

@author: eisti
"""

import igraph

import sklearn 
from sklearn import tree
import pandas as pd

import re

import numpy as np

from sklearn import datasets, svm

from sklearn import preprocessing
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import KFold, cross_val_score
from sklearn.grid_search import GridSearchCV


def in_giant(G):
    cl = G.components()
    cl_sizes = cl.sizes()
    giant_component_index = cl_sizes.index(max(cl_sizes))
    return [x == giant_component_index for x in cl.membership]  




    
def get_giant_component(g):
    
    """if (igraph.is_igraph(g)):
    if (g.is_connected):
        return (g)
    else:"""
    #cmp = igraph.clusters(g)
    #matrix_FT = in_giant(g)
    #res = g.induced.subgraph(g, matrix_FT)
    clusters_components = g.clusters(mode ='strong')
    res = clusters_components.giant()
    return (res)

def graph_summary(g):
    if(type(g) == igraph.Graph):
        chaine =""
        chaine = chaine+" nb de noeuds "+ str(g.vcount())
        chaine = chaine+"\n nombre de liens " + str(g.ecount())
        chaine = chaine+"\n densité = "+ str(g.density())
        chaine = chaine+"\n diametre = "+ str(g.diameter())
        #chaine = chaine+"\n distribution degree = "+ str(g.distribution())
        return chaine
    else:
        chaine = "no graph"
        return chaine



def localisation_liens(g1,g2):
    lien_ext = 0
    lien_int = 0
      
    com = igraph.Graph.community_multilevel(g1)

    List1 = g1.get_edgelist()
    List2 = g2.get_edgelist()

    for i in range(len(List2)):    #i iterate toutes les edges gcomp2 
        v2 = List2[i]
        ok = False     #v2 contient chaque ligne
        for j in range(len(List1)):   #j iterate toutes les edges gcomp1
          v1 = List1[j]                 #v1 contient chaque ligne
          ok = ( ok or ((v2[0] in v1) and (v2[1] in v1)))   #si un edge de gcomp2 sous test, il est inclus dans gcomp1
        
        if (not ok ):
            #for i in range(len(com)):
                
            if (com.membership[v2[0]] == com.membership[v2[1]]):     
                lien_int = lien_int+1     
            else:     
                lien_ext = lien_ext+1
    #res = [lien_int,lien_ext, len(com)]
    res = {"interne":lien_int,"externe":lien_ext,"nb_communaute":len(com)}
    return(res)  



#prévision commence, calculer la matrice de distance des couples non-liées dans une même communauté
def data_generation(graphe1, graphe2):
  
  cgcc = igraph.Graph.complementer(graphe1)
  lp = igraph.Graph.get_edgelist(cgcc)
  
  
  x = []
  y = []
  jac = []
  AA = []
  AP = []
  SP = []
  classe = []
  
  communaute = igraph.Graph.community_multilevel(graphe1)
  
  for i in range(igraph.Graph.ecount(cgcc)):
    
    print(i)
    
    n1 =  graphe1.vs["id"].index(cgcc.vs[lp[i][1]]["id"])
    n2 =  graphe1.vs["id"].index(cgcc.vs[lp[i][1]]["id"])
    
    gg = igraph.Graph.shortest_paths_dijkstra(gcomp1)

    
    
    if(communaute.membership[n1] == communaute.membership[n2]):            
      x.append(lp[i][0])
      y.append(lp[i][1])
      jac.append(igraph.Graph.similarity_jaccard(graphe1)[0][1])
      AA.append(igraph.Graph.similarity_inverse_log_weighted(graphe1)[0][1])
      AP.append(igraph.Graph.degree(graphe1, lp[i][0]) * igraph.Graph.degree(graphe1, lp[i][1]))
      SP.append(gg[lp[i][0]][lp[i][1]])
      classe.append(igraph.Graph.are_connected(graphe2, lp[i][0], lp[i][1]))
    
    

    data_frame = pd.DataFrame.from_items([("x",x),("y",y),("jac",jac),("AA",AA),("AP",AP),("SP",SP),("classe",classe)])
  
  return (data_frame)     
    

dataset_train = data_generation(gcomp1,gcomp2)






"""
def classification_supervise(data, methode):
  
  set.seed(1234)
  
  positif = data[data.class,]
  negatif = data[not data.class,]
  #tester l'influence de composition sur la ratio d'erreur
  np_ind <- sample(2, nrow(positif), replace = TRUE, prob = c(0.8, 0.2) )
  ng_ind <- sample(2, nrow(negatif), replace = TRUE, prob = c(0.7, 0.3) )
  
  training <- rbind(positif[np_ind == 1,], negatif[ng_ind == 1,])
  print("training")
  print(nrow(training))
  test <- rbind(positif[np_ind == 2,], negatif[ng_ind == 2,])
  print("test")
  print(nrow(test))
  
  
  myFormula <- class~jac+AA+AP+SP
  
  data_tree <- methode(myFormula, data = training)
  matrix_training <- table(predict(data_tree)>0.5, training$class)
  
  #testPred <- predict(data_tree, newdata = test)
  #print("testPRed")
  #print(testPred)
  
  matrix_test <- table(predict(data_tree, newdata = test)>0.5, test$class)
  
  
  return(list(matrix_training, matrix_test))
}
"""


#Utilisation d'un cross validation pour prédire les noeuds possibles




y_train = dataset_train.loc[:,'classe']
x_train = dataset_train.loc[:, 'x': 'SP']

k_fold = sklearn.cross_validation.KFold(n = len(dataset_train), n_folds = 10, random_state = 7)


#Utilisation d'un algo utilisant le cross validation
svc = svm.SVC(C=1, kernel='linear')
digits = datasets.load_digits()
x = digits.data[:1000]
y = digits.target[:1000]
scores = sklearn.cross_validation.cross_val_score(svc, x_train, y_train,cv = k_fold)

#ou !! mais ici on a une copie
clf = sklearn.tree.DecisionTreeClassifier()
scores = sklearn.cross_validation.cross_val_score(clf, x_train, y_train,cv = k_fold)

#ou fit=apprentissage et predict=test
split_train = dataset_train.loc[1:176,:]
split_test = dataset_train.loc[176:251,:]

split_train_y = dataset_train.loc[1:176,:]
split_test_y = dataset_train.loc[176:251,:] 


clf=clf.fit(split_train,split_train_y)
clf.predict(split_test,split_test_y )

#clf est devenu un classifieur

sklearn.tree.export_graphviz(clf,out_file="/home/eisti/Documents/tree.dot")

y_pred=clf.predict(dataset_train)


for i in range(5):
    df.loc[i] = [1 for n in range(3)]




def evalation_model(confusion_matrix):
  
  precision = np.diag(confusion_matrix)/np.sum(confusion_matrix,axis=0)
  rappel = np.diag(confusion_matrix)/np.sum(confusion_matrix,axis=1)
  f_measur = 2 * rappel * precision / (rappel + precision)
  
  evaluation_frame = pd.DataFrame.from_items([("precision",precision),("rappel",rappel),("f_measur",f_measur)])
  names(evaluation_frame) = ["precision", "rappel", "f_measur"]
  #rownames(evaluation_frame) = ["FALSE", "TRUE"]
    
  return(evaluation_frame)


#Prediction de liens en utilisant le modele


#Determiner la qualite d'un noeud

g = gcomp1
### weight ####
weight = weight = [0]*(len(g.vs))

#g$weight=weight


def qualite_arg2(g,limit):
    
     weight = weight = [0]*(len(g.vs))
     for l in range(limit):
         
         for i in range(len(g.vs)):
             
             a =[]
             b =[]
             a =[]
             b =[]
             d =[]
             e =[]
             u1 =[]
             u2 =[]
        
             a = g.neighbors(i,mode = "in")
             e = g.neighbors(i,mode = "out")
             print(a)
             print(e)
        
             u1 = set(a).intersection(b)
             u2 = set(d).intersection(e)
             u1 = list(u1)
             u2 = list(u2)
                 
             for j in range(len(a)):
                
                 if weight[a[j]]>=1:
                     
                     weight[i] = weight[i]-2
                 else:
                     weight[i] = weight[i]-1
                     print(weight[i])

                     
            
                    
             for j in range(len(e)):
                if weight[a[j]]>=1:
                    weight[i] = weight[i]+2
                else:
                    weight[i] = weight[i]+1
                    print(weight[i])

     return weight

         

def qualite_arg(g):
    weight = weight = [0]*(len(g.vs))

    ###p1 for
    for i in range(len(g.vs)):
      for j in range(i):
        a =[]
        b =[]
        d =[]
        e =[]
        u1 =[]
        u2 =[]
        
        a = g.neighbors(i,mode = "in")
        b = g.neighbors(j,mode = "out")
        
        d = g.neighbors(j,mode = "in")
        e = g.neighbors(i,mode = "out")
        
        u1 = set(a).intersection(b)
        u2 = set(d).intersection(e)
        u1 = list(u1)
        u2 = list(u2)
        
        if(len(u1)>1):
          print(u1)
          for n in range(len(u1)) :
            weight[u1[n]] = weight[u1[n]]+3*len(u1)
          
        
        if(len(u2)>1):
          print(u2)
          for n in range(len(u2)):
            weight[u2[n]] = weight[u2[n]]+3*len(u2)
          
         
         
    
    ###p2
    print('P2 in:')
    for i in range(len(g.vs)):
      a = []
    #  b <- c()
      a = g.neighbors(i,mode = "in")
    #  b <- neighbors(g,i,mode = "out")
      if(len(a)>1):
        print(a)
        for n in range(len(a)) :
          weight[a[n]] = weight[a[n]]+2*len(a)
          
        
    
    print('P2 out')
    for i in range(len(g.vs)):
      b =[]
      b = g.neighbors(i,mode = "out")
      if(len(b)>1):
        print(b)
        for n in range(len(b)) :
          weight[b[n]] = weight[b[n]]+2*len(b)
        
      
    
    
    
    ###p3
    for i in range(len(g.vs)):
      for j in range(i):
        a = []
        b = []
        d = []
        e = []
        
        a = g.neighbors(j,mode = "in")
        b = g.neighbors(i,mode = "out")
        
        d = g.neighbors(i,mode = "in")
        e = g.neighbors(j,mode = "out")
        
        u1 = list(set(a).intersection(b))
        u2 = list(set(a).intersection(e))
        if (len(u1)>1 or len(u2)>1) :
          print(j)
          print(i)
          weight[i] = weight[i]+1
          weight[j] = weight[j]+1    
    return weight


weight = qualite_arg2(gcomp1,10)   

weight2= [(weight[0],0)] 

for i in range(len(weight))[1:]:
    weight2.append((weight[i],i))

 #Etude statistique 
degre = igraph.Graph.degree_distribution(g2)  
closeness = igraph.Graph.closeness(g2)
between = igraph.Graph.community_edge_betweenness(g2)


#Similarités entre acteurs
#g connexe
def sim(g,act1,act2):
    similarite=0
    a1=0
    a2=0
    for i in range(len(g.vs)):
        if(g.vs[i]["acteur"]==act1 and g.vs[i]["nature"]=="argument pour"):
            a1=a1+1
        if(g.vs[i]["acteur"]==act1 and g.vs[i]["nature"]=="argument contre"):
            a1=a1-1

        if(g.vs[i]["acteur"]==act2 and g.vs[i]["nature"]=="argument pour"):
            a2=a2+1
        if(g.vs[i]["acteur"]==act2 and g.vs[i]["nature"]=="argument contre"):
            a2=a2-1
    print a1
    print a2
    similarite= (a1+a2)/2
    return similarite


            
        



def main():
    g1 = igraph.read("/Users/irene/Desktop/pfe/arguments_politique start.gml", format= "gml") 
    g2 = igraph.read("/Users/irene/Desktop/pfe/arguments_politiques_complets.gml", format = "gml")
    g3 = igraph.read("/Users/irene/Desktop/pfe/arguments_politique1.gml", format = "gml")

    
    gcomp1 = get_giant_component(g1)
    gcomp2 = igraph.Graph.induced_subgraph(g2,gcomp1.vs["name"])

    
    print graph_summary(g1)
    print graph_summary(g2)
    
main()

layout = gcomp1.layout("kk")
g.vs["label"] = g.vs["name"]
igraph.plot(gcomp1, layout = layout)