import tkinter as tk
import tkinter.ttk as ttk
import logging
from PIL import Image, ImageTk
from models import Game

logger = logging.getLogger(__name__)

NO_IMAGE_PATH = "assets/no_image.png"

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

        image_path = self.game.image if self.game.image else NO_IMAGE_PATH

        try:
            image = Image.open(image_path)
            image = image.resize((150, 150))
            self.image_tk = ImageTk.PhotoImage(image)
            self.image_label = ttk.Label(self.image_frame, image=self.image_tk)
            self.image_label.pack()
        except Exception as e:
            logger.error(f"Error loading image: {e}")
            self.image_label = ttk.Label(
                self.image_frame, text="Image not available"
            )
            self.image_label.pack()

        # Right section: Game details
        self.details_frame = ttk.Frame(self.container)
        self.details_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        ttk.Label(
            self.details_frame,
            text=f"{self.game.title}",
            font=("Arial", 14, "bold"),
        ).pack(anchor=tk.W, pady=5)
        ttk.Label(
            self.details_frame,
            text=f"{self.game.description}",
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
                self.details_frame, text=f"- {category.name} ({weight})"
            ).pack(anchor=tk.W)

        ttk.Label(
            self.details_frame, text="Cognitive Functions:", font=("Arial", 12, "bold")
        ).pack(anchor=tk.W, pady=5)
        for function, weight in self.game.functions:
            ttk.Label(
                self.details_frame, text=f"- {function.name} ({weight})"
            ).pack(anchor=tk.W)
