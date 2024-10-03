import customtkinter as ctk
from customtkinter import CTk, FontManager, CTkFont, BOTH
from services.database_handler import DatabaseHandler
from frames.log_in_frame import LogInFrame
from frames.sign_up_frame import SignUpFrame
from frames.user_frame import UserFrame
from frames.admin_frame import AdminFrame

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent))

FontManager.load_font("fonts/OpenSans.ttf")
ctk.set_default_color_theme("dark-blue")

class Application(CTk):
    def __init__(self):
        super().__init__()

        self.default_font = CTkFont(family="Open Sans", size=20)
        self.title("Log in - YLibrary")
        self.iconbitmap("images/icon.ico")
        self.resizable(False, False)

        self.database_handler = DatabaseHandler()
        
        self.password_strength = 0
        
        # region LogInPage
        self.log_in_frame = LogInFrame(master=self, default_font=self.default_font, registration_button_command=self.go_to_registration,
                                       log_in_button_command=self.log_in)
        self.log_in_frame.pack(fill=BOTH, expand=True, ipadx=20, ipady=20)
        #endregion
             
        # region RegistrationPage
        self.registration_frame = SignUpFrame(master=self, default_font=self.default_font, registration_button_command=self.sign_up,
                                       back_button_command=self.from_registration_to_log_in)
        #endregion

        #region UserPage

        self.user_frame = {}

        #endregion

        #region AdminPage

        self.admin_frame = {}

        #endregion

    def go_to_registration(self):
        self.title("Sign up - YLibrary")
        self.log_in_frame.pack_forget()
        self.registration_frame.pack(fill=BOTH, expand=True, ipadx=20, ipady=20)
        self.is_password_visible = False

    def from_registration_to_log_in(self):
        self.title("Log in - YLibrary")
        self.registration_frame.pack_forget()

        self.log_in_frame.pack(fill=BOTH, expand=True, ipadx=20, ipady=20)
        # self.is_password_visible = False

    def from_admin_page_to_log_in(self):
        self.title("Log in - YLibrary")
        self.admin_frame.pack_forget()

        self.log_in_frame.pack(fill=BOTH, expand=True, ipadx=20, ipady=20)

    def from_user_page_to_log_in(self):
        self.title("Log in - YLibrary")
        self.user_frame.pack_forget()
        self.user_frame.destroy()

        self.log_in_frame.pack(fill=BOTH, expand=True, ipadx=20, ipady=20)

    def sign_up(self):

        registration_result = self.database_handler.sign_up(self.registration_frame.get_entered_login(),
                                                            self.registration_frame.get_entered_password(),
                                                            self.registration_frame.get_entered_email(),
                                                            self.registration_frame.get_entered_phone())
        
        self.registration_frame.configure_sign_up_button_text(f"{registration_result}!")

        if registration_result == "Error":         
            self.after(1000, lambda : self.registration_frame.return_sign_up_button_text())
        else:
            self.after(1000, self.return_text_and_change_page)

    def return_text_and_change_page(self):
        self.registration_frame.return_sign_up_button_text()
        self.go_to_log_in()

    def log_in(self):

        if self.log_in_frame.get_entered_login() == "admin" and self.log_in_frame.get_entered_password() == "admin":
            if not isinstance(self.admin_frame, AdminFrame):
                self.admin_frame = AdminFrame(self, self.default_font, self.database_handler, self.from_admin_page_to_log_in)
            self.admin_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
            self.title("Admin - YLibrary")
            self.log_in_frame.pack_forget()
            return

        authorization_result = self.database_handler.check_authorization(self.log_in_frame.get_entered_login(),
                                                                        self.log_in_frame.get_entered_password())
        if authorization_result == False:
            self.log_in_frame.configure_log_in_button_text("Wrong credentials")
        else:
            self.log_in_frame.configure_log_in_button_text(f"Hello, {authorization_result.login}!")
            self.after(1000, lambda: self.log_in_frame.configure_log_in_button_text("Log in"))         
            self.user_frame = UserFrame(self, self.default_font, self.database_handler, self.from_user_page_to_log_in)
            self.user_frame.set_user(authorization_result)
            self.user_frame.pack(fill=BOTH, expand=True)
            self.title(f"{authorization_result.phone} - YLibrary")
            self.log_in_frame.pack_forget()
        
        self.after(1000, lambda: self.log_in_frame.configure_log_in_button_text("Log in"))

app = Application()
app.mainloop()