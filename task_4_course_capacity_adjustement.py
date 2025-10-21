'''
*******************************
Author: Group 43 (Tuesday 1:30 - 3:30)
Assessment 3 - 10/16/2025
File Name: task_4_course_capacity_adjustment.py
*******************************
'''   

import random
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
     
  def drop_course(self,course): 
    # Drops the Course from the listn of enrolled course
    if course in self.__enrolled_courses:
        self.__enrolled_courses.remove(course) 

        
  def __str__(self):
      # Srtring representation of the student
      return f"{self.__name} (ID : {self.__id}, Type: {self.__type})"
        

class Course:
  """Course Class with name, code, enrolled students and maximum capacity."""

  def __init__(self,
               name : str,
               code : str,
               max_capacity:int,
               enrolled_students:list,
               displaced_students:list ):
    self.__name = name
    self.__code = code
    self.__max_capacity = max_capacity
    self.__enrolled_students = enrolled_students
    self.__displaced_students = displaced_students

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

  def remove_student(self,student): 
     # Removing Student from the course after they drop the course
      if student in self.__enrolled_students: 
          self.__enrolled_students.remove(student) 
          print(f'Sucess! Student "{student.name}" dropped from the course "{self.__name}"') 
      else: 
          print(f'Failure! Student "{student.name}" NOT enrolled in course "{self.__name}" ')
  
  def adjust_capcity(self,new_capcity:int):
    # Adjusting the course capcity
    self.__max_capacity = new_capcity

    # Validating if the new capcity is lower than 
    if new_capcity < len(self.__enrolled_students):

      print(f"Warning! New Capactiy ({new_capcity}) is less than current enrollement ({len(self.__enrolled_students)}).")
      print(f"{len(self.__enrolled_students)-new_capcity} needs to be reassigned")

      total_removal = len(self.__enrolled_students) - new_capcity

      # Taking Random List of elements | Ref for Sample Method : https://www.geeksforgeeks.org/python/python-random-sample-function
      random_students : list[Student] = random.sample(self.__enrolled_students,int(total_removal))

      #Displaced students can also be re-enrolled
      for student in random_students:
        self.__enrolled_students.remove(student)
        student.drop_course(self)

      # Adding each students individually as a list
      self.__displaced_students.extend(random_students)
    
    else:
       print(f"Sucess! New Capactiy of {new_capcity} is set for {self.__name}")
    

  def get_displaced_students(self) :
     # Returns List of Students
     return self.__displaced_students
     

  def clear_displaced_students(self):
    # Clears the Students from the displaced lists
     return self.__displaced_students.clear()

  def __str__(self):
      # String Representation of the courses
      return f"{self.__name} (Code:{self.__code}, Enrolled: {len(self.__enrolled_students)}/{self.__max_capacity})"

class Advisor:
    """Advisor Class with name and assigned students"""

    def __init__(self,
                 name : str,
                 assigned_students:list,
                 pending_request:list):
      self.__name = name
      self.__assigned_students = assigned_students
      self.__pending_request = pending_request
    
    @property
    def name(self):
       # Returns the advisor's name:
       return self.__name
    
    @property
    def assigned_students(self):
      # Returns list of assigned_students
      return self.__assigned_students
    
    @property
    def pending_request(self):
       # Returns list of pending requests
       return self.__pending_request
    
    def add_requests(self,student,course):
       # Adds request as tuple 
       self.__pending_request.append((student,course))

    def approve_students(self,student : Student, course: Course,index:int):
      # Accepting Requests

      #Validating if there are requests
      if 0<= index <= len(self.__pending_request):

        # Getting Student and Course from the tuple
        pen_student,pen_course = self.__pending_request[index]

        # Validating
        if pen_student == student and pen_course == course:
          
          # Removing the request from the index
          self.__pending_request.pop(index)
          
          # Enrolling the course for the student after approval
          student.enrolled_courses.append(course)
          # Updating the student in the course class
          course.add_students(student)
          
          return True
      return False


    def deny_request(self,student,course,index:int):
      # Denies Request

      #Validating if there are requests
      if 0<= index <= len(self.__pending_request):
        
        # Getting Student and Course from the tuple
        pen_student,pen_course = self.__pending_request[index]

        # Validating
        if pen_student == student and pen_course == course:

           # Removing the request from the index
          self.__pending_request.pop(index)

          return True
      return False

        
def main() :
    '''Main Function displat the students and classes'''

    # Storing the Students and Courses
    students = []
    courses= []
    advisors= []
    
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
        course_from_csv = csv.DictReader(csvfile)
        for rows in course_from_csv:
            course = Course(
                name=rows["course_name"],   
                code=rows["course_code"],
                max_capacity=int(rows["max_capacity"]),
                enrolled_students=[],
                displaced_students=[]
            )
            courses.append(course)
    
    # Loading Advisors from the csv file
    with open("advisors.csv",newline="") as csvfile:
       advisors_from_csv = csv.reader(csvfile)
       for rows in advisors_from_csv:
          name = rows[0]
          student_ids = rows[1:]
          advisor = Advisor(
             name=name,
             assigned_students=student_ids,
             pending_request=[]
          )
          advisors.append(advisor)

    # Displaying Output
    print(f"Initalized {len(students)} students including {len(courses)} courses.\n")


    while menu_is_running:
      # Displaying Menu
      print("="*40)
      print("Enter your choice:")
      print("1. Enrol Student")
      print("2. Drop a Course")
      print("3. Re-enrol a Course")
      print("4. List Enrolled Students")
      print("5. List All Courses and Enrolled Students")
      print("6. Advisor Login")
      print("7. Adjust Course Capacity")
      print("0. Quit")
      print("="*40)

      # User Input for the menu option
      user_choice  = input().strip()
      
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
        found_advisor: Advisor = None

        while not found_course:
          # User Input
          course_choice = input("Enter the name of the course: ").strip()

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
              print(f'"{course_choice}" not found. Try again')
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
            print(f'"{student_choice}" not found. Try Again')
            continue
          
          # Checking if the student is already enrolled in the course
          if not found_student.can_enroll(found_course):
            print(f"Student {found_student.name} is already enrolled in {found_course.name}")
            print(f"Failure! {found_student.name} NOT enrolled in course {found_course.name}")
            continue
                  
          if found_student.type == "Postgraduate":
              # Searching if the user entered course choice is in the list
              for advisor in advisors:
                  if found_student.id in advisor.assigned_students:
                    found_advisor = advisor
                    break
              # Validating if the course is found or not
              if not found_advisor:
                  print(f'Advisor for Student"{found_student.name}" not found. Try again')
                  continue
              
              found_advisor.add_requests(student=found_student,course=found_course)
              print(f"Request sent to advisor {found_advisor.name} for approval.")
          else:   
              # Adding Students to the course
              found_course.add_students(found_student)

              # Updating the studnet's enrolled courses list
              found_student.enrolled_courses.append(found_course)

      # User Option 2
      elif user_choice == 2:
        # Variables to store courses and students
        found_course = None
        found_student = None
        
        while not found_course:

          #User Input
          course_input = input("Enter the name of the course: ").strip()

          # Validating if its a string or not
          if course_input.isdigit():
              print("Please enter a valid string")
              continue
          else:
              course_input = str(course_input)

          # Searching the course from the list of courses
          for course in courses:
             if course.name.lower() == course_input.lower():
                found_course = course
                break
          
          # Validating if the course is not found
          if not found_course:
             print(f'Course "{course_input}" not found. Try Again!')
             continue
          
        while not found_student:

          # User Input
          student_input = input("Enter the name of the student: ").strip()
          
          # Validating if its a input
          if student_input.isdigit():
              print("Please enter a valid string")
              continue
          else:
              student_input = str(student_input)

          # Searching Student from the list of students
          for student in students:
             if student.name.lower() == student_input.lower():
                found_student = student
                break
             
          # Validating if student not found
          if not found_student:
            print(f'Student "{student_input}" not found! Try Again')
            continue
        
        # Removing the course from the student class
        found_student.drop_course(found_course)

        # Updating the changes on the course class
        found_course.remove_student(found_student)

      # User Option 3
      elif user_choice == 3:
        
        # Variables to store courses and students
        found_course : Course = None
        found_student : Student = None

        while not found_course:
          # User Input
          course_choice = input("Enter the name of the  you want to re-enrol: ")

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

      # User Option 4
      elif user_choice == 4:
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
                 print(f"Course {course_input} not found. Try Again!")
                 continue
              
              # Displaying Output
              print(found_course)
              if len(found_course.enrolled_students) == 0:
                print("    ","No Enrolled Students")
              else:
                for student in found_course.enrolled_students:
                  print("   ",student,)

      # User Input Choice 5
      elif user_choice == 5:
          
          all_course = [] # Creating a new list for tabulate

          # Extracting each course from the list
          for course in courses:
            students_names = ", ".join([student.name for student in course.enrolled_students]) or "None"
            all_course.append({
               "Course Code":course.code,
                "Course Name":course.name,
               "Max Capacity":course.max_capacity,
               "Enrolled Students":len(course.enrolled_students),
               "Students Name":students_names
            })

          # Reference for tabulate : https://www.geeksforgeeks.org/python/introduction-to-python-tabulate-library/
          print(tabulate(all_course,headers="keys",tablefmt="grid"))

      # User Input  Choice 6
      elif user_choice == 6:
          
          # Varaible for Storing Advisor
          found_advisor : Advisor = None
          
          while not found_advisor:
              # User Input 
              advisor_input = input("Enter your name: ").strip()

              # Searching Advisor from the list
              for advisor in advisors:
                if advisor_input.lower() == advisor.name.lower():
                      found_advisor = advisor
                      break
                
              # Validating if the Advisor not found
              if not found_advisor:
                print(f"No advisor found with the name {advisor_input}.")
                continue

              print(f"Welcome, {found_advisor.name}. Here are your pending requests:")

              # Validating if Advisor has penidng requests
              if len(found_advisor.pending_request)>0:

                # Showing all pending request
                for index,(student,course) in enumerate(found_advisor.pending_request):
                    print(f"{index+1}. Student {student.name} requests to enroll in {course.name}.")

                while True:

                      
                      # User Input
                      answer = input("Would you like to approve or deny the request? (a=approve, d=deny, q=quit): ")
                      
                      # Validating input
                      if answer not in ["a","d","q"]:
                        print("Invalid input. Please enter 'a' to approve, 'd' to deny, or 'q' to quit.\n")
                        continue
                      
                      # For Approval
                      if answer.lower() == "a":
                          
                          # User Confirmation
                          confirm_input = input("Enter the number of the request to approve: ").strip()

                          # Validating Confirmation
                          if confirm_input.isdigit():

                            # Typecasting to int
                            confirm_input = int(confirm_input)

                            # Validating if its approved
                            if found_advisor.approve_students(student=student,course=course,index=int(confirm_input-1)):
                                print(f"Request approved. {student.name} is now enrolled in {course.name}.")
                                break
                            
                          else:
                            print("Invalid input. Please enter integers")
                            continue
                      
                      # For Disapproval
                      elif answer.lower() == "d":

                        # User Confirmation
                        confirm_input = input("Enter the number of the request to deny: ").strip()

                        # Validating Confirmation
                        if confirm_input.isdigit():
                          # TypeCasting
                          confirm_input = int(confirm_input)

                          # Validating if its denied
                          if found_advisor.deny_request(student=student,course=course,index=int(confirm_input-1)):
                            print(f"Request denied for {student.name}.")
                            break

                        else:
                          print("Invalid input. Please enter integers")
                          continue
                      
                      # For exiting the advisor menu
                      elif answer.lower() == "q":
                          print("Exiting advisor menu.")
                          break
              else:
                    print("    No Pending Requests")

      elif user_choice == 7:
         found_course : Course = None 

         # User Input and Validation for Course
         while not found_course:
            course_input = input("Enter the name of the course: ").strip()

            if course_input.isdigit():
               print("Invalid Input. Please enter a string")
               continue
            else:  
              for course in courses:
                if course.name.lower() == course_input.lower():
                  found_course = course
                  break
              if not found_course:
                print(f"Course {course_input} not found! Try Again.")
                continue
            
            print(f"Current capcity of {found_course.name}: {found_course.max_capacity}")

            #User Input for New Capacity
            new_capcity_input :int = input(f"Enter the new capcity for {found_course.name}: ")

            if not new_capcity_input.isdigit():
               print("Invalid Input. Please enter a number")

            # Calling the Adjust Method
            found_course.adjust_capcity(int(new_capcity_input))  

            # Getting the list of displaced students
            displaced_students: list[Student] = found_course.get_displaced_students()

            # Only run reassignment if students were actually displaced (capacity DECREASED)
            if len(displaced_students) > 0:
                successes = []   # list of tuples (student, new_course)
                failures = []    # list of students not reassigned

                for student in displaced_students:
                    reassignment = False
                    for course in courses:
                        # Skip same course and check available capacity
                        if course is not found_course and len(course.enrolled_students) < course.max_capacity:
                            # Avoid double-enrolling the student in the same course
                            if student in course.enrolled_students:
                                continue

                            # Enroll student in the new course
                            course.add_students(student)

                            # Record enrollment on student's side only if not already present
                            if course not in student.enrolled_courses:
                                student.enrolled_courses.append(course)

                            successes.append((student, course))
                            reassignment = True
                            break

                    if not reassignment:
                        failures.append(student)

                # Print all successful reassignments first
                for student, course in successes:
                    print(f"Student {student.name} reassigned from {found_course.name} to {course.name}")

                # Then print one warning per student who could not be reassigned
                for student in failures:
                    print(f"Warning: No Available spots for student {student.name}. They will remain unassigned for now.")

                # Once done, clear the displaced list
                found_course.clear_displaced_students()

            else:
                # When capacity increases, no reassignment needed
                print(f"No students were displaced during capacity adjustment for {found_course.name}.")


      elif user_choice == 0:
          # Exiting the Program
          menu_is_running = False
      else :
          print("Please enter number between 0-7.")
          continue
          


if __name__=="__main__":
   main()
