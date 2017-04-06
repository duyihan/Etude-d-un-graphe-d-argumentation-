setwd("~/Desktop/pfe")

library(igraph)
library(datasets)
library(cluster)


#### data####
g <- read.graph("arguments_politique1.gml",format=c("gml"))

#g <- read.graph("test.gml",format=c("gml"))
g
V(g)



### community ####

### cluster
plot(cluster_edge_betweenness(g),g,vertex.size=10, ,edge.arrow.size=0.5,main="cluster_edge_betweenness")
plot(cluster_walktrap(g),g,vertex.size=10, ,edge.arrow.size=0.5,main="cluster_walktrap")
plot(cluster_louvain(g),g,vertex.size=10, ,edge.arrow.size=0.5,main="cluster_walktrap")

#cluster_louvain couldn't show because of data

# community par acteur
display_community <- function(g){
  le <-c()
  if(is.igraph(g)){
    com_id <- unique(V(g)$acteur)
    colors <- rainbow(length(com_id))
    for(i in 1:length(com_id)){
      V(g)[acteur==com_id[i]]$color <-colors[i]
      le[i] <-com_id[i]
    }
    plot(g, vertex.size=10, ,edge.arrow.size=0.5,main="par acteur")
    legend("topleft", legend=le, fill = colors, col = colors,bty="n",cex=0.7)
  }
}

display_community(g)

# community par theme
display_community <- function(g){
  le <-c()
  if(is.igraph(g)){
    com_id <- unique(V(g)$theme)
    colors <- rainbow(length(com_id))
    for(i in 1:length(com_id)){
      V(g)[theme==com_id[i]]$color <-colors[i]
      le[i] <-com_id[i]
    }
    plot(g, vertex.size=10, ,edge.arrow.size=0.5,main="par theme")
    legend("topleft", legend=le, fill = colors, col = colors,bty="n",cex=0.7)
  }
}

display_community(g)

#plot(display_community(g),g)


#plot(cluster_edge_betweenness(g),g,vertex.size=10, ,edge.arrow.size=0.5)
#plot(cluster_walktrap(g),g,vertex.size=10, ,edge.arrow.size=0.5)
#plot(cluster_louvain(g),g)







### class ####
### methode set ####
#make group by methode(theme)

group_theme <- function(g){
  
  com_id <- unique(V(g)$theme)
  member<-c(1:length(com_id))
  
  for(i in 1:length(com_id))
    V(g)[theme==com_id[i]]$membership <-member[i]
  
  return(V(g))
}

#group_theme(g)$membership



data_generation <- function(g,methode){
  
  lp<-c()
  n<-0
  for (i in 1:ecount(g)){
    for (j in 1:ecount(g)){
      if(i!=j){
        m<-c(i, j)
        lp<-c(lp,m)
        n<-n+1
      }
    }
  }
  lp<-matrix(lp, ncol = 2,nrow = n,byrow = TRUE)
  lp
  
  x <- c()
  y <- c()
  jac <- c()
  AA <- c()
  AP <- c()
  SP <- c()
  class <- c()
  
  
  communaute <- methode(g)
  
  
  for (i in 1:n) {
    # print(i)
    
    n1 <- lp[i,1]
    n2 <- lp[i,2]
    if(communaute$membership[n1] == communaute$membership[n2]){
      x <- c(x, lp[i,1])
      y <- c(y, lp[i,2])
      jac <- c(jac, similarity.jaccard(g, vids = c(lp[i,1], lp[i,2]))[1,2])
      AA <- c(AA, similarity.invlogweighted(g, vids = c(lp[i,1], lp[i,2]))[1,2])
      AP <- c(AP, degree(g, lp[i,1]) * degree(g, lp[i,2]))
      SP <- c(SP, shortest.paths(g, v = lp[i,1], to = lp[i,2]))
      
      
      if(are.connected(g, lp[i,1], lp[i,2])||are.connected(g, lp[i,2], lp[i,1])){
        direction <- 1
        if(are.connected(g, lp[i,2], lp[i,1]))
          direction <- -1
      }
      else
        direction <-0
      
      class <- c(class, direction)
    }
  }
  
  data_frame <- data.frame(x, y, jac, AA, AP, SP,class)
  names(data_frame) <- c("x", "y", "jac", "AA", "AP", "SP","class") 

  return (data_frame)
}



#### methode ####
#data_generation(g,methode)
# methode = group_theme,cluster_walktrap,cluster_edge_betweenness,cluster_louvain

#data_set_2 <- data_generation(g,group_theme)
data_set_2 <- data_generation(g,cluster_walktrap)
#data_set_2 <- data_generation(g,cluster_edge_betweenness)
#data_set_2 <- data_generation(g,cluster_louvain)
#  0   no connected
#  1   x  connected y
# -1   y  connected x

data_set_2



#### centerality ####
# Degree
degree(g)
# Closeness (inverse of average dist)
closeness(g)
# Betweenness
betweenness(g)
# Local cluster coefficient
transitivity(g, type="local")
# Eigenvector centrality
evcent(g)$vector
# Now rank them
order(degree(g))
order(closeness(g))
order(betweenness(g))
order(evcent(g)$vector)




