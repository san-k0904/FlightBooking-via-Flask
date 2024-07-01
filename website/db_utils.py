import sqlite3
from werkzeug.security import generate_password_hash
from . import db_path

def populate_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Populate flights table
    flights_data = [
        ('6D7932', 'IndiGo'),
        ('AI101', 'Air India'),
        ('SG345', 'SpiceJet'),
        ('GA456', 'GoAir'),
        ('UK789', 'Vistara'),
        ('AA123', 'AirAsia India'),
        ('AL456', 'Alliance Air'),
        ('TJ789', 'TruJet'),
        ('SA012', 'Star Air'),
        ('AO345', 'Air Odisha')
    ]
    
    cursor.executemany('INSERT INTO flights (flight_id, airline) VALUES (?, ?)', flights_data)

    # Populate flight_details table
    flight_details_data = [
        ('6D7932', '2024-05-01', '08:00', '10:30', 2000.50, 150, 'Delhi', 'Mumbai'),
        ('AI101', '2024-05-02', '10:00', '12:30', 1800.00, 200, 'Mumbai', 'Delhi'),
        ('SG345', '2024-05-03', '12:00', '14:30', 2200.75, 180, 'Delhi', 'Bangalore'),
        ('GA456', '2024-05-04', '14:00', '16:30', 1500.00, 220, 'Bangalore', 'Delhi'),
        ('UK789', '2024-05-05', '16:00', '18:30', 3000.00, 100, 'Delhi', 'Kolkata'),
        ('AA123', '2024-05-06', '18:00', '20:30', 2500.00, 120, 'Kolkata', 'Delhi'),
        ('AL456', '2024-05-07', '20:00', '22:30', 1800.50, 180, 'Delhi', 'Chennai'),
        ('TJ789', '2024-05-08', '22:00', '00:30', 1600.00, 190, 'Chennai', 'Delhi'),
        ('SA012', '2024-05-09', '08:00', '10:30', 2100.25, 160, 'Delhi', 'Hyderabad'),
        ('AO345', '2024-05-10', '10:00', '12:30', 1900.00, 210, 'Hyderabad', 'Delhi'),
        ('6D7932', '2024-05-11', '12:00', '14:30', 2200.75, 180, 'Delhi', 'Bangalore'),
        ('AI101', '2024-05-12', '14:00', '16:30', 1500.00, 220, 'Bangalore', 'Delhi'),
        ('SG345', '2024-05-13', '16:00', '18:30', 3000.00, 100, 'Delhi', 'Kolkata'),
        ('GA456', '2024-05-14', '18:00', '20:30', 2500.00, 120, 'Kolkata', 'Delhi'),
        ('UK789', '2024-05-15', '20:00', '22:30', 1800.50, 180, 'Delhi', 'Chennai'),
        ('AA123', '2024-05-16', '22:00', '00:30', 1600.00, 190, 'Chennai', 'Delhi'),
        ('AL456', '2024-05-17', '08:00', '10:30', 2100.25, 160, 'Delhi', 'Hyderabad'),
        ('TJ789', '2024-05-18', '10:00', '12:30', 1900.00, 210, 'Hyderabad', 'Delhi'),
        ('SA012', '2024-05-19', '12:00', '14:30', 2200.75, 180, 'Delhi', 'Bangalore'),
        ('AO345', '2024-05-20', '14:00', '16:30', 1500.00, 220, 'Bangalore', 'Delhi'),
        ('AI101', '2024-05-03', '14:30', '17:00', 2300.50, 170, 'Delhi', 'Bangalore'),
        ('SG345', '2024-05-03', '15:00', '17:30', 2400.25, 160, 'Delhi', 'Bangalore'),
        ('GA456', '2024-05-04', '12:30', '15:00', 2200.00, 200, 'Bangalore', 'Delhi'),
        ('UK789', '2024-05-04', '13:00', '15:30', 2350.75, 180, 'Bangalore', 'Delhi'),
        ('AA123', '2024-05-04', '13:30', '16:00', 2450.50, 170, 'Bangalore', 'Delhi'),
        ('TJ789', '2024-05-05', '14:00', '16:30', 2100.75, 0, 'Delhi', 'Mumbai'),
        ('AO345', '2024-05-06', '14:30', '17:00', 2300.50, 1, 'Mumbai', 'Delhi'),
        ('SA012', '2024-05-07', '15:00', '17:30', 2400.25, 2, 'Delhi', 'Bangalore')
    ]

    cursor.executemany('''
    INSERT INTO flight_details (
        flight_id, date, departure, landing, price, available_seats, from_destination, to_destination
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', flight_details_data)

     # Populate users table
    users_data = [
        ('Rahul Sharma', 'rahul@example.com', generate_password_hash('password123'), '9876543210'),
        ('Priya Patel', 'priya@example.com', generate_password_hash('password456'), '9876543211'),
        ('Amit Kumar', 'amit@example.com', generate_password_hash('password789'), '9876543212')
    ]
    cursor.executemany('INSERT INTO user (name, email, password, contact) VALUES (?, ?, ?, ?)', users_data)

    # Populate booking table
    booking_data = [
        (1, 1),
        (1, 2),
        (2, 3),
        (2, 4),
        (3, 5),
        (3, 6),
        (3, 7),
        (3, 8),
        (3, 9),
        (3, 10)
    ]
    cursor.executemany('INSERT INTO booking (user_id, detail_id) VALUES (?, ?)', booking_data)

    conn.commit()
    conn.close()
