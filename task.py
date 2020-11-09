# Class diary
#
# Create program for handling lesson scores.
# Use python to handle student (highscool) class scores, and attendance.
# Make it possible to:
# - Get students total average score (average across classes)
# - get students average score in class
# - hold students name and surname
# - Count total attendance of student
#
# Please, use your imagination and create more functionalities.
# Your project should be able to handle entire school(s?).
# If you have enough courage and time, try storing (reading/writing)
# data in text files (YAML, JSON).
# If you have even more courage, try implementing user interface (might be text-like).
#
#Try to expand your implementation as best as you can. 
#Think of as many features as you can, and try implementing them.
#Make intelligent use of pythons syntactic sugar (overloading, iterators, generators, etc)
#Most of all: CREATE GOOD, RELIABLE, READABLE CODE.
#The goal of this task is for you to SHOW YOUR BEST python programming skills.
#Impress everyone with your skills, show off with your code.
#
#Your program must be runnable with command "python task.py".
#Show some usecases of your library in the code (print some things)
#
#When you are done upload this code to your github repository. 
#
#Delete these comments before commit!
#Good luck.


class ClassDiary:
  def __init__(self, students):
    self.students = students
  
    def student_average(self, student):
      return sum(self.students[student])/len(self.students[student])
    
    def class_average(self):
      sum_of_grades = 0
      for student in self.students:
        sum_of_grades += sum(student[student_full_name])
      return sum_of_grades/5


list_of_students = [{"Jan Kowalski": [3,4,4,5,30]}, {"Piotr Nowak": [3,2,5,3,4]}]

class_diary = ClassDiary(list_of_students) 

print(class_diary.student_average("Jan Kowalski"))
