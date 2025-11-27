Pour cloner le repo, créer un dossier où le mettre, déplacer vous dans le dossier puis : git clone https://github.com/cloeithr/Projet_coloration.git

Ensuite pour ajouter un dossier/fonctionnalité au projet il faut créer une branche avec : git switch --create NomDeLaBranche Puis vous pouvez travailler depuis cette branche. Commandes importantes :

.git status : permet de voir tous les dossiers modifiés depuis le dernier commit

.git add . : permet d'ajouter dans le commit toutes les modifications vues dans le git status

.git commit : permet de sauvegarder sur votre branche locale les modifications ajoutées par le git add

.git push -u NomDeLaBranche : permet de d'ajouter votre branche au repo en ligne (sur github)
