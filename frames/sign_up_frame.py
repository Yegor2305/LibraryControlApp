from typing import Any
from customtkinter import CTkFrame, CTkFont, CTkImage, CTkEntry, CTkButton, CTkLabel, CTkProgressBar
from ctkmaskedentry import CTkMaskedEntry, Mask
from general import general_methods as gm
from PIL import Image
import re

class SignUpFrame(CTkFrame):
    def __init__(self, master: Any, default_font : CTkFont, registration_button_command : callable,
                back_button_command : callable, **kwargs):
        super().__init__(master, **kwargs)
        
        self.default_font = default_font
        self.registration_button_command = registration_button_command
        self.back_button_command = back_button_command

        #region Controls
        #region BackButton
        self.back_button_image = CTkImage(light_image=Image.open("images/back_arrow.png"), size=(20, 20))
        self.back_button = CTkButton(self, text="", font=self.default_font, width=20, height=20,
                    image=self.back_button_image, fg_color="transparent", hover_color="#DAD9D8", command=self.back_button_click)
        self.back_button.pack(anchor="ne")
        #endregion

        #region Email
        CTkLabel(self, width=280, anchor="w", text="Email", padx=30).pack()
        self.email_input_box = CTkEntry(self, placeholder_text="email@gmail.com", border_color="black",
                                        corner_radius=28, width=280, height=56, font=self.default_font)
        self.email_input_box.pack(pady=(0, 10))
        #endregion
        
        #region Nickname
        CTkLabel(self, width=280, anchor="w", text="Nickname", padx=30).pack()
        self.nickname_input_box = CTkEntry(self, placeholder_text="nickname", border_color="black",
                                           corner_radius=28, width=280, height=56, font=self.default_font)
        self.nickname_input_box.pack(pady=(0,10))
        self.nickname_input_box.bind("<Key>", gm.prevent_space)
        #endregion

        #region Phone
        CTkLabel(self, width=280, anchor="w", text="Phone", padx=30).pack()
        self.phone_input_box = CTkMaskedEntry(self, border_color="black", mask=Mask("fixed", "+38(999)9999999"),
                                           corner_radius=28, width=280, height=56, font=self.default_font)
        self.phone_input_box.pack(pady=(0,10))
        #self.phone_input_box.bind("<Key>", self.prevent_space)
        #endregion
        
        #region NewPassword
        CTkLabel(self, width=280, anchor="w", text="Password", padx=30).pack()
        self.new_password_input_box = CTkEntry(self, border_color="black",
                                               corner_radius=28, width=280, height=56, font=self.default_font, show="*")
        self.new_password_input_box.pack(pady=(0,10))
        self.new_password_input_box.bind("<KeyRelease>", self.new_password_text_change)
        self.new_password_input_box.bind("<Key>", gm.prevent_space)

        self.show_password_button = CTkButton(self.new_password_input_box, width=10, height=10, corner_radius=5, text="",
                                              image=gm.closed_eye_image, fg_color="transparent", hover=False)
        self.show_password_button.place(relx=0.94, rely=0.5, anchor="e")
        self.show_password_button.bind("<ButtonPress-1>", gm.show_hide_password)
        self.show_password_button.bind("<ButtonRelease-1>", gm.show_hide_password)
        #endregion

        #region RepeatPassword
        CTkLabel(self, width=280, anchor="w", text="Repeat password", padx=30).pack()
        self.repeat_password_input_box = CTkEntry(self, border_color="black",
                                                  corner_radius=28, width=280, height=56, font=self.default_font, show="*")
        self.repeat_password_input_box.pack()
        self.show_password_button = CTkButton(self.repeat_password_input_box, width=10, height=10, corner_radius=5, text="",
                                              image=gm.closed_eye_image, fg_color="transparent", hover=False)
        self.show_password_button.place(relx=0.94, rely=0.5, anchor="e")
        self.show_password_button.bind("<ButtonPress-1>", gm.show_hide_password)
        self.show_password_button.bind("<ButtonRelease-1>", gm.show_hide_password)
        #endregion
        
        self.password_safety_progress_bar = CTkProgressBar(self, width=250, height=10, corner_radius=10, progress_color="#8B0000")
        self.password_safety_progress_bar.pack(pady=15)
        self.password_safety_progress_bar.set(0.0)        

        self.sign_up_button = CTkButton(self, text="Sign up", font=self.default_font, width=280, height=56,
                                        corner_radius=28, command=self.sign_up_button_click)
        self.sign_up_button.pack()
        #endregion

    def new_password_text_change(self, event):
        password_strength = 0
        if event.char == " ":
            return "break"
        if len(self.new_password_input_box.get()) >= 8:
            password_strength += 25
            if bool(re.search(r"\d", self.new_password_input_box.get())):
                password_strength += 25
            if bool(re.search(r"(\W|\_)", self.new_password_input_box.get())):
                password_strength += 25
            if bool(re.search(r"[A-Z]", self.new_password_input_box.get())):
                password_strength += 25
        
        color = "#8B0000"
        if  25 < password_strength <= 50:
            color = "#FF4500"
        elif 50 < password_strength <= 75:
            color = "#90EE90"
        elif password_strength > 75:
            color = "#006400"

        self.password_strength = password_strength
        self.password_safety_progress_bar.configure(progress_color=color)
        self.password_safety_progress_bar.set(password_strength/100)

    def get_entered_login(self):
        return self.nickname_input_box.get()
    
    def get_entered_email(self):
        return self.email_input_box.get()
    
    def get_entered_phone(self):
        return self.phone_input_box.get().translate(str.maketrans("", "", "()_"))

    def get_entered_password(self):
        return self.new_password_input_box.get()

    def configure_sign_up_button_text(self, text : str):
        self.sign_up_button.configure(text=text)

    def return_sign_up_button_text(self):
        self.sign_up_button.configure(text="Sign up")

    def sign_up_button_click(self):

        for child in self.winfo_children():
            if isinstance(child, CTkEntry) or isinstance(child, CTkMaskedEntry):
                child.configure(border_color="black")

        is_error = False

        if not bool(re.match(r"[^@]+(@gmail.com|@yahoo.com|ukr.net)\Z", self.email_input_box.get())):
            is_error = True
            self.email_input_box.configure(border_color="red")
        if self.nickname_input_box.get() == "":
            is_error = True
            self.nickname_input_box.configure(border_color="red")
        if len(self.phone_input_box.get().translate(str.maketrans("", "", "()_"))) != 13:
            is_error = True
            self.phone_input_box.configure(border_color="red")
        if self.new_password_input_box.get() != self.repeat_password_input_box.get():
            is_error = True
            self.repeat_password_input_box.configure(border_color="red")
        # if self.password_strength < 25:
        #     is_error = True
        #     self.new_password_input_box.configure(border_color="red")
        
        if is_error: return

        self.registration_button_command()

    def back_button_click(self):
        self.back_button_command()
