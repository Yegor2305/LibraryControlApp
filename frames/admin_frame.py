from customtkinter import *
from frames.books_catalogue_frame import BooksCatalogueFrame
from tkinter import ttk
from tkinter import Event
import datetime as dt
from PIL import Image
from typing import Literal

from services.database_handler import DatabaseHandler
from objects.book import Book

class AdminFrame(CTkFrame):
    def __init__(self, master, default_font : CTkFont,
                database_handler_obj : DatabaseHandler,
                back_button_command : callable, **kwargs):
        super().__init__(master, **kwargs)

        self.default_font = default_font
        self.database_handler = database_handler_obj
        self.back_button_command = back_button_command
        self.users = self.database_handler.get_users()
   
        #region Catalogue

        self.catalogue_label = CTkLabel(self, font=self.default_font, text="All books")
        self.catalogue_label.grid(column=0, row=0)

        self.catalogue = BooksCatalogueFrame(self, self.default_font, self.database_handler)       
        self.catalogue.grid(column=0, row=1, rowspan=5, padx=5, sticky="nwse")

        self.catalogue.bind_on_selection_changed(self.on_book_selected)

        #region Inputs
        self.inputs_label = CTkLabel(self, font=self.default_font, text="Add book").grid(column=1, columnspan=2, row=0)

        self.name_entry = CTkEntry(self, placeholder_text="Name", border_color="black",
                                    corner_radius=15, width=200, height=30, font=self.default_font)
        self.name_entry.grid(column=1, row=1)

        self.author_entry = CTkEntry(self, placeholder_text="Author", border_color="black",
                                    corner_radius=15, width=200, height=30, font=self.default_font)
        self.author_entry.grid(column=1, row=2)

        self.year_entry = CTkEntry(self, placeholder_text="Year", border_color="black",
                                    corner_radius=15, width=200, height=30, font=self.default_font)
        self.year_entry.grid(column=1, row=3)
        self.year_entry.bind("<Key>", self.only_numbers)

        self.description_entry = CTkEntry(self, placeholder_text="Description", border_color="black",
                                    corner_radius=15, width=200, height=30, font=self.default_font)
        self.description_entry.grid(column=1, row=4)

        self.quantity_entry = CTkEntry(self, placeholder_text="Quantity", border_color="black",
                                    corner_radius=15, width=200, height=30, font=self.default_font)
        self.quantity_entry.grid(column=1, row=5)
        self.quantity_entry.bind("<Key>", self.only_numbers)

        self.add_book_button = CTkButton(self, width = 35, text="\u2795", font=self.default_font,
                                        corner_radius=15, command=self.add_book_button_click)
        self.add_book_button.grid(column=2, row=1, rowspan=5, sticky="ns", padx=5)

        #endregion

        #endregion

        #region TakenByTable

        self.taken_by_label = CTkLabel(self, font=self.default_font, text="Taken by")
        self.taken_by_label.grid(column=0, row=6)

        #region Table
        self.taken_by_table = self.table = ttk.Treeview(self, columns=["login", "phone", "from", "to", "penalty"],
                                  show="headings", style="Custom.Treeview", selectmode="browse")
    
        self.taken_by_table.tag_configure("evenrow", background="lightgray")
        self.taken_by_table.heading("login", text="Login")
        self.taken_by_table.heading("phone", text="Phone")
        self.taken_by_table.heading("from", text="From")
        self.taken_by_table.heading("to", text="To")
        self.taken_by_table.heading("penalty", text="Penalty")

        self.taken_by_table.column("login", anchor="center", minwidth=10, width=120)
        self.taken_by_table.column("phone", anchor="center", minwidth=10, width=150)
        self.taken_by_table.column("from", anchor="center", minwidth=10, width=100)
        self.taken_by_table.column("to", anchor="center", minwidth=10, width=100)
        self.taken_by_table.column("penalty", anchor="center", minwidth=10, width=100)

        self.taken_by_table.grid(column=0, row=7, rowspan=5, padx=5, sticky="nwse")
        #endregion

        self.returns_button = CTkButton(self, height=30, corner_radius=15, command=self.returns_button_click,
                                        text="Returns", font=self.default_font)
        self.returns_button.grid(row=7, column=1, padx=5, columnspan=2, sticky="nwe")


        #endregion

        #region QueueTable
        
        self.queue_label = CTkLabel(self, font=self.default_font, text="Queue")
        self.queue_label.grid(row=12, column=0)

        #region Table
        self.queue_table = self.table = ttk.Treeview(self, columns=["priority", "login", "phone", "to"],
                                  show="headings", style="Custom.Treeview", selectmode="browse")
    
        self.queue_table.tag_configure("expired", background="red")
        self.queue_table.heading("priority", text="Priority")
        self.queue_table.heading("login", text="Login")
        self.queue_table.heading("phone", text="Phone")
        self.queue_table.heading("to", text="Expiry")

        self.queue_table.column("priority", anchor="center", minwidth=10, width=70)
        self.queue_table.column("login", anchor="center", minwidth=10, stretch=True)
        self.queue_table.column("phone", anchor="center", minwidth=10, stretch=True)
        self.queue_table.column("to", anchor="center", minwidth=10, width=100)

        self.queue_table.grid(row=13, column=0, rowspan=5, padx=5, sticky="nwse")
        #endregion
        
        self.takes_button = CTkButton(self, height=30, corner_radius=15, command=self.takes_button_click,
                                        text="Takes", font=self.default_font)
        self.takes_button.grid(row=13, column=1, padx=5, columnspan=2, sticky="nwe")

        self.delete_button = CTkButton(self, height=30, corner_radius=15, command=self.delete_button_click,
                                        text="Delete", font=self.default_font)
        self.delete_button.grid(row=14, column=1, padx=5, columnspan=2, sticky="nwe")

        #endregion

        self.refresh_button = CTkButton(self, width=20, height=20, hover_color="lightgrey",
                                        fg_color="transparent", corner_radius=10, text="", command=self.refresh_button_click,
                                        image=CTkImage(light_image=Image.open("images/refresh_arrow.png"), size=(20, 20)))
        self.refresh_button.grid(row=17, column=1, sticky="w")

        self.back_button = CTkButton(self, width=20, height=20, hover_color="lightgrey",
                                        fg_color="transparent", corner_radius=10, text="", command=self.back_button_click,
                                        image=CTkImage(light_image=Image.open("images/back_arrow.png"), size=(20, 20)))
        self.back_button.grid(row=17, column=2, sticky="e")

    def get_selected_taken_by_item(self):
        if len(self.taken_by_table.selection()) == 0: return None
        return self.taken_by_table.selection()[0]
    
    def get_selected_queue_item(self):
        if len(self.queue_table.selection()) == 0: return None
        return self.queue_table.selection()[0]

    def add_book_button_click(self):
        if self.name_entry.get().strip() == "" or self.author_entry.get().strip() == "" or self.year_entry.get().strip() == "" :
            self.add_button_result("Error")
            return
        name = self.name_entry.get().strip()
        author = self.author_entry.get().strip()
        year = self.year_entry.get()
        if len(year) != 4:
            self.add_button_result("Error")
            return
        description = self.description_entry.get().strip()
        description = description if len(description) > 0 else "-"
        quantity = self.quantity_entry.get()
        quantity = quantity if len(quantity) > 0 else "1"

        result = self.database_handler.add_book(name, author, year, description, quantity)
        if result != "Error": self.refresh()

        self.add_button_result(result)

    def add_button_result(self, result = Literal["Success", "Error"]):
        if result == "Success":
            self.add_book_button.configure(text="\u2714")
        else:
            self.add_book_button.configure(text="\u2716")
        self.add_book_button.after(1000, lambda : self.add_book_button.configure(text="\u2795"))

    def returns_button_click(self):
        if self.get_selected_taken_by_item() is None : return
        self.database_handler.return_book(
                self.catalogue.get_selected_item().taken_by[int(self.get_selected_taken_by_item())].user_id,
                self.catalogue.get_selected_item().taken_by[int(self.get_selected_taken_by_item())].book_id
            )
        self.refresh()

    def takes_button_click(self):
        if self.get_selected_queue_item() is None : return
        result = self.database_handler.take_book(
            self.catalogue.get_selected_item().queue[int(self.get_selected_queue_item())].user_id,
            self.catalogue.get_selected_item().queue[int(self.get_selected_queue_item())].book_id
        )
        self.takes_button.configure(text=result)
        self.takes_button.after(1000, lambda : self.takes_button.configure(text="Takes"))
        if result == "Success": self.refresh()

    def delete_button_click(self):
        if self.get_selected_queue_item() is None : return
        self.database_handler.delete_from_queue(
            self.catalogue.get_selected_item().queue[int(self.get_selected_queue_item())].user_id,
            self.catalogue.get_selected_item().queue[int(self.get_selected_queue_item())].book_id
        )
        self.refresh()   

    def on_book_selected(self, event):
        self.fill_taken_by_table(self.catalogue.get_selected_item())
        self.fill_queue_table(self.catalogue.get_selected_item())

    def fill_taken_by_table(self, book : Book):

        self.clear_taken_by_table()
        
        for tbi in book.taken_by:
            penalty = 0
            if dt.date.today() > tbi.expiry_date:
                penalty = (dt.date.today() - tbi.expiry_date).days * 20
            self.taken_by_table.insert("", "end",
                values=(self.users[tbi.user_id - 1].login, self.users[tbi.user_id - 1].phone,
                         tbi.start_date, tbi.expiry_date, penalty), iid=book.taken_by.index(tbi))

    def fill_queue_table(self, book : Book):

        self.clear_queue_table()
        
        for qi in book.queue:
            tag = "expired" if qi.expiry_date is not None and dt.date.today() > qi.expiry_date else ""
            expiry_date = "" if qi.expiry_date is None else qi.expiry_date
            self.queue_table.insert("", "end",
                values=(qi.priority, self.users[qi.user_id - 1].login, self.users[qi.user_id - 1].phone,
                         expiry_date), iid=book.queue.index(qi), tags=tag)

    def clear_taken_by_table(self):
        for item in self.taken_by_table.get_children():
            self.taken_by_table.delete(item)

    def clear_queue_table(self):
        for item in self.queue_table.get_children():
            self.queue_table.delete(item)

    def back_button_click(self):
        self.back_button_command()

    def refresh_button_click(self):
        self.refresh()

    def refresh(self):
        self.clear_taken_by_table()
        self.clear_queue_table()
        self.catalogue.fill_table() 

    def only_numbers(self, event : Event):
        if event.char.isdigit() or event.keysym in ("BackSpace", "Delete"):
            return True
        
        return "break"
    