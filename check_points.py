from app import create_app, db
from app.models import User

def check():
    app = create_app()
    with app.app_context():
        users = User.query.filter_by(role='alumni').order_by(User.points.desc()).all()
        for u in users:
            print(f"User: {u.username} (ID: {u.id}) - Points: {u.points}")

if __name__ == "__main__":
    check()
