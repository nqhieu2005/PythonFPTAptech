import tkinter as tk 
from tkinter import messagebox, Toplevel, Label, Button

BOARD_SIZE = 10

class CaroGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Cờ Caro - Tkinter")
        self.root.configure(bg = "#D4E6F1")

        self.center_window(self.root, 500, 600)

        self.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = "X"

        