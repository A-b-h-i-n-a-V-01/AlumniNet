import sys
import os
from app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    for col in ['deleted_for_sender', 'deleted_for_recipient', 'is_deleted_everyone']:
        try:
            db.session.execute(text(f"ALTER TABLE message ADD COLUMN {col} BOOLEAN DEFAULT 0"))
            db.session.commit()
            print(f"Added {col}")
        except Exception as e:
            db.session.rollback()
            print(f"Failed to add {col}: {e}")
