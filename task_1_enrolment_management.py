import csv
from tabulate import tabulate
class Student:
  MAX_COURSES = 4
  """Student Class with name, ID and Type(UG/G)"""
  def __init__(self,
               name : str,
               id : str,
               type: str,
               enrolled_courses: list):
    
    self.__name = name
    self.__id = id
    self.__type = type
    self.__enrolled_courses = enrolled_courses if enrolled_courses else []
  
  @property
  def name(self):
      # Returns the student's name
      return self.__name

  @property
  def id(self):
      # Returns the student's ID
      return self.__id

  @property
  def type(self):
      # Returns the student's Type
      return self.__type
  
  @property
  def enrolled_courses(self):
     # Returns enrolled_courses
     return self.__enrolled_courses
  
  def can_enroll(self,course):
      # Returns boolean value after checking the eligibility of course enrollement
      if course in self.__enrolled_courses:
          return False
      if len(self.__enrolled_courses) >= Student.MAX_COURSES:
         return False
      return True
     
  
  def __str__(self):
      # Srtring representation of the student
      return f"{self.__name} (ID : {self.__id}, Type: {self.__type})"
        


class Course:
  """Course Class with name, code, enrolled students and maximum capacity."""

  def __init__(self,
               name : str,
               code : str,
               max_capacity:int,
               enrolled_students:list ):
    self.__name = name
    self.__code = code
    self.__max_capacity = max_capacity
    self.__enrolled_students = enrolled_students

  @property
  def name(self):
      # Returns the course's name
      return self.__name
  
  @property
  def code(self):
      # Returns the course's code
      return self.__code

  @property
  def max_capacity(self):
      # Returns the course's maximum capacity of enrollement
      return self.__max_capacity
  
  @property
  def enrolled_students(self):
      # Returns the list of enrolled students
      return self.__enrolled_students

  def add_students(self,student:Student):
     # Validating if the max capacity for a course is reached
     if len(self.__enrolled_students) < self.__max_capacity:
        self.__enrolled_students.append(student)
        print(f'Success! Student "{student.name}" enrolled in course "{self.__name}"')
     else:
        print(f'Failure! Student "{student.name}" NOT enrolled in course "{self.__name}"')

  def __str__(self):
      # String Representation of the courses
      return f"{self.__name} (Code:{self.__code}, Enrolled: {len(self.__enrolled_students)}/{self.__max_capacity})"


def main() :
    '''Main Function displat the students and classes'''

    # Storing the Students and Courses
    students = []
    courses= []
    
    menu_is_running = True

    # Loading Students from the csv file
    with open("students.csv", newline="") as csvfile:
        students_from_csv = csv.DictReader(csvfile)
        for rows in students_from_csv:
            student = Student(
                id=rows["student_id"],
                name=rows["name"],
                type=rows["student_type"],
                enrolled_courses=[]
            )
            students.append(student)
   

    # Loading Courses from the csv file
    with open("courses.csv", newline="") as csvfile:
        courses_from_csv = csv.DictReader(csvfile)
        for rows in courses_from_csv:
            course = Course(
                name=rows["course_name"],   
                code=rows["course_code"],
                max_capacity=int(rows["max_capacity"]),
                enrolled_students=[]
            )
            courses.append(course)
        
    # Displaying Output
    print(f"Initalized {len(students)} students including {len(courses)} courses.\n")


    while menu_is_running:
      # Displaying Menu
      print("="*40)
      print("Enter your choice:")
      print("1. Enrol Student")
      print("2. List Enrolled Students")
      print("3. List All Courses and Enrolled Students")
      print("0. Quit")
      print("="*40)

      # User Input for the menu option
      user_choice  = input()
      
      # Validating if its a number
      if not user_choice.isdigit():
          print("Please enter a valid number!")
          continue
      else:
         user_choice = int(user_choice)
      
      # User Option 1
      if user_choice == 1:
        
        # Variables to store courses and students
        found_course : Course = None
        found_student : Student = None

        while not found_course:
          # User Input
          course_choice = input("Enter the name of the course: ")

          # Validating if its a string
          if course_choice.isdigit():
            print("Please enter a valid string.")
            continue

          else:
            # Keeping the Choice as String
            course_choice = str(course_choice)
          

          # Searching if the user entered course choice is in the list
          for course in courses:
              if course.name.lower() == course_choice.lower():
                found_course = course
                break

          # Validating if the course is found or not
          if not found_course:
              print(f'Course "{course_choice}" not found. Try again')
              continue
        

        while not found_student:
          # User Input
          student_choice = input("Enter the name of the student: ")

            # Validating if its a string
          if student_choice.isdigit():
            print("Please enter a valid string.")
            continue
          else:
            student_choice = str(student_choice)

          # Searching if the user entered student choice is in the list
          for student in students:
              if student.name.lower() == student_choice.lower():
                found_student = student
                break
          # Validating if the student is found or not
          if not found_student:
            print(f'Student "{student_choice}" not found. Try Again')
            continue
          
          # Checking if the student is already enrolled in the course
          if not found_student.can_enroll(found_course):
            print(f"Failure! {found_student.name} NOT enrolled in course {found_course.name}")
            continue
          
          # Adding Students to the course
          found_course.add_students(found_student)

          # Updating the studnet's enrolled courses list
          found_student.enrolled_courses.append(found_course)

      # User Option 2
      elif user_choice == 2:
          found_course = None

          while not found_course:
              # User Input
              course_input = input("Enter the name of the course: ").strip()

              # Validating if the input is digit
              if course_input.isdigit():
                print("Please enter a valid string.")
                continue
              else:
                course_input = str(course_input)
              
              # Searching for course in the list
              for course in courses:
                if course.name.lower() == course_input.lower():
                   found_course = course
                   break
              # Validation for the course if not found
              if not found_course:
                 print(f"{course_input} not found. Try Again!")
                 continue
              
              # Displaying Output
              print(found_course)
              if len(found_course.enrolled_students) == 0:
                print("    ","No Enrolled Students")
              else:
                for student in found_course.enrolled_students:
                  print("   ",student,)
      

      # User Input Choice 3
      elif user_choice == 3:
          
          all_course = [] # Creating a new list for tabulate

          # Extracting each course from the list
          for course in courses:
            students_names = ", ".join([student.name for student in course.enrolled_students]) or "None"
            all_course.append({
               "Course Name":course.name,
               "Course Code":course.code,
               "Max Capacity":course.max_capacity,
               "Enrolled Students":len(course.enrolled_students),
               "Students Name":students_names
            })

          # Reference for tabulate : https://www.geeksforgeeks.org/python/introduction-to-python-tabulate-library/
          print(tabulate(all_course,headers="keys",tablefmt="grid"))

      elif user_choice == 0:
          # Exiting the Program
          menu_is_running = False
      else :
          print("Please enter number between 0-3.")
          continue
          


if __name__=="__main__":
   main()
