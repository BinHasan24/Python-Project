"""
main.py - Task Manager User Interface
This is the main file that runs the program
"""
from logic import TaskManager, EmptyDescriptionError, TaskNotFoundError
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
        
        Now we have 4 features implemented: create, view, edit, and delete.
        We will add search in the next iteration.
        """
        print("\n" + "=" * 50)
        print("       TASK MANAGER - MAIN MENU")
        print("=" * 50)
        print("1. Create a new task")
        print("2. View all tasks")
        print("3. Edit a task")
        print("4. Delete a task")
        print("5. Exit")
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
    
    def edit_task_flow(self) -> None:
        """
        Handle editing an existing task.
        
        This method:
        1. Shows all tasks (so user can see IDs)
        2. Asks for task ID to edit
        3. Shows current task info
        4. Asks what to edit (description, status, or both)
        5. Gets new values
        6. Updates the task
        7. Shows success or error message
        
        We use try-except to handle errors like task not found or invalid status.
        """
        print("\n--- EDIT TASK ---")
        
        #first, check if there are any tasks
        if self.manager.is_empty():
            print("No tasks to edit. Create a task first!")
            return
        
        #show all tasks so user can see the IDs
        print("\nCurrent tasks:")
        print(f"{'ID':<5} {'Description':<30} {'Status':<15}")
        print("-" * 50)
        for task in self.manager.get_all_tasks():
            print(task)
        
        #get task ID from user
        try:
            task_id_input = input("\nEnter task ID to edit: ")
            task_id = int(task_id_input)  #convert to integer
        except ValueError:
            #if user enters something that is not a number
            print("Error: Please enter a valid number for task ID!")
            return
        
        #find and show the current task
        task = self.manager.find_task_by_id(task_id)
        if task is None:
            print(f"Error: Task with ID {task_id} not found!")
            return
        
        print(f"\nCurrent task: {task.description} [{task.status}]")
        
        #ask what to edit
        print("\nWhat do you want to edit?")
        print("1. Description only")
        print("2. Status only")
        print("3. Both description and status")
        edit_choice = input("Enter choice (1-3): ")
        
        new_description = None
        new_status = None
        
        try:
            #handle based on user choice
            if edit_choice == "1":
                #edit description only
                new_description = input("Enter new description: ")
                self.manager.edit_task(task_id, new_description=new_description)
                print("\n✓ Task description updated successfully!")
                
            elif edit_choice == "2":
                #edit status only
                print("\nChoose new status:")
                print("1. Not Started")
                print("2. In Progress")
                print("3. Completed")
                status_choice = input("Enter choice (1-3): ")
                
                #convert choice to status string
                if status_choice == "1":
                    new_status = "Not Started"
                elif status_choice == "2":
                    new_status = "In Progress"
                elif status_choice == "3":
                    new_status = "Completed"
                else:
                    print("Error: Invalid status choice!")
                    return
                
                self.manager.edit_task(task_id, new_status=new_status)
                print(f"\n✓ Task status updated to: {new_status}")
                
            elif edit_choice == "3":
                #edit both
                new_description = input("Enter new description: ")
                
                print("\nChoose new status:")
                print("1. Not Started")
                print("2. In Progress")
                print("3. Completed")
                status_choice = input("Enter choice (1-3): ")
                
                #convert choice to status string
                if status_choice == "1":
                    new_status = "Not Started"
                elif status_choice == "2":
                    new_status = "In Progress"
                elif status_choice == "3":
                    new_status = "Completed"
                else:
                    print("Error: Invalid status choice!")
                    return
                
                self.manager.edit_task(task_id, new_description=new_description, 
                                     new_status=new_status)
                print("\n✓ Task updated successfully!")
                
            else:
                print("Error: Invalid choice! Please enter 1, 2, or 3.")
                
        except TaskNotFoundError as error:
            #if task was not found (should not happen since we checked above)
            print(f"Error: {error}")
            
        except EmptyDescriptionError as error:
            #if new description was empty
            print(f"Error: {error}")
            
        except ValueError as error:
            #if status validation failed (invalid status)
            print(f"Error: {error}")
            
        except Exception as error:
            #catch any other unexpected errors
            print(f"Unexpected error: {error}")
    
    def delete_task_flow(self) -> None:
        """
        Handle deleting a task.
        
        This method:
        1. Shows all tasks (so user can see IDs)
        2. Asks for task ID to delete
        3. Shows the task that will be deleted
        4. Asks for confirmation (to prevent accidental deletion)
        5. Deletes the task if confirmed
        6. Shows success or error message
        
        We ask for confirmation because deletion is permanent and cannot be undone.
        """
        print("\n--- DELETE TASK ---")
        
        #first, check if there are any tasks
        if self.manager.is_empty():
            print("No tasks to delete. Your task list is empty!")
            return
        
        #show all tasks so user can see the IDs
        print("\nCurrent tasks:")
        print(f"{'ID':<5} {'Description':<30} {'Status':<15}")
        print("-" * 50)
        for task in self.manager.get_all_tasks():
            print(task)
        
        #get task ID from user
        try:
            task_id_input = input("\nEnter task ID to delete: ")
            task_id = int(task_id_input)  #convert to integer
        except ValueError:
            #if user enters something that is not a number
            print("Error: Please enter a valid number for task ID!")
            return
        #find and show the task that will be deleted
        task = self.manager.find_task_by_id(task_id)
        if task is None:
            print(f"Error: Task with ID {task_id} not found!")
            return
        print(f"\nTask to delete: {task.description} [{task.status}]")
        
        #ask for confirmation
        #we use lower() to accept both "yes" and "YES" and "Yes"
        confirmation = input("\nAre you sure you want to delete this task? (yes/no): ")
        
        if confirmation.lower() == "yes":
            #user confirmed, delete the task
            try:
                deleted_task = self.manager.delete_task(task_id)
                print(f"\n✓ Task deleted successfully: {deleted_task.description}")
                
            except TaskNotFoundError as error:
                #if task was not found (should not happen since we checked above)
                print(f"Error: {error}")
                
            except Exception as error:
                #catch any other unexpected errors
                print(f"Unexpected error: {error}")
        else:
            #user cancelled
            print("\nDeletion cancelled. Task was not deleted.")
    
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
            choice = input("\nEnter your choice (1-5): ")
            
            #handle the choice
            if choice == "1":
                self.create_task_flow()
                
            elif choice == "2":
                self.view_all_tasks_flow()
                
            elif choice == "3":
                self.edit_task_flow()
                
            elif choice == "4":
                self.delete_task_flow()
                
            elif choice == "5":
                #to exit
                print("\nThank you for using Task Manager!")
                print("Goodbye!")
                break  #exit the loop
                
            else:
                #invalid choice
                print("\nInvalid choice! Please enter 1, 2, 3, 4, or 5.")

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
