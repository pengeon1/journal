import json
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Load existing journal entries from a JSON file
def load_entries():
    try:
        with open('entries.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Save journal entries to a JSON file
def save_entries(entries):
    with open('entries.json', 'w') as f:
        json.dump(entries, f)

journal_entries = load_entries()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = {'title': title, 'content': content, 'date_created': date_created}
        journal_entries.append(new_entry)
        save_entries(journal_entries)
        return redirect(url_for('index'))
    return render_template('index.html', entries=journal_entries)

if __name__ == "__main__":
    app.run(debug=True)
