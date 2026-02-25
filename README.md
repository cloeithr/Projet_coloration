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

## Entrées du programme

| Type                       | Élément                      | Source                         | Rôle                                                                      |
| -------------------------- | ---------------------------- | ------------------------------ | ------------------------------------------------------------------------- |
| **Donnée planifiée**       | Liste des opérations         | `operations.csv`               | Noyau du programme : contient centre, produit, dates, durée, job_id, etc. |
| **Donnée de référence**    | Liste des machines           | `DataMachine.csv`              | Structure le tri par machine et la création des graphes.                  |
| **Paramètre (choix)**      | Critère de coloration        | Saisi ou défini dans `main.py` | Définit ce qui constitue un nœud dans le graphe (codprod, uid…).          |
| **Paramètre (calcul)**     | Règle de voisinage 1         | Logique interne                | Conflit entre deux opérations consécutives sur la même machine.           |
| **Paramètre (calcul)**     | Règle de voisinage 2         | Logique interne                | Conflit supplémentaire entre opérations séparées d’un saut.               |
| **Paramètre (limitation)** | Liste des couleurs possibles | Code interne                   | Contraint l’affectation des couleurs.                                     |


## Sorties du programme

| Type de sortie         | Format             | Contenu                                       | Objectif                                       |
| ---------------------- | ------------------ | --------------------------------------------- | ---------------------------------------------- |
| **Résultat textuel**   | Fichier TXT ou CSV | Jeu de données initial + colonne `Couleur_ID` | Permet une exploitation ou un contrôle externe |
| **Résultat graphique** | Diagramme de Gantt | Gantt coloré selon la coloration obtenue      | Visualisation claire et intuitive              |
| **Métrique clé**       | Entier             | Nombre chromatique du graphe                  | Nombre minimal de couleurs nécessaires         |

## Fonctionnement du projet 

Le déroulement du programme suit plusieurs étapes :

**Numérisation (numerisation.py)**
- Lecture des fichiers CSV
- Conversion de chaque ligne en objet Operation
- Assignation d’un uid unique pour chaque opération (important pour le voisinage 2)

**Regroupement (regrouper_par_machine.py)**
- Classement des opérations par machine
- Tri chronologique des opérations par machine; permet de détecter les voisins directs

**Construction du graphe de conflit (construire_graph_conflit.py)**
Le graphe dépend du niveau de voisinage :
- Voisinage 1 : Conflit entre opérations consécutives (i et i+1)
- Voisinage 2 : Conflit entre opérations séparées d’un saut (i et i+2)

Chaque nœud correspond au critère choisi : code_produit, ou uid lorsqu’on colore par opération.

**Coloration du graphe (colorier_graphe.py)**

Algorithme glouton :
- Parcourt les nœuds dans un ordre donné
- Assigne la couleur la plus petite disponible
- Evite les couleurs des voisins

**Affectation aux opérations (affecter_couleurs.py)**

- Chaque objet Operation reçoit sa couleur finale.

**Generation du fichier résultat (generer_fichier_sortie.py)**

- Écriture du fichier identique aux données d’origine + colonne Couleur_ID.

**Génération du diagramme de Gantt (gantt_generer.py)**

- Visualisation colorée

- Navigation semaine par semaine

- Modes réalistes (semaines réelles)

## Exemple 

Données : 

MAC1 ; ProdA ; 08:00 ; 10:00
MAC1 ; ProdB ; 10:00 ; 12:00
MAC2 ; ProdB ; 09:00 ; 11:00
MAC2 ; ProdC ; 11:00 ; 13:00
MAC3 ; ProdC ; 10:00 ; 12:00
MAC3 ; ProdA ; 12:00 ; 14:00

Les produits A, B et C entrent en conflit, on obtient un triangle :
A <-> B <-> C <-> A -> nombre chromatique = 3
(minimum 3 couleurs)

## Structure du projet 

├── affecter_couleurs.py
├── calculer_nb_chromatiques.py
├── colorier_graphe.py
├── construire_graph_conflit.py
├── gantt_generer.py
├── generer_fichier_sortie.py
├── models.py
├── numerisation.py
├── regrouper_par_machine.py
├── main.py
└── README.md

## Description des modules

**affecter_couleur.py**
Affecte l'identifiant de couleur à chaque objet Operation en utilisant le résultat de la coloration du graphe.

**calculer_nb_chromatiques.py**
Calcule le nombre chromatique, c'est-à-dire le nombre minimal de couleurs à partir du résultat de la coloration.

**colorier_graphe.py**
Applique l'algorithme de coloration gloutonne au graphe de conflit pour déterminer le nombre minimal de couleurs nécessaires et attribuer une couleur à chaque nœud.

**construire_graph_conflit.py**
Construit le graphe de conflit pour des niveaux différents.
Niveau 1 : Opérations adjacentes (i, i+1).
Niveau 2 : Opérations séparées par une (i, i+2).

**gantt_generer.py**
Génère un diagramme de Gantt.

**generer_fichier_sortie.py**
Génère un fichier de sortie CSV contenant toutes les colonnes initiales avec en plus la nouvelle colonne 'Couleur_ID'.

**models.py**
Constructeur du modèle Operation.C'est dans ce code qu'on transforme les colonnes du CSV en attributs utilisables.

**numerisation.py**
Lit les CSV et retourne une liste d'objets Operation et une liste de Machines.

**regrouper_par_machine.py**
Regroupe les opérations par machine et trie la liste d'opérations de chaque machine par date de début.

**main.py**
Script principal orchestrant toutes les étapes.

## Documentation sur les fonctions à lancer 

Pour exécuter tout le projet, il faut lancer la commande python main.py . En effet, cette commande charge les données, trie les opérations, construit le graphe, calcule les couleurs, génère le fichier résultat et affiche le Gantt coloré interactif. 

## Détails sur la gestion du voisinage 2

Pour permettre au voisinage 2, il est nécessaire de :

- Colorer par opération (uid) car deux opérations ayant le même code produit doivent pouvoir avoir des couleurs différentes selon le contexte

Changements réalisés :

- Ajout d’un UID unique par opération

- Passage du critère de coloration à uid

- Adaptation de la construction des graphes







