from models.user import User
from views.ui import UI

if __name__ == "__main__":
    # 初始化UI和用户
    ui = UI()
    user = User()
    ui.render(user)
