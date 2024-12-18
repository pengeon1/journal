from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

TASKS_FILE = 'tasks.json'

# Function to read tasks from the JSON file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    return []

# Function to save tasks to the JSON file
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks, editing=False)

@app.route('/add', methods=['POST'])
def add_task():
    task_text = request.form.get('task')
    if task_text:
        tasks = load_tasks()
        tasks.append({'text': task_text, 'completed': False})
        save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    tasks = load_tasks()
    tasks[task_id]['completed'] = True
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    tasks = load_tasks()
    tasks.pop(task_id)
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    tasks = load_tasks()
    task = tasks[task_id]
    
    if request.method == 'POST':
        task_text = request.form.get('task')
        if task_text:
            task['text'] = task_text
            save_tasks(tasks)
        return redirect(url_for('index'))
    
    # Pass 'editing=True' to render the task edit form
    return render_template('index.html', tasks=tasks, task=task, task_id=task_id, editing=True)

if __name__ == '__main__':
    app.run(debug=True)
