SET NAMES utf8mb4;

CREATE TABLE IF NOT EXISTS candidates (
    id   INT AUTO_INCREMENT PRIMARY KEY,
    prenom VARCHAR(100) NOT NULL,
    nom    VARCHAR(150) NOT NULL,
    abandoned BOOLEAN NOT NULL DEFAULT FALSE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS voeux (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT      NOT NULL,
    rank         TINYINT  NOT NULL,
    role         VARCHAR(100) NOT NULL,
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE,
    UNIQUE KEY uq_candidate_rank (candidate_id, rank)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS action_logs (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT NOT NULL,
    action       ENUM('abandoned', 'restored', 'voeu_deleted', 'voeu_restored') NOT NULL,
    voeu_rank    SMALLINT NULL,
    voeu_role    VARCHAR(100) NULL,
    created_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

INSERT INTO candidates (id, prenom, nom) VALUES
(1,  'Aicha',               'Ahmed Mze Zoubeiri'),
(2,  'Alexander',           'Anagnostos'),
(3,  'Nathan',              'Anciaux'),
(4,  'Satine',              'Ardisson'),
(5,  'Kenza',               'Attia'),
(6,  'Vittorio',            'Bassi'),
(7,  'Adrian',              'Benazzouz'),
(8,  'Gustave',             'Berthier'),
(9,  'Yvan',                'Bona'),
(10, 'Sébastien',           'Bouchet'),
(11, 'Alexis',              'Brucker'),
(12, 'Julian',              'Cattin-Quest'),
(13, 'Gabriel',             'Chevallier'),
(14, 'Silouane',            'Chouteau'),
(15, 'Maxence',             'Cristiani'),
(16, 'Maxime',              'Curie'),
(17, 'Killian',             'Darde'),
(18, 'Pierre',              'De Barrigue de Montvallon'),
(19, 'Paul',                'De Rose'),
(20, 'Chloé',               'Dejoux'),
(21, 'Gabriel Jason Harlys','Dong'),
(22, 'Gabriel',             'Entremont'),
(23, 'Amal',                'Fagbemi'),
(24, 'Hugo',                'Fedoroff'),
(25, 'Manon',               'Feraud Jouberteix'),
(26, 'Paul',                'Fievet'),
(27, 'Paul',                'Gabriel Lhermet'),
(28, 'Justine',             'Gallienne'),
(29, 'Paul',                'Giraud'),
(30, 'Raphael',             'Hallak'),
(31, 'Alexis',              'Hubert'),
(32, 'Corentin',            'Lepeltier'),
(33, 'Olivia',              'Mazille'),
(34, 'Constant',            'Mignot'),
(35, 'Pierre',              'Morineaux'),
(36, 'Clémentine',          'Nammour'),
(37, 'Nicolas',             'Normand'),
(38, 'Chadi',               'Noureddine'),
(39, 'Umang',               'Rawat'),
(40, 'Augustin',            'Regnouf de Vains'),
(41, 'Ludovic',             'Salati'),
(42, 'Thibault',            'Senhadji'),
(43, 'Mael',                'Seytre'),
(44, 'Meaghan',             'Smadja'),
(45, 'Arthur',              'Soupiron'),
(46, 'Loïc',                'Tcheutchouatchinde'),
(47, 'Serge André',         'Tchouameni Hameni'),
(48, 'Julie',               'Thomas'),
(49, 'Line',                'Tralongo'),
(50, 'Yannick',             'Van Heerden'),
(51, 'Clémence',            'Vercaemer'),
(52, 'Aaron',               'Wipliez'),
(53, 'Alexandre',           'Yang');

INSERT INTO voeux (candidate_id, rank, role) VALUES
-- 1 Aicha Ahmed Mze Zoubeiri
(1,1,'CDM SI'),(1,2,'CDM Comm'),(1,3,'CDM Market'),
-- 2 Alexander Anagnostos
(2,1,'Chef de Projet'),(2,2,'CDM SI'),(2,3,'CDM Market'),
-- 3 Nathan Anciaux
(3,1,'CDM Perf'),(3,2,'DirOps'),(3,3,'Chef de Projet'),
-- 4 Satine Ardisson
(4,1,'SG'),(4,2,'DirOps'),(4,3,'CDM RH'),
-- 5 Kenza Attia
(5,1,'CDM Market'),(5,2,'CDM Comm'),(5,3,'CDM RH'),
-- 6 Vittorio Bassi
(6,1,'CDM Market'),(6,2,'CDM SI'),(6,3,'CDM Perf'),
-- 7 Adrian Benazzouz
(7,1,'SG'),(7,2,'CDM RH'),(7,3,'RM'),
-- 8 Gustave Berthier
(8,1,'Chef de Projet'),(8,3,'CDM SI'),
-- 9 Yvan Bona
(9,1,'CDM Comm'),(9,2,'CDM RH'),(9,3,'CDM SI'),
-- 10 Sébastien Bouchet
(10,1,'RTC Elec'),(10,2,'CDM Perf'),
-- 11 Alexis Brucker
(11,1,'CDM Market'),(11,2,'CDM Perf'),(11,3,'CDM Comm'),
-- 12 Julian Cattin-Quest
(12,1,'DirCo'),(12,2,'Chef de Projet'),
-- 13 Gabriel Chevallier
(13,1,'DirOps'),(13,2,'DirCo'),(13,3,'Chef de Projet'),
-- 14 Silouane Chouteau
(14,1,'RTC'),(14,2,'DSI'),(14,3,'RC'),
-- 15 Maxence Cristiani
(15,1,'CDM Perf'),(15,2,'CDM SI'),(15,3,'CDM RH'),
-- 16 Maxime Curie
(16,1,'Trésorerie'),(16,2,'RDI'),(16,3,'CDM SI'),
-- 17 Killian Darde
(17,1,'CDM Market'),(17,2,'CDM SI'),(17,3,'CDM Perf'),
-- 18 Pierre De Barrigue de Montvallon
(18,1,'CDM Market'),(18,2,'CDM Perf'),(18,3,'CDM RH'),
-- 19 Paul De Rose
(19,1,'CDM Perf'),(19,2,'DSI'),(19,3,'CDM SI'),
-- 20 Chloé Dejoux
(20,1,'DirOps'),(20,2,'CDM RH'),(20,3,'RM'),
-- 21 Gabriel Jason Harlys Dong
(21,1,'CDM RH'),(21,2,'CDM Perf'),(21,3,'RM'),
-- 22 Gabriel Entremont
(22,1,'CDM Market'),(22,2,'CDM Perf'),
-- 23 Amal Fagbemi
(23,1,'RM'),(23,2,'CDM RH'),(23,3,'RC'),
-- 24 Hugo Fedoroff
(24,1,'CDM Perf'),(24,2,'CDM Market'),(24,3,'CDM RH'),
-- 25 Manon Feraud Jouberteix
(25,1,'RM'),(25,2,'CDM Market'),(25,3,'RC'),
-- 26 Paul Fievet
(26,1,'DirOps'),(26,2,'CDM Perf'),(26,3,'Chef de Projet'),
-- 27 Paul Gabriel Lhermet
(27,1,'Chef de Projet'),(27,2,'CDM Market'),(27,3,'CDM Comm'),
-- 28 Justine Gallienne
(28,1,'DirOps'),(28,2,'CDM Perf'),(28,3,'Chef de Projet'),
-- 29 Paul Giraud
(29,1,'Chef de Projet'),(29,2,'CDM Market'),(29,3,'CDM SI'),
-- 30 Raphael Hallak
(30,1,'RM'),(30,2,'CDM Market'),(30,3,'CDM SI'),
-- 31 Alexis Hubert
(31,1,'DirOps'),(31,2,'CDM Perf'),
-- 32 Corentin Lepeltier
(32,1,'Trésorerie'),(32,2,'CDM SI'),(32,3,'CDM Perf'),
-- 33 Olivia Mazille
(33,1,'CDM Comm'),(33,2,'CDM Market'),(33,3,'CDM Perf'),
-- 34 Constant Mignot
(34,1,'Trésorerie'),(34,2,'DirOps'),
-- 35 Pierre Morineaux
(35,1,'Trésorerie'),(35,2,'DirCo'),(35,3,'RM'),
-- 36 Clémentine Nammour
(36,1,'Trésorerie'),(36,2,'DirOps'),(36,3,'RM'),
-- 37 Nicolas Normand
(37,1,'Trésorerie'),(37,2,'CDM Perf'),(37,3,'CDM SI'),
-- 38 Chadi Noureddine
(38,1,'Chef de Projet'),
-- 39 Umang Rawat
(39,1,'RM'),(39,2,'CDM Market'),(39,3,'SG'),
-- 40 Augustin Regnouf de Vains
(40,1,'CDM Perf'),(40,2,'CDM RH'),
-- 41 Ludovic Salati
(41,1,'Président'),(41,2,'Trésorerie'),(41,3,'DirCo'),
-- 42 Thibault Senhadji
(42,1,'RDI'),(42,2,'CDM RH'),
-- 43 Mael Seytre
(43,1,'Chef de Projet'),(43,2,'Trésorerie'),(43,3,'CDM Perf'),
-- 44 Meaghan Smadja
(44,1,'CDM RH'),(44,2,'CDM Perf'),(44,3,'CDM SI'),
-- 45 Arthur Soupiron
(45,1,'CDM SI'),(45,2,'DSI'),
-- 46 Loïc Tcheutchouatchinde
(46,1,'RM'),(46,2,'Chef de Projet'),(46,3,'RTC'),
-- 47 Serge André Tchouameni Hameni
(47,1,'CDM SI'),(47,2,'CDM Perf'),(47,3,'Chef de Projet'),
-- 48 Julie Thomas
(48,1,'CDM Perf'),(48,2,'Trésorerie'),(48,3,'CDM RH'),
-- 49 Line Tralongo
(49,1,'Chef de Projet'),(49,2,'CDM SI'),
-- 50 Yannick Van Heerden
(50,1,'Président'),(50,2,'DirCo'),(50,3,'Trésorerie'),
-- 51 Clémence Vercaemer
(51,1,'Président'),(51,2,'DirOps'),(51,3,'Trésorerie'),
-- 52 Aaron Wipliez
(52,1,'Président'),(52,2,'Trésorerie'),(52,3,'Chef de Projet'),
-- 53 Alexandre Yang
(53,1,'RTC'),(53,2,'RDI');
