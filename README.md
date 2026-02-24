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

### **affecter_couleur.py**
Affecte l'identifiant de couleur à chaque objet Operation en utilisant le résultat de la coloration du graphe.

### **calculer_nb_chromatiques**
Calcule le nombre chromatique, c'est-à-dire le nombre minimal de couleurs à partir du résultat de la coloration.

### **colorier_graphe**
Applique l'algorithme de coloration gloutonne au graphe de conflit pour déterminer le nombre minimal de couleurs nécessaires et attribuer une couleur à chaque nœud.

### **construire_graph_conflit.py**
Construit le graphe de conflit pour des niveaux différents.
Niveau 1 : Opérations adjacentes (i, i+1).
Niveau 2 : Opérations séparées par une (i, i+2).

### **gantt_generer.py**
Génère un diagramme de Gantt.

### **generer_fichier_sortie.py**
Génère un fichier de sortie CSV contenant toutes les colonnes initiales avec en plus la nouvelle colonne 'Couleur_ID'.

### **models.py**
Constructeur du modèle Operation.C'est dans ce code qu'on transforme les colonnes du CSV en attributs utilisables.

### **numerisation.py**
Lit les CSV et retourne une liste d'objets Operation et une liste de Machines.

### **regrouper_par_machine.py**
Regroupe les opérations par machine et trie la liste d'opérations de chaque machine par date de début.

### **main.py**
Script principal orchestrant toutes les étapes.










