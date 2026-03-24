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
    # Crée la table si elle n'existe pas (volume neuf sans init.sql complet)
    op.execute("""
        CREATE TABLE IF NOT EXISTS action_logs (
            id           INT AUTO_INCREMENT PRIMARY KEY,
            candidate_id INT NOT NULL,
            action       ENUM('abandoned', 'restored', 'voeu_deleted') NOT NULL,
            voeu_rank    SMALLINT NULL,
            voeu_role    VARCHAR(100) NULL,
            created_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
    """)
    # Ajoute les colonnes si elles n'existent pas déjà (table créée par une ancienne version d'init.sql)
    op.execute("ALTER TABLE action_logs ADD COLUMN IF NOT EXISTS voeu_rank SMALLINT NULL")
    op.execute("ALTER TABLE action_logs ADD COLUMN IF NOT EXISTS voeu_role VARCHAR(100) NULL")
    op.execute("ALTER TABLE action_logs MODIFY COLUMN action ENUM('abandoned', 'restored', 'voeu_deleted') NOT NULL")


def downgrade():
    op.execute("ALTER TABLE action_logs MODIFY COLUMN action ENUM('abandoned', 'restored') NOT NULL")
    with op.batch_alter_table('action_logs', schema=None) as batch_op:
        batch_op.drop_column('voeu_role')
        batch_op.drop_column('voeu_rank')
