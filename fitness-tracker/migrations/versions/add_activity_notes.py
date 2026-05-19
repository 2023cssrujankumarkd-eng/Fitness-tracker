"""add activity notes column

Revision ID: add_activity_notes
Revises: add_activity_calories
Create Date: 2024-05-17 06:50:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_activity_notes'
down_revision = 'add_activity_calories'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('activity', sa.Column('notes', sa.Text(), nullable=True))

def downgrade():
    op.drop_column('activity', 'notes') 