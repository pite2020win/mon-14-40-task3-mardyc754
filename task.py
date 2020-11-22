import json
import schooldata
import logging
import sys
from pathlib import Path


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='')


def student_decoder(student_dict):
    return schooldata.Student(student_dict['name'], student_dict['surname'],
                              student_dict['class_name'], student_dict['school_name'],
                              student_dict['grades'], student_dict['attendance'])


def class_diary_decoder(class_diary_dict):
    new_student_list = []
    for student in class_diary_dict['students']:
        new_student_list.append(student_decoder(student))
    return schooldata.ClassDiary(class_diary_dict['class_name'],
                                 new_student_list)


def school_decoder(school_dict):
    new_class_diary_dict = {}
    for class_diary in school_dict['class_diaries']:
        new_class_diary_dict[class_diary['class_name']] = class_diary_decoder(class_diary)
    return schooldata.School(school_dict['school_name'], new_class_diary_dict)


def schools_decoder(school_dict):
    new_school_dict = {}
    for school in school_dict:
        new_school_dict[school['school_name']] = school_decoder(school)
    return new_school_dict


def get_students_info(class_diary):
    return_text = ""
    for i, student in enumerate(class_diary.students):
        return_text += f"{i + 1}. {student.surname}, {student.name}\n"
    return return_text


def get_names_of_all_students_in_the_school(school):
    return_text = f"{school.school_name.title()}\n"
    for class_diary in school.class_diaries.values():
        return_text += f"{class_diary.class_name}\n" \
                       f"{get_students_info(class_diary)}"
    return return_text


def get_student_class_name(name, surname, schools_database):
    for school in schools_database.values():
        found_student = school.get_to_the_student(name, surname)
        if found_student:
            return found_student.class_name


def get_student_school_name(name, surname, schools_database):
    for school in schools_database.values():
        found_student = school.get_to_the_student(name, surname)
        if found_student:
            return found_student.school_name.title()


def display_student_grades(student):
    student_grades = map(lambda subject, subject_grade:  f"{subject}: {subject_grade}",
                         student.grades.keys(), student.grades.values())
    student_grades = f"{', '.join(list(student_grades))}"
    return student_grades


def student_info(student):
    student_attendance = round(student.attendance_percentage() *
                               len(student.attendance) / 100)

    return f"Name: {student.name.title()}\n" \
           f"Surname {student.surname.title()}\n" \
           f"Class: {student.class_name.title()}\n" \
           f"School: {student.school_name.title()}\n" \
           f"Grades: {display_student_grades(student)}\n" \
           f"Attendance: {student.attendance_percentage()}% " \
           f"({student_attendance}/{len(student.attendance)})\n"


def display_students_averages(class_diary):
    return_text = class_diary.class_name
    for i, student in enumerate(class_diary.students):
        return_text += f"{i + 1}. {student.surname}, {student.name}: " \
                       f"{student.student_average()}"
    return return_text


def get_all_grades_in_the_class(class_diary):
    return_text = f"{class_diary.class_name}\n"
    for i, student in enumerate(class_diary.students):
        return_text += f"{i+1}. {student.name} {student.surname}: " \
                       f"{display_student_grades(student)}\n"
    return return_text


def get_all_grades_in_the_school(school):
    return_text = f"{school.school_name.title()}\n"
    for class_diary in school.class_diaries.values():
        return_text += get_all_grades_in_the_class(class_diary)
    return return_text


if __name__ == '__main__':
    with open(str(Path.cwd() / 'data.json')) as read_file:
        schools = schools_decoder(json.load(read_file))

    logging.info("Getting students names from all schools:")
    for school in schools.values():
        logging.info(get_names_of_all_students_in_the_school(school))

    class_1a_xyz = schools['xyz'].class_diaries['1A']
    class_1a_abc = schools['abc'].class_diaries['1A']

    logging.info(f"Ksawery Iksinsky attends to class: "
                 f"{get_student_class_name('Ksawery', 'Iksinsky', schools)}")
    logging.info(f"Ksawery Iksinsky attends to school: "
                 f"{get_student_school_name('Ksawery', 'Iksinsky', schools)}\n")

    logging.info("Displaying information about Feliks Kot from 2B, Xyz:")
    boy = schools['xyz'].get_to_the_student("Feliks", "Kot", "2B")
    logging.info(student_info(boy))

    logging.info("Displaying information about Sabacka Sabina from 1A, Abc:")
    girl = class_1a_abc.get_to_the_student("Sabina", "Sabacka")
    logging.info(student_info(girl))

    logging.info(f"Average of Feliks Kot: {boy.student_average():.2f}")
    logging.info(f"Average of Sabina Sabacka: "
                 f"{class_1a_abc.get_student_average('Sabina', 'Sabacka'):.2f}\n")

    logging.info(f"Displaying all grades in school Xyz:\n"
                 f"{get_all_grades_in_the_school(schools['xyz'])}")
    for class_diary in schools['xyz'].class_diaries.values():
        logging.info(f"Average of class {class_diary.class_name}: "
                     f"{class_diary.class_average():.2f}")

    for school in schools.values():
        logging.info(f"Average of school {school.school_name.title()}: "
                     f"{school.school_average():.2f}")

    logging.info(f"Average from Maths in class 1A, Xyz: "
                 f"{class_1a_xyz.subject_average('maths')}")
    logging.info(f"Average from Maths in school Xyz: "
                 f"{schools['xyz'].school_subject_average('maths')}")

    logging.info(f"Average from Physics in class 1A from school Abc: "
                 f"{class_1a_abc.subject_average('physics')}\n")

    for class_diary in schools['xyz'].class_diaries.values():
        logging.info(f"Class {class_diary.class_name}, Xyz attendance: "
                     f"{class_diary.class_attendance_percentage():.2f}")

    for school in schools.values():
        logging.info(f"School {school.school_name.title()} attendance: "
                     f"{school.school_attendance_percentage():.2f}")
