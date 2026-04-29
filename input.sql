/* DEMO QUERIES*/
SELECT name FROM students;
INSERT INTO students VALUES (101);
UPDATE students SET marks = 90;
DELETE FROM students;
SELECT * FROM students;

/* more queries added with differnt meaning and use cases*/

SELECT name, marks FROM students;

SELECT * FROM students WHERE marks > 80;

SELECT * FROM students WHERE name = 'Rahul';

DELETE FROM students WHERE id = 101;

DELETE FROM students WHERE marks < 40;

DELETE FROM students WHERE name = 'Amit';

DELETE FROM students WHERE marks IS NULL;

UPDATE students SET marks = 95 WHERE id = 101;

UPDATE students SET name = 'Arjun' WHERE id = 102;

UPDATE students SET marks = marks + 5;

UPDATE students SET marks = 0 WHERE marks IS NULL;

INSERT INTO students VALUES (102, 'Amit', 85);

INSERT INTO students (id, name) VALUES (103, 'Neha');

INSERT INTO students (id, name, marks) VALUES (104, 'Riya', 92);

INSERT INTO students VALUES (105, 'Karan', 78), (106, 'Simran', 88);
