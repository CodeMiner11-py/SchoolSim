from classes_dont_touch import *

# STARTING SIMULATION

def load_simulation(filename):
    global school, student
    path_folder = filename+"/"
    school_path = os.path.join("game_" + filename, "school.schoolsim")
    student_path = os.path.join("game_" + filename, "student.schoolsim")
    with open(school_path, 'rb') as load_from:
        school = pickle.load(load_from)
    with open(student_path, 'rb') as load_from:
        student = pickle.load(load_from)
    print(f"\nYour game was loaded successfully! Just to confirm, your name is {student.name}.\n")

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
    school = School(input("Please enter the name of the school you are applying to: "))
    student = Student(input("Please enter your name: "), input("Please enter your grade: "), school)
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


    print(f"""
Before going to your first day of school in {student.grade}th grade, would you like to add curriculum to your classes? (True, False): """, end="")
    add_curriculum_bool = input()
    if add_curriculum_bool == "True":
        student.add_curriculum()
    else:
        print("Skipped adding curriculum")

day = 1

while True:
    print("It is a new day. Day", day, "\n")
    time.sleep(3)
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
            choice = input("Choices: savegame, quitmenu, play, addtocurriculum, deletegame: ")
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
                with open(school_path, 'wb') as dump_to:
                    pickle.dump(school, dump_to)
                with open(student_path, 'wb') as dump_to:
                    pickle.dump(student, dump_to)
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

    student.sleep()
    day += 1