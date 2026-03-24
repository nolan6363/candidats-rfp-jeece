-- Migration 001 : ajout du suivi des suppressions de vœux
ALTER TABLE action_logs
    MODIFY COLUMN action ENUM('abandoned', 'restored', 'voeu_deleted') NOT NULL,
    ADD COLUMN voeu_rank TINYINT NULL AFTER action,
    ADD COLUMN voeu_role VARCHAR(100) NULL AFTER voeu_rank;
