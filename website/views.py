from logging import error
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import user
from werkzeug.utils import redirect
from .models import Note
from . import db

import json

views = Blueprint('views', __name__)


@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if not note:
            error_statement = "Please type note.."
            return render_template('home.html', error_statement=error_statement, note=note, user=current_user)

        new_note = Note(data=note, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash('Note added!', category='success')

    allnote = Note.query.all()
    return render_template("home.html", user=current_user, allnote=allnote)


@views.route('/show')
def show():
    return render_template('show.html', user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        note = request.form.get('note')

        note = Note.query.filter_by(id=id).first()
        note.note = note
        db.session.add(note)
        db.session.commit()
        return redirect('/show')

    note = Note.query.filter_by(id=id).first()
    return render_template("update.html", note=note, user=current_user)