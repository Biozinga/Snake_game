"""
Module pour le jeu Snake.

Ce module contient la classe Game qui gère la logique principale du jeu Snake.
"""

from tkinter import Canvas
from snake import Snake
from food import Food

import config
import os


class Game:
    def __init__(self, root):
        """Initialise le jeu Snake."""
        # Met le statut du jeu sur "On"
        self.is_game_over = False
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

        # Initialisation des éléments importants du jeu :
        # serpent, nourriture, score, niveau, vitesse et suivi des passages de niveau
        self.snake = Snake(self.canvas)  # Création du serpent
        self.snake_size = len(self.snake.segments)  # Taille initiale du serpent
        self.food = Food(self.canvas)  # Création de la nourriture
        self.food.draw_food()  # Dessin initial de la nourriture
        self.score = 0  # Score initial
        self.level = 1  # Niveau initial
        self.actual_snake_speed = (  # Vitesse initiale du serpent
            config.SNAKE_REFRESH_RATE
        )
        self.last_level_up_score = 0  # Score du dernier passage de niveau

        # Initialisation des statuts nessesaire au blink (clignotant) des messages
        self.blinking_game_over = False
        self.blinking_hight_score = False
        self.hight_score_pass = False

        # Obtenir le chemin du répertoire contenant le jeu
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Définir le chemin complet du fichier contenant le meilleur score
        self.high_score_file = os.path.join(current_dir, "high_score.txt")
        # Stocker le meilleur score
        self.high_score = self.read_high_score()

        # Lier les touches du clavier à la méthode on_key_press
        self.root.bind("<KeyPress>", self.on_key_press)

        # Afficher le score initial
        self.score_text = self.canvas.create_text(
            100,
            430,
            text=f"Score: {self.score}",
            fill=config.COULEUR_ECRITURE,
            font=(config.POLICE_ECRITURE, 16),
        )

        # Afficher le niveau initial
        # Stocke l'identifiant du texte "Level:"
        self.level_text_id = self.canvas.create_text(
            400,
            430,
            text=f"Level: {self.level}",
            fill=config.COULEUR_ECRITURE,
            font=(config.POLICE_ECRITURE, 16),
        )

        # Afficher le meilleur score
        # Stocke l'identifiant du texte "High score:"
        self.hight_score_text_id = self.canvas.create_text(
            250,
            430,
            text=f"High score: {self.high_score}",
            fill=config.COULEUR_ECRITURE,
            font=(config.POLICE_ECRITURE, 16),
        )

        # Change l'état du jeu de "off" à "on"
        self.running = True
        self.is_game_over = False

        # Planifie la première mise à jour
        self.root.after(self.actual_snake_speed, self.update)

    def read_high_score(self):
        """Fonction pour lire le meilleur score stocké dans le fichier texte"""
        if os.path.exists(self.high_score_file):
            with open(self.high_score_file, "r") as file:
                try:
                    return int(file.read().strip())
                except ValueError:
                    return 0
        else:
            return 0

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
            self.update_high_score()
            self.increase_level()
            self.root.after(self.actual_snake_speed, self.update)

    def update_score(self):
        """Met à jour le label du score sur le canevas."""
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

    def update_high_score(self):
        """
        Met à jour le meilleur score si le score actuel est supérieur
        au meilleur score précédent puis l'affiche."""
        if self.score > self.high_score:
            self.high_score = self.score
            self.canvas.itemconfig(
                self.hight_score_text_id, text=f"High score: {self.score}"
            )

            if not self.hight_score_pass:
                self.blink_hight_score()
                self.hight_score_pass = True

    def update_level(self):
        """Met à jour le label du niveau sur le canevas et le fait clignoter."""
        self.canvas.itemconfig(self.level_text_id, text=f"Level: {self.level}")
        self.blink_level(6)

    def increase_level(self):
        """Augmente le niveau en réduisant actual_snake_speed de 10 à chaque palier de 100 points."""
        if (
            self.score % 100 == 0
            and self.score != 0
            and self.score != self.last_level_up_score
        ):
            self.actual_snake_speed = max(self.actual_snake_speed - 10, 10)
            self.last_level_up_score = self.score
            self.level += 1
            self.update_level()

    def blink_level(self, count):
        """Fait clignoter le texte du niveau un certain nombre de fois."""
        if count > 0:
            current_state = self.canvas.itemcget(self.level_text_id, "state")
            new_state = "hidden" if current_state == "normal" else "normal"
            self.canvas.itemconfig(self.level_text_id, state=new_state)
            self.root.after(500, self.blink_level, count - 1)
        else:
            self.canvas.itemconfig(self.level_text_id, state="normal")

    def blink_hight_score(self):
        """Fait clignoter le message "High score:" si le meilleur score est battu."""
        if self.score == self.high_score:
            if self.hight_score_text_id is not None:
                if self.blinking_hight_score:
                    self.canvas.itemconfig(self.hight_score_text_id, state="hidden")
                else:
                    self.canvas.itemconfig(self.hight_score_text_id, state="normal")

                self.blinking_hight_score = not self.blinking_hight_score
                self.root.after(500, self.blink_hight_score)

    def write_to_high_score_file(self):
        """
        Écrit le meilleur score  dans le fichier contenant le meilleur score.
        """
        with open(self.high_score_file, "w") as file:
            file.write(str(self.high_score))

    def display_game_over(self):
        """Affiche le message "Game over !"""
        if self.is_game_over:
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()

            # Stocke l'identifiant du texte "GAME OVER!"
            self.game_over_text_id = self.canvas.create_text(
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

    def blink_game_over(self):
        """Fait clignoter le message "Game over !"."""
        if self.game_over_text_id is not None:
            if self.blinking_game_over:
                self.canvas.itemconfig(self.game_over_text_id, state="hidden")
            else:
                self.canvas.itemconfig(self.game_over_text_id, state="normal")

            self.blinking_game_over = not self.blinking_game_over
            self.root.after(500, self.blink_game_over)

    def end_game(self):
        """Arrête le jeu."""
        if self.is_game_over:
            self.display_game_over()
            self.blink_game_over()
            self.write_to_high_score_file()
            self.root.after(2000, self.snake.delete_snake)
            self.root.after(4000, lambda: self.canvas.delete("food"))
