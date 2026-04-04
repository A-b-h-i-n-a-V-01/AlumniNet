from app import create_app, db
from sqlalchemy import text

def patch_db():
    app = create_app()
    with app.app_context():
        print("Starting database schema patch and data cleanup...")
        
        # SQL commands to fix schema and defaults
        commands = [
            # 1. Add missing columns
            "ALTER TABLE alumni_profile ADD COLUMN enrollment_year INT AFTER user_id;",
            "ALTER TABLE student_profile ADD COLUMN expected_graduation_year INT AFTER enrollment_year",
            
            # 2. Fix points field defaults (existing users might have NULL points)
            "UPDATE user SET points = 0 WHERE points IS NULL;",
            "ALTER TABLE user MODIFY COLUMN points INT NOT NULL DEFAULT 0;"
        ]
        
        for command in commands:
            try:
                print(f"Executing: {command}")
                db.session.execute(text(command))
                db.session.commit()
                print("Success.")
            except Exception as e:
                db.session.rollback()
                if "Duplicate column name" in str(e):
                    print("Column already exists. Skipping.")
                else:
                    print(f"Error executing command: {e}")
        
        print("Database schema patch and cleanup complete.")

if __name__ == "__main__":
    patch_db()
