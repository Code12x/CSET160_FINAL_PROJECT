CREATE DATABASE IF NOT EXISTS CSET160_FINAL_PROJECT;
USE CSET160_FINAL_PROJECT;

DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Teachers;
DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Tests;
DROP TABLE IF EXISTS TestQuestions;
DROP TABLE IF EXISTS TestAttempts;
DROP TABLE IF EXISTS TestAttemptQuestions;

CREATE TABLE IF NOT EXISTS `Users` (
  `user_id` INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(25) NOT NULL UNIQUE,
  `email` VARCHAR(50) NOT NULL UNIQUE,
  `password` VARCHAR(40) NOT NULL,
  `date_created` DATETIME DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS `Teachers` (
  `teacher_id` INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL,
  FOREIGN KEY(user_id) REFERENCES Users(user_id)
);

CREATE TABLE IF NOT EXISTS `Students` (
  `student_id` INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL,
  FOREIGN KEY(user_id) REFERENCES Users(user_id)
);

CREATE TABLE IF NOT EXISTS `Tests` (
  `test_id` INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
  `teacher_id` INT NOT NULL,
  `test_name` VARCHAR(40) NOT NULL,
  `date_created` DATETIME NOT NULL DEFAULT NOW(),
  `date_edited` DATETIME NOT NULL DEFAULT NOW(),
  FOREIGN KEY(teacher_id) REFERENCES Teachers(teacher_id)
);

CREATE TABLE IF NOT EXISTS `TestQuestions` (
  `test_question_id` INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
  `test_id` INT NOT NULL,
  `question` VARCHAR(255) NOT NULL,
  `answer` VARCHAR(255) NOT NULL,
  FOREIGN KEY(test_id) REFERENCES Tests(test_id)
);

CREATE TABLE IF NOT EXISTS `TestAttempts` (
  `test_attempt_id` INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
  `student_id` INT NOT NULL,
  `test_id` INT NOT NULL,
  FOREIGN KEY(student_id) REFERENCES Students(student_id),
  FOREIGN KEY(test_id) REFERENCES Tests(test_id)
);

CREATE TABLE IF NOT EXISTS `TestAttemptQuestions` (
  `test_attempt_question_id` INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
  `test_attempt_id` INT NOT NULL,
  `question_id` INT NOT NULL,
  `attempted_answer` VARCHAR(255) NOT NULL,
  FOREIGN KEY(test_attempt_id) REFERENCES TestAttempts(test_attempt_id),
  FOREIGN KEY(question_id) REFERENCES TestQuestions(test_question_id)
);
