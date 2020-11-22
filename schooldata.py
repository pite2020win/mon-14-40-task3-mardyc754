import statistics
from dataclasses import dataclass

from typing import List, Dict


@dataclass
class Student:
    name: str
    surname: str
    class_name: str
    school_name: str
    grades: dict
    attendance: dict

    def student_average(self):
        return statistics.fmean(list(self.grades.values()))

    def attendance_percentage(self):
        total_attendance = sum(list(self.attendance.values()))
        return total_attendance * 100 / len(self.attendance)


@dataclass
class ClassDiary:
    class_name: str
    students: List[Student]

    def class_average(self):
        list_of_grades = []
        for student in self.students:
            list_of_grades.extend(list(student.grades.values()))
        return statistics.fmean(list_of_grades)

    def subject_grades(self, subject_name):
        return list(map(lambda student: student.grades[subject_name],
                        self.students))

    def subject_average(self, subject_name):
        subject_grades = self.subject_grades(subject_name)
        return statistics.fmean(subject_grades)

    def class_attendance_percentage(self):
        attendace_percentages = list(map(Student.attendance_percentage, self.students))
        return statistics.fmean(attendace_percentages)

    def get_to_the_student(self, name, surname):
        for student in self.students:
            if (student.name, student.surname) == (name, surname):
                return student

    def get_student_average(self, name, surname):
        student = self.get_to_the_student(name, surname)
        if student:
            return student.student_average()


@dataclass
class School:
    school_name: str
    class_diaries: Dict[str, ClassDiary]

    def school_average(self):
        extracted_school_grades = []
        for class_diary in self.class_diaries.values():
            for student in class_diary.students:
                extracted_school_grades.extend(list(student.grades.values()))
        return statistics.fmean(extracted_school_grades)

    def school_subject_average(self, subject_name):
        subject_grades = []
        for class_diary in self.class_diaries.values():
            class_subject_grades = class_diary.subject_grades(subject_name)
            subject_grades.extend(class_subject_grades)
        return statistics.fmean(subject_grades)

    def school_attendance_percentage(self):
        attendance_percentages = list(map(ClassDiary.class_attendance_percentage,
                                          self.class_diaries.values()))
        return statistics.fmean(attendance_percentages)

    def get_to_the_student(self, name, surname, class_name=''):
        found_class_diary = self.class_diaries.get(class_name, "")
        if found_class_diary != '':
            found_student = found_class_diary.get_to_the_student(name, surname)
            if found_student:
                return found_student
        else:
            for class_diary in self.class_diaries.values():
                found_student = class_diary.get_to_the_student(name, surname)
                if found_student:
                    return found_student
