CREATE DATABASE elearning;
USE elearning;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(255),
    xp INT DEFAULT 0,
    level INT DEFAULT 1
);

CREATE TABLE lessons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    content TEXT
);

CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lesson_id INT,
    question TEXT,
    FOREIGN KEY (lesson_id) REFERENCES lessons(id)
);

CREATE TABLE answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT,
    option_text VARCHAR(255),
    is_correct BOOLEAN,
    FOREIGN KEY (question_id) REFERENCES questions(id)
);

-- DATE DE TEST
INSERT INTO lessons (title, content) VALUES
("Python Basics", "Introducere în Python"),
("If Statements", "Structuri condiționale");

INSERT INTO questions (lesson_id, question) VALUES
(1, "Ce tip de limbaj este Python?"),
(2, "Ce face if?");

INSERT INTO answers (question_id, option_text, is_correct) VALUES
(1, "Interpretat", TRUE),
(1, "Compilat", FALSE),
(2, "Verifică condiții", TRUE),
(2, "Face loop", FALSE);