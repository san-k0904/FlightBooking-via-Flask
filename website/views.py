from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
import json
import sqlite3
from urllib.parse import quote, unquote
from .models import User
from . import db_path

views = Blueprint('views', __name__)

@views.route('/home')
@login_required
def home():
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT f.airline, fd.date, fd.departure, fd.landing, fd.flight_id, fd.from_destination, fd.to_destination
            FROM booking AS b
            JOIN flight_details AS fd ON b.detail_id = fd.detail_id
            JOIN flights AS f ON fd.flight_id = f.flight_id
            WHERE b.user_id = ?
        ''', (current_user.id,))
        
        booked_flights = cursor.fetchall()

    return render_template('home.html', user=current_user, booked_flights=booked_flights)

@views.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        to_dest = request.form.get('TO')
        from_dest = request.form.get('FROM')
        date = request.form.get('travel_date')
        if not to_dest or not from_dest or not date:
            flash('Please fill out all fields.', category='error')
        else:
            with sqlite3.connect(db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT fd.detail_id, f.airline, fd.departure, fd.landing, fd.flight_id, fd.price, fd.available_seats
                    FROM flights AS f
                    JOIN flight_details AS fd ON f.flight_id = fd.flight_id
                    WHERE fd.from_destination = ? AND fd.to_destination = ? AND fd.date = ? AND fd.available_seats > 0
                ''', (from_dest, to_dest, date))
                
                available_flights = cursor.fetchall()
                if not available_flights:
                    flash('Sorry, No flights available.', category='error')
                else:
                    # Encode available_flights and search_params as JSON
                    available_flights_json = json.dumps([dict(row) for row in available_flights])
                    search_params = json.dumps({"to_dest": to_dest, "from_dest": from_dest, "date": date})
                    
                    # Pass as query parameters
                    return redirect(url_for('views.search_results',  user=current_user, available_flights=quote(available_flights_json), search_params=quote(search_params)))

    return render_template('flight_index.html', user=current_user)

@views.route('/search-results', methods=['GET', 'POST'])
def search_results():
    available_flights_json = request.args.get('available_flights', None)
    search_params_json = request.args.get('search_params', None)
    
    # Decode the JSON strings
    available_flights = json.loads(unquote(available_flights_json))
    search_params = json.loads(unquote(search_params_json))
    
    to_dest = search_params["to_dest"]
    from_dest = search_params["from_dest"]
    date = search_params["date"]

    if request.method == 'POST':
        detail_id = request.form.get('detail_id')
        if not detail_id:
            flash('Please select a flight to book.', category='error')
        else:
            with sqlite3.connect(db_path) as conn:
                try:
                    conn.execute('BEGIN TRANSACTION')
                    
                    conn.execute('''
                        INSERT INTO booking (user_id, detail_id) VALUES (?, ?)
                    ''', (current_user.id, detail_id))
                    
                    conn.execute('''
                        UPDATE flight_details SET available_seats = available_seats - 1 WHERE detail_id = ?
                    ''', (detail_id,))
                    
                    conn.execute('COMMIT')
                    
                    flash('Flight booked successfully!', category='success')
                    return redirect(url_for('views.home', user=current_user))
                
                except Exception as e:
                    conn.execute('ROLLBACK')
                    flash('Error occurred while booking the flight.', category='error')
                    return redirect(url_for('views.search_results'))

    return render_template('flight_check.html', available_flights=available_flights, user=current_user)