import os

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database import Database
from models import Game, Material


class CreateGameWindow(tk.Toplevel):
    db: Database
    materials: dict[Material, tk.BooleanVar]
    categories: dict[int, tuple[tk.BooleanVar, ttk.Scale]]
    functions: dict[int, tuple[tk.BooleanVar, ttk.Scale]]
    action_button: ttk.Button

    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.db = db
        self.title("Add Game")
        self.geometry("500x700")

        # Title
        ttk.Label(self, text="Title").pack()
        self.title_entry = ttk.Entry(self)
        self.title_entry.pack()

        # Description
        ttk.Label(self, text="Description").pack()
        self.description_entry = ttk.Entry(self)
        self.description_entry.pack()

        # Image
        ttk.Label(self, text="Image").pack()
        self.image_path = tk.StringVar()
        ttk.Entry(self, textvariable=self.image_path).pack()
        ttk.Button(self, text="Select Image", command=self._select_image_file).pack()

        # Materials
        ttk.Label(self, text="Materials").pack()
        self.materials: dict[Material, tk.BooleanVar] = {}
        for material in Material:
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(self, text=material.name, variable=var)
            chk.pack(anchor=tk.W)
            self.materials[material] = var

        # Categories
        ttk.Label(self, text="Categories").pack()
        self.categories = {}
        for category in self.db.get_all_cognitive_categories():
            frame = ttk.Frame(self)
            frame.pack(anchor=tk.W)
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(frame, text=category.name, variable=var)
            chk.pack(side=tk.LEFT)
            int_var = tk.IntVar(value=5)
            weight_slider = ttk.Scale(
                frame,
                from_=0,
                to=10,
                orient="horizontal",
                variable=int_var,
                command=lambda value, var=int_var: var.set(int(float(value))),
            )
            weight_slider.pack(side=tk.LEFT, padx=5)
            ttk.Label(frame, textvariable=int_var).pack(side=tk.LEFT, padx=5)
            self.categories[category.id] = (var, weight_slider)

        # Functions
        ttk.Label(self, text="Functions").pack()
        self.functions = {}
        for function in self.db.get_all_cognitive_functions():
            frame = ttk.Frame(self)
            frame.pack(anchor=tk.W)
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(frame, text=function.name, variable=var)
            chk.pack(side=tk.LEFT)
            int_var = tk.IntVar(value=5)
            weight_slider = ttk.Scale(
                frame,
                from_=0,
                to=10,
                orient="horizontal",
                variable=int_var,
                command=lambda value, var=int_var: var.set(int(float(value))),
            )
            weight_slider.pack(side=tk.LEFT, padx=5)
            ttk.Label(frame, textvariable=int_var).pack(side=tk.LEFT, padx=5)
            self.functions[function.id] = (var, weight_slider)

        # Add Button
        self.action_button = ttk.Button(self, text="Add", command=self._add_to_db)
        self.action_button.pack(pady=10)

    def _select_image_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("All Files", "*.*"),
            ],
        )
        if file_path:
            self.image_path.set(file_path)

    def _save_image(self, image_path: str):
        # create ./images directory if it doesn't exist
        if not os.path.exists("./images"):
            os.makedirs("./images")
        pass

    def _game_from_form(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        image = self.image_path.get()
        materials = [material for material, var in self.materials.items() if var.get()]
        categories = [
            (
                self.db.get_cognitive_category_by_id(category_id),
                int(weight_slider.get()),
            )
            for category_id, (var, weight_slider) in self.categories.items()
            if var.get()
        ]
        functions = [
            (
                self.db.get_cognitive_function_by_id(function_id),
                int(weight_slider.get()),
            )
            for function_id, (var, weight_slider) in self.functions.items()
            if var.get()
        ]

        if not title:
            messagebox.showerror("Error", "Title cannot be empty!")
            return

        return Game(
            title=title,
            description=description,
            image=image,
            materials=materials,
            categories=categories,
            functions=functions,
        )

    def _add_to_db(self):
        game = self._game_from_form()
        try:
            self.db.add_game(game)
            messagebox.showinfo("Success", "Game added successfully!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _populate_form(self, game: Game):
        # Populate title and description
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, game.title)
        self.description_entry.delete(0, tk.END)
        self.description_entry.insert(0, game.description)

        # Populate image path
        self.image_path.set(game.image)

        # Populate materials
        for material, var in self.materials.items():
            var.set(material in game.materials)

        # Populate categories
        for category_id, (var, weight_slider) in self.categories.items():
            category = next(
                (cat for cat, weight in game.categories if cat.id == category_id), None
            )
            if category:
                var.set(True)
                weight_slider.set(
                    next(
                        weight
                        for cat, weight in game.categories
                        if cat.id == category_id
                    )
                )

        # Populate functions
        for function_id, (var, weight_slider) in self.functions.items():
            function = next(
                (func for func, weight in game.functions if func.id == function_id),
                None,
            )
            if function:
                var.set(True)
                weight_slider.set(
                    next(
                        weight
                        for func, weight in game.functions
                        if func.id == function_id
                    )
                )
