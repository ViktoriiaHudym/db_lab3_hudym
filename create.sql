DROP TABLE IF EXISTS Courses_Organizations CASCADE;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Organization;
DROP TABLE IF EXISTS Certification;
DROP TABLE IF EXISTS DifficultyType;
DROP TABLE IF EXISTS Ratings;
DROP TABLE IF EXISTS Students;

CREATE TABLE Course(
    course_id SERIAL PRIMARY KEY,
	course_title VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE Organization(
    organization_id SERIAL PRIMARY KEY,
	organization_name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE Certification(
    certification_id SERIAL PRIMARY KEY,
	certificate_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE DifficultyType(
    type_id SERIAL PRIMARY KEY,
	type_name VARCHAR(20) UNIQUE NOT NULL	
);

CREATE TABLE Courses_Organizations(
    course_id       INT NOT NULL REFERENCES Course(course_id) ON DELETE CASCADE,
    organization_id INT NOT NULL REFERENCES Organization(organization_id) ON DELETE CASCADE,
	course_number SERIAL UNIQUE NOT NULL,
	course_certificate INT REFERENCES Certification(certification_id) ON DELETE RESTRICT,
	course_difficulty  INT REFERENCES DifficultyType(type_id) ON DELETE RESTRICT,
	CONSTRAINT course_organization_pkey PRIMARY KEY(course_id, organization_id)
);

CREATE TABLE Ratings(
    course_number INT UNIQUE REFERENCES Courses_Organizations(course_number) ON DELETE CASCADE,
	rating_value  NUMERIC,
	PRIMARY KEY(course_number)
);

CREATE TABLE Students(
    course_number INT UNIQUE REFERENCES Courses_Organizations(course_number) ON DELETE CASCADE,
	students_enrolled  INT,
	PRIMARY KEY(course_number)
);

