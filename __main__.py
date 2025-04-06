import tkinter as tk
import tkinter.ttk as ttk
import logging
import tkinter.filedialog as filedialog

from models import Game, CognitiveCategory, CognitiveFunction, Material
from database import Database, DuplicateError

logger = logging.getLogger(__name__)


class SearchBarWithAutocomplete(ttk.Frame):
    def __init__(self, parent, get_game_callback):
        super().__init__(parent)
        self.get_game_callback = get_game_callback

        # Search bar (Entry widget)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self, textvariable=self.search_var)
        self.search_entry.pack(fill=tk.X, padx=5, pady=5)
        self.search_entry.bind("<KeyRelease>", self._on_key_release)

        # Listbox for autocompletion
        self.result_listbox = tk.Listbox(self)
        self.result_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.result_listbox.bind("<<ListboxSelect>>", self._on_select)

    def _on_key_release(self, event):
        # Fetch matching game titles
        query = self.search_var.get()
        if len(query) >= 2:
            try:
                matches = [game.title for game in self.get_game_callback(query)]
                self._update_listbox(matches)
            except Exception as e:
                logger.error(f"Error fetching games: {e}")
                self._update_listbox([])  # Clear the listbox on error
        else:
            self._update_listbox([])

    def _update_listbox(self, matches):
        # Clear the Listbox and populate it with new matches
        self.result_listbox.delete(0, tk.END)
        for match in matches:
            self.result_listbox.insert(tk.END, match)

    def _on_select(self, event):
        # Handle selection from the Listbox
        selected_index = self.result_listbox.curselection()
        if selected_index:
            selected_game = self.result_listbox.get(selected_index)
            print(f"Selected game: {selected_game}")  # Replace with desired action


class Window(tk.Tk):
    def __init__(self, db: Database):
        super().__init__()
        self.title("Neuropsy Games")

        self.db = db

        self._setup_add_game()
        self._setup_add_cognitive_category()
        self._setup_add_cognitive_function()
        self.search_bar = SearchBarWithAutocomplete(
            self, lambda query: self.db.get_game(game_title=query)
        )
        self.search_bar.pack(fill=tk.X, padx=10, pady=10)

    def _setup_add_game(self):
        self._add_game_frame = ttk.Frame(self)
        self._add_game_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(self._add_game_frame, text="Add a Game").pack()

        # Title
        ttk.Label(self._add_game_frame, text="Title").pack()
        self._add_game_title = ttk.Entry(self._add_game_frame)
        self._add_game_title.pack()

        # Description
        ttk.Label(self._add_game_frame, text="Description").pack()
        self._add_game_description = ttk.Entry(self._add_game_frame)
        self._add_game_description.pack()

        # Image
        ttk.Label(self._add_game_frame, text="Image").pack()
        self._add_game_image_path = tk.StringVar()
        self._add_game_image_label = ttk.Label(
            self._add_game_frame, textvariable=self._add_game_image_path
        )
        self._add_game_image_label.pack()
        self._add_game_image_button = ttk.Button(
            self._add_game_frame, text="Select Image", command=self._select_image_file
        )
        self._add_game_image_button.pack()

        # Materials
        ttk.Label(self._add_game_frame, text="Materials").pack()
        self._add_game_materials = {}
        for material in Material:
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(
                self._add_game_frame, text=material.name, variable=var
            )
            chk.pack(anchor=tk.W)
            self._add_game_materials[material] = var

        # Categories
        ttk.Label(self._add_game_frame, text="Categories").pack()
        self._add_game_categories = {}
        for category in self.db.get_all_cognitive_categories():
            frame = ttk.Frame(self._add_game_frame)
            frame.pack(anchor=tk.W)
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(frame, text=category.name, variable=var)
            chk.pack(side=tk.LEFT)
            weight_entry = ttk.Entry(frame, width=5)
            weight_entry.pack(side=tk.LEFT, padx=5)
            self._add_game_categories[category.id] = (var, weight_entry)

        # Functions
        ttk.Label(self._add_game_frame, text="Functions").pack()
        self._add_game_functions = {}
        for function in self.db.get_all_cognitive_functions():
            frame = ttk.Frame(self._add_game_frame)
            frame.pack(anchor=tk.W)
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(frame, text=function.name, variable=var)
            chk.pack(side=tk.LEFT)
            weight_entry = ttk.Entry(frame, width=5)
            weight_entry.pack(side=tk.LEFT, padx=5)
            self._add_game_functions[function.id] = (var, weight_entry)

        # Add Game Button
        self._add_game_button = ttk.Button(
            self._add_game_frame, text="Add Game", command=self._add_game_to_db
        )
        self._add_game_button.pack()

    def _select_image_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("All Files", "*.*"),
            ],
        )
        if file_path:
            self._add_game_image_path.set(file_path)

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

    def _add_game_to_db(self):
        title = self._add_game_title.get()
        if title == "":
            ttk.Label(self, text="Title cannot be empty!").pack()
            return

        description = self._add_game_description.get()
        image = self._add_game_image_path.get()
        materials = [
            material for material, var in self._add_game_materials.items() if var.get()
        ]
        categories = [
            (
                self.db.get_cognitive_category_by_id(category_id),
                int(weight_entry.get()) if weight_entry.get().isdigit() else None,
            )
            for category_id, (var, weight_entry) in self._add_game_categories.items()
            if var.get()
        ]
        functions = [
            (
                self.db.get_cognitive_function_by_id(function_id),
                int(weight_entry.get()) if weight_entry.get().isdigit() else None,
            )
            for function_id, (var, weight_entry) in self._add_game_functions.items()
            if var.get()
        ]

        for item in categories + functions:
            if item[1] and item[1] < 0 and item[1] > 10:
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
