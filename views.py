import datetime
from flask import request, redirect, url_for, render_template, render_template_string, flash
from flask_peewee.utils import get_object_or_404
from app import app
from auth import auth
from models import User, Note
from flaskext.markdown import Markdown


markdown = Markdown(app)
@app.route('/')
def homepage():
    if auth.get_logged_in_user():
        return redirect(url_for('getNotes'))
    else:
        return render_template("homepage.html")


@app.route('/notes/')
@app.route('/notes/<int:note_id>', methods=['GET', 'POST'])
@auth.login_required
def getNotes(note_id=None):
    user = auth.get_logged_in_user()
    notes = Note.select().where(Note.user == user
                                ).order_by(Note.created_date.desc())
    context = {
        'notes': notes,
    }
    if note_id:
        note = get_object_or_404(Note, Note.user == user, Note.id == note_id)
        context['note'] = note
    return render_template('notes.html', context=context)


@app.route('/join/', methods=['GET', 'POST'])
def join():
    if request.method == 'POST' and request.form['username']:
        try:
            user = User.select().where(
                User.username == request.form['username']).get()
            flash('That username is already taken')
        except User.DoesNotExist:
            user = User(
                username=request.form['username'],
                password=request.form['password'],
                email=request.form['email'],
                join_date=datetime.datetime.now()
            )
            user.set_password(request.form['password'])
            user.save()

            auth.login_user(user)
            return getNotes()

    return render_template('join.html')


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            user = User().select().where(User.username ==
                                         request.form['username']).get()
            if user.check_password(request.form['password']):
                auth.login_user(user)
                return getNotes()
        except Exception:
            pass

    elif request.method == 'GET':
        if auth.get_logged_in_user():
            return redirect(url_for('getNotes'))
    return render_template('login.html')


@app.route('/create/', methods=['GET', 'POST'])
@auth.login_required
def create():
    user = auth.get_logged_in_user()
    if request.method == 'POST' and request.form["content"]:
        Note.create(
            user=user,
            content=request.form["content"],
        )
        flash('Your note has been created')
        return redirect(url_for('getNotes'))

    return render_template('create.html')


@app.route('/edit/<int:note_id>/', methods=['POST'])
@auth.login_required
def edit(note_id):
    user = auth.get_logged_in_user()
    note = get_object_or_404(Note, Note.user == user, Note.id == note_id)

    note.content = request.form.get('content')
    note.save()
    return redirect(url_for('getNotes', note_id=note.id))


@app.route('/delete/<int:note_id>/', methods=['POST'])
@auth.login_required
def delete_entry(note_id):
    user = auth.get_logged_in_user()
    note = get_object_or_404(Note, Note.user == user, Note.id == note_id)

    note.delete_instance()
    return redirect(url_for('getNotes'))
