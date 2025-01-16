import unittest
from unittest.mock import MagicMock, patch
from tkinter import Tk
from src.views.login_view import LoginView

USER_DATA_FILE = "users.json"


class TestLoginView(unittest.TestCase):

    @patch('src.views.login_view.LoginView.load_users')
    def test_login_success(self, mock_load_users):
        """测试正确的用户名和密码登录"""
        mock_load_users.return_value = {"test_user": "password"}
        root = Tk()
        view = LoginView(root)

        print(view.load_users())

        view.username_entry.insert(0, "test_user")
        view.password_entry.insert(0, "password")

        with patch("src.views.login_view.messagebox.showerror") as mock_showerror:
            view.authenticate()
            mock_showerror.assert_not_called()

    @patch('src.views.login_view.LoginView.load_users')
    def test_login_failed_due_to_wrong_username(self, mock_load_users):
        """测试错误的用户名"""
        mock_load_users.return_value = {"test_user": "password"}
        root = Tk()
        view = LoginView(root)
        view.username_entry.insert(0, "wrong_user")
        view.password_entry.insert(0, "password")

        with patch("src.views.login_view.messagebox.showerror") as mock_showerror:
            view.authenticate()
            mock_showerror.assert_called_once_with("Login Failed", "Incorrect username or password.")

    @patch('src.views.login_view.LoginView.load_users')
    def test_login_failed_due_to_wrong_password(self, mock_load_users):
        """测试错误的密码"""
        mock_load_users.return_value = {"test_user": "password"}
        root = Tk()
        view = LoginView(root)
        view.username_entry.insert(0, "test_user")
        view.password_entry.insert(0, "wrong_password")

        with patch("src.views.login_view.messagebox.showerror") as mock_showerror:
            view.authenticate()
            mock_showerror.assert_called_once_with("Login Failed", "Incorrect username or password.")

    @patch('src.views.login_view.LoginView.load_users')
    def test_login_failed_due_to_empty_username(self, mock_load_users):
        """测试空用户名登录"""
        mock_load_users.return_value = {"test_user": "password"}
        root = Tk()
        view = LoginView(root)
        view.username_entry.insert(0, "")
        view.password_entry.insert(0, "password")

        with patch("src.views.login_view.messagebox.showerror") as mock_showerror:
            view.authenticate()
            mock_showerror.assert_called_once_with("Login Failed", "Incorrect username or password.")

    @patch('src.views.login_view.LoginView.load_users')
    def test_login_failed_due_to_empty_password(self, mock_load_users):
        """测试空密码登录"""
        mock_load_users.return_value = {"test_user": "password"}
        root = Tk()
        view = LoginView(root)
        view.username_entry.insert(0, "test_user")
        view.password_entry.insert(0, "")

        with patch("src.views.login_view.messagebox.showerror") as mock_showerror:
            view.authenticate()
            mock_showerror.assert_called_once_with("Login Failed", "Incorrect username or password.")

    @patch('src.views.login_view.LoginView.load_users')
    @patch('src.views.login_view.LoginView.save_users')
    def test_register_success(self, mock_save_users, mock_load_users):
        """测试注册新用户"""
        mock_load_users.return_value = {}
        root = Tk()
        view = LoginView(root)
        view.username_entry.insert(0, "new_user")
        view.password_entry.insert(0, "new_password")

        with patch("src.views.login_view.messagebox.showinfo") as mock_showinfo:
            view.register()
            mock_showinfo.assert_called_once_with("Register Success", "Registration successful. Please login.")
            mock_save_users.assert_called_once()

    @patch('src.views.login_view.LoginView.load_users')
    @patch('src.views.login_view.LoginView.save_users')
    def test_register_save_success(self, mock_save_users, mock_load_users):
        """测试注册新用户"""
        mock_load_users.return_value = {}
        root = Tk()
        view = LoginView(root)
        self.assertEqual(len(view.load_users()), 0)
        view.username_entry.insert(0, "new_user")
        view.password_entry.insert(0, "new_password")
        with patch("src.views.login_view.messagebox.showinfo") as mock_showinfo:
            view.register()
            self.assertEqual(len(view.load_users()), 1)

    @patch('src.views.login_view.LoginView.load_users')
    def test_register_failed_due_to_empty_username(self, mock_load_users):
        """测试注册时用户名为空"""
        mock_load_users.return_value = {}
        root = Tk()
        view = LoginView(root)
        view.username_entry.insert(0, "")
        view.password_entry.insert(0, "new_password")

        with patch("src.views.login_view.messagebox.showerror") as mock_showerror:
            view.register()
            mock_showerror.assert_called_once_with("Register Failed", "Username and password cannot be empty.")

    @patch('src.views.login_view.LoginView.load_users')
    def test_register_failed_due_to_empty_password(self, mock_load_users):
        """测试注册时密码为空"""
        mock_load_users.return_value = {}
        root = Tk()
        view = LoginView(root)
        view.username_entry.insert(0, "new_user")
        view.password_entry.insert(0, "")

        with patch("src.views.login_view.messagebox.showerror") as mock_showerror:
            view.register()
            mock_showerror.assert_called_once_with("Register Failed", "Username and password cannot be empty.")

    @patch('src.views.login_view.LoginView.load_users')
    def test_register_failed_due_to_existing_username(self, mock_load_users):
        """测试注册时用户名已存在"""
        mock_load_users.return_value = {"existing_user": "password"}
        root = Tk()
        view = LoginView(root)
        view.username_entry.insert(0, "existing_user")
        view.password_entry.insert(0, "new_password")

        with patch("src.views.login_view.messagebox.showerror") as mock_showerror:
            view.register()
            mock_showerror.assert_called_once_with("Register Failed", "Username already exists.")


if __name__ == '__main__':
    unittest.main()
