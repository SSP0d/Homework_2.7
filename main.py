from datetime import datetime

from sqlalchemy import func, desc, and_

from database.db import session
from database.models import Subject, Student, Grade, Teacher, Team


# Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def query_01():
    results = session.query(
        Student.name,
        func.round(func.avg(Grade.grades), 2).label('avg_grade')
    ).select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
    print(f'5 cтудентів з найвищим середнім балом')
    for result in results:
        print(
            f'Студент: {result[0]} Бал: {result[1]}'
        )


# Знайти студента із найвищим середнім балом з певного предмета.
def query_02(subject_id: int):
    student_avg = session.query(
        Student.name,
        func.round(func.avg(Grade.grades), 2).label("avg_grade"),
        Subject.subject_name
    ).select_from(Grade).join(Student).join(Subject).filter(
        Subject.id == subject_id
    ).group_by(
        Subject.id,
        Student.id
    ).order_by(
        desc("avg_grade")
    ).first()

    result = []
    for el in student_avg:
        result.append(str(el))
    n = '\n'
    print(
        f"{n}Студент із найвищим середнім балом{n}"
        f"Ім'я: {result[0]}{n}"
        f"Cередній бал: {result[1]}{n}Предмет: {result[2]}"
    )


# Знайти середній бал у групах з певного предмета.
def query_03(subject_id: int):
    avg_grade = session.query(
        Team.team_name,
        func.round(func.avg(Grade.grades), 2).label("avg_grade"),
        Subject.subject_name
    ).select_from(Grade).join(Student).join(Team).join(Subject).filter(
        Subject.id == subject_id
    ).group_by(
        Team.id,
        Subject.id
    ).order_by(
        Team.id).all()
    for el in avg_grade:
        print(
            f'Група: {el[0]} має середній бал: {el[1]} за пердметом: {el[2]}'
        )


# Знайти середній бал на потоці (по всій таблиці оцінок).
def query_04():
    average = session.query(
        func.round(func.avg(Grade.grades), 2).label('avg_grade')
    ).select_from(Grade).one()
    n = '\n'
    print(
        f'{n}Середній бал на потоці: {average[0]}'
    )


# Знайти які курси читає певний викладач.
def query_05(teacher_id: int):
    teacher_subjects = session.query(
        Teacher.name,
        Subject.subject_name,
    ).select_from(Subject).join(Teacher).filter(Teacher.id == teacher_id).all()
    # print(teacher_subjects)
    subjects = []
    teacher = ''
    for result in teacher_subjects:
        teacher = result[0]
        subjects.append(result[1])
    n = '\n'
    print(
        f"{n}Викладач: {teacher}{n}"
        f"Читає предмети: {', '.join([el for el in subjects])}"
    )

# Знайти список студентів у певній групі.
def query_06(group_id: int):
    students = session.query(
        Student.name,
        Team.team_name
    ).select_from(Student).join(Team).filter(Team.id == group_id).all()

    student_list = []
    group_name = ''
    for student in students:
        student_list.append(student[0])
        group_name = student[1]
    n = '\n'
    print(
        f"{n}Група: {group_name}{n}"
        f"Студенти: {', '.join(el for el in student_list)}"
    )


# Знайти оцінки студентів у окремій групі з певного предмета.
def query_07(subject_id: int, group_id: int):
    grades = session.query(
        Grade.grades,
        Subject.subject_name,
        Team.team_name
    ).select_from(Grade).join(Subject).join(Student).join(Team).filter(and_(
        Subject.id == subject_id,
        Team.id == group_id
    )).all()

    all_grades = []
    group = ''
    subject = ''
    for grade in grades:
        all_grades.append(grade[0])
        subject = grade[1]
        group = grade[2]
    n = '\n'
    print(
        f'{n}Група: {group}{n}'
        f'Предмет: {subject}{n}'
        f'Оцінки: {", ".join(str(el) for el in all_grades)}'
    )



# Знайти середній бал, який ставить певний викладач зі своїх предметів.
def query_08(teacher_id: int):
    avg_grades = session.query(
        func.round(func.avg(Grade.grades), 2).label('avg_grade'),
        Teacher.name
    ).select_from(Grade).join(Subject).join(Teacher).group_by(Teacher.name).filter(
        Subject.teacher_id == teacher_id
    ).all()

    avg_grade = ''
    teacher = ''
    for result in avg_grades:
        avg_grade = result[0]
        teacher = result[1]
    n = '\n'
    print(
        f'{n}Викладач: {teacher} ставить середній бал: {avg_grade}'
    )


# Знайти список курсів, які відвідує певний студент.
def query_09(student_id: int):
    courses = session.query(
        Student.name,
        Subject.subject_name
    ).select_from(Student).join(Grade).join(Subject).filter(
        Student.id == student_id
    ).all()

    student = ''
    subjects = []
    for result in courses:
        student = result[0]
        subjects.append(result[1])
    n = '\n'
    print(
        f'{n}Студент: {student}{n}'
        f'Відвідує заняття: {", ".join(el for el in subjects)}'
    )


# Список курсів, які певному студенту читає певний викладач.
def query_10(teacher_id: int, student_id: int):
    courses = session.query(
        Student.name,
        Subject.subject_name,
        Teacher.name
    ).select_from(Student).join(Grade).join(Subject).join(Teacher).filter(and_(
        Student.id == student_id,
        Teacher.id == teacher_id
    )).all()

    subjects = []
    student = ''
    teacher = ''
    for result in courses:
        student = result[0]
        subjects.append(result[1])
        teacher = result[2]
    n = '\n'
    print(
        f'{n}Викладач: {teacher}{n}'
        f'Студент: {student}{n}'
        f'Предмети: {", ".join(el for el in subjects)}'
    )


# Середній бал, який певний викладач ставить певному студентові.
def query_11(student_id: int, teacher_id: int):
    avg_grade = session.query(
        Student.name,
        func.round(func.avg(Grade.grades), 2).label("avg_grade"),
        Teacher.name
    ).select_from(Grade).join(Student).join(Subject).join(Teacher).filter(and_(
        Student.id == student_id,
        Teacher.id == teacher_id
    )).group_by(
        Student.id,
        Teacher.id).all()

    temp_list = []
    for el in avg_grade:
        for i in el:
            temp_list.append(i)
    n = '\n'
    print(
        f'{n}Викладач: {temp_list[2]}{n}'
        f'Студент: {temp_list[0]}{n}'
        f'Отриманий середній бал: {temp_list[1]}'
    )


# Оцінки студентів у певній групі з певного предмета на останньому занятті.
def query_12(team_id: int, subject_id: int):
    last_date = session.query(
        Grade.lesson_date.label('t')
    ).select_from(Grade).join(Student).join(Team).join(Subject).order_by((desc('t'))).filter(and_(
        Team.id == team_id,
        Subject.id == subject_id
    )).first()

    grades = session.query(
        Team.team_name,
        Grade.grades,
        Subject.subject_name,
        Grade.lesson_date.label('time')
    ).select_from(Team).join(Student).join(Grade).join(Subject).order_by(
        desc(Grade.lesson_date)).filter(and_(
            Team.id == team_id,
            Subject.id == subject_id,
        )).all()

    last_day = []
    for el in grades:
        day_edit = datetime.date(el[3]).strftime('%Y%m%d')
        for day in last_date:
            last_lesson = datetime.date(day).strftime('%Y%m%d')
            if day_edit == last_lesson:
                last_day.append(el)

    team = ''
    grades = []
    subject = ''
    date = ''

    tuple_to_list = []
    for el in last_day:
        tuple_to_list.append([i for i in el])

    for i in tuple_to_list:
        team = i[0]
        grades.append(i[1])
        subject = i[2]
        date = i[3]

    print(f'На останньому занятті {datetime.date(date)} з предмету {subject} група {team} отримала оцінки:{grades}')


if __name__ == '__main__':
    # query_01()
    # query_02(5)
    # query_03(5)
    # query_04()
    # query_05(5)
    # query_06(3)
    # query_07(5, 3)
    # query_08(5)
    # query_09(5)
    # query_10(5, 5)
    query_11(5, 5)
    # query_12(3, 7)