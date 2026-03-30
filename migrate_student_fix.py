import os
import sys
from app import create_app, db
from sqlalchemy import text

def migrate():
    app = create_app()
    with app.app_context():
        print("--- Student Profile Migration ---")
        try:
            # Add current_year column
            db.session.execute(text("ALTER TABLE student_profile ADD COLUMN current_year VARCHAR(20) DEFAULT '1st Year'"))
            # Add semester column
            db.session.execute(text("ALTER TABLE student_profile ADD COLUMN semester VARCHAR(10) DEFAULT 'S1'"))
            db.session.commit()
            print("Successfully added 'current_year' and 'semester' columns to 'student_profile' table.")
        except Exception as e:
            db.session.rollback()
            # If columns already exist, this might fail, which is fine for a simple migration script
            print(f"Notice: {e}")

        # Update existing students to reasonable defaults if they were null
        try:
            db.session.execute(text("UPDATE student_profile SET current_year = '1st Year' WHERE current_year IS NULL"))
            db.session.execute(text("UPDATE student_profile SET semester = 'S1' WHERE semester IS NULL"))
            db.session.commit()
            print("Updated existing records with default values.")
        except Exception as e:
            db.session.rollback()
            print(f"Migration Update Error: {e}")

if __name__ == "__main__":
    migrate()
