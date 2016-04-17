# -*- coding: utf-8 -*-
"""
IS211 Wk-11 Assignemnt
"""

from flask import Flask, render_template, request, redirect
import re
import pickle
import os.path
app = Flask(__name__)


toDoList = [] #empty set
emailPattern = re.compile("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$") #specific keys


def load(): #loads file
    fileName = 'toDoList.pkg1'
    if os.path.exists(fileName):
        return pickle.load(open(fileName, 'rb'))
    else:
        return []


@app.route('/') #template
def hello_world():
    return render_template('index.html', toDoList=toDoList)


@app.route('/submit', methods=['POST']) #submit
def submit():
    
    task = request.form['task']
    email = request.form['email']
    priority = request.form['priority']

    if re.match(emailPattern, email) is None:
        return redirect('/')
    elif len(task) == 0:
        return redirect('/')
    elif priority not in ('low', 'medium', 'high'):
        return redirect('/')
    else:
        toDoList.append((email, task, priority))
        return redirect('/')


@app.route('/clear', methods=['POST']) #clear
def clear():
    toDoList[:] = []
    return redirect('/')


@app.route('/delete', methods=['POST']) #delete
def delete():
    email = request.form['email']
    deletetask = request.form['deletetask']
    priority = request.form['priority']
    entry = (email, deletetask, priority)
    toDoList.remove(entry)
    return redirect('/')


@app.route('/save', methods=['POST']) #save
def save():
    pickle.dump(toDoList, open('toDoList.pkg1', 'wb'))
    return redirect('/')


if __name__ == "__main__":
    toDoList = load()
    app.run()