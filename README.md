# PROJET :

##  Objectif du projet
Ce projet consiste à améliorer la visualisation d’un diagramme de Gantt en appliquant une **coloration intelligente** basée sur la **théorie des graphes**.  
L’objectif est de garantir que les tâches partageant un même critère soient cohérentes visuellement, tout en évitant les conflits de couleurs entre éléments voisins.

Le programme doit :
- Lire un jeu de données (CSV ou JSON)
- Construire un graphe de voisinage entre opérations
- Calculer une coloration minimale du graphe
- Associer les couleurs aux opérations
- Produire un résultat texte et une visualisation graphique du Gantt
- Gérer des modifications du jeu de données

##  Structure du projet



## Description des modules

### **operation.py**
Contient les classes représentant les opérations (tâches du Gantt).

### **chargement.py**
Gère la lecture des fichiers CSV/JSON et crée les objets `Operation`.

### **graph.py**
Construit le graphe de voisinage selon :
- chevauchement dans le temps,
- critère de différenciation.

### **coloration.py**
Implémente un algorithme de coloration du graphe (Greedy, Welsh-Powell…).

### **visualisation.py**
Génère :
- un fichier texte récapitulatif,
- un diagramme de Gantt coloré (via `matplotlib`).

### **main.py**
Script principal orchestrant toutes les étapes.


##  Jeu de données minimal

### **Version CSV** :









