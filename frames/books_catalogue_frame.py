from customtkinter import CTkFrame, CTkFont, BOTH
from tkinter import ttk

from services.database_handler import DatabaseHandler
from objects.book import Book
import general.general_methods as gm

class BooksCatalogueFrame(CTkFrame):
    def __init__(self, master, default_font : CTkFont, database_handler_obj : DatabaseHandler, **kwargs):
        super().__init__(master, **kwargs)
        self.books = {}
        self.default_font = default_font
        self.database_handler = database_handler_obj
        self.last_selected_book : Book = None
        self.handler = lambda a : None

        gm.get_style()

        self.table = ttk.Treeview(self, columns=["name", "author", "year", "description"],
                                  show="headings", style="Custom.Treeview", selectmode="browse")

        self.table.tag_configure("evenrow", background="lightgray")
        self.table.heading("name", text="Name")
        self.table.heading("author", text="Author")
        self.table.heading("year", text="Year")
        self.table.heading("description", text="Description")

        self.table.column("name", anchor="center", minwidth=10)
        self.table.column("author", anchor="center", minwidth=10)
        self.table.column("year", anchor="center", minwidth=10, width=55)
        self.table.column("description", anchor="center", minwidth=10, width=100)

        self.table.bind("<ButtonRelease-1>", self.on_selection_changed)

        self.fill_table()
        
        self.table.pack(fill=BOTH, expand=True)

    def bind_on_selection_changed(self, handler):
        self.handler = handler

    def on_selection_changed(self, event):
        if self.last_selected_book == self.get_selected_item(): return
        self.last_selected_book = self.get_selected_item()
        self.handler(event)

    def fill_table(self):
        was_selected = None
        if len(self.table.selection()) != 0:
            was_selected = self.table.selection()
        self.books = self.database_handler.get_books()
        for item in self.table.get_children():
            self.table.delete(item)
        for book in self.books.catalogue:
            tag = "evenrow" if book.id % 2 == 0 else ""
            self.table.insert("", "end", values=(book.name, book.author, book.year, book.description), iid = book.id, tags=tag)
        if was_selected is not None:
            self.table.selection_set(was_selected)

    def get_selected_item(self):
        if len(self.table.selection()) == 0: return None      
        return self.books.catalogue[int(self.table.selection()[0]) - 1]
    
    def get_catalogue(self):
        return self.books
        

