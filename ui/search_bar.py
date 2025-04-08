import tkinter as tk
import tkinter.ttk as ttk
import logging

from ui.game.game_list import GameListFrame
from database import Database
from models import Material

logger = logging.getLogger(__name__)

# TODO: Refresh the cognitive functions and categories dynamically
# TODO: Fix database searching for filters

class SearchBarFrame(ttk.Frame):
    db: Database
    material_vars: dict[Material, tk.BooleanVar]
    category_vars: dict[str, tuple[tk.BooleanVar, int]]
    function_vars: dict[str, tuple[tk.BooleanVar, int]]

    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.db = db

        # Title
        ttk.Label(self, text="Search Games", font=("Arial", 16)).pack(pady=10)

        # Search bar
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self, textvariable=self.search_var)
        self.search_entry.pack(fill=tk.X, padx=10, pady=5)
        self.search_entry.bind("<KeyRelease>", self._on_key_release)

        # Filters
        ttk.Label(self, text="Filters").pack(pady=5)
        filter_frame = ttk.Frame(self)
        filter_frame.pack(fill=tk.X, padx=10)

        # Material filter
        ttk.Label(filter_frame, text="Material:").grid(row=0, column=0, padx=5)
        self.material_vars = {
            material: tk.BooleanVar()
            for material in Material
        }
        for i, (material, var) in enumerate(self.material_vars.items()):
            ttk.Checkbutton(filter_frame, text=material.name, variable=var).grid(
                row=0, column=i + 1, padx=5
            )

        # Category filter
        ttk.Label(filter_frame, text="Category:").grid(row=1, column=0, padx=5)
        self.category_vars = {}
        self.category_frame = ttk.Frame(filter_frame)
        self.category_frame.grid(row=1, column=1, columnspan=4, sticky="w")
        categories = (
            self.db.get_all_cognitive_categories()
        )
        for i, category in enumerate(categories):
            var = tk.BooleanVar()
            self.category_vars[category.name] = (var, category.id)
            ttk.Checkbutton(self.category_frame, text=category.name, variable=var).grid(
                row=0, column=i, padx=5
            )

        # Function filter
        ttk.Label(filter_frame, text="Function:").grid(row=2, column=0, padx=5)
        self.function_vars = {}
        self.function_frame = ttk.Frame(filter_frame)
        self.function_frame.grid(row=2, column=1, columnspan=4, sticky="w")
        functions = self.db.get_all_cognitive_functions()  # Dynamically load functions
        for i, function in enumerate(functions):
            var = tk.BooleanVar()
            self.function_vars[function.name] = (var, function.id)
            ttk.Checkbutton(self.function_frame, text=function.name, variable=var).grid(
                row=0, column=i, padx=5
            )

        # Search Button
        ttk.Button(self, text="Search", command=self._search).pack(pady=10)

        # Game List Frame
        self.game_list_frame = GameListFrame(self, self.db)
        self.game_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _on_key_release(self, event):
        # Trigger search only if at least 2 characters are entered
        query = self.search_var.get()
        if len(query) >= 2:
            self._search()

    def _search(self):
        # Collect filters
        game_title = self.search_var.get() if len(self.search_var.get()) >= 2 else None
        materials = [
            material for material, var in self.material_vars.items() if var.get()
        ]
        category_ids = [
            _id for _, (var, _id) in self.category_vars.items() if var.get()
        ]
        function_ids = [
            _id for _, (var, _id) in self.function_vars.items() if var.get()
        ]

        try:
            # Fetch games from the database
            games = self.db.get_games_with_filters(
                game_title=game_title,
                cognitive_categories_ids=category_ids,
                cognitive_functions_ids=function_ids,
                materials=materials,
            )
            # Update GameListFrame with search results
            self.game_list_frame.update_games(games)
        except Exception as e:
            logger.error(f"Error during search: {e}")
