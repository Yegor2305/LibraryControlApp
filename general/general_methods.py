from customtkinter import CTkImage
from PIL import Image
from tkinter import ttk

closed_eye_image = CTkImage(light_image=Image.open("images/closed_eye.png"), size=(26, 26))
opened_eye_image = CTkImage(light_image=Image.open("images/opened_eye.png"), size=(26, 26))

def get_style():   
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Custom.Treeview", background="#F9F9FA", foreground="black",
                    fieldbackground="#F9F9FA", relief="flat", font=("Open Sans", 12), rowheight=25)
    style.configure("Custom.Treeview.Heading", background="lightgrey", border_width = 1,
                        foreground="black", relief="flat", border_color="white", font=("Open Sans", 12))
    style.map('Custom.Treeview', background=[('selected', "#3a7ebf")], foreground=[('selected', "white")])

def show_hide_password(event):
    button = event.widget.master
    input_box = button.master
    if event.type == "4":
        button.configure(image=opened_eye_image)
        input_box.configure(show="")
    elif event.type == "5":
        button.configure(image=closed_eye_image)
        input_box.configure(show="*")

def prevent_space(event):
    if event.char == " ":
        return "break"