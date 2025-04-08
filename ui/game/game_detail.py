import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from models import Game


class GameDetailFrame(ttk.Frame):
    def __init__(self, parent, game: Game):
        super().__init__(parent)
        self.game = game

        # Main container
        self.container = ttk.Frame(self, padding=10)
        self.container.pack(fill=tk.BOTH, expand=True)

        # Left section: Game image
        self.image_frame = ttk.Frame(self.container)
        self.image_frame.pack(side=tk.LEFT, padx=10, pady=10)

        if self.game.image:
            try:
                image = Image.open(self.game.image)
                image = image.resize((150, 150), Image.ANTIALIAS)
                self.image_tk = ImageTk.PhotoImage(image)
                self.image_label = ttk.Label(self.image_frame, image=self.image_tk)
                self.image_label.pack()
            except Exception as e:
                self.image_label = ttk.Label(
                    self.image_frame, text="Image not available"
                )
                self.image_label.pack()

        # Right section: Game details
        self.details_frame = ttk.Frame(self.container)
        self.details_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        ttk.Label(
            self.details_frame,
            text=f"Title: {self.game.title}",
            font=("Arial", 14, "bold"),
        ).pack(anchor=tk.W, pady=5)
        ttk.Label(
            self.details_frame,
            text=f"Description: {self.game.description}",
            wraplength=400,
        ).pack(anchor=tk.W, pady=5)

        ttk.Label(
            self.details_frame, text="Materials:", font=("Arial", 12, "bold")
        ).pack(anchor=tk.W, pady=5)
        for material in self.game.materials:
            ttk.Label(self.details_frame, text=f"- {material.name}").pack(anchor=tk.W)

        ttk.Label(
            self.details_frame, text="Cognitive Categories:", font=("Arial", 12, "bold")
        ).pack(anchor=tk.W, pady=5)
        for category, weight in self.game.categories:
            ttk.Label(
                self.details_frame, text=f"- {category.name} (Weight: {weight})"
            ).pack(anchor=tk.W)

        ttk.Label(
            self.details_frame, text="Cognitive Functions:", font=("Arial", 12, "bold")
        ).pack(anchor=tk.W, pady=5)
        for function, weight in self.game.functions:
            ttk.Label(
                self.details_frame, text=f"- {function.name} (Weight: {weight})"
            ).pack(anchor=tk.W)
