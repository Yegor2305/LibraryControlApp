from typing import Any
from customtkinter import CTkFrame, CTkFont, CTkEntry, CTkButton
from general import general_methods as gm

class LogInFrame(CTkFrame):
    def __init__(self, master: Any, default_font : CTkFont, registration_button_command : callable,
                log_in_button_command : callable, **kwargs):
        super().__init__(master, **kwargs)
        
        self.default_font = default_font
        self.registration_button_command = registration_button_command
        self.log_in_button_command = log_in_button_command

        #region Controls
        self.login_input_box = CTkEntry(self, placeholder_text="Login (nickname)", border_color="black",
                                        corner_radius=28, width=280, height=56, font=self.default_font)
        self.password_input_box = CTkEntry(self, placeholder_text="Password", border_color="black",
                                           corner_radius=28, width=280, height=56, font=self.default_font, show="*")
        
        self.show_password_button = CTkButton(self.password_input_box, width=10, height=10, corner_radius=5, text="",
                                              image=gm.closed_eye_image, fg_color="transparent", hover=False)
        self.show_password_button.place(relx=0.94, rely=0.5, anchor="e")
        self.show_password_button.bind("<ButtonPress-1>", gm.show_hide_password)
        self.show_password_button.bind("<ButtonRelease-1>", gm.show_hide_password)

        self.log_in_button = CTkButton(self, text="Log in", width=280, height=56, corner_radius=28,
                                        font=self.default_font, command=self.log_in_button_click)
        self.sign_up_button = CTkButton(self, text="No account?", width=280, height=56, corner_radius=28,
                                        font=self.default_font, command=self.sign_up_button_click)

        self.login_input_box.pack(pady=10)
        self.password_input_box.pack()
        self.log_in_button.pack(pady=10)
        self.sign_up_button.pack()

        #endregion

    def log_in_button_click(self):
        self.log_in_button_command()

    def sign_up_button_click(self):
        self.registration_button_command()

    def get_entered_login(self):
        return self.login_input_box.get()
    
    def get_entered_password(self):
        return self.password_input_box.get()
    
    def configure_log_in_button_text(self, text : str):
        self.log_in_button.configure(text=text)

    def configure_sign_up_button_text(self, text : str):
        self.sign_up_button.configure(text=text)
