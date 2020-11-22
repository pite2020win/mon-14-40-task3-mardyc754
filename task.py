import json
import school_data
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='')


def student_decoder(student_dict):
    return school_data.Student(student_dict['name'], student_dict['surname'], student_dict['class_name'],
                   student_dict['school'], student_dict['grades'], student_dict['attendance'])


def class_diary_decoder(class_diary_dict):
    new_student_list = []
    for student in class_diary_dict['students']:
        new_student_list.append(student_decoder(student))
    return school_data.ClassDiary(class_diary_dict['class_name'],
                      new_student_list)


def school_decoder(school_dict):
    new_class_diary_list = []
    for class_diary in school_dict['class_diaries']:
        new_class_diary_list.append(class_diary_decoder(class_diary))
    return school_data.School(school_dict['school_name'], new_class_diary_list)


def schools_decoder(schools):
    new_school_dict = {}
    for school in schools:
        new_school_dict[school['school_name']] = school_decoder(school)
    return new_school_dict


def display_student_grades(student):
    student_grades = map(lambda subject, subject_grade: f"{subject}: {subject_grade}",
                         student.grades.keys(), student.grades.values())
    student_grades = f"{', '.join(list(student_grades))}"
    return student_grades


def student_info(student):
    return f"Name: {student.name.title()}\n" \
           f"Surname {student.surname.title()}\n" \
           f"Class: {student.class_name.title()}\n" \
           f"School: {student.school.title()}\n" \
           f"Grades: {display_student_grades(student)}\n" \
           f"Attendance: {student.attendance_percentage()}%" \
           f"{student.get_total_attendance()}/{len(student.attendance)})"


def get_students_info(class_diary):
    return_text = ""
    for i, student in enumerate(class_diary.students):
        return_text += f"{i+1}. {student.surname}, {student.name}\n"
    return return_text


def get_info_of_all_students_in_the_school(school):
    return_text = school.school_name.title()
    for class_diary in school.class_diaries:
        return_text += f" {class_diary.class_name}\n" \
                       f"{get_students_info(class_diary)}"
    return return_text


if __name__ == '__main__':
    with open('data.json') as read_file:
        schools = schools_decoder(json.load(read_file))

    print(schools)
    print(schools['xyz'].class_diaries[0].students[-1])
    class_1a = schools['xyz'].class_diaries[0]
    someone_average = class_1a.get_student_average("Jan", "Kowalski")
    class_1a.display_averages_of_all_students()
    logging.info(get_students_info(class_1a))
    someone = class_1a.get_to_the_student("Adam", "Abacki")
    logging.info(student_info(someone))
    print(someone)
    print(class_1a.class_average())
    logging.info(get_info_of_all_students_in_the_school(schools['xyz']))
    print(schools['xyz'].school_average())
    print(class_1a.subject_average("biology"))
    print(class_1a.subject_grades("biology"))
    print(schools['xyz'].school_subject_average("biology"))
    print(schools['xyz'].get_all_grades())
    print(schools['xyz'].get_to_the_student("Jan", "Kowalski"))

