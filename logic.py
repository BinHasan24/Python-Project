"""
logic.py - Task Manager logic
This file contains the TaskManager class and custom error classes.
It handles all the operations like creating, finding, and saving tasks.
"""
import json
import os
from typing import List, Optional
from models import Task

#custom error classes 
class TaskManagerError(Exception):
    """
    Base error class
    We create our own error types
    """
    pass

class EmptyDescriptionError(TaskManagerError):
    """
    Error raised when someone tries to create a task with no description.
    This inherits from TaskManagerError so we can catch all task-related
    errors together if needed.
    """
    pass

class TaskNotFoundError(TaskManagerError):
    """
    Error raised when we try to find a task that does not exist.
    """
    pass

class TaskManager:
    """
    Manages all the tasks in our application.
    
    This class is responsible for:
    - Creating new tasks
    - Storing tasks in a list
    - Saving tasks to a file
    - Loading tasks from a file
    Attributes:
        tasks: A list that holds all our Task objects
        _next_id: Counter to generate unique IDs for new tasks
        _save_file: Name of the JSON file where we save tasks
    """
    
    def __init__(self, save_file: str = "tasks.json") -> None:
        """
        Initialize the TaskManager.
        starts with an empty list
        and tries to load any existing tasks from the file.

        Args:
            save_file: name of the file to save/load tasks (default: "tasks.json")
        """
        self.tasks: List[Task] = []  #empty list
        self._next_id: int = 1  #first task will have ID 1
        self._save_file: str = save_file
        
        self._load_tasks()
    
    def create_task(self, description: str) -> Task:
        """
        Create a new task and add it to our list
        
        This method:
        1. Checks if description is empty
        2. Creates a new Task object
        3. Adds it to our tasks list
        4. Increments the ID counter
        5. Saves everything to file
        
        Args:
            description: What the task is about
            
        Returns:
            The newly created Task object
            
        Raises:
            EmptyDescriptionError: If description is empty or just spaces
        """
        if not description.strip(): #1
            raise EmptyDescriptionError("Task description cannot be empty!")
        
        new_task = Task(task_id=self._next_id, description=description)   #2
        
        self.tasks.append(new_task)  #3
        
        self._next_id += 1  #4
        
        self._save_tasks()   #5
        
        return new_task
    
    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks in the manager.
        Returns:
            List of all Task objects
        """
        return self.tasks
    
    def find_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Find a specific task by its ID.
        
        loop through tasks and return the one with matching ID.
        If no task is found, we return None.
        
        Args:
            task_id: The ID number to search for
            
        Returns:
            The Task object if found, None if not found
        """
        #loop through all tasks
        for task in self.tasks:
            #check if this task has the ID we are looking for
            if task.task_id == task_id:
                return task
        
        #if we get here, task was not found
        return None
    
    def is_empty(self) -> bool:
        """
        Check if we have any tasks
        
        Returns:
            true if no tasks exist, false if we have at least one task
        """
        return len(self.tasks) == 0
    
    def _save_tasks(self) -> None:
        """
        Save all tasks to a JSON file.
        """
        try:
            #create a dictionary with all data
            data = {
                "next_id": self._next_id,
                "tasks": [task.to_dict() for task in self.tasks]
            }
            
            #open file and write JSON
            with open(self._save_file, 'w') as file:
                json.dump(data, file, indent=2)  # indent=2 makes it readable
                
        except IOError as error:
            #if something goes wrong with file, print warning but do not crash
            print(f"Warning: Could not save tasks: {error}")
    
    def _load_tasks(self) -> None:
        """
        Load tasks from JSON file when program starts.
        
        If the file does not exist (first time running), that is okay -
        we just start with an empty list.
        """
        #check if file exists
        if not os.path.exists(self._save_file):
            return
        
        try:
            #open and read the JSON file
            with open(self._save_file, 'r') as file:
                data = json.load(file)
                
                #restore the next_id counter
                self._next_id = data.get("next_id", 1)
                
                #recreate all Task objects from the saved data
                self.tasks = [
                    Task.from_dict(task_data) 
                    for task_data in data.get("tasks", [])
                ]
                
        except (IOError, json.JSONDecodeError) as error:
            #if file is corrupted or can not be read, start fresh
            print(f"Warning: Could not load tasks: {error}")
            self.tasks = []
            self._next_id = 1
