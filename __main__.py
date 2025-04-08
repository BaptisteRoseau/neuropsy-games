import tkinter as tk
from tkinter import ttk
from database import Database
from ui.game.game_crud import GameCRUDFrame
from ui.category.category_crud import CategoryCRUDFrame
from ui.function.function_crud import FunctionCRUDFrame
from ui.search_bar import SearchBarFrame
from ui.game.game_list import GameListFrame


class MainApp(tk.Tk):
    def __init__(self, db: Database):
        super().__init__()
        self.title("Neuropsy Games")
        self.geometry("800x600")
        self.db = db
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self._add_tabs()
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    def _add_tabs(self):
        game_crud_frame = GameCRUDFrame(self, self.db)
        self.notebook.add(game_crud_frame, text="Games")

        category_crud_frame = CategoryCRUDFrame(self, self.db)
        self.notebook.add(category_crud_frame, text="Categories")

        function_crud_frame = FunctionCRUDFrame(self, self.db)
        self.notebook.add(function_crud_frame, text="Functions")

        self.search_frame = SearchBarFrame(self, self.db)
        self.notebook.add(self.search_frame, text="Search & List")

    def _on_tab_changed(self, event):
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        if selected_tab == "Search & List" and self.search_frame:
            self.search_frame.refresh()


if __name__ == "__main__":
    db = Database()
    db.setup()
    app = MainApp(db)
    app.mainloop()
