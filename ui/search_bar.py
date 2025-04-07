import tkinter as tk
import tkinter.ttk as ttk
import logging

from database import Database

logger = logging.getLogger(__name__)


class SearchBarWithAutocomplete(ttk.Frame):
    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.db = db

        # Search bar (Entry widget)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self, textvariable=self.search_var)
        self.search_entry.pack(fill=tk.X, padx=5, pady=5)
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
            selected_game = self.result_listbox.get(selected_index)
            print(f"Selected game: {selected_game}")  # Replace with desired action
