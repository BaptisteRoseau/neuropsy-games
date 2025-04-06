import tkinter as tk
import tkinter.ttk as ttk
import logging
import tkinter.filedialog as filedialog

from models import Game, CognitiveCategory, CognitiveFunction, Material
from database import Database

logger = logging.getLogger(__name__)


class Window(tk.Tk):
    def __init__(self, db: Database):
        super().__init__()
        self.title("Neuropsy Games")

        self.db = db

        self._setup_add_game()
        self._setup_add_cognitive_category()
        self._setup_add_cognitive_function()

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
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(
                self._add_game_frame, text=category.name, variable=var
            )
            chk.pack(anchor=tk.W)
            self._add_game_categories[category.id] = var  # Use category.id as the key

        # Functions
        ttk.Label(self._add_game_frame, text="Functions").pack()
        self._add_game_functions = {}
        for function in self.db.get_all_cognitive_functions():
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(
                self._add_game_frame, text=function.name, variable=var
            )
            chk.pack(anchor=tk.W)
            self._add_game_functions[function.id] = var  # Use function.id as the key

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

    def _add_game_to_db(self):
        title = self._add_game_title.get()
        description = self._add_game_description.get()
        image = (
            self._add_game_image_path.get()
        )  # Updated to use the selected image path
        materials = [
            material for material, var in self._add_game_materials.items() if var.get()
        ]
        categories = [
            category_id
            for category_id, var in self._add_game_categories.items()
            if var.get()
        ]
        functions = [
            function_id
            for function_id, var in self._add_game_functions.items()
            if var.get()
        ]

        game = Game(
            title=title,
            description=description,
            image=image,
            materials=materials,
            categories=[
                (CognitiveCategory(id=category_id), 1) for category_id in categories
            ],  # Default weight of 1
            functions=[
                (CognitiveFunction(id=function_id), 1) for function_id in functions
            ],  # Default weight of 1
        )
        self.db.add_game(game)

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
            self._add_cognitive_category_frame, text="Add a Cognitive Category"
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
            self._add_cognitive_function_frame, text="Add a Cognitive Function"
        )
        self._add_cognitive_function_button.pack()


if __name__ == "__main__":
    db = Database()
    db.setup()

    window = Window(db)
    window.mainloop()
