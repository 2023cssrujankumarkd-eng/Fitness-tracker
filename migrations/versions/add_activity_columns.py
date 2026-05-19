"""add missing activity columns

Revision ID: add_activity_columns
Revises: create_activity_table
Create Date: 2024-05-17 06:20:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_activity_columns'
down_revision = 'create_activity_table'
branch_labels = None
depends_on = None

def upgrade():
    # Add missing columns to activity table
    op.add_column('activity', sa.Column('name', sa.String(length=100), nullable=False, server_default=''))
    op.add_column('activity', sa.Column('type', sa.String(length=50), nullable=False, server_default=''))
    op.add_column('activity', sa.Column('duration', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('activity', sa.Column('calories_burned', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('activity', sa.Column('timestamp', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')))
    op.add_column('activity', sa.Column('notes', sa.Text(), nullable=True))

def downgrade():
    # Remove added columns from activity table
    op.drop_column('activity', 'notes')
    op.drop_column('activity', 'timestamp')
    op.drop_column('activity', 'calories_burned')
    op.drop_column('activity', 'duration')
    op.drop_column('activity', 'type')
    op.drop_column('activity', 'name') 