import csv

class Student:
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

  def __str__(self):
      # String Representation of the courses
      return f"{self.__name} (Code:{self.__code}, Enrolled: {len(self.__enrolled_students)}/{self.__max_capacity})"


def main() :
    '''Main Function displat the students and classes'''

    # Storing the Students and Courses
    students = []
    courses= []


    # Loading Students from the csv file
    with open("students.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for rows in reader:
            student = Student(
                id=rows["student_id"],
                name=rows["name"],
                type=rows["student_type"],
                enrolled_courses=[]
            )
            students.append(student)

    #sorting first postgraduate and undergraduate
    postgraduates = [s for s in students if s.type.lower() == "postgraduate"]
    undergraduates = [s for s in students if s.type.lower() == "undergraduate"]

    #sorting undergraduate students name in ascending order
    undergraduates.sort(key=lambda s: s.name.lower())

    sorted_students = postgraduates + undergraduates


    # Loading Courses from the csv file
    with open("courses.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for rows in reader:
            course = Course(
                name=rows["course_name"],   
                code=rows["course_code"],
                max_capacity=int(rows["max_capacity"]),
                enrolled_students=[]
            )
            courses.append(course)
        
    # Displaying Output
    print(f"Initalized {len(students)} students including {len(courses)} courses.")

    print("\nStudents:")
    for student in sorted_students:
      print(student)
    
    print("\nCourses:")
    for course in courses:
      print(course)


if __name__=="__main__":
   main()
