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
    op.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id        INT AUTO_INCREMENT PRIMARY KEY,
            prenom    VARCHAR(100) NOT NULL,
            nom       VARCHAR(150) NOT NULL,
            abandoned BOOLEAN NOT NULL DEFAULT FALSE
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
    """)
    op.execute("""
        CREATE TABLE IF NOT EXISTS voeux (
            id           INT AUTO_INCREMENT PRIMARY KEY,
            candidate_id INT NOT NULL,
            rank         TINYINT NOT NULL,
            role         VARCHAR(100) NOT NULL,
            FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE,
            UNIQUE KEY uq_candidate_rank (candidate_id, rank)
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
    """)
    op.execute("""
        CREATE TABLE IF NOT EXISTS action_logs (
            id           INT AUTO_INCREMENT PRIMARY KEY,
            candidate_id INT NOT NULL,
            action       ENUM('abandoned', 'restored', 'voeu_deleted', 'voeu_restored') NOT NULL,
            voeu_rank    SMALLINT NULL,
            voeu_role    VARCHAR(100) NULL,
            created_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
    """)
    op.execute("ALTER TABLE action_logs ADD COLUMN IF NOT EXISTS voeu_rank SMALLINT NULL")
    op.execute("ALTER TABLE action_logs ADD COLUMN IF NOT EXISTS voeu_role VARCHAR(100) NULL")
    op.execute("ALTER TABLE action_logs MODIFY COLUMN action ENUM('abandoned', 'restored', 'voeu_deleted', 'voeu_restored') NOT NULL")


def downgrade():
    op.execute("ALTER TABLE action_logs MODIFY COLUMN action ENUM('abandoned', 'restored') NOT NULL")
    with op.batch_alter_table('action_logs', schema=None) as batch_op:
        batch_op.drop_column('voeu_role')
        batch_op.drop_column('voeu_rank')
