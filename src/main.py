from views.login_view import LoginView
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Task Management App")
    root.geometry("500x400")
    app = LoginView(root)
    root.mainloop()
