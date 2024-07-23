"""
Module qui définit la classe Snake pour le jeu Snake.

La classe Snake gère le mouvement, la croissance et le dessin du serpent sur le canevas.
"""

import config


class Snake:
    """
    Représente le serpent dans le jeu Snake.

    Les coordonnées des segments sont toujours celles de leur coin supérieur gauche (x1, y1).
    Sinon, elles sont données sous la forme (x2, y2) pour le coin inférieur gauche.
    """

    def __init__(self, canvas):
        """Initialise le serpent sur le canevas."""
        self.canvas = canvas
        # Crée les 3 premiers segments du serpent
        self.segments = [(20, 20), (40, 20), (60, 20)]
        self.direction = "Right"
        self.draw_snake()

    def draw_snake(self):
        """Dessine le serpent."""
        # Supprime tous les objets tagués comme snake de la fenêtre (tous les anciens segments)
        self.canvas.delete("snake")
        # Itère sur chaque segment du serpent et le dessine
        for segment in self.segments:
            x1_segment = segment[0]
            y1_segment = segment[1]

            x2_segment = x1_segment + 20
            y2_segment = y1_segment + 20

            self.canvas.create_rectangle(
                x1_segment,
                y1_segment,
                x2_segment,
                y2_segment,
                outline=config.COULEUR_ARRIERE_PLAN,
                fill=config.COULEUR_SERPENT,
                width=2,
                tag="snake",
            )

    def delete_snake(self):
        """Supprime le serpent du canevas."""
        self.canvas.delete("snake")

    def change_direction(self, new_direction):
        """Change la direction du serpent."""
        self.direction = new_direction

    def move(self):
        """Fait bouger le serpent."""
        # Récupère la position de la tête
        x1_head, y1_head = self.segments[-1]

        # Détermine la nouvelle position de la tête
        if self.direction == "Left":
            new_position_head = (x1_head - 20, y1_head)
        elif self.direction == "Right":
            new_position_head = (x1_head + 20, y1_head)
        elif self.direction == "Up":
            new_position_head = (x1_head, y1_head - 20)
        elif self.direction == "Down":
            new_position_head = (x1_head, y1_head + 20)

        # Ajoute la nouvelle tête au début de la liste des segments
        self.segments.append(new_position_head)
        # Supprime le dernier segment pour simuler l'avancée du serpent
        self.segments.pop(0)
        self.draw_snake()

    def grow(self):
        """Augmente la taille du serpent d'un segment en l'ajoutant dans la liste segments."""
        # Récupère la position du dernier segment du serpent (la queue)
        x_tail, y_tail = self.segments[0]

        # Détermine la direction à partir de l'avant-dernier segment
        x_next, y_next = self.segments[1]
        if x_next < x_tail:
            x_new, y_new = x_tail + 20, y_tail
        elif x_next > x_tail:
            x_new, y_new = x_tail - 20, y_tail
        elif y_next < y_tail:
            x_new, y_new = x_tail, y_tail + 20
        elif y_next > y_tail:
            x_new, y_new = x_tail, y_tail - 20

        # Ajoute le nouveau segment à la fin de la liste des segments (derrière la queue)
        self.segments.insert(0, (x_new, y_new))
        self.draw_snake()
