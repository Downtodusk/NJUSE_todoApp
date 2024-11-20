import tkinter as tk
import tkinter.messagebox as messagebox
import json
import os
from views.main_view import MainView

USER_DATA_FILE = "users.json"  # 用户信息存储文件


class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("450x350")
        self.root.configure(bg="#f0f0f5")  # 柔和的背景色

        # 标题
        tk.Label(
            self.root, text="TODO LIST", font=("Segoe UI", 24, "bold"), bg="#f0f0f5", fg="#2c3e50"
        ).pack(pady=20)

        # 登录框架
        self.frame = tk.Frame(self.root, bg="#ffffff", bd=0, relief="flat", padx=20, pady=20)
        self.frame.pack(pady=10)

        # 用户名输入
        tk.Label(
            self.frame, text="Username:", font=("Segoe UI", 12), bg="#ffffff", fg="#34495e"
        ).grid(row=0, column=0, sticky="w", pady=10, padx=10)
        self.username_entry = tk.Entry(
            self.frame,
            font=("Segoe UI", 12),
            bd=0,
            highlightthickness=2,
            highlightbackground="#bdc3c7",
            highlightcolor="#3498db",
            width=20,
        )
        self.username_entry.grid(row=0, column=1, pady=10, padx=5)

        # 密码输入
        tk.Label(
            self.frame, text="Password:", font=("Segoe UI", 12), bg="#ffffff", fg="#34495e"
        ).grid(row=1, column=0, sticky="w", pady=10, padx=10)
        self.password_entry = tk.Entry(
            self.frame,
            font=("Segoe UI", 12),
            bd=0,
            show="*",
            highlightthickness=2,
            highlightbackground="#bdc3c7",
            highlightcolor="#3498db",
            width=20,
        )
        self.password_entry.grid(row=1, column=1, pady=10, padx=5)

        # 登录按钮
        self.login_button = tk.Button(
            self.frame,
            text="Login",
            font=("Segoe UI", 12, "bold"),
            bg="#2980b9",
            fg="white",
            bd=0,
            padx=30,
            pady=10,
            cursor="hand2",
            activebackground="#3498db",
            activeforeground="white",
            command=self.authenticate,
        )
        self.login_button.grid(row=2, column=0, pady=20)

        # 注册按钮
        self.register_button = tk.Button(
            self.frame,
            text="Register",
            font=("Segoe UI", 12, "bold"),
            bg="#27ae60",
            fg="white",
            bd=0,
            padx=30,
            pady=10,
            cursor="hand2",
            activebackground="#2ecc71",
            activeforeground="white",
            command=self.register,
        )
        self.register_button.grid(row=2, column=1, pady=20)

        # 底部提示
        tk.Label(
            self.root,
            text="Made with ❤️ by Shuai Jiang",
            font=("Segoe UI", 10, "italic"),
            bg="#f0f0f5",
            fg="#7f8c8d",
        ).pack(side="bottom", pady=10)

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        users = self.load_users()

        if username in users and users[username] == password:
            self.frame.destroy()
            MainView(self.root, username)  # 登录成功后进入主界面
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Register Failed", "Username and password cannot be empty.")
            return

        users = self.load_users()

        if username in users:
            messagebox.showerror("Register Failed", "Username already exists.")
        else:
            users[username] = password
            self.save_users(users)
            os.makedirs(f"data/{username}", exist_ok=True)  # 创建用户专属任务文件夹
            messagebox.showinfo("Register Success", "Registration successful. Please login.")

    def load_users(self):
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, "r") as file:
                return json.load(file)
        return {}

    def save_users(self, users):
        with open(USER_DATA_FILE, "w") as file:
            json.dump(users, file)


# Example Usage
if __name__ == "__main__":
    root = tk.Tk()
    LoginView(root)
    root.mainloop()
