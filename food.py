"""
Module qui définit la classe Food pour le jeu Snake.

La classe Food gère la création et l'affichage de la nourriture sur le canevas.
"""

import random
import config


class Food:
    """
    Représente la nourriture dans le jeu Snake.

    Les coordonnées de la nourriture sont toujours celles de son coin supérieur gauche (x1, y1).
    Sinon, elles sont données sous la forme (x2, y2) pour le coin inférieur gauche.
    """

    def __init__(self, canvas):
        """Initialise la nourriture sur le canevas."""
        self.canvas = canvas
        self.position = self.create_food_position()
        self.draw_food()

    def create_food_position(self):
        """Crée une nouvelle position aléatoire pour la nourriture."""
        # Créer une position aléatoire pour la nouvelle nourriture
        x1_new_food = random.randrange(0, config.LONGUEUR_COTE_FENETRE - 20, 20)
        y1_new_food = random.randrange(0, config.LONGUEUR_COTE_FENETRE - 20, 20)
        return x1_new_food, y1_new_food

    def draw_food(self):
        """Dessine la nourriture sur le canevas."""
        # Supprime l'ancienne nourriture si elle existe
        self.canvas.delete("food")

        # Prend la position de la nouvelle nourriture et la dessine
        x1_new_food, y1_new_food = self.position
        x2_new_food = x1_new_food + 20
        y2_new_food = y1_new_food + 20

        self.canvas.create_rectangle(
            x1_new_food,
            y1_new_food,
            x2_new_food,
            y2_new_food,
            outline=config.COULEUR_FOOD,
            fill=config.COULEUR_FOOD,
            width=2,
            tag="food",
        )
