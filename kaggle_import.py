import psycopg2
import csv

username = 'student01'
password = '1111'
database = 'Lab2_CourseraCourses'

INPUT_CSV_FILE = 'coursera_data.csv'

query_0 = """
DELETE FROM courses_organizations;
DELETE FROM certification;
DELETE FROM course;
DELETE FROM difficultytype;
DELETE FROM organization;
DELETE FROM ratings;
DELETE FROM students;
"""

query_1 ="""
INSERT INTO difficultytype(type_name) VALUES (%s)
"""

query_2 ="""
INSERT INTO certification(certificate_name) VALUES (%s)
"""

query_3 ="""
INSERT INTO organization(organization_name) VALUES (%s)
"""

query_4 ="""
INSERT INTO course(course_title) VALUES (%s)
"""

query_5 = """
INSERT INTO courses_organizations(course_id, organization_id, course_certificate, course_difficulty) 
SELECT course_id, organization_id, certification_id, type_id FROM course, organization, Certification, DifficultyType
WHERE course_title = %s AND organization_name = %s AND certificate_name = %s AND type_name = %s
ON CONFLICT DO NOTHING;
"""

query_6 = """
INSERT INTO ratings(course_number, rating_value) VALUES
((SELECT course_number FROM courses_organizations JOIN 
course USING(course_id) JOIN
organization USING(organization_id) WHERE course_title = %s AND organization_name = %s), %s)
ON CONFLICT DO NOTHING
"""
query_7 = """
INSERT INTO students(course_number, students_enrolled) VALUES
((SELECT course_number FROM courses_organizations JOIN 
course USING(course_id) JOIN
organization USING(organization_id) WHERE course_title = %s AND organization_name = %s), %s)
ON CONFLICT DO NOTHING
"""


conn = psycopg2.connect(user=username, password=password, dbname=database)

with conn:
    cur = conn.cursor()
    cur.execute(query_0)
    with open(INPUT_CSV_FILE, 'r', encoding='utf-8') as inf:
        reader = csv.reader(inf)
        next(reader)
        difficulties = []
        certificates = []
        courses = []
        organizations = []
        for row in reader:
            courses.append(row[1])
            organizations.append(row[2])
            certificates.append(row[3])
            difficulties.append(row[5])

        values_d = list(set(difficulties))
        values_o = list(set(organizations))
        values_co = list(set(courses))
        values_ce = list(set(certificates))

        for v in values_d:
            cur.execute(query_1, tuple([v]))
        for v in values_ce:
            cur.execute(query_2, tuple([v]))
        for v in values_o:
            cur.execute(query_3, tuple([v]))
        for v in values_co:
            cur.execute(query_4, tuple([v]))

    conn.commit()

    with open(INPUT_CSV_FILE, 'r', encoding='utf-8') as inf:
        reader = csv.reader(inf)
        next(reader)
        for row in reader:
            cur.execute(query_5, (row[1], row[2], row[3], row[5]))
            cur.execute(query_6, (row[1], row[2], float(row[4])))
            if 'k' in row[6]:
                st = float(row[6].replace('k', '')) * 1000
            elif 'm' in row[6]:
                st = float(row[6].replace('m', '')) * 1000000
            cur.execute(query_7, (row[1], row[2], int(st)))

    conn.commit()