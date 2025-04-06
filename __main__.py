import tkinter as tk
import tkinter.ttk as ttk
import datetime
import sqlite3
import logging
from pydantic import BaseModel
from enum import Enum
import logging

logger = logging.getLogger(__name__)

# 1. display search bar
# 2. Add game


class Material(Enum):
    VISUAL = 1
    VERBAL = 2
    TACTILE = 3
    AUDITIF = 4


class CognitiveCategory(BaseModel):
    name: str


class CognitiveFunction(BaseModel):
    name: str


class Game(BaseModel):
    title: str
    description: str = ""
    categories: list[tuple[CognitiveCategory, int]]
    functions: list[tuple[CognitiveFunction, int]]


class Database:
    def __init__(self, file: str = "DO_NOT_REMOVE.db"):
        self.con = sqlite3.connect(file)

    def setup(self):
        logger.info("Setting up database")
        self._setup_cognitive_category()
        self._setup_cognitive_function()
        self._setup_game()
        self.con.commit()

    def _setup_cognitive_category(self):
        logger.info("Setting up cognitive_categories table")
        self.con.execute(
            """
            CREATE TABLE if NOT EXISTS cognitive_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

    def _setup_cognitive_function(self):
        logger.info("Setting up cognitive_functions table")
        self.con.execute(
            """
            CREATE TABLE if NOT EXISTS cognitive_functions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

    def _setup_game(self):
        logger.info("Setting up games table")
        self.con.execute(
            """
            CREATE TABLE if NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL UNIQUE,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


class Window(tk.Tk):
    def __init__(self, db: Database):
        super().__init__()
        self.title("Neuropsy Games")
        self.geometry("800x600")

        self.db = db

        self._setup_add_game()
        self._setup_add_cognitive_category()
        self._setup_add_cognitive_function()

    def _setup_add_game(self):
        ttk.Label(self, text="Add a Game").pack()
        ttk.Label(self, text="Title").pack()
        self._add_game_title = ttk.Entry(self)
        self._add_game_title.pack()
        ttk.Label(self, text="Description").pack()
        self._add_game_description = ttk.Entry(self)
        self._add_game_description.pack()
        # Categories
        self._add_game_button = ttk.Button(self, text="Add Game")
        self._add_game_button.pack()

    def _setup_add_cognitive_category(self):
        ttk.Label(self, text="Add a Cognitive Category").pack()
        ttk.Label(self, text="Title").pack()
        self._add_cognitive_category_title = ttk.Entry(self)
        self._add_cognitive_category_title.pack()
        self._add_cognitive_category_button = ttk.Button(
            self, text="Add a Cognitive Category"
        )
        self._add_cognitive_category_button.pack()

    def _setup_add_cognitive_function(self):
        ttk.Label(self, text="Add a Cognitive Function").pack()
        ttk.Label(self, text="Title").pack()
        self._add_cognitive_function_title = ttk.Entry(self)
        self._add_cognitive_function_title.pack()
        self._add_cognitive_function_button = ttk.Button(
            self, text="Add a Cognitive Function"
        )
        self._add_cognitive_function_button.pack()


if __name__ == "__main__":
    db = Database()
    db.setup()

    window = Window(db)
    window.mainloop()
