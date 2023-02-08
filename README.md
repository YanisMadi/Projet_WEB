# Projet_WEB


Le but de ce projet est de construire une application web en utilisant django pour permettre aux utilisateurs de faire des annotations de séquences génomiques .

## Outils

Pour ce projet on a utilisé  [python 3.9.12](https://www.python.org/downloads/release/python-3912/) et  [django 4.1.4](https://www.djangoproject.com).  


## Les différents rôles
Pour chaque utilisateur une permission est accordée selon son rôle :


- **Lecteur** peut seulement lire les informations de la base et poser ses requêtes via un formulaire.

- **Annoateur** peut faire tout ce que fait un utilisateur et en plus peut annoter des séquences.

- **Validateur** peut faire tout ce que fait un annotateur et en plus il peut valider les annotations des annotateurs.

- **Administrateur** a accès à la liste des utilisateurs, il est le seul à pouvoir créer, supprimer et affecter des rôles aux utilisateurs. Il a aussi accès aux informations de dernière connexion des utilisateurs.

##


## Diagramme UML

![Diagramme UML](/genome_annotation/myapp_models.png "Diagramme UML")

## Import data
