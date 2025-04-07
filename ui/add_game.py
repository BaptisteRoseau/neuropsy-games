import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from models import Material


class AddGameFrame(ttk.Frame):
    def __init__(self, parent, db, add_game_callback):
        super().__init__(parent)
        self.db = db
        self.add_game_callback = add_game_callback

        ttk.Label(self, text="Add a Game").pack()

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
        self.image_label = ttk.Label(self, textvariable=self.image_path)
        self.image_label.pack()
        self.image_button = ttk.Button(
            self, text="Select Image", command=self._select_image_file
        )
        self.image_button.pack()

        # Materials
        ttk.Label(self, text="Materials").pack()
        self.materials = {}
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
            weight_slider = ttk.Scale(frame, from_=0, to=10, orient="horizontal")
            weight_slider.pack(side=tk.LEFT, padx=5)
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
            int_var = tk.IntVar()
            weight_slider = ttk.Scale(
                frame,
                from_=0,
                to=10,
                orient="horizontal",
                variable=int_var,
                command=lambda value: int_var.set(int(float(value))),
            )
            weight_slider.pack(side=tk.LEFT, padx=5)
            ttk.Label(frame, textvariable=int_var).pack(side=tk.LEFT, padx=5)
            self.functions[function.id] = (var, weight_slider)

        # Add Game Button
        self.add_game_button = ttk.Button(
            self, text="Add Game", command=self.add_game_callback
        )
        self.add_game_button.pack()

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
