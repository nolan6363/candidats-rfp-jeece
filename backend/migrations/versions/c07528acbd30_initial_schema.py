"""initial schema

Revision ID: c07528acbd30
Revises: 
Create Date: 2026-03-24 15:59:15.624067

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c07528acbd30'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('action_logs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('voeu_rank', sa.SmallInteger(), nullable=True))
        batch_op.add_column(sa.Column('voeu_role', sa.String(length=100), nullable=True))
    op.execute("ALTER TABLE action_logs MODIFY COLUMN action ENUM('abandoned', 'restored', 'voeu_deleted') NOT NULL")


def downgrade():
    op.execute("ALTER TABLE action_logs MODIFY COLUMN action ENUM('abandoned', 'restored') NOT NULL")
    with op.batch_alter_table('action_logs', schema=None) as batch_op:
        batch_op.drop_column('voeu_role')
        batch_op.drop_column('voeu_rank')
