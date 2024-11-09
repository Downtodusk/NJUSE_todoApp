import tkinter as tk
import tkinter.messagebox as messagebox
from views.main_view import MainView

class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x250")
        self.root.configure(bg="#f5f5f5")  # 背景浅灰色

        # 标题
        tk.Label(self.root, text="✅TODO LIST", font=("Arial", 18, "bold"), bg="#f5f5f5", fg="#333").pack(pady=20)

        # 登录框架
        self.frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief="groove", padx=20, pady=20)
        self.frame.pack(pady=10)

        tk.Label(self.frame, text="Username:", font=("Arial", 12), bg="#ffffff", fg="#555").grid(row=0, column=0, sticky="w", pady=10)
        self.username_entry = tk.Entry(self.frame, font=("Arial", 12), bd=0, highlightthickness=1, highlightbackground="#ddd", highlightcolor="#0c87d4")
        self.username_entry.grid(row=0, column=1, pady=10, padx=5)

        tk.Label(self.frame, text="Password:", font=("Arial", 12), bg="#ffffff", fg="#555").grid(row=1, column=0, sticky="w", pady=10)
        self.password_entry = tk.Entry(self.frame, font=("Arial", 12), bd=0, show="*", highlightthickness=1, highlightbackground="#ddd", highlightcolor="#0c87d4")
        self.password_entry.grid(row=1, column=1, pady=10, padx=5)

        # 登录按钮
        self.login_button = tk.Button(self.frame, text="Login", font=("Arial", 12), bg="#0c87d4", fg="white", bd=0, padx=20, pady=5, cursor="hand2", command=self.authenticate)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=15)

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "123" and password == "123":  # 简化的认证
            self.frame.destroy()
            MainView(self.root)  # 登录成功后进入主界面
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")
