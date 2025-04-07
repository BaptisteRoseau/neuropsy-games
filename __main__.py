import tkinter as tk
import tkinter.ttk as ttk
import logging
import tkinter.filedialog as filedialog

from models import Game, CognitiveCategory, CognitiveFunction, Material
from database import Database, DuplicateError
from ui.search_bar import SearchBarWithAutocompleteFrame
from ui.add_game import AddGameFrame

logger = logging.getLogger(__name__)

#FIXME: Saved cognitive functions and categories are saved under "Function Name" 
# and "Category Name" instead of their IDs.

class Window(tk.Tk):
    def __init__(self, db: Database):
        super().__init__()
        self.title("Neuropsy Games")

        self.db = db

        self.add_game_frame = AddGameFrame(self, self.db, self._add_game_to_db)
        self.add_game_frame.pack(fill=tk.X, padx=10, pady=10)

        self._setup_add_cognitive_category()
        self._setup_add_cognitive_function()
        self.search_bar = SearchBarWithAutocompleteFrame(self, self.db)
        self.search_bar.pack(fill=tk.X, padx=10, pady=10)

    def _add_game_to_db(self):
        title = self.add_game_frame.title_entry.get()
        if title == "":
            ttk.Label(self, text="Title cannot be empty!").pack()
            return

        description = self.add_game_frame.description_entry.get()
        image = self.add_game_frame.image_path.get()
        materials = [
            material
            for material, var in self.add_game_frame.materials.items()
            if var.get()
        ]
        categories = [
            (
                self.db.get_cognitive_category_by_id(category_id),
                int(weight_slider.get()) if weight_slider.get() else None,
            )
            for category_id, (var, weight_slider) in self.add_game_frame.categories.items()
            if var.get()
        ]
        functions = [
            (
                self.db.get_cognitive_function_by_id(function_id),
                int(weight_slider.get()) if weight_slider.get() else None,
            )
            for function_id, (var, weight_slider) in self.add_game_frame.functions.items()
            if var.get()
        ]

        for item in categories + functions:
            if item[1] and (item[1] < 0 or item[1] > 10):
                ttk.Label(self, text="Weight must be between 0 and 10!").pack()
                return

        game = Game(
            title=title,
            description=description,
            image=image,
            materials=materials,
            categories=categories,
            functions=functions,
        )
        try:
            self.db.add_game(game)
            ttk.Label(self, text="Game added!").pack()
            logger.info(f"Game added: {game.title}")
        except DuplicateError as e:
            ttk.Label(self, text="This game already exist!").pack()
            logger.error(f"Duplicate game error: {e}")

    def _setup_add_cognitive_category(self):
        self._add_cognitive_category_frame = ttk.Frame(self)
        self._add_cognitive_category_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(
            self._add_cognitive_category_frame, text="Add a Cognitive Category"
        ).pack()
        ttk.Label(self._add_cognitive_category_frame, text="Title").pack()
        self._add_cognitive_category_title = ttk.Entry(
            self._add_cognitive_category_frame
        )
        self._add_cognitive_category_title.pack()
        self._add_cognitive_category_button = ttk.Button(
            self._add_cognitive_category_frame,
            text="Add a Cognitive Category",
            command=self._add_cognitive_category_to_db,
        )
        self._add_cognitive_category_button.pack()

    def _setup_add_cognitive_function(self):
        self._add_cognitive_function_frame = ttk.Frame(self)
        self._add_cognitive_function_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(
            self._add_cognitive_function_frame, text="Add a Cognitive Function"
        ).pack()
        ttk.Label(self._add_cognitive_function_frame, text="Title").pack()
        self._add_cognitive_function_title = ttk.Entry(
            self._add_cognitive_function_frame
        )
        self._add_cognitive_function_title.pack()
        self._add_cognitive_function_button = ttk.Button(
            self._add_cognitive_function_frame,
            text="Add a Cognitive Function",
            command=self._add_cognitive_function_to_db,
        )
        self._add_cognitive_function_button.pack()

    def _add_cognitive_category_to_db(self):
        title = self._add_cognitive_category_title.get()
        if title == "":
            ttk.Label(self, text="Title cannot be empty!").pack()
            return

        category = CognitiveCategory(name=title)

        try:
            self.db.add_cognitive_category(category)
            ttk.Label(self, text="Cognitive Category added!").pack()
            logger.info(f"Cognitive Category added: {category.name}")
            self._refresh_cognitive_categories()  # Refresh categories in _add_game_frame
        except DuplicateError as e:
            ttk.Label(self, text="This cognitive category already exist!").pack()
            logger.error(f"Duplicate cognitive category error: {e}")

    def _add_cognitive_function_to_db(self):
        title = self._add_cognitive_function_title.get()
        if title == "":
            ttk.Label(self, text="Title cannot be empty!").pack()
            return

        function = CognitiveFunction(name=title)

        try:
            self.db.add_cognitive_function(function)
            ttk.Label(self, text="Cognitive Function added!").pack()
            logger.info(f"Cognitive Function added: {function.name}")
            self._refresh_cognitive_functions()  # Refresh functions in _add_game_frame
        except DuplicateError as e:
            ttk.Label(self, text="This cognitive function already exist!").pack()
            logger.error(f"Duplicate cognitive function error: {e}")

    def _refresh_cognitive_categories(self):
        # Clear existing categories
        # TODO
        pass

    def _refresh_cognitive_functions(self):
        # Clear existing functions
        # TODO
        pass


if __name__ == "__main__":
    db = Database()
    db.setup()

    window = Window(db)
    window.mainloop()
