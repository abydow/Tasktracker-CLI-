import json
import os
import sys
import argparse
from datetime import datetime

class TaskTracker:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """Load tasks from JSON file or return empty list if file doesn't exist"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as file:
                    tasks = json.load(file)
                    # Ensure tasks is a list
                    if isinstance(tasks, list):
                        return tasks
                    else:
                        print(f"Warning: Invalid format in {self.filename}. Starting with empty task list.")
                        return []
            else:
                return []
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {self.filename}. {e}")
            print("Starting with empty task list.")
            return []
        except Exception as e:
            print(f"Error loading tasks: {e}")
            return []

    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.tasks, file, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")
            return False
        return True

    def get_next_id(self):
        """Get the next available ID for a new task"""
        if not self.tasks:
            return 1
        return max(task['id'] for task in self.tasks) + 1

    def get_task_by_id(self, task_id):
        """Find task by ID"""
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None

    def add_task(self, description):
        """Add a new task"""
        if not description.strip():
            print("Error: Task description cannot be empty.")
            return False

        task = {
            "id": self.get_next_id(),
            "description": description.strip(),
            "status": "todo",
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat()
        }

        self.tasks.append(task)

        if self.save_tasks():
            print(f"Task added successfully (ID: {task['id']})")
            return True
        return False

    def update_task(self, task_id, description):
        """Update task description"""
        task = self.get_task_by_id(task_id)

        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return False

        if not description.strip():
            print("Error: Task description cannot be empty.")
            return False

        task['description'] = description.strip()
        task['updatedAt'] = datetime.now().isoformat()

        if self.save_tasks():
            print(f"Task {task_id} updated successfully.")
            return True
        return False

    def delete_task(self, task_id):
        """Delete a task"""
        task = self.get_task_by_id(task_id)

        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return False

        self.tasks = [t for t in self.tasks if t['id'] != task_id]

        if self.save_tasks():
            print(f"Task {task_id} deleted successfully.")
            return True
        return False

    def mark_in_progress(self, task_id):
        """Mark task as in-progress"""
        return self._update_task_status(task_id, "in-progress")

    def mark_done(self, task_id):
        """Mark task as done"""
        return self._update_task_status(task_id, "done")

    def mark_todo(self, task_id):
        """Mark task as todo"""
        return self._update_task_status(task_id, "todo")

    def _update_task_status(self, task_id, status):
        """Helper method to update task status"""
        task = self.get_task_by_id(task_id)

        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return False

        task['status'] = status
        task['updatedAt'] = datetime.now().isoformat()

        if self.save_tasks():
            print(f"Task {task_id} marked as {status}.")
            return True
        return False

    def list_tasks(self, status_filter=None):
        """List tasks, optionally filtered by status"""
        if not self.tasks:
            print("No tasks found.")
            return True

        # Filter tasks if status_filter is provided
        tasks_to_show = self.tasks
        if status_filter:
            tasks_to_show = [task for task in self.tasks if task['status'] == status_filter]

            if not tasks_to_show:
                print(f"No tasks with status '{status_filter}' found.")
                return True

        # Sort tasks by ID for consistent display
        tasks_to_show.sort(key=lambda x: x['id'])

        print("\nTasks:")
        print("-" * 80)

        for task in tasks_to_show:
            # Format created and updated dates for better readability
            created = self._format_datetime(task['createdAt'])
            updated = self._format_datetime(task['updatedAt'])

            # Status display with visual indicators
            status_display = {
                'todo': '⏳ TODO',
                'in-progress': '🔄 IN-PROGRESS', 
                'done': '✅ DONE'
            }.get(task['status'], task['status'].upper())

            print(f"ID: {task['id']}")
            print(f"Description: {task['description']}")
            print(f"Status: {status_display}")
            print(f"Created: {created}")
            print(f"Updated: {updated}")
            print("-" * 80)

        return True

    def _format_datetime(self, iso_string):
        """Format ISO datetime string for display"""
        try:
            dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            return iso_string

def create_parser():
    """Create argument parser with all commands and arguments"""
    parser = argparse.ArgumentParser(
        description='Task Tracker CLI - Track and manage your tasks',
        epilog='Examples:\n'
               '  %(prog)s add "Buy groceries"\n'
               '  %(prog)s update 1 "Buy groceries and cook dinner"\n'
               '  %(prog)s mark-in-progress 1\n'
               '  %(prog)s mark-done 1\n'
               '  %(prog)s list\n'
               '  %(prog)s list done\n'
               '  %(prog)s delete 1',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('description', help='Task description')

    # Update command
    update_parser = subparsers.add_parser('update', help='Update a task')
    update_parser.add_argument('id', type=int, help='Task ID')
    update_parser.add_argument('description', help='New task description')

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('id', type=int, help='Task ID')

    # Mark in-progress command
    mark_progress_parser = subparsers.add_parser('mark-in-progress', help='Mark task as in-progress')
    mark_progress_parser.add_argument('id', type=int, help='Task ID')

    # Mark done command
    mark_done_parser = subparsers.add_parser('mark-done', help='Mark task as done')
    mark_done_parser.add_argument('id', type=int, help='Task ID')

    # Mark todo command (optional - to revert status)
    mark_todo_parser = subparsers.add_parser('mark-todo', help='Mark task as todo')
    mark_todo_parser.add_argument('id', type=int, help='Task ID')

    # List command
    list_parser = subparsers.add_parser('list', help='List tasks')
    list_parser.add_argument('status', nargs='?', choices=['todo', 'in-progress', 'done'],
                           help='Filter tasks by status (optional)')

    return parser

def main():
    """Main function to handle command line arguments and execute commands"""
    parser = create_parser()

    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()

    # If no command provided, show help
    if not args.command:
        parser.print_help()
        return

    # Initialize task tracker
    tracker = TaskTracker()

    # Execute command based on arguments
    try:
        if args.command == 'add':
            tracker.add_task(args.description)

        elif args.command == 'update':
            tracker.update_task(args.id, args.description)

        elif args.command == 'delete':
            tracker.delete_task(args.id)

        elif args.command == 'mark-in-progress':
            tracker.mark_in_progress(args.id)

        elif args.command == 'mark-done':
            tracker.mark_done(args.id)

        elif args.command == 'mark-todo':
            tracker.mark_todo(args.id)

        elif args.command == 'list':
            tracker.list_tasks(args.status)

        else:
            print(f"Unknown command: {args.command}")
            parser.print_help()

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
