from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db_path

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Please fill out all fields.', category='error')
        else:
            with sqlite3.connect(db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM user WHERE email = ?;', (email,))
                existing_user = cursor.fetchone()
                if existing_user:
                    if check_password_hash(existing_user['password'], password):
                        flash('Logged in successfully!', category='success')
                        user_obj = User(existing_user['uid'], existing_user['email'], existing_user['password'], existing_user['name'], existing_user['contact'])
                        login_user(user_obj, remember=True)
                        return redirect(url_for('views.home'))
                    else:
                        flash('Incorrect password. Please try again.', category='error')
                else:
                    flash('Account does not exist.', category='error')
                
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        contact = request.form.get('contact')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if not name or not email or not contact or not password1 or not password2:
            flash('Please fill out all fields.', category='error')
        elif len(email) < 4:
            flash('Email must be at least 4 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 6:
            flash('Password must be at least 6 characters.', category='error')
        elif len(contact) < 10:
            flash('Invalid contact number.', category='error')
        else:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM user WHERE email = ?;', (email,))
                existing_user = cursor.fetchone()
                if existing_user:
                    flash(f'Account for {email} already exists', category='error')
                else:
                    cursor.execute('''
                    INSERT INTO user (email, password, name, contact)
                    VALUES (?, ?, ?, ?);
                    ''', (email, generate_password_hash(password1), name, contact))
                    conn.commit()
                    flash('Account created successfully', category='success')
                    return redirect(url_for('auth.login'))

    return render_template('sign_up.html', user=current_user)