from customtkinter import *
from frames.books_catalogue_frame import BooksCatalogueFrame
import datetime as dt
from PIL import Image
from objects.user import User
from objects.books_catalogue import BooksCatalogue
from services.database_handler import DatabaseHandler


class UserFrame(CTkFrame):
    def __init__(self, master, default_font : CTkFont,
                database_handler_obj : DatabaseHandler,
                back_button_command : callable, **kwargs):
        super().__init__(master, **kwargs)

        self.default_font = default_font
        self.database_handler = database_handler_obj
        self.back_button_command = back_button_command
        self.books_taken_by_user : BooksCatalogue = {}
        self.user = {}
        self.book_index = -1

        self.card_width = 250

        self.tabview = CTkTabview(self, corner_radius=20)
        self.catalogue_tab = self.tabview.add("My books")
        self.catalogue_tab = self.tabview.add("Catalogue")

        #region CatalogueTab
        self.catalogue = BooksCatalogueFrame(self.tabview.tab("Catalogue"), self.default_font, database_handler_obj)
        self.catalogue.pack(fill=BOTH, expand=True)

        self.get_in_line_button = CTkButton(self.tabview.tab("Catalogue"), text="Get in line", width=220,
                                            height=40, corner_radius=20, font=self.default_font, command=self.get_in_line_button_click)
        self.get_in_line_button.pack(pady=10)
        #endregion

        #region MyBooksTab

        self.book_card = CTkFrame(self.tabview.tab("My books"), fg_color="white", width=self.card_width+10, height=310)
        self.book_card.pack_propagate(False)
        self.queue_card = CTkScrollableFrame(self.tabview.tab("My books"), fg_color="white", width=self.card_width, height=300)
        self.refresh_button = CTkButton(self.tabview.tab("My books"), width=20, height=20, hover_color="grey",
                                        fg_color="transparent", corner_radius=10, text="", command=self.refresh_button_click,
                                        image=CTkImage(light_image=Image.open("images/refresh_arrow.png"), size=(20, 20)))
        self.back_button = CTkButton(self.tabview.tab("My books"), width=20, height=20, hover_color="grey",
                                        fg_color="transparent", corner_radius=10, text="", command=self.back_button_click,
                                        image=CTkImage(light_image=Image.open("images/back_arrow.png"), size=(20, 20)))

        self.book_info_frame = CTkFrame(self.book_card, fg_color="lightgrey")
        self.date_label = CTkLabel(self.book_card, font=self.default_font, text = "")
        self.buttons_frame = CTkFrame(self.book_card, fg_color="transparent")     
        
        self.prev_book_button = CTkButton(self.buttons_frame, width=20, height=20, hover_color="lightgrey",
                                        fg_color="transparent", corner_radius=10, text="", command=self.left_arrow_click,
                                        image=CTkImage(light_image=Image.open("images/left_arrow.png"), size=(25, 25)))
        self.book_number_label = CTkLabel(self.buttons_frame, font=self.default_font, text="   ")
        self.next_book_button = CTkButton(self.buttons_frame, width=20, height=20, hover_color="lightgrey",
                                        fg_color="transparent", corner_radius=10, text="", command=self.right_arrow_click,
                                        image=CTkImage(light_image=Image.open("images/right_arrow.png"), size=(25, 25)))
        
        self.prev_book_button.pack(side=LEFT, padx=5)
        self.book_number_label.pack(side=LEFT)
        self.next_book_button.pack(side=LEFT, padx=5)

        self.author_label = CTkLabel(self.book_info_frame, font=self.default_font, text="", wraplength=self.card_width)
        self.title_label = CTkLabel(self.book_info_frame, font=self.default_font, text="", wraplength=self.card_width)
        self.year_label = CTkLabel(self.book_info_frame, font=self.default_font, text="", wraplength=self.card_width)

        self.author_label.pack(side=TOP, pady=5)
        self.title_label.pack(side=TOP, fill=Y, expand=True)
        self.year_label.pack(side=BOTTOM, pady=5)

        self.back_button.pack(side=TOP, anchor="e", padx=8)
        self.book_info_frame.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.date_label.pack(side=TOP)
        self.buttons_frame.pack(side=BOTTOM, pady = 8)
        self.book_card.pack(side=LEFT, padx=10)
        self.refresh_button.pack(side=LEFT, anchor="n")
        self.queue_card.pack(side=RIGHT, padx=10)

        #endregion
        
        self.tabview.pack(fill=BOTH, expand=True, pady=15, padx=15)

    def get_in_line_button_click(self):
        self.catalogue.fill_table()
        book = self.catalogue.get_selected_item()
        if book is None:
            self.switch_button_text("Choose a book")
        else:
            expiry_date = dt.date.today() + dt.timedelta(days=1)
            if (book.quantity == 0):
                self.switch_button_text("There is no such book")
                return
            if len(book.taken_by) + len(book.queue) >= book.quantity:
                expiry_date = None          
            result = self.database_handler.get_in_line(self.user.id, book.id, len(book.queue) + 1, expiry_date)
            self.switch_button_text(result)

    def back_button_click(self):
        self.back_button_command()

    def switch_button_text(self, text : str):
        self.get_in_line_button.configure(text=text)
        self.get_in_line_button.after(1000, lambda : self.get_in_line_button.configure(text="Get in line"))      

    def fill_user_books_info(self):
        self.books_taken_by_user = self.database_handler.get_books(self.user.id, taken_or_queue="taken")
        if len(self.books_taken_by_user.catalogue) != 0: self.book_index = 0
        else: self.book_index = -1
        self.fill_book_card()
        self.fill_queue_card()

    def set_user(self, user : User):
        self.user = user
        
        self.fill_user_books_info()
        
    def left_arrow_click(self):
        if self.book_index != -1:
            self.book_index = self.book_index - 1 if self.book_index != 0 else len(self.books_taken_by_user.catalogue) - 1

        self.fill_book_card()

    def right_arrow_click(self):
        if self.book_index != -1:
            self.book_index = (self.book_index + 1) % len(self.books_taken_by_user.catalogue)
        self.fill_book_card()

    def refresh_button_click(self):
        self.fill_user_books_info()

    def fill_book_card(self):
        if self.book_index == -1:
            self.author_label.configure(text="")
            self.title_label.configure(text="You haven't taken the books yet")
            self.year_label.configure(text=str(dt.date.today().year))
            self.book_number_label.configure(text="   ")
            self.date_label.configure(text="")
        else:
            user_taken_by_record = [tbi for tbi in self.books_taken_by_user.catalogue[self.book_index].taken_by if tbi.user_id == self.user.id][0]
            self.author_label.configure(text=self.books_taken_by_user.catalogue[self.book_index].author)
            self.title_label.configure(text=self.books_taken_by_user.catalogue[self.book_index].name)
            self.year_label.configure(text=self.books_taken_by_user.catalogue[self.book_index].year)
            self.book_number_label.configure(text=f"{self.book_index + 1}/{len(self.books_taken_by_user.catalogue)}")
            self.date_label.configure(
                text=f"{user_taken_by_record.start_date.strftime("%d.%m.%Y")}" + 
                f" ‒ {user_taken_by_record.expiry_date.strftime("%d.%m.%Y")}")

    def fill_queue_card(self):
        user_queue_books = self.database_handler.get_books(self.user.id, "queue")
        for item in self.queue_card.winfo_children():
            item.destroy()

        if len(user_queue_books.catalogue) == 0:
            CTkLabel(self.queue_card, font=self.default_font, text="You don't stand in line for books", wraplength=self.card_width).pack()
            return
        else:
            for book in user_queue_books.catalogue:
                user_queue_place = [qi for qi in book.queue if qi.user_id == self.user.id][0]
                expiry_date_text = "" if user_queue_place.expiry_date is None else f"\nTake to: {user_queue_place.expiry_date}"
                CTkLabel(self.queue_card, font=self.default_font, justify=LEFT,
                        text=f"Priority {user_queue_place.priority}.\n{book.name}{expiry_date_text}",
                        wraplength=self.card_width).pack(side=TOP, anchor="w")
                CTkFrame(self.queue_card, height=2, width=self.card_width, fg_color="grey").pack(side=TOP)
    

