# Etude d'un graphe d'argumentation

# Objectif:
Evaluer la qualité d’un argument
Trouver les noeuds les plus controversés
Regrouper des acteurs ayant des arguments similaires Prédiction de liens via machine learning

# data:
Pour le graphe complet:
nombre d’idées = 6 (économie,demanteler les bases nucléaire,immigration,voile,famille, service national)
nombre de noeuds = 130 nombre de liens = 138 densité = 0.016
diamètre = 16

# Modélisation
Les noeuds centraux:
  Un sujet sous forme de question fermée: pour ou contre
  
Les noeuds:
  Un acteur
  Son bord politique
  Son contenu
  Une position vis a vis du sujet
  
Les liens:
  liens d’attaque -
  Liens d’approbation +
  liens entre acteurs (attaque) ou vers le sujet directement (attaque ou approbation)
