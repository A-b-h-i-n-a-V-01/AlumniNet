from app import create_app, db
from app.models import User

app = create_app()

def list_users_details():
    with app.app_context():
        users = User.query.all()
        for u in users:
            print(f"ID: {u.id}, Username: {u.username}, Email: {u.email}")

if __name__ == "__main__":
    list_users_details()
