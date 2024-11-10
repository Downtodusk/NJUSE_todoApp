from src.views.main_view import MainView
from views.login_view import LoginView
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Task Management App")
    root.geometry("600x400")
    app = LoginView(root)
    root.mainloop()
