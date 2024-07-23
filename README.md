# Jeu Snake v2.0

Ceci est un jeu Snake classique implémenté en Python en utilisant la bibliothèque Tkinter.

## Fonctionnalités

Mécaniques de jeu :

- Apparition aléatoire de nourriture que le serpent peut manger.
- Le serpent grandit à mesure qu'il mange la nourriture.
- Le jeu se termine si le serpent entre en collision avec lui-même ou avec les murs.
- Affichage du score actuel et du meilleur score (high score).
- Affichage du niveau actuel avec un système de progression des niveaux.
- Écran de fin de jeu avec le score final.

## Améliorations v2.0

- Résolution d'un bug dans la croissance du serpent, qui se fait maintenant à partir de la queue. (Auparavant, si le serpent mangeait une pomme en face de son corps, cela faisait perdre le joueur)
- Amélioration de l'interface graphique avec une pomme plus réaliste.
- Ajout de clignotements pour les messages importants tels que le game over et le high score.
- Introduction d'un système de high score pour suivre le meilleur score atteint.
- Introduction d'un système de niveaux avec augmentation progressive de la vitesse du serpent à chaque nouveau niveau.

## Fichiers

**Installer les dépendances requises** :

Le jeu utilise la bibliothèque Tkinter, qui est incluse avec la plupart des installations Python. Si Tkinter n'est pas installé, vous pouvez l'installer en utilisant votre gestionnaire de paquets. Le jeu utilise également le module `os` pour la gestion des fichiers et des chemins, qui est inclus dans la bibliothèque standard de Python.

- `main.py` : Le point d'entrée du jeu.
- `game.py` : Contient la classe `Game` qui gère la logique du jeu.
- `snake.py` : Contient la classe `Snake` qui gère le comportement du serpent.
- `food.py` : Contient la classe `Food` qui gère le comportement de la nourriture.
- `config.py` : Contient les variables de configuration.
- `high_score.txt` : Fichier pour stocker le meilleur score.

## Remarque

Il s'agit de la deuxième version de mon tout premier programme, et bien qu'il ne soit pas parfait, j'ai fait de mon mieux pour respecter les standards de PEP 8 et les bonnes pratiques de programmation. J'ai utilisé de nombreuses ressources en ligne et, bien entendu, je ne suis pas l'auteur de chaque ligne de code. Ce projet a été réalisé dans le but de pratiquer la programmation orientée objet après ma première année de licence.
