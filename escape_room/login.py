from flask_login import LoginManager

from escape_room.models import User, engine

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return engine.find_one(Model=User, query=(User.username == user_id))
