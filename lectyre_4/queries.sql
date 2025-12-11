-- Database Structure: Creating Tables and Indexes

-- Enabling support for foreign keys
PRAGMA foreign_keys = ON;

-- Removing existing tables for a clean start
DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS students;

-- Students table
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    birth_year INTEGER
);

-- Grades table with foreign key
CREATE TABLE grades (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    grade INTEGER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- Creating indexes for optimization
CREATE INDEX idx_student_name ON students (full_name);
CREATE INDEX idx_student_grade ON grades (student_id, grade);


-- INSERTING SAMPLE DATA

-- Inserting students
INSERT INTO students (full_name, birth_year) VALUES
('Alice Johnson', 2005),
('Brian Smith', 2004),
('Carla Reyes', 2006),
('Daniel Kim', 2005),
('Eva Thompson', 2003),
('Felix Nguyen', 2007),
('Grace Patel', 2005),
('Henry Lopez', 2004),
('Isabella Martinez', 2006);

-- Inserting ratings
INSERT INTO grades (student_id, subject, grade) VALUES
(1, 'Math', 88), (1, 'English', 92), (1, 'Science', 85),
(2, 'Math', 75), (2, 'History', 83), (2, 'English', 79),
(3, 'Science', 95), (3, 'Math', 91), (3, 'Art', 89),
(4, 'Math', 84), (4, 'Science', 88), (4, 'Physical Education', 93),
(5, 'English', 90), (5, 'History', 85), (5, 'Math', 88),
(6, 'Science', 72), (6, 'Math', 78), (6, 'English', 81),
(7, 'Art', 94), (7, 'Science', 87), (7, 'Math', 90),
(8, 'History', 77), (8, 'Math', 83), (8, 'Science', 80),
(9, 'English', 96), (9, 'Math', 89), (9, 'Art', 92);


--ANALYTICAL QUERY

--Find all grades for a specific student

SELECT
    s.full_name,
    g.subject,
    g.grade
FROM
    grades g
JOIN
    students s ON g.student_id = s.id
WHERE
    s.full_name = 'Alice Johnson';


--Calculate the average grade for each student


SELECT
    s.full_name,
    ROUND(AVG(g.grade), 2) AS average_grade
FROM
    students s
JOIN
    grades g ON s.id = g.student_id
GROUP BY
    s.full_name
ORDER BY
    average_grade DESC;


--List all students born after 2004


SELECT
    full_name,
    birth_year
FROM
    students
WHERE
    birth_year > 2004;


--List of all subjects and their average grades


SELECT
    subject,
    ROUND(AVG(grade), 2) AS average_grade
FROM
    grades
GROUP BY
    subject
ORDER BY
    average_grade DESC;


--Find the top 3 students with the highest grade point averages

SELECT
    s.full_name,
    ROUND(AVG(g.grade), 2) AS average_grade
FROM
    students s
JOIN
    grades g ON s.id = g.student_id
GROUP BY
    s.full_name
ORDER BY
    average_grade DESC
LIMIT 3;


--Show all students who scored less than 80 points in any subject


SELECT DISTINCT
    s.full_name
FROM
    students s
JOIN
    grades g ON s.id = g.student_id
WHERE
    g.grade < 80
ORDER BY
    s.full_name;



