import csv
import psycopg2

username = 'student01'
password = '1111'
database = 'Lab2_CourseraCourses'

OUTPUT_FILE_T = 'Hudym_DB_{}.csv'

TABLES = [
    'course',
    'organization',
    'courses_organizations',
    'difficultytype',
    'ratings',
    'students',
    'certification'
]

conn = psycopg2.connect(user=username, password=password, dbname=database)

with conn:
    cur = conn.cursor()

    for table_name in TABLES:
        cur.execute('SELECT * FROM ' + table_name)
        fields = [x[0] for x in cur.description]
        with open(OUTPUT_FILE_T.format(table_name), 'w', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(fields)
            for row in cur:
                writer.writerow([str(x) for x in row])