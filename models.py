"""
models.py - Task data structure

This file contains the Task class that represents a single task.
"""
from dataclasses import dataclass, field
from typing import ClassVar

@dataclass
class Task:
    """
    Represents a single task in our task manager.
    
    Attributes:
        task_id: A unique number for each task
        description: What the task is about
        _status: Current status
    """
    #these are the fields that every task needs
    task_id: int
    description: str
    _status: str = field(default="Not Started", repr=False)
    
    #valid status options
    VALID_STATUSES: ClassVar[set] = {"Not Started", "In Progress", "Completed"}
    
    @property
    def status(self) -> str:
        """
        Get the current status of the task.
        
        Using @property decorator so we can control how status is accessed.
        
        Returns:
            The current status as a string
        """
        return self._status
    
    @status.setter
    def status(self, new_status: str) -> None:
        """
        Set a new status for the task with validation.
        
        Args:
            new_status: The new status we want to set
            
        Raises:
            ValueError: If the new status is not in our valid list
        """
        #check if the new status is valid
        if new_status not in self.VALID_STATUSES:
            raise ValueError(
                f"Status '{new_status}' is not valid. "
                f"Please use one of: {self.VALID_STATUSES}"
            )
        self._status = new_status
    
    def __str__(self) -> str:
        """
        Create a formatted string when we print a task.
        The :<5 and :<30 control spacing to make columns line up nicely.
        
        Returns:
            Formatted string with task information
        """
        return f"{self.task_id:<5} {self.description:<30} {self.status:<15}"
    
    def to_dict(self) -> dict:
        """
        Convert task to a dictionary so we can save it to JSON.
        
        Returns:
            Dictionary with task data
        """
        return {
            "task_id": self.task_id,
            "description": self.description,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """
        Create a Task from a dictionary (when loading from JSON).
        This is the opposite of to_dict(). We use @classmethod because
        we are creating a new Task object.
        
        Args:
            data: Dictionary containing task information
            
        Returns:
            A new Task object created from the dictionary
        """
        #create a new task with the basic info
        new_task = cls(
            task_id=data["task_id"],
            description=data["description"]
        )
        #set the status directly (passing validation since it is from file)
        new_task._status = data["status"]
        return new_task
