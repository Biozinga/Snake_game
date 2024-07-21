"""
Module pour le jeu Snake.

Ce module contient la classe Game qui gère la logique principale du jeu Snake.
"""

from tkinter import Canvas
from snake import Snake
from food import Food

import config


class Game:
    def __init__(self, root):
        """Initialise le jeu Snake."""
        # Crée la fenêtre
        self.root = root
        root.geometry(f"{config.LONGUEUR_COTE_FENETRE}x{config.LONGUEUR_COTE_FENETRE}")

        # Fenêtre non redimensionnable
        root.resizable(False, False)

        # Crée le canevas
        self.canvas = Canvas(
            self.root,
            width=config.LONGUEUR_COTE_FENETRE,
            height=config.LONGUEUR_COTE_FENETRE,
            bg=config.COULEUR_ARRIERE_PLAN,
        )
        self.canvas.pack()

        # Initialisation du serpent, de la nourriture et du score
        self.snake = Snake(self.canvas)
        self.snake_size = len(self.snake.segments)
        self.food = Food(self.canvas)
        self.food.draw_food()
        self.score = 0

        # Lier les touches du clavier à la méthode on_key_press
        self.root.bind("<KeyPress>", self.on_key_press)

        # Afficher le score initial
        self.score_text = self.canvas.create_text(
            235,
            430,
            text=f"SCORE: {self.score}",
            fill=config.COULEUR_ECRITURE,
            font=(config.POLICE_ECRITURE, 16),
        )

        # Change l'état du jeu de "off" à "on"
        self.running = True
        self.is_game_over = False

        # Planifie la première mise à jour après 100 ms
        self.root.after(100, self.update)

    def on_key_press(self, e):
        """Gère les événements de pression des touches pour changer la direction du serpent."""
        new_direction = None
        if e.keysym == "Right":
            new_direction = "Right"
        elif e.keysym == "Left":
            new_direction = "Left"
        elif e.keysym == "Up":
            new_direction = "Up"
        elif e.keysym == "Down":
            new_direction = "Down"

        if new_direction:
            self.snake.change_direction(new_direction)

    def check_collision(self):
        """Vérifie qu'une collision n'a pas eu lieu."""
        # Récupération de la position de la tête du serpent
        head = self.snake.segments[-1]

        # Vérifie s'il y a une collision avec une bordure de fenêtre
        if not (
            0 <= head[0] < config.LONGUEUR_COTE_FENETRE
            and 0 <= head[1] < config.LONGUEUR_COTE_FENETRE
        ):
            self.running = False
            self.is_game_over = True

        # Vérifie s'il y a une collision avec un segment du serpent
        for segment in self.snake.segments[
            :-1
        ]:  # Itération sur tout le serpent sauf la tête
            if segment == head:
                self.running = False
                self.is_game_over = True
                break

    def check_eating_food(self):
        """Vérifie si le serpent a mangé une unité de nourriture."""
        head = self.snake.segments[-1]
        if head == self.food.position:
            self.snake.grow()
            self.food.position = self.food.create_food_position()
            self.food.draw_food()
            self.score += 10
            self.update_score()

    def update(self):
        """Mise à jour du jeu après une action si le jeu est "on"."""
        if self.running:
            self.snake.move()
            self.check_collision()
            self.end_game()
            self.check_eating_food()
            self.snake.draw_snake()
            self.update_score()
            self.root.after(100, self.update)

    def update_score(self):
        """Met à jour le label du score sur le canevas."""
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

    def display_game_over(self):
        """Affiche le message "Game over !"""
        if self.is_game_over:
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()

            self.canvas.create_text(
                width // 2,
                height // 2,
                text="GAME OVER!",
                fill=config.COULEUR_ECRITURE,
                font=(config.POLICE_ECRITURE, 26),
            )
            self.canvas.create_text(
                width // 2,
                height // 2 + 30,
                text=f"Score: {self.score}",
                fill=config.COULEUR_ECRITURE,
                font=(config.POLICE_ECRITURE, 26),
            )

    def end_game(self):
        """Arrête le jeu."""
        if self.is_game_over:
            self.display_game_over()
