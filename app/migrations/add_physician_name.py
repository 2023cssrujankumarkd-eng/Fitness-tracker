from app import create_app, db
from sqlalchemy import text

def upgrade():
    app = create_app()
    with app.app_context():
        # Add name column
        with db.engine.connect() as conn:
            # Add name column
            conn.execute(text('ALTER TABLE physician ADD COLUMN name VARCHAR(100)'))
            
            # Update existing records with names
            updates = {
                'Sports Medicine': 'Dr. John Smith',
                'Nutrition': 'Dr. Sarah Johnson',
                'Physical Therapy': 'Dr. Michael Williams',
                'Exercise Physiology': 'Dr. Emily Brown'
            }
            
            for specialty, name in updates.items():
                conn.execute(
                    text('UPDATE physician SET name = :name WHERE specialty = :specialty'),
                    {'name': name, 'specialty': specialty}
                )
            
            # Make name column not null after setting values
            conn.execute(text('ALTER TABLE physician MODIFY name VARCHAR(100) NOT NULL'))
            conn.commit()

if __name__ == '__main__':
    upgrade() 