import tkinter as tk
import tkinter.ttk as ttk
import logging

from ui.game_detail import GameDetailFrame
from database import Database

logger = logging.getLogger(__name__)


class SearchBarWithAutocompleteFrame(ttk.Frame):
    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.db: Database = db
        self.parent = parent
        self.selected_game: GameDetailFrame|None = None

        # Search bar (Entry widget)
        ttk.Label(self, text="Search Games", font=("Arial", 16)).pack(pady=10)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self, textvariable=self.search_var)
        self.search_entry.pack(fill=tk.X, padx=10, pady=5)
        self.search_entry.bind("<KeyRelease>", self._on_key_release)
        self.search_entry.bind(
            "<KeyRelease>",
            lambda _: (
                self.result_listbox.pack_forget()
                if len(self.result_listbox.get(0)) == 0
                else self.result_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            ),
            add=True,
        )

        # Filters
        ttk.Label(self, text="Filters").pack(pady=5)
        self.filter_frame = ttk.Frame(self)
        self.filter_frame.pack(fill=tk.X, padx=10)

        ttk.Label(self.filter_frame, text="Material:").grid(row=0, column=0, padx=5)
        self.material_filter = ttk.Combobox(self.filter_frame, values=["All", "Visual", "Verbal", "Tactile", "Auditory"])
        self.material_filter.grid(row=0, column=1, padx=5)

        ttk.Label(self.filter_frame, text="Category:").grid(row=1, column=0, padx=5)
        self.category_filter = ttk.Entry(self.filter_frame)
        self.category_filter.grid(row=1, column=1, padx=5)

        ttk.Label(self.filter_frame, text="Function:").grid(row=2, column=0, padx=5)
        self.function_filter = ttk.Entry(self.filter_frame)
        self.function_filter.grid(row=2, column=1, padx=5)

        # Search Button
        ttk.Button(self, text="Search", command=self._search).pack(pady=10)

        # Listbox for autocompletion
        self.result_listbox = tk.Listbox(self)
        self.result_listbox.bind("<<ListboxSelect>>", self._on_select)

    def _on_key_release(self, event):
        # Fetch matching game titles
        query = self.search_var.get()
        if len(query) >= 2:
            try:
                matches = [game.title for game in self.db.get_game(game_title=query)]
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
            if self.selected_game:
                self.selected_game.destroy()
            selected_game = self.result_listbox.get(selected_index)
            self.selected_game = GameDetailFrame(
                self.parent,
                self.db.get_game(game_title=selected_game)[0],
            ).pack(fill=tk.BOTH, expand=True)

    def _search(self):
        # Logic to perform search with filters
        pass


class SearchBarFrame(ttk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db

        # Title
        ttk.Label(self, text="Search Games", font=("Arial", 16)).pack(pady=10)

        # Search bar
        self.search_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.search_var).pack(fill=tk.X, padx=10, pady=5)

        # Filters
        ttk.Label(self, text="Filters").pack(pady=5)
        filter_frame = ttk.Frame(self)
        filter_frame.pack(fill=tk.X, padx=10)

        ttk.Label(filter_frame, text="Material:").grid(row=0, column=0, padx=5)
        self.material_filter = ttk.Combobox(filter_frame, values=["All", "Visual", "Verbal", "Tactile", "Auditory"])
        self.material_filter.grid(row=0, column=1, padx=5)

        ttk.Label(filter_frame, text="Category:").grid(row=1, column=0, padx=5)
        self.category_filter = ttk.Entry(filter_frame)
        self.category_filter.grid(row=1, column=1, padx=5)

        ttk.Label(filter_frame, text="Function:").grid(row=2, column=0, padx=5)
        self.function_filter = ttk.Entry(filter_frame)
        self.function_filter.grid(row=2, column=1, padx=5)

        # Search Button
        ttk.Button(self, text="Search", command=self._search).pack(pady=10)

    def _search(self):
        # Placeholder for search logic
        print("Search triggered")
