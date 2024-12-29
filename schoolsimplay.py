import random, time, pickle, os

class School:
    def __init__(self, name):
        self.name = name
        self.students = []
        print("School", name)

    def add_student(self, student):
        self.students.append(student)

class Student:
    def __init__(self, name, grade, school, password):
        self.name = name
        self.grade = grade
        self.school = school
        self.school.students.append(self)
        self.classes = []
        self.gradebook1 = []
        self.gradebook2 = []
        self.gradebook3 = []
        self.gradebook4 = []
        self.totalgradebook = []
        self.password = password

    def add_class(self, class_obj):
        self.classes.append(class_obj)

    def ask(self, curriculum_questions, class_obj):
        qs = 0
        questions = list(curriculum_questions)
        random.shuffle(questions)
        for question in questions:
            if qs > 3:
                print("That's enough questions.")
                break
            print("Question:", question, "Your Answer: ", end="")
            given_answer = input()
            score = class_obj.evaluate_response(question, given_answer)
            qs += 1
            exec(f"self.gradebook{quarter}.append(score)")
            self.totalgradebook.append(score)
        print(f"\nYou are done learning curriculum for {class_obj.name} class.")

    def learn(self, class_obj):
        if class_obj not in self.classes:
            print("You cannot learn this class")
        else:
            print("Learning", class_obj.name, "\n")
            if len(class_obj.curriculum) > 0:
                self.ask(class_obj.curriculum.keys(), class_obj)

    def sleep(self):
        print("You are sleeping\n")

    def add_curriculum(self):
        for class_name in self.classes:
            yesno = input(f"(True/False) Would you like to add curriculum for {class_name.name}? ")
            if yesno:
                print("""First, it will ask you to enter a question. Then input the answer.
If you would like to finish, for the question enter 'done'.\n""")
                while True:
                    question = input("Enter a question or 'done': ")
                    if question == 'done':
                        break
                    else:
                        answer = input("Enter an answer for that question: ")
                        class_name.add_curriculum(question, answer)
                print(f"Added curriculum for class {class_name.name}")
            else:
                print(f"Skipped adding curriculum for {class_name.name}")
        print("\nDone adding curriculum for classes\n")

class Class:
    def __init__(self, name):
        self.name = name
        self.curriculum = {}

    def add_curriculum(self, question, answer):
        self.curriculum[question] = answer

    def evaluate_response(self, question, given_answer):
        if self.curriculum[question] == given_answer:
            print("The given answer was correct")
            return 100
        else:
            print(f"The given answer was wrong. Correct answer: {self.curriculum[question]}")
            return 0

# STARTING SIMULATION

def load_simulation(filename):
    global school, student, progress
    school_path = os.path.join(filename, "school.schoolsim")
    student_path = os.path.join(filename, "student.schoolsim")
    password_path = os.path.join(filename, "password.schoolsim")
    progress_path = os.path.join(filename, "progress.schoolsim")
    with open(school_path, 'rb') as load_from:
        school = pickle.load(load_from)
    with open(student_path, 'rb') as load_from:
        student = pickle.load(load_from)
    with open(password_path, 'rb') as load_from:
        password = pickle.load(load_from)
    with open(progress_path, 'rb') as load_from:
        progress = pickle.load(load_from)
    print(f"\nYour game was loaded successfully! Just to confirm, you need to enter your password.")
    password_given = input("Enter your password: ")
    if password_given == password:
        print("Identity authenticated! Loading game")
    else:
        print("Access denied")
        print("game ending")
        time.sleep(3)
        quit()

pickle_choice = input("(True/False) Would you like to import a saved game? ")
if pickle_choice.lower() == "true":
    filename = ""
    while not os.path.exists(filename):
        filename = "game_"+input("Please enter a valid folder name (without the game_) or 'quit' to exit: ")
        if filename == 'quit':
            pickle_choice = "False"
    if filename != 'quit':
        load_simulation(filename)

if pickle_choice.lower() != 'true':
    progress = [1, 1]
    school = School(input("Please enter the name of the school you are joining: "))
    student = Student(input("Please enter your name: "), input("Please enter your grade: "), school, password=input("Choose a password: "))
    school.add_student(student)
    classes_joined = []
    print("Enter a class name to join a class, or type 'done' to finish.")
    number_of_classes_joined = 0
    while True:
        class_to_join = input("Enter a class name: ").lower()
        if class_to_join != "done":
            print("You are joining", class_to_join)
            classes_joined.append(Class(class_to_join))
            number_of_classes_joined += 1
        else:
            classes_joined_names = []
            for class_joined in classes_joined:
                classes_joined_names.append(class_joined.name)
            print("You have joined", number_of_classes_joined, "classes.")
            print("You have joined these classes:", classes_joined_names)
            break

    for class_name in classes_joined:
        student.add_class(class_name)

    print(f"""
You have joined {school.name}.
Your classes begin tomorrow""")
    student.sleep()


    print(f"""Before going to your first day of school in {student.grade}th grade, would you like to add curriculum to your classes? (True, False): """, end="")
    add_curriculum_bool = input()
    if add_curriculum_bool == "True":
        student.add_curriculum()
    else:
        print("Skipped adding curriculum")

day, quarter = progress

def get_average_of_list(list_to_get):
    sum = 0
    count = len(list_to_get)
    for item in list_to_get:
        sum += item
    return sum/count

def join_lists(*args):
    full_list = []
    for list_to_use in args:
        for object_to_use in list_to_use:
            full_list.append(object_to_use)

while True:
    if day == 45:
        quarter = 2
    if day == 90:
        quarter = 3
    if day == 135:
        quarter = 4
    print("It is a new day. Day", day, f"Quarter {quarter}.\n")
    time.sleep(3)
    if day in [45, 90, 135, 180]:
        if day == 45:
            print("Grades for Q1:", student.gradebook1)
            print("Total Score: "+str(get_average_of_list(student.gradebook1))+"%\n")
        elif day == 90:
            print("Grades for Q2:", student.gradebook2)
            print("Total Score: " + str(get_average_of_list(student.gradebook2)) + "%\n")
        elif day == 135:
            print("Grades for Q3:", student.gradebook3)
            print("Total Score: " + str(get_average_of_list(student.gradebook3)) + "%\n")
        elif day == 180:
            print("Grades for Q4:", student.gradebook4)
            print("Total Score: " + str(get_average_of_list(student.gradebook4)) + "%\n")
            time.sleep(3)
            print(f"Total School Year {student.grade}th Grade Score: " + str(get_average_of_list(student.totalgradebook)) + "%\n")
            time.sleep(3)
            print("SUMMER BREAK!")
            time.sleep(3)
            print("SUMMER BREAK! IS over.")
            print("Updating grade...")
            student.grade += 1
            time.sleep(3)
            day = 1
            quarter = 1
            print("It is a new day. Day 1 Quarter 1.")
            print(f"Welcome to {student.grade}th Grade.")

    print("You are at school")
    todays_class_list = student.classes
    random.shuffle(todays_class_list)
    for todays_class in todays_class_list:
        print("Your next class is", todays_class.name)
        student.learn(todays_class)

    print("\nThe school day is over. You are going home. Type 'choices' to see the menu: ", end="")
    choices_yesno = input()
    if choices_yesno.lower() == "choices":
        while True:
            choice = input("Choices: savegame, quitmenu, play, addtocurriculum, deletegame, passwordchange: ")
            if choice == 'quitmenu':
                print("Exiting menu\n")
                break
            elif choice == "savegame":
                filechoice = input("Please choose a file name (no extension): ")
                while os.path.exists(("game_"+filechoice)):
                    filechoice = input("That already exists. Try again: ")
                folder_new = "game_"+filechoice
                os.mkdir(folder_new)
                school_path = os.path.join("game_" + filechoice, "school.schoolsim")
                student_path = os.path.join("game_" + filechoice, "student.schoolsim")
                password_path = os.path.join("game_" + filechoice, "password.schoolsim")
                progress_path = os.path.join("game_" + filechoice, "progress.schoolsim")
                with open(school_path, 'wb') as dump_to:
                    pickle.dump(school, dump_to)
                with open(student_path, 'wb') as dump_to:
                    pickle.dump(student, dump_to)
                with open(password_path, 'wb') as dump_to:
                    pickle.dump(student.password, dump_to)
                with open(progress_path, 'wb') as dump_to:
                    pickle.dump([day, quarter], dump_to)
                print(f"""\nYour game '{filechoice}' was successfully saved.
Do not delete any files in the 'game_{filechoice}/' folder.
Thanks for playing School Simulator.""")
                time.sleep(2)
                quit()
            elif choice == "play":
                print("You played with your friends")
            elif choice == "addtocurriculum":
                student.add_curriculum()
            elif choice == "deletegame":
                print("\nIf you would like to destroy this game, you must confirm your identity.")
                check_name = input("Enter the name you used for this game: ")
                if check_name != student.name:
                    print("Access denied\n")
                else:
                    print("Your game is deleting...")
                    print("Your game was deleted.")
                    print("If there are other copies of this game as saved folders, you can delete those too.")
                    print("Exiting...")
                    time.sleep(5)
                    quit()
            elif choice == "passwordchange":
                passwordold = input("Enter your old password to change it: ")
                if student.password == passwordold:
                    student.password = input("Authenticated! New password: ")
                else:
                    print("Access denied")

    student.sleep()
    day += 1