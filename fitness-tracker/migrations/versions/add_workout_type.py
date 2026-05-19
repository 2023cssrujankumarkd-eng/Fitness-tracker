"""add workout type column

Revision ID: add_workout_type
Revises: 
Create Date: 2024-05-17 06:01:54.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_workout_type'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Add type column to workout table
    op.add_column('workout', sa.Column('type', sa.String(50), nullable=False, server_default='strength'))

def downgrade():
    # Remove type column from workout table
    op.drop_column('workout', 'type') 