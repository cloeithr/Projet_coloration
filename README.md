### Infos cloner le repo 

Créer un dossier où le mettre, déplacer vous dans le dossier puis : git clone https://github.com/cloeithr/Projet_coloration.git

Ensuite pour ajouter un dossier/fonctionnalité au projet il faut créer une branche avec : git switch --create NomDeLaBranche Puis vous pouvez travailler depuis cette branche. 

### Commandes importantes :

.git status : permet de voir tous les dossiers modifiés depuis le dernier commit

.git add . : permet d'ajouter dans le commit toutes les modifications vues dans le git status

.git commit : permet de sauvegarder sur votre branche locale les modifications ajoutées par le git add

.git push -u NomDeLaBranche : permet de d'ajouter votre branche au repo en ligne (sur github)

 # PROJET :

Pour le moment sur la feuille on a noté : 

- Liste entrées : centre / codprod / codof / sequence / codop / dtedeb / dtefin / criteres
- Liste sorties : attribution d'une couleur à une tâche / nombre minimum de couleurs / Gantt bien coloré

Quand on a posé la question au prof sur les voisins éloignés, il nous a dit que pour savoir le nombre de couleurs qu'on va devoir avoir : lui-même (le point dans le graphe) + celui qui le le plus de voisins. 

Il va aussi falloir qu'on réfléchisse au bout de combien d'arêtes on considère que c'est plus un voisin (sur sa feuille il nous a dit à partir de 5 donc à voir si on prend ça ou pas). 


