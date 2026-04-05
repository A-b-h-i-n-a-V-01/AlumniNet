from app import create_app, db
from app.models import User

app = create_app()

def update_users_robust():
    with app.app_context():
        # Mapping: Old Name -> New Name
        mapping = {
            "John Doe": "Akhil Shaji",
            "Jane Smith": "Abel Shibu",
            "Robert Brown": "Aswin Soman"
        }
        
        # 1. First, handle any existing accounts with the TARGET names that aren't our intended IDs
        # (This prevents IntegrityError/clashes)
        target_names = list(mapping.values())
        conflicting_users = User.query.filter(User.username.in_(target_names)).all()
        for u in conflicting_users:
            if u.id not in [5, 6, 7]: # Only delete if it's not the actual users we want to update
                print(f"Removing redundant conflicting user: {u.username} (ID: {u.id})")
                db.session.delete(u)
        
        db.session.commit() # Clear conflicts first
        
        # 2. Now perform the rename
        for old_name, new_name in mapping.items():
            user = User.query.filter_by(username=old_name).first()
            if user:
                user.username = new_name
                print(f"Renamed ID {user.id}: {old_name} -> {new_name}")
            else:
                # If name was already changed or doesn't exist, try by ID as a fallback
                fallback_id = {"John Doe": 5, "Jane Smith": 6, "Robert Brown": 7}.get(old_name)
                user = User.query.get(fallback_id)
                if user:
                    print(f"Renamed ID {user.id} (fallback): {user.username} -> {new_name}")
                    user.username = new_name
                else:
                    print(f"User {old_name} not found.")
        
        db.session.commit()
        print("Updates complete.")

if __name__ == "__main__":
    update_users_robust()
