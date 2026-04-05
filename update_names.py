from app import create_app, db
from app.models import User

app = create_app()

def update_users():
    with app.app_context():
        mapping = {
            "John Doe": "Akhil Shaji",
            "Jane Smith": "Abel Shibu",
            "Robert Brown": "Aswin Soman"
        }
        
        for old_name, new_name in mapping.items():
            user = User.query.filter_by(username=old_name).first()
            if user:
                user.username = new_name
                print(f"Updated User ID {user.id}: {old_name} -> {new_name}")
            else:
                print(f"User '{old_name}' not found.")
        
        db.session.commit()
        print("Done.")

if __name__ == "__main__":
    update_users()
