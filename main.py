import psycopg2
import matplotlib.pyplot as plt
import numpy as np


username = 'student01'
password = '1111'
database = 'Lab2_CourseraCourses'
host = 'localhost'
port = '5432'

query_1 = '''
CREATE VIEW CoursesStudents AS
SELECT course_title, students_enrolled FROM Students 
JOIN Courses_Organizations USING(course_number)
JOIN Course USING(course_id);
'''

query_2 = '''
CREATE VIEW DifficultyTypesTotal AS
SELECT type_name, COUNT(*) FROM DifficultyType 
JOIN Courses_Organizations
ON DifficultyType.type_id = Courses_Organizations.course_difficulty
GROUP BY type_name;
'''

query_3 = '''
CREATE VIEW StudentsRatings AS
SELECT rating_value, students_enrolled FROM Courses_Organizations 
JOIN Ratings USING(course_number)
JOIN Students USING(course_number)
ORDER BY rating_value ASC;
'''

conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

with conn:

    cur1 = conn.cursor()
    cur1.execute('DROP VIEW IF EXISTS CoursesStudents')
    cur1.execute(query_1)
    cur1.execute('SELECT * FROM CoursesStudents')
    courses = []
    students = []

    for row in cur1:
        courses.append(row[0])
        students.append(row[1])

    cur2 = conn.cursor()
    cur2.execute('DROP VIEW IF EXISTS DifficultyTypesTotal')
    cur2.execute(query_2)
    cur2.execute('SELECT * FROM DifficultyTypesTotal')
    difficulties = []
    difficulties_amount = []

    for row in cur2:
        difficulties.append(row[0])
        difficulties_amount.append(row[1])

    cur3 = conn.cursor()
    cur3.execute('DROP VIEW IF EXISTS StudentsRatings')
    cur3.execute(query_3)
    cur3.execute('SELECT * FROM StudentsRatings')
    students_enrolled = []
    ratings = []

    for row in cur3:
        ratings.append(row[0])
        students_enrolled.append(row[1])


# Bar chart
fig, ax = plt.subplots(figsize=(10, 6))

y_pos = np.arange(len(courses))
hbars = ax.barh(y_pos, students, align='center', color='#8c66ff')
ax.set_yticks(y_pos)
ax.set_yticklabels(courses, fontweight='bold')
ax.xaxis.set_visible(False)
for s in ['top', 'bottom', 'left', 'right']:
    ax.spines[s].set_visible(False)
ax.set_title('Кількість студентів, що залучені до курсу', fontweight='bold', fontsize=14)
ax.bar_label(hbars, padding=4, labels=students, fontsize=8)
plt.tight_layout()

# Pie chart
fig1, ax = plt.subplots()
colors = ['#8c66ff', '#ff66ff', '#66b3ff']
patches, texts, autotexts = ax.pie(difficulties_amount, labels=difficulties, autopct='%.1f%%',
                                   wedgeprops={'linewidth': 3.0, 'edgecolor': 'white'},
                                   textprops={'size': 'x-large'}, colors=colors)
plt.setp(autotexts, color='white', fontweight='bold')
plt.setp(texts, fontsize=14)
ax.set_title('Розподіл складностей', fontsize=18, fontweight='bold')
plt.tight_layout()

# Dependency graph
fig2, ax = plt.subplots()

ax.plot(ratings, students_enrolled, color='black', marker='o')
ax.set(xlabel='Рейтинг', ylabel='Кількість студентів', title='Залежність кількості студенів від рейтингу курсу')
for rt, student in zip(ratings, students_enrolled):
    ax.annotate(student, xy=(rt, student), xytext=(7, 2), textcoords='offset points', fontsize=7)

plt.tight_layout()
plt.show()
