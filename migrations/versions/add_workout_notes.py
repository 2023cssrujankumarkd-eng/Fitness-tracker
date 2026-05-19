"""add workout notes column

Revision ID: add_workout_notes
Revises: add_workout_timestamp
Create Date: 2024-05-17 06:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_workout_notes'
down_revision = 'add_workout_timestamp'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('workout', sa.Column('notes', sa.Text(), nullable=True))

def downgrade():
    op.drop_column('workout', 'notes') 