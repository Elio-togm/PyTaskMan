import sys

class TaskTracker:
    def __init__(self):
        self.tasks = {} # ID: [Task, Description,Status, Creation_Date, Last_Modified]
    
    def __help__(self): # Shows the help message which includes all available commands
        print("\n-----------------------------------------------------------------------------")
        print("\nPyTaskMan: A Task Tracker CLI program written in Python\n")
        print("Commands:")
        print("add: Adds a task and returns its ID")
        print("update (task_id) 'updated task': Updates a task")
        print("delete (task_id): Deletes a task")
        print("mark_in_progress (task_id): Marks a task as in progress")
        print("mark_done (task_id): Marks a task as done")
        print("mark_not_done (task_id): Marks a task as not done")
        print("list (optional: status): Lists all tasks(if a status is provided, lists only tasks with that status)")
        print("help: Shows this help message")
        print("quit: Quits the program\n")
        print("Optional Arguments (Only on startup of the program):")
        print("-h, --help: Show this help message and exit\n")
        return("-----------------------------------------------------------------------------\n")
    
    def add(self, task):
        self.tasks.add(task) #! NOT IMPLEMENTED
        return "Task added successfully (ID: 1)"
    
    def update(self, task_id): #! NOT IMPLEMENTED
        pass

    def delete(self, task_id): #! NOT IMPLEMENTED
        pass

    def mark_in_progress(self, task_id): #! NOT IMPLEMENTED
        pass

    def mark_done(self, task_id): #! NOT IMPLEMENTED
        pass

    def mark_not_done(self, task_id): #! NOT IMPLEMENTED
        pass

    def list(self, command=None): #! NOT IMPLEMENTED
        pass

if __name__ == "__main__":
    pyTaskMan = TaskTracker()
    if len(sys.argv) > 1:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print(pyTaskMan.__help__())
            sys.exit()
        else:
            print("\nINVALID ARGUMENT\n")
            print("For help, use the '-h' or '--help' flag")
            sys.exit()
    command_number = 0
    max_command_number = float("inf")

    while command_number < max_command_number:
        if command_number == 0:
            command_number += 1
            print(pyTaskMan.__help__())
        user_command = input("PyTaskMan> ")
        methods = [(func, getattr(pyTaskMan, func)) for func in dir(pyTaskMan) if not func.startswith("_")]

        if user_command.strip(' ') == '':
            print(methods)
        elif user_command.split()[0] in methods:
            pyTaskMan.add(user_command.split()[1])
        elif user_command.split()[0] == "quit":
            sys.exit()