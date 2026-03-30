from app import create_app, db
from app.models import User

def adjust_points():
    app = create_app()
    with app.app_context():
        # Target the new alumni by their usernames to be safe
        alumni_points = {
            "John Doe": 450,
            "Jane Smith": 320,
            "Robert Brown": 280,
            "akalumni": 150
        }
        
        for username, points in alumni_points.items():
            u = User.query.filter_by(username=username).first()
            if u:
                u.points = points
                print(f"Updated {username} to {points} XP")
            else:
                print(f"User {username} not found")

        db.session.commit()
        print("\nLeaderboard updated correctly!")

if __name__ == "__main__":
    adjust_points()
