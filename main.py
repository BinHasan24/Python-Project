"""
main.py - Task Manager User Interface
This is the main file that runs the program
"""
from logic import TaskManager, EmptyDescriptionError
from models import Task

class TaskManagerUI:
    """
    Handles the user interface for the task manager.
    This class is responsible for:
    - Showing menus to the user
    - Getting user input
    - Calling the appropriate TaskManager methods
    - Displaying results
    """
    def __init__(self) -> None:
        """
        Initialize the UI.
        Creates a TaskManager object that will handle all the business logic
        """
        self.manager = TaskManager()
    
    def show_welcome(self) -> None:
        """
        Display welcome message
        """
        print("\n" + "*" * 50)
        print("   WELCOME TO TASK MANAGER!")
        print("*" * 50)
    
    def show_menu(self) -> None:
        """
        Display the main menu options
        
        shows what the user can do. Right now we only have 2 features
        (create and view) but we will add more in future iterations
        """
        print("\n" + "=" * 50)
        print("       TASK MANAGER - MAIN MENU")
        print("=" * 50)
        print("1. Create a new task")
        print("2. View all tasks")
        print("3. Exit")
        print("=" * 50)
    
    def create_task_flow(self) -> None:
        """
        Handle the process of creating a new task.
        This method:
        1. Asks user for task description
        2. Create the task
        3. Shows success or error message
        
        We use try-except to catch errors gracefully instead of crashing.
        """
        print("\n--- CREATE NEW TASK ---")
        
        #get input from user
        description = input("Enter task description: ")
        
        try:
            #try to create the task
            task = self.manager.create_task(description)
            
            #if successful, show confirmation
            print(f"\nSuccess! Task created with ID: {task.task_id}")
            
        except EmptyDescriptionError as error:
            #if description was empty, show the error message
            print(f"Error: {error}")
            
        except Exception as error:
            #catch any other unexpected errors
            print(f"Unexpected error: {error}")
    
    def view_all_tasks_flow(self) -> None:
        """
        Handle displaying all tasks
        
        Shows all tasks. If there are no tasks,
        shows a friendly message instead of an empty table.
        """
        print("\n--- ALL TASKS ---")
        
        #check if we have any tasks
        if self.manager.is_empty():
            print("No tasks found. Your task list is empty!")
            print("Use option 1 to create your first task.")
            return
        
        #print table header
        print(f"\n{'ID':<5} {'Description':<30} {'Status':<15}")
        print("-" * 50)
        
        #print each task
        for task in self.manager.get_all_tasks():
            print(task)
    
    def run(self) -> None:
        """
        Main loop that runs the program.
        
        This method:
        1. Shows welcome message
        2. Shows menu
        3. Gets user choice
        4. Calls appropriate method
        5. Repeats until user chooses to exit
        
        The while True loop runs forever until we break out of it.
        """
        #show welcome message once at start
        self.show_welcome()
        
        #main loop
        while True:
            #show menu
            self.show_menu()
            
            #get the choice
            choice = input("\nEnter your choice (1-3): ")
            
            #handle the choice
            if choice == "1":
                self.create_task_flow()
                
            elif choice == "2":
                self.view_all_tasks_flow()
                
            elif choice == "3":
                #to exit
                print("\nThank you for using Task Manager!")
                print("Goodbye!")
                break  #exit the loop
                
            else:
                #invalid choice
                print("\nInvalid choice! Please enter 1, 2, or 3.")


def main() -> None:
    """
    Entry point of the program.
    
    This function creates the UI and starts it running.
    It is called when we run: python main.py
    """
    #create UI
    app = TaskManagerUI()
    
    #start
    app.run()


# This special check makes sure main() only runs when we execute this file directly
# (not when we import it as a module)
if __name__ == "__main__":
    main()