"""
Task tracker CLI 
version 1.0
(basic)

"""

import json 
import sys
import os
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
    @classmethod
    def from_dict(cls, data):
        "task creation"
        return cls(
            task_id=data["id"],
            description=data["description"],
            status=data["status"],
            created_at=data["createdAt"],
            updated_at=data["updatedAt"]

        )
#tasktracker
class TaskTracker:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        """Load tasks from JSON file"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as file:
                    data = json.load(file)
                    self.tasks = [Task.from_dict(task_data) for task_data in data]
        except Exception as e:
            print(f"Warning: Could not load tasks: {e}")
            self.tasks = []

    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            with open(self.filename, 'w') as file:
                json.dump([task.to_dict() for task in self.tasks], file, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def get_next_id(self):
        """Get next available ID"""
        if not self.tasks:
            return 1
        return max(task.id for task in self.tasks) + 1

    def add_task(self, description):
        """Add a new task"""
        task = Task(self.get_next_id(), description)
        self.tasks.append(task)
        self.save_tasks()
        return task.id

    def update_task(self, task_id, description):
        """Update task description"""
        for task in self.tasks:
            if task.id == task_id:
                task.description = description
                task.updated_at = datetime.now().isoformat()
                self.save_tasks()
                return True
        return False

    def delete_task(self, task_id):
        """Delete a task"""
        original_count = len(self.tasks)
        self.tasks = [task for task in self.tasks if task.id != task_id]
        if len(self.tasks) < original_count:
            self.save_tasks()
            return True
        return False

    def mark_status(self, task_id, status):
        """Update task status"""
        for task in self.tasks:
            if task.id == task_id:
                task.status = status
                task.updated_at = datetime.now().isoformat()
                self.save_tasks()
                return True
        return False

    def list_tasks(self, status_filter=None):
        """List tasks, optionally filtered by status"""
        filtered_tasks = self.tasks
        if status_filter:
            filtered_tasks = [task for task in self.tasks if task.status == status_filter]

        if not filtered_tasks:
            if status_filter:
                print(f"No tasks with status '{status_filter}'")
            else:
                print("No tasks found.")
            return

        print("\nYour Tasks:")
        print("-" * 60)
        for task in sorted(filtered_tasks, key=lambda x: x.id):
            status_icon = {"todo": "⏳", "in-progress": "🔄", "done": "✅"}.get(task.status, "❓")
            print(f"[{task.id}] {status_icon} {task.description} ({task.status})")

# Step 5: command line interface
def main():
    tracker = TaskTracker()

    if len(sys.argv) < 2:
        print("Task Tracker CLI - Version 2")
        print("Commands:")
        print("  add 'description'           - Add a new task")
        print("  update <id> 'description'   - Update task description")
        print("  delete <id>                 - Delete a task")
        print("  mark-done <id>              - Mark task as done")
        print("  mark-progress <id>          - Mark task as in-progress")
        print("  list [status]               - List tasks (optionally filter by status)")
        return

    command = sys.argv[1]

    try:
        if command == "add":
            if len(sys.argv) < 3:
                print("Please provide a task description")
                return
            description = sys.argv[2]
            task_id = tracker.add_task(description)
            print(f"✅ Task added successfully (ID: {task_id})")

        elif command == "update":
            if len(sys.argv) < 4:
                print("Usage: update <id> 'new description'")
                return
            task_id = int(sys.argv[2])
            description = sys.argv[3]
            if tracker.update_task(task_id, description):
                print(f"✅ Task {task_id} updated successfully")
            else:
                print(f"❌ Task {task_id} not found")

        elif command == "delete":
            if len(sys.argv) < 3:
                print("Usage: delete <id>")
                return
            task_id = int(sys.argv[2])
            if tracker.delete_task(task_id):
                print(f"✅ Task {task_id} deleted successfully")
            else:
                print(f"❌ Task {task_id} not found")

        elif command == "mark-done":
            if len(sys.argv) < 3:
                print("Usage: mark-done <id>")
                return
            task_id = int(sys.argv[2])
            if tracker.mark_status(task_id, "done"):
                print(f"✅ Task {task_id} marked as done")
            else:
                print(f"❌ Task {task_id} not found")

        elif command == "mark-progress":
            if len(sys.argv) < 3:
                print("Usage: mark-progress <id>")
                return
            task_id = int(sys.argv[2])
            if tracker.mark_status(task_id, "in-progress"):
                print(f"🔄 Task {task_id} marked as in-progress")
            else:
                print(f"❌ Task {task_id} not found")

        elif command == "list":
            status_filter = sys.argv[2] if len(sys.argv) > 2 else None
            if status_filter and status_filter not in ["todo", "in-progress", "done"]:
                print("Valid statuses: todo, in-progress, done")
                return
            tracker.list_tasks(status_filter)

        else:
            print(f"Unknown command: {command}")

    except ValueError:
        print("Error: Task ID must be a number")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()