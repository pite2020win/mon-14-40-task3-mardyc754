import statistics
from dataclasses import dataclass
from typing import List


def extract_grades(grades_dict):
    return list(grades_dict.values())


@dataclass
class Student:
    name: str
    surname: str
    class_name: str
    school: str
    grades: dict
    attendance: dict

    def average_grade(self):
        return statistics.fmean(list(self.grades.values()))

    def get_total_attendance(self):
        total_attendance = sum(list(self.attendance.values()))
        return total_attendance

    def attendance_percentage(self):
        total_attendance = self.get_total_attendance()
        return total_attendance * 100 / len(self.attendance)


@dataclass
class ClassDiary:
    class_name: str
    students: List[Student]

    def class_grades(self):
        students_grades = {}
        for student in self.students:
            students_grades[f"{student.name} {student.surname}"] = \
                        student.grades
        return students_grades

    def class_average(self):
        list_of_grades = []
        for student in self.students:
            list_of_grades.extend(extract_grades(student.grades))
        return statistics.fmean(list_of_grades)

    def display_averages_of_all_students(self):
        return_info = self.class_name
        for i, student in enumerate(self.students):
            return_info += f"{i+1}. {student.surname}, {student.name}: " \
                           f"{student.average_grade()}"

    def subject_grades(self, subject_name):
        grades_dict = {}
        for student in self.students:
            grades_dict[f"{student.name} {student.surname}"] = \
                student.grades[subject_name]
        return grades_dict

    def subject_average(self, subject_name):
        subject_grades = self.subject_grades(subject_name)
        return statistics.fmean(subject_grades.values())

    def class_attendance_percentage(self):
        attendace_percentages = []
        for student in self.students:
            attendace_percentages.append(student.attendance_percentage())
        return statistics.fmean(attendace_percentages)

    def get_to_the_student(self, name, surname):
        for student in self.students:
            if (student.name, student.surname) == (name, surname):
                return student

    def get_student_average(self, name, surname):
        student = self.get_to_the_student(name, surname)
        if student:
            return student.average_grade()


@dataclass
class School:
    school_name: str
    class_diaries: List[ClassDiary]

    def school_average(self):
        extracted_school_grades = []
        for class_diary in self.class_diaries:
            for student in class_diary.students:
                extracted_school_grades.extend(extract_grades(student.grades))
        return statistics.fmean(extracted_school_grades)

    def school_subject_average(self, subject_name):
        subject_grades = []
        for class_diary in self.class_diaries:
            class_subject_grades = class_diary.subject_grades(subject_name)
            class_subject_grades = extract_grades(class_subject_grades)
            subject_grades.extend(class_subject_grades)
        return statistics.fmean(subject_grades)

    def get_all_grades(self):
        all_grades = {}
        for class_diary in self.class_diaries:
            all_grades.update(class_diary.class_grades())
        return all_grades

    def school_attendance_percentage(self):
        attendance_percentages = []
        for class_diary in self.class_diaries:
            attendance_percentages.append(class_diary.class_attendance_percentage())
        return statistics.fmean(attendance_percentages)

    def get_to_the_student(self, name, surname):
        for class_diary in self.class_diaries:
            found_student = class_diary.get_to_the_student(name, surname)
            if found_student:
                return found_student
