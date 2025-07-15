import json
import os

TODO_FILE = 'todos.json'

def load_todos():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as f:
            return json.load(f)
    return []

def save_todos(todos):
    with open(TODO_FILE, 'w') as f:
        json.dump(todos, f, indent=4)

def add_task(task):
    todos = load_todos()
    todos.append({"task": task, "done": False})
    save_todos(todos)
    print(f" Added: {task}")

def list_tasks():
    todos = load_todos()
    for i, t in enumerate(todos, 1):
        status = "✅" if t['done'] else "❌"
        print(f"{i}. {status} {t['task']}")

def mark_done(index):
    todos = load_todos()
    if 0 <= index < len(todos):
        todos[index]['done'] = True
        save_todos(todos)
        print(f" Marked done: {todos[index]['task']}")

# Example usage
add_task("Buy groceries")
add_task("Call Alice")
mark_done(0)
list_tasks()
