import sys
import sqlite3
from flask import \
    Flask, render_template, request, redirect, g, session
app = Flask(__name__, static_url_path='/static')
app.secret_key = 'secret'

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Column, String

#creating a session 
engine = create_engine('sqlite:///todo.db')
Session = sessionmaker(bind=engine, autocommit=True)
session = Session()

Base = declarative_base()
#declaring the model for the table we need in our database
class Todo(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    due = Column(String)
    description = Column(String)
    state = Column(String)

    def __init__(self, due, title, description, state):
        self.due = due
        self.title = title
        self.description = description
        self.state = state

Base.metadata.create_all(engine)

#the following two methods render the basic templates
@app.route("/")
def say_hello():
    return render_template('hello.html', name = 'name')

@app.route("/todo")
def todo_list():
    entries = session.query(Todo).all()
    return render_template('todo.html', entries = entries)

#this method look for a certain entry by using its title and renders the search template
@app.route("/search" , methods=['POST'])
def search_screen():
    title = request.form['title']
    looked_up_entry = session.query(Todo).filter_by(title = title).first()
    return render_template('search.html', entry = looked_up_entry)

#the remeining methods are for adding, deleting, changing the state and showing all entries
@app.route('/add', methods=['POST'])
def add_entry():
    title = request.form['title']
    due = request.form['due']
    description  = request.form['description']
    new_entry = Todo(title = title, due = due, description = description, state = 'NEW')
    session.add(new_entry)
    return redirect('/todo')


@app.route('/delete',  methods=['POST'])
def delete_entry():
    id = request.args.get('ID')
    print(id)
    e = session.query(Todo).filter_by(id = id).first()
    session.delete(e)
    return redirect('/todo')

@app.route('/update', methods =['Post'])
def update_entry():
    id = request.args.get('ID')
    print(id)
    finished_entry = session.query(Todo).filter_by(id = id).first()
    finished_entry.state = 'FINISHED!'
    return redirect('/todo')

@app.route('/show', methods = ['Post'])
def show_all():
    return redirect('/todo')

app.run(debug=True)