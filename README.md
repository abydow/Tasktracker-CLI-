## [Task Tracker CLI](https://roadmap.sh/projects/task-tracker)

A simple command-line interface (CLI) application to track and manage your tasks. Built with Python using only standard library modules.

Features

- ✅ Add, update, and delete tasks
- 🔄 Mark tasks as `todo`, `in-progress`, or `done`
- 📋 List all tasks or filter by status
- 💾 Persistent storage using JSON file
- 🕐 Automatic timestamp tracking (created/updated)
- 🎯 Unique task IDs for easy management
- 🛡️ Robust error handling and edge case management

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## Installation

1. Clone or download the `task_tracker.py` file
2. Make it executable (optional on Unix-like systems):
   ```bash
   chmod +x task_tracker.py
   ```

## Usage

### Basic Commands

```bash
# Show help
python task_tracker.py --help

# Add a new task
python task_tracker.py add "Buy groceries"

# List all tasks
python task_tracker.py list

# Update a task
python task_tracker.py update 1 "Buy groceries and cook dinner"

# Mark task as in-progress
python task_tracker.py mark-in-progress 1

# Mark task as done
python task_tracker.py mark-done 1

# Mark task as todo (revert status)
python task_tracker.py mark-todo 1

# Delete a task
python task_tracker.py delete 1

# List tasks by status
python task_tracker.py list todo
python task_tracker.py list in-progress
python task_tracker.py list done
```

### Command Reference

| Command | Arguments | Description |
|---------|-----------|-------------|
| `add` | `<description>` | Add a new task with the given description |
| `update` | `<id> <description>` | Update the description of task with given ID |
| `delete` | `<id>` | Delete the task with given ID |
| `mark-in-progress` | `<id>` | Mark task as in-progress |
| `mark-done` | `<id>` | Mark task as done |
| `mark-todo` | `<id>` | Mark task as todo |
| `list` | `[status]` | List all tasks or filter by status (todo, in-progress, done) |

### Examples

```bash
# Adding tasks
python task_tracker.py add "Study Python programming"
python task_tracker.py add "Complete project documentation"
python task_tracker.py add "Review code changes"

# Managing task status
python task_tracker.py mark-in-progress 1
python task_tracker.py mark-done 2

# Filtering tasks
python task_tracker.py list in-progress  # Show only in-progress tasks
python task_tracker.py list done        # Show only completed tasks

# Updating and deleting
python task_tracker.py update 3 "Review and merge code changes"
python task_tracker.py delete 2
```

## Task Properties

Each task has the following properties:

- **id**: Unique identifier for the task (auto-generated)
- **description**: Short description of the task
- **status**: Current status (`todo`, `in-progress`, `done`)
- **createdAt**: Timestamp when the task was created (ISO format)
- **updatedAt**: Timestamp when the task was last updated (ISO format)

## Data Storage

Tasks are stored in a `tasks.json` file in the current directory. The JSON structure looks like:

```json
[
  {
    "id": 1,
    "description": "Buy groceries",
    "status": "todo",
    "createdAt": "2025-08-19T13:30:45.123456",
    "updatedAt": "2025-08-19T13:30:45.123456"
  },
  {
    "id": 2,
    "description": "Write documentation",
    "status": "in-progress",
    "createdAt": "2025-08-19T13:31:20.654321",
    "updatedAt": "2025-08-19T14:15:30.987654"
  }
]
```

## Error Handling

The application gracefully handles various error scenarios:

- **Invalid JSON file**: Creates a new empty task list and shows a warning
- **Missing tasks.json**: Automatically creates a new file when saving tasks
- **Invalid task IDs**: Shows appropriate error messages
- **Empty descriptions**: Prevents adding/updating tasks with empty descriptions
- **File permission issues**: Shows error messages for read/write failures

## Running the Demo

A demo script is provided to showcase all functionality:

```bash
python demo.py
```

This will demonstrate:
1. Adding multiple tasks
2. Listing all tasks
3. Updating task descriptions
4. Changing task statuses
5. Filtering tasks by status
6. Deleting tasks

## Project Structure

```
task-tracker/
├── task_tracker.py    # Main application file
├── demo.py           # Demonstration script
├── README.md         # This documentation
└── tasks.json        # Data file (created automatically)
```

## Architecture

The application follows a clean, object-oriented design:

### TaskTracker Class
- **Data Management**: Handles loading/saving tasks from/to JSON file
- **Task Operations**: Provides methods for CRUD operations
- **Error Handling**: Robust error handling for file operations and validation

### CLI Interface
- **Argument Parsing**: Uses argparse with subcommands for clean CLI design
- **User Experience**: Helpful error messages and command examples
- **Flexibility**: Supports both required and optional arguments

### Key Features
- **ID Management**: Auto-incrementing unique IDs for tasks
- **Status Validation**: Ensures valid status transitions
- **Timestamp Tracking**: Automatic creation and update timestamp management
- **Data Validation**: Input validation and sanitization

## Best Practices Implemented

1. **Error Handling**: Comprehensive try-catch blocks with meaningful error messages
2. **Data Validation**: Input sanitization and validation
3. **Code Organization**: Clean separation of concerns with class-based design
4. **User Experience**: Intuitive CLI with helpful examples and error messages
5. **Data Integrity**: Atomic operations and consistent data structure
6. **Extensibility**: Modular design allows easy addition of new features

## Potential Enhancements

Future versions could include:
- Task priorities and categories
- Due dates and reminders
- Task search functionality
- Export/import capabilities
- Configuration options
- Colored output for better readability
- Task statistics and reporting

## License

This project is provided as-is for educational and practical use. Feel free to modify and distribute according to your needs.

## Contributing

This is a learning project. Suggestions and improvements are welcome!

---

**Happy task tracking! 🎯**
