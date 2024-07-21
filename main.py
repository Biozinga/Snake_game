"""
Module principal pour lancer le jeu Snake.

Ce module initialise une instance de Tkinter et crée le jeu Snake en utilisant
la classe Game.
"""

from game import Game
import tkinter as tk


def main():
    """Fonction principale pour démarrer le jeu Snake."""
    # Crée une instance de Tk
    root = tk.Tk()
    root.title("Snake_game")
    # Crée une instance de la classe Game en passant l'instance root
    game = Game(root)
    # Démarre la boucle principale de Tkinter
    root.mainloop()


if __name__ == "__main__":
    main()
