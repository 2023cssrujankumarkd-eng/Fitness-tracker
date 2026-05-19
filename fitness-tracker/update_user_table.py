from app import create_app, db
from app.models.user import User
from sqlalchemy import text

app = create_app()

with app.app_context():
    # Drop the columns
    with db.engine.connect() as conn:
        conn.execute(text('ALTER TABLE user DROP COLUMN is_doctor, DROP COLUMN is_admin'))
        conn.commit()
    print("Successfully removed is_doctor and is_admin columns from user table") 