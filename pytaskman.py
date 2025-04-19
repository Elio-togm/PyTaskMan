import sys, time, os, json

class PyTaskMan:
    def __init__(self, tasks={}):
        self.tasks = {int(task): tasks[task] for task in tasks} # ID: [Task, Status, Creation_Date, Last_Modified]

        # A list of all IDs in use
        self.__all_ids__ = set(self.tasks.keys()) # IDs in use can't be reused
        self.__all_ids__.add(0) # Adds 0 to the beginning of the list in case there are no tasks

        self.__find_lowest_id__()
        
        self.HELP_MESSAGE = """
---------------------------------------------------------------------------------------------------------
PyTaskMan: A Task Tracker CLI program written in Python

Commands:
    add (name of task): Adds a task and returns its ID
    update (task_id) 'updated task': Updates a task
    delete (task_id): Deletes a task
    mark (task_id) (status: todo, doing, done): Marks a task as TODO, IN PROGRESS, or DONE
    list (optional: status): Lists all tasks(if a status is provided, lists only tasks with that status)
    help: Shows this help message
    quit: Quits the program

Optional Arguments (Only on startup of the program):
    -h, --help: Show this help message and exit

---------------------------------------------------------------------------------------------------------
"""
        
        
    # Sets the lowest ID to the next available ID; Avaliable IDs include natural numbers but not 0
    def __find_lowest_id__(self):
        self.__lowest_id__ = next((id for id in range(1, max(self.__all_ids__) + 2) if id not in self.__all_ids__), 1)
    
    # Error handler
    def __error_handler__(self, *args): #* I'll get to you little buddy :(
        # Checks if the user entered a valid command
        if user_command.strip(' ') == '':
            print(self.__invalid_command__()) # Prints an error message for invalid arguments

        try:
            command = user_command.lower().split()[0]
            valid_arguments_command = command in [method[0] for method in methods]

            if user_command.lower().strip(' ') in [method[0] for method in methods]: # Checks if the user entered a valid command without extra arguments: list, help, quit
                print(self.__getattribute__(user_command.lower().strip(' '))()) # Calls the function given by the command

            elif valid_arguments_command and command in double_commmands: # Checks if the user entered a valid command with 2 arguments: add, delete, marks, lists
                print(self.__getattribute__(command)(" ".join(user_command.split()[1:]))) # Calls the 2-argument function given by the command

            elif valid_arguments_command and command in triple_commmands: # Checks if the user entered a valid command with 3 arguments: update
                print(self.__getattribute__(command)(user_command.split()[1], " ".join(user_command.split()[2:]))) # Calls the 3-argument function given by the command
            
            else:
                print(self.__invalid_command__())
        
        except TypeError:
            self.__handle_missing_args__
        except ValueError:
            self.__handle_task_id_not_integer__
        except KeyError:
            self.__handle_invalid_task_id__

    def __handle_missing_args__(self):
        print("\nError: Function is missing positional arguments.") # Prints the error message
        print(self.__invalid_command__())

    def __handle_task_id_not_integer__(self):
        print("\nError: task_id isn't given as an integer.") # Prints the error message
        print(self.__invalid_command__())

    def __handle_invalid_task_id__(self):
        print("\nError: invalid ID(ID doesn't exist in the recorded tasks).") # Prints the error message
        print(self.__invalid_command__())

    def __invalid_command__(self):
        print("\nINVALID COMMAND\n") 
        return "For help, use the 'help' command\n"
    
    # Adds a new task and assigns it an ID
    def add(self, task):
        id = self.__lowest_id__ # Saves the ID of the task for future reference
        default_task_values = {
            "status": "NOT DONE",
            "creation_date": time.asctime(time.gmtime(time.time())),
            "last_modified_date": time.asctime(time.gmtime(time.time()))
        }
        self.tasks[self.__lowest_id__] = [task, *default_task_values.values()] 
        self.__all_ids__.add(self.__lowest_id__) # Adds the ID of the task to the list of all IDs
        self.__find_lowest_id__() # Sets the lowest ID to the next available ID
        return "Task added successfully (ID: {})".format(id) # Returns the ID of the task
    
    # Updates a task description
    def update(self, task_id, updated_task):
        task_id = int(task_id)
        task = self.tasks[task_id]
        self.tasks[task_id] = [updated_task, *task[1:3], time.asctime(time.gmtime(time.time()))] 
        return 'Task updated successfully (ID: {})'.format(task_id)

    # Deletes a task
    def delete(self, task_id):

        # If the user wants to delete all tasks
        if task_id.lower() == "all" or task_id.lower() == "a":
            self.tasks = {}
            self.__all_ids__ = [0]
            self.__lowest_id__ = 1
            return 'All tasks deleted successfully'
        
        # If the user wants to delete a specific task
        task_id = int(task_id)
        self.tasks.pop(task_id)
        self.__all_ids__.remove(task_id)
        self.__lowest_id__ = min(self.__lowest_id__, task_id)
        return 'Task deleted successfully (ID: {})'.format(task_id)
    
    # Marks a task as one of three statuses: TODO, IN PROGRESS, or DONE
    def mark(self, task_id, command):
        command = command.upper().strip(' ')
        valid_commands = {
            "NOT DONE": self.mark_todo, 
            "TODO": self.mark_todo, 
            "N": self.mark_todo, 
            "ND": self.mark_todo, 
            "T": self.mark_todo, 
            "IN_PROGRESS": self.mark_in_progress, 
            "I": self.mark_in_progress, 
            "IP": self.mark_in_progress, 
            "IN PROGRESS": self.mark_in_progress, 
            "INPROGRESS": self.mark_in_progress, 
            "DOING": self.mark_in_progress, 
            "DO": self.mark_in_progress,
            "DONE": self.mark_done, 
            "D": self.mark_done
        }
        return(valid_commands.get(command, self.__invalid_command__)(task_id))

    def mark_in_progress(self, task_id):
        task_id = int(task_id)
        task = self.tasks[task_id]
        self.tasks[task_id] = [task[0], "IN PROGRESS", task[2], time.asctime(time.gmtime(time.time()))]
        return 'Task marked in progress successfully (ID: {})'.format(task_id)

    def mark_done(self, task_id):
        task_id = int(task_id)
        task = self.tasks[task_id]
        self.tasks[task_id] = [task[0], "DONE", task[2], time.asctime(time.gmtime(time.time()))]
        return 'Task marked done successfully (ID: {})'.format(task_id)

    def mark_todo(self, task_id):
        task_id = int(task_id)
        task = self.tasks[task_id]
        self.tasks[task_id] = [task[0], "TODO", task[2], time.asctime(time.gmtime(time.time()))]
        return 'Task marked not done successfully (ID: {})'.format(task_id)
    
    # Returns a list of all tasks, or a list of all tasks with a specific status
    def list(self, command=None):

        # Returns a list of all tasks
        if command == None:
            print("\nAll Tasks:")
            self.tasks = dict(sorted(self.tasks.items()))
            return '\n'.join(f'[{key}] {value[0]} - Status: {value[1]}' for key, value in self.tasks.items())+"\n"
        
        command = command.upper().strip(' ')
        valid_commands = {
            "NOT DONE": self.list_todo, 
            "TODO": self.list_todo, 
            "N": self.list_todo, 
            "ND": self.list_todo,  
            "T": self.list_todo, 
            "IN_PROGRESS": self.list_in_progress, 
            "I": self.list_in_progress, 
            "IP": self.list_in_progress, 
            "IN PROGRESS": self.list_in_progress, 
            "INPROGRESS": self.list_in_progress, 
            "DOING": self.list_in_progress, 
            "DO": self.list_in_progress,
            "DONE": self.list_done, 
            "D": self.list_done
        }
        
        return valid_commands.get(command, self.__invalid_command__)()
    
    def list_todo(self):
        print("\nTasks [TODO]:")
        tasks = dict(sorted({key: value for key, value in self.tasks.items() if value[1] == "NOT DONE"}.items()))
        return '\n'.join(f'[{key}] {value[0]} - Status: {value[1]}' for key, value in tasks.items()) + "\n"
    
    def list_in_progress(self):
        print("\nTasks [In Progress]:")
        tasks = dict(sorted({key: value for key, value in self.tasks.items() if value[1] == "IN PROGRESS"}.items()))
        return '\n'.join(f'[{key}] {value[0]} - Status: {value[1]}' for key, value in tasks.items()) + "\n"
    
    def list_done(self):
        print("\nTasks [Done]:")
        tasks = dict(sorted({key: value for key, value in self.tasks.items() if value[1] == "DONE"}.items()))
        return '\n'.join(f'[{key}] {value[0]} - Status: {value[1]}' for key, value in tasks.items()) + "\n"

    # Prints the help message
    def help(self):
        return self.HELP_MESSAGE 

    # Quits the program
    def quit(self):
        confirm = input("\nAre you sure you want to quit? (Y/N)\n\n").upper().strip(' ')
        while confirm != 'Y' and confirm != 'N': 
            print("\nInvalid input, Try Again.\n")
            confirm = input("\nAre you sure you want to quit? (Y/N)\n\n").upper().strip(' ')
        if confirm == 'Y': # If the user confirms, the program is saved and exited
            print("\nQuitting...\n")
            self.tasks = dict(sorted(self.tasks.items())) # Organizes the tasks by ID before saving task data
            with open("taskData.json", "w") as f: # Opens the tasks.json file in write mode
                json.dump(self.tasks, f)
            exit()
        else: # If the user does not confirm, the program continues
            print("\nQuit cancelled.\n")

# Prints an error message for invalid arguments
def invalid_argument():
    print("\nINVALID ARGUMENT\n") 
    return("For help, use the '-h' or '--help' flag\n") # Prints instructions for using the '-h' or '--help' flag


if __name__ == "__main__":
    if os.path.exists("taskData.json"): # Checks if the tasks.json file exists
        with open("taskData.json", "r") as f: # Opens the tasks.json file in read mode
            pyTaskMan = PyTaskMan(json.load(f)) # Creates an instance of the PyTaskMan class to begin tracking tasks
    else:
        with open("taskData.json", "w") as f: # Opens the tasks.json file in write mode
            json.dump({}, f)
        pyTaskMan = PyTaskMan() # Creates an instance of the PyTaskMan class to begin tracking tasks

    if len(sys.argv) > 1: # Checks if the user provided any optional arguments
        if sys.argv[1] == "-h" or sys.argv[1] == "--help": # Checks if the user provided the '-h' or '--help' flag
            print(pyTaskMan.help()) # Prints the help message
            pyTaskMan.quit() # Exits the program
        else:
            invalid_argument() # Prints an error message for invalid arguments
            pyTaskMan.quit() # Exits the program

    command_number = 0 # Keeps track of the number of commands the user has entered
    single_commmands = ['list', 'help', 'quit'] # A list of commands that can be entered without any arguments
    double_commmands = ['add', 'delete', 'list'] # A list of commands that can be entered with 2 arguments
    triple_commmands = ['update', 'mark'] # A list of commands that can be entered with 3 arguments

    while True:
        if command_number == 0: # Prints the help message the first time the user starts the program
            command_number += 1
            print(pyTaskMan.help())

        # Asks the user for a command
        user_command = input("PyTaskMan> ")
        # Gets all callable methods from the PyTaskMan class
        methods = [(func, getattr(pyTaskMan, func)) for func in dir(pyTaskMan) if not func.startswith("_")]

        # Checks if the user entered a valid command
        pyTaskMan.__error_handler__()