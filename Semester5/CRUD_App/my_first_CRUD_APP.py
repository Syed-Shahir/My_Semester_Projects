from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# Define the Todo_list model
class Todo_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}>'

# Create the database tables
with app.app_context():
    db.create_all()

# Route to handle GET (retrieve all tasks) and POST (create a task) requests
@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'POST':
        task_content = request.json.get('content')  # Get the task content from the JSON request
        new_task = Todo_list(content=task_content)  # Create a new task object

        try:
            db.session.add(new_task)
            db.session.commit()
            return jsonify({'message': 'Task created successfully'}), 201  # Return success message with status code 201
        except Exception as e:
            return jsonify({'error': 'Failed to create task'}), 500  # Return error message with status code 500

    else:  # For GET requests
        tasks = Todo_list.query.order_by(Todo_list.date_created).all()  # Retrieve all tasks
        output = [{'id': task.id, 'content': task.content, 'date_created': task.date_created} for task in tasks]
        return jsonify({'tasks': output}), 200  # Return tasks with status code 200

# Route to handle DELETE (delete a task) and PUT (update a task) requests by ID
@app.route('/tasks/<int:id>', methods=['DELETE', 'PUT'])
def task(id):
    task_to_edit = Todo_list.query.get_or_404(id)  # Get the task by ID

    if request.method == 'DELETE':
        try:
            db.session.delete(task_to_edit)
            db.session.commit()
            return jsonify({'message': 'Task deleted successfully'}), 200
        except Exception as e:
            return jsonify({'error': 'Failed to delete task'}), 500

    elif request.method == 'PUT':
        new_content = request.json.get('content')  # Get updated content from JSON request
        if new_content:
            task_to_edit.content = new_content  # Update task content

            try:
                db.session.commit()
                return jsonify({'message': 'Task updated successfully'}), 200
            except Exception as e:
                return jsonify({'error': 'Failed to update task'}), 500
        else:
            return jsonify({'error': 'No content provided for update'}), 400

if __name__ == "__main__":
    app.run(debug=True)
