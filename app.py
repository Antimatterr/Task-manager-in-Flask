from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

with open("config.json", "r") as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)

if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']

db = SQLAlchemy(app)


class Tasks(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(30), nullable=True)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task = request.form.get('task')
        entry = Tasks(task=task, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
    tasks = Tasks.query.all()
    return render_template('index.html', params=params, tasks=tasks)


@app.route('/delete/<string:sno>')
def delete(sno):
    task_to_delete = Tasks.query.filter_by(sno=sno).first()
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')


@app.route('/update/<string:sno>', methods=['GET', 'POST'])
def update(sno):
    task = Tasks.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        task.task = request.form.get('tasks')
        db.session.commit()
        return redirect('/')
    else:
        return render_template('update.html', tasks=task)


if __name__ == '__main__':
    app.run(debug=True)
