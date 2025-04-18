import sys, time, os, json

class TaskTracker:
    def __init__(self, tasks={}):
        self.tasks = tasks # ID: [Task, Status, Creation_Date, Last_Modified]

        # Properly sets up the dictionary to have the ID be a integer and not a string
        tasks_to_delete = []
        for task in self.tasks:
            tasks_to_delete.append(task)
        for task in tasks_to_delete:
            self.tasks[int(task)] = self.tasks[task]
            del self.tasks[task]

        # A list of all IDs in use
        self.__all_ids__ = list(self.tasks.keys()) # IDs in use can't be reused
        self.__all_ids__.insert(0, 0) # Adds 0 to the beginning of the list in case there are no tasks

        self.__find_lowest_id__()
        
        
    # Sets the lowest ID to the next available ID; Avaliable IDs include natural numbers but not 0
    def __find_lowest_id__(self):
        self.__lowest_id__ = 0
        while self.__lowest_id__ + 1 in self.__all_ids__:
            self.__lowest_id__ += 1
        self.__lowest_id__ += 1
    
    # Shows the help message which includes all available commands
    def __help__(self): 
        print("\n---------------------------------------------------------------------------------------------------------")
        print("\nPyTaskMan: A Task Tracker CLI program written in Python\n")
        print("Commands:")
        print("    add (name of task): Adds a task and returns its ID")
        print("    update (task_id) 'updated task': Updates a task")
        print("    delete (task_id): Deletes a task")
        print("    mark (status: todo, doing, done) (task_id): Marks a task as TODO, IN PROGRESS, or DONE")
        print("    list (optional: status): Lists all tasks(if a status is provided, lists only tasks with that status)")
        print("    help: Shows this help message")
        print("    quit: Quits the program\n")
        print("Optional Arguments (Only on startup of the program):")
        print("    -h, --help: Show this help message and exit\n")
        return("--------------------------------------------------------------------------------------------------------\n")
    
    # Error handler
    def __error_handler__(self, *args): 
        pass
    
    # Adds a new task and assigns it an ID
    def add(self, task):
        id = self.__lowest_id__ # Saves the ID of the task for future reference
        self.tasks[self.__lowest_id__] = [task,     # Sets the task, status, creation date, and last modified date of a task to an unused ID
                                          "NOT DONE", 
                                          time.asctime(time.gmtime(time.time())), 
                                          time.asctime(time.gmtime(time.time()))] 
        self.__all_ids__.append(self.__lowest_id__) # Adds the ID of the task to the list of all IDs
        self.__find_lowest_id__() # Sets the lowest ID to the next available ID
        return "Task added successfully (ID: {})".format(id) # Returns the ID of the task
    
    # Updates a task description
    def update(self, task_id, updated_task):
        self.tasks[int(task_id)] = [updated_task, 
                                    self.tasks[int(task_id)][1], 
                                    self.tasks[int(task_id)][2], 
                                    time.asctime(time.gmtime(time.time()))] 
        return 'Task updated successfully (ID: {})'.format(task_id)

    # Deletes a task
    def delete(self, task_id):
        task_id = int(task_id)
        self.tasks.pop(task_id)
        self.__all_ids__.remove(task_id)
        if self.__lowest_id__ > (task_id):
            self.__lowest_id__ = (task_id)
        return 'Task deleted successfully (ID: {})'.format(task_id)
    
    # Marks a task as one of three statuses: TODO, IN PROGRESS, or DONE
    def mark(self, command, task_id):
        if command.upper() == 'NOT_DONE' or command.upper() == 'N' or command.upper() == 'ND' or command.upper() == 'NOT DONE'\
            or command.upper() == 'TODO' or command.upper() == 'T' or command.upper() == 'TODO':
            return self.mark_todo(task_id) # Marks a task as not done
        
        elif command.upper() == 'IN_PROGRESS' or command.upper() == 'I' or command.upper() == 'IP' or command.upper() == 'IN PROGRESS' \
            or command.upper() == 'INPROGRESS' or command.upper() == 'DOING' or command.upper() == 'DO':
            return self.mark_in_progress(task_id) # Marks a task as in progress
        
        elif command.upper() == 'DONE' or command.upper() == 'D':
            return self.mark_done(task_id) # Marks a task as done

    def mark_in_progress(self, task_id):
        self.tasks[int(task_id)][1] = "IN PROGRESS"
        self.tasks[int(task_id)][3] = time.asctime(time.gmtime(time.time()))
        return 'Task marked in progress successfully (ID: {})'.format(task_id)

    def mark_done(self, task_id):
        self.tasks[int(task_id)][1] = "DONE"
        self.tasks[int(task_id)][3] = time.asctime(time.gmtime(time.time()))
        return 'Task marked done successfully (ID: {})'.format(task_id)

    def mark_todo(self, task_id):
        self.tasks[int(task_id)][1] = "TODO"
        self.tasks[int(task_id)][3] = time.asctime(time.gmtime(time.time()))
        return 'Task marked not done successfully (ID: {})'.format(task_id)
    
    # Returns a list of all tasks, or a list of all tasks with a specific status
    def list(self, command=None):
        if command == None:
            return dict(sorted(self.tasks.items())) # Returns a list of all tasks
        
        elif command.upper() == "TODO" or command.upper() == "NOT DONE" or command.upper() == "T" or command.upper() == "N":
            return dict(sorted({key: value for key, value in self.tasks.items() if value[1] == "NOT DONE"}.items())) # Returns a list of all tasks that are not done
        
        elif command.upper() == "IN PROGRESS" or command.upper() == "I" or command.upper() == "IP" or command.upper() == "P" \
            or command.upper() == "DOING" or command.upper() == "DO":
            return dict(sorted({key: value for key, value in self.tasks.items() if value[1] == "IN PROGRESS"}.items())) # Returns a list of all tasks that are in progress
        
        elif command.upper() == "DONE" or command.upper() == "D":
            return dict(sorted({key: value for key, value in self.tasks.items() if value[1] == "DONE"}.items())) # Returns a list of all tasks that are done

    # Prints the help message
    def help(self):
        return self.__help__() 

    # Quits the program
    def quit(self):
        self.tasks = dict(sorted(self.tasks.items())) # Organizes the tasks by ID before saving task data
        with open("taskData.json", "w") as f: # Opens the tasks.json file in write mode
            json.dump(self.tasks, f)
        sys.exit()

# Prints an error message for invalid arguments
def invalid_command():
    print("\nINVALID ARGUMENT\n") 
    print("For help, use the '-h' or '--help' flag\n") # Prints instructions for using the '-h' or '--help' flag


if __name__ == "__main__":
    if os.path.exists("taskData.json"): # Checks if the tasks.json file exists
        with open("taskData.json", "r") as f: # Opens the tasks.json file in read mode
            pyTaskMan = TaskTracker(json.load(f)) # Creates an instance of the TaskTracker class to begin tracking tasks
    else:
        with open("taskData.json", "w") as f: # Opens the tasks.json file in write mode
            json.dump({}, f)
        pyTaskMan = TaskTracker() # Creates an instance of the TaskTracker class to begin tracking tasks

    if len(sys.argv) > 1: # Checks if the user provided any optional arguments
        if sys.argv[1] == "-h" or sys.argv[1] == "--help": # Checks if the user provided the '-h' or '--help' flag
            print(pyTaskMan.help()) # Prints the help message
            pyTaskMan.quit() # Exits the program
        else:
            invalid_command() # Prints an error message for invalid arguments
            pyTaskMan.quit() # Exits the program
    command_number = 0 # Keeps track of the number of commands the user has entered
    max_command_number = float("inf") # Keeps track of the maximum number of commands the user can enter
    single_commmands = ['list', 'help', 'quit'] # A list of commands that can be entered without any arguments
    double_commmands = ['add', 'delete', 'list'] # A list of commands that can be entered with 2 arguments
    triple_commmands = ['update', 'mark'] # A list of commands that can be entered with 3 arguments

    while command_number < max_command_number:
        if command_number == 0: # Prints the help message the first time the user starts the program
            command_number += 1
            print(pyTaskMan.help())

        # Asks the user for a command
        user_command = input("PyTaskMan> ")
        # Gets all callable methods from the TaskTracker class
        methods = [(func, getattr(pyTaskMan, func)) for func in dir(pyTaskMan) if not func.startswith("_")]

        # Checks if the user entered a valid command
        if user_command.strip(' ') == '':
            invalid_command() # Prints an error message for invalid arguments

        command = user_command.lower().split()[0]
        valid_arguments_command = command in [method[0] for method in methods]

        if user_command.lower().strip(' ') in [method[0] for method in methods]: # Checks if the user entered a valid command without extra arguments: list, help, quit
            print(pyTaskMan.__getattribute__(user_command.lower().strip(' '))()) # Calls the function given by the command

        elif valid_arguments_command and command in double_commmands: # Checks if the user entered a valid command with 2 arguments: add, delete, marks, lists
            print(pyTaskMan.__getattribute__(command)(" ".join(user_command.split()[1:]))) # Calls the 2-argument function given by the command

        elif valid_arguments_command and command in triple_commmands: # Checks if the user entered a valid command with 3 arguments: update
            print(pyTaskMan.__getattribute__(command)(user_command.split()[1], " ".join(user_command.split()[2:]))) # Calls the 3-argument function given by the command
        
        else:
            invalid_command()