class School:
    def __init__(self, name):
        self.name = name
        self.students = []
        print("School", name)

    def add_student(self, student):
        self.students.append(student)

class Student:
    def __init__(self, name, grade, school):
        self.name = name
        self.grade = grade
        self.school = school
        self.school.students.append(self)
        self.classes = []

    def add_class(self, class_obj):
        self.classes.append(class_obj)

    def ask(self, curriculum_questions, class_obj):
        questions = list(curriculum_questions)
        random.shuffle(questions)
        for question in questions:
            print("Question:", question, "Your Answer: ", end="")
            given_answer = input()
            class_obj.evaluate_response(question, given_answer)
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
                print("""First, it will ask you to enter a question. Then input the answers separated by commas with no spaces.
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
        else:
            print(f"The given answer was wrong. Correct answer: {self.curriculum[question]}")
