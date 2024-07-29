from sqlalchemy import func,desc
from models import Student, Group, Teacher, Subject, Grade
from models import Session

from termcolor import colored
from colorama import Fore, Back, Style



# 1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1():

    session = Session()
    results = (
        session.query(Student.name, func.round(func.avg(Grade.grade), 2)
        .label('avg_grade'))
        .select_from(Grade)
        .join(Student)
        .group_by(Student.id)
        .order_by(desc('avg_grade'))
        .limit(5)
        .all()
    )
    # return f"\n1. Five students with the highest avr. grade:\n\t {colored(results, "light_yellow")}"
    print(Fore.LIGHTGREEN_EX+ "\n1. Five students with the highest avr. grade are:\n\t" + Style.RESET_ALL, colored(results, "light_yellow"))
    
# 2. Знайти студента із найвищим середнім балом з певного предмета.
def select_2(subject_name):
    session = Session()
    results = (
        session.query(Student)
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .first()
    )
    session.close()
    return f"\n2. Name of the students with the highest avr. grade is:\n\t {colored(results, "light_yellow")}"

# 3. Знайти середній бал у групах з певного предмета.
def select_3(subject_name):
    session = Session()
    results = (
        session.query(Group.name, func.round(func.avg(Grade.grade).label('avg_grade'), 2))
        .join(Student, Group.id == Student.group_id)
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Group.name)
        .all()
    )
    session.close()
    return f"\n3. The average score in groups for a certain subject is:\n\t {colored(results, "light_yellow")}"

# 4. Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4():
    session = Session()
    results = (
        session.query(func.round(func.avg(Grade.grade).label('avg_grade'), 2))
       .join(Student, Grade.student_id == Student.id)
       .join(Group, Student.group_id == Group.id)
       .first()
    )
    session.close()
    return f'\n4. The avr. grade for a course (across the entire grade table) is:\n\t {colored(results, "light_yellow")}'


# 5. Знайти які курси читає певний викладач.
def select_5(name_teacher):
    session = Session()
    results = (
        session.query(Subject)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .filter(Teacher.name.contains(name_teacher))
        .all()
    )
    session.close()
    subject_names = [str(subject) for subject in results]
    return f"\n5. The instructor's courses are:\n\t {colored(subject_names, "light_yellow")}"
    
# 6. Знайти список студентів у певній групі.
def select_6(group_name):
    session = Session()
    results = (
        session.query(Student)
        .join(Group, Student.group_id == Group.id)
        .filter(Group.name == group_name)
        # .group_by(Student.group_id)
        .order_by(Student.name)
        .all()
    )
    students_name = [str(Student) for Student in results]
    return f"\n6. The students list in the certain group is:\n\t {colored(students_name, "light_yellow")}"

# 7. Знайти оцінки студентів у окремій групі з певного предмета.
def select_7(group_name, subject_name):
    session = Session()
    results = (
        session.query(Grade)
        .join(Student, Grade.student_id == Student.id)
        .join(Group, Student.group_id == Group.id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Group.name == group_name)
        .filter(Subject.name == subject_name)
        .all()
    )
    session.close()
    results = [str(Grade) for Grade in results]
    return f"\n7. The students grades in a separate group for the certain subject are:\n\t {colored(results, "light_yellow")}"

# 8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8(teacher_name):
    session = Session()
    result = (
        session.query(func.round(func.avg(Grade.grade), 2))
        .join(Subject, Teacher.id == Subject.teacher_id)
        .join(Teacher, Teacher.id == Subject.teacher_id)
        .filter(Teacher.name == teacher_name)
        .scalar()
    )
    session.close()
    return f"\n8. The average score given by a certain teacher in his subjects are:\n\t {colored(result, "light_yellow")}"

# 9. Знайти список курсів, які відвідує певний студент.
def select_9(name_student):
    session = Session()
    result = (
        session.query(Subject)
        .join(Grade, Subject.id == Grade.subject_id)
        .join(Student, Grade.student_id == Student.id)
        .filter(Student.name == name_student)
        .all()
    )
    session.close()
    subject_names = [str(subject) for subject in result]
    return f"\n9. The courses list attended by a student is:\n\t {colored(subject_names, "light_yellow")}"

# 10. Список курсів, які певному студенту читає певний викладач.
def select_10(student_name, teacher_name):
    session = Session()
    result = (
        session.query(Subject)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .join(Grade, Subject.id == Grade.subject_id)
        .join(Student, Grade.student_id == Student.id)
        .filter(Student.name == student_name)
        .filter(Teacher.name == teacher_name)
        .all()
    )
    session.close()
    subject_names = [str(subject) for subject in result]
    return f"\n10. The courses list taught to a specific student by a specific teacher are:\n\t {colored(subject_names, "light_yellow")}"

# 11. Середній бал, який певний викладач ставить певному студентові.
def select_11(teacher_name, student_name):
    session = Session()
    result = (
        session.query(func.round(func.avg(Grade.grade), 2))
        .join(Subject, Grade.subject_id == Subject.id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .join(Student, Grade.student_id == Student.id)
        .filter(Teacher.name == teacher_name)
        .filter(Student.name == student_name)
        .scalar()
    )
    session.close()
    return f"\n11. The average score given by a particular teacher to a particular student is:\n\t {colored(result, "light_yellow")}"

# 12. Оцінки студентів у певній групі з певного предмета на останньому занятті.
def select_12(group_name, subject_name):
    session = Session()
    subquery = (
        session.query(func.max(Grade.date).label("max_date"))
        .join(Student, Grade.student_id == Student.id)
        .join(Group, Student.group_id == Group.id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Group.name == group_name)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .subquery()
    )

    result = (
        session.query(Grade)
        .join(subquery, Grade.date == subquery.c.max_date)
        .join(Student, Grade.student_id == Student.id)
        .join(Group, Student.group_id == Group.id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Group.name == group_name)
        .filter(Subject.name == subject_name)
        .all()
    )
    results = [str(Grade) for Grade in result]
    return f"\n12. The students grades in a certain group in a certain subject in the last lesson are:\n\t {colored(results, "light_yellow")}"

if __name__ == "__main__":
    result1 = select_1()
    result2 = select_2("German")
    result3 = select_3("English")
    result4 = select_4()
    result5 = select_5('Julia Patterson')
    result6 = select_6("A")
    result7 = select_7("A","Ukrainian")
    result8 = select_8("Jerome Mcdonald")
    result9 = select_9('Mr. Jonathan Reese')
    result10 = select_10('Rachel Kim','Julia Patterson')
    result11 = select_11('Sarah Dunn','Corey Meyer')
    result12 = select_12("B","Italian")
    # print(result1)
    print(result2)
    print(result3)
    print(result4)
    print(result5)
    print(result6)
    print(result7)
    print(result8)
    print(result9)
    print(result10)
    print(result11)
    print(result12)


