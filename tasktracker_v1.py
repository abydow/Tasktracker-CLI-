"""
Task tracker CLI 
version 1.0
(basic)

"""

import json 
import sys
from datetime import datetime

# simple Task Class to represent the data 

class Task:
    def __init__(self,task_id,description):
        self.id = task_id
        self.description = description
        self.status = "todo"
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

    def to_dict(self):
        "I will use a dictionary format where I will assign the value as task and key as the id"
        return{
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
#tasktracker
class TaskTracker:
    def __init__(self):
        self.tasks = []
        self.next_id = 1
    #the task adding feature here
    def add_task(self, description):
        task = Task(self.next_id, description)
        self.tasks.append(task)
        self.next_id += 1
        return task.id
    #list of tasks
    def list_task(self):
        if not self.tasks:
            print("Add some tasks!!")
            return
        print("\n" + "-" * 20)
        print("\n       ->YOUR TASKS<-      ")
        print("_" * 20)
        for task in self.tasks:
            print(f"ID: {task.id}, Description: {task.description}, Status: {task.status}")
#for bash
def main():
    tracker = TaskTracker()
    
    if len(sys.argv) < 2:
        print("Usage: ")
        print("  python tasktracker.py add <task_description>")
        print("  python tasktracker.py list")
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Please provide a task description.")
            return
        description = sys.argv[2]
        task_id = tracker.add_task(description)
        print(f"Task added with ID: {task_id}")

    elif command == "list":
        tracker.list_task()

    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()