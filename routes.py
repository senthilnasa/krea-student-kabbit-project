from app import app, db, mail
from flask import render_template, request, redirect, url_for, session, flash
from models import TemporaryLogin, VerificationToken, User, CabRequest, JoinRequest
from flask_mail import Message
import secrets
from datetime import datetime, timedelta
from uuid import uuid4



@app.route('/')
def index():
    return redirect(url_for('home_page'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone']
        
        session['user_name'] = name
        session['user_email'] = email
        session['user_phone'] = phone_number
        
        temp_login = TemporaryLogin()
        temp_login.name = name
        temp_login.email = email
        temp_login.phone_number = phone_number
        
        db.session.add(temp_login)
        db.session.commit()
        
        token = secrets.token_urlsafe()
        
        # Check if a token already exists for the given email and update it
        verification_token = VerificationToken.query.filter_by(email=email).first()
        if verification_token:
            verification_token.token = token
        else:
            verification_token = VerificationToken()
            verification_token.email = email
            verification_token.token = token
            db.session.add(verification_token)
        
        db.session.commit()

        verification_url = url_for('verify_email', token=token, _external=True)
        msg = Message("Email Verification", sender=app.config['MAIL_USERNAME'], recipients=[email])
        msg.body = f'Please click on the link to verify your email: {verification_url}'
        mail.send(msg)

        return render_template('verify_email_prompt.html')
    
    return render_template('login.html')

@app.route('/verify_email/<token>')
def verify_email(token):
    verification_record = VerificationToken.query.filter_by(token=token).first()
    if verification_record:
        temp_login = TemporaryLogin.query.filter_by(email=verification_record.email).first()
        if temp_login:
            new_user = User()
            new_user.name = temp_login.name
            new_user.email = temp_login.email
            db.session.add(new_user)
            
            session['logged_in'] = True
            session['user_name'] = temp_login.name
            session['user_email'] = temp_login.email
            db.session.commit()

            return redirect(url_for('home_page'))

    return render_template('verification_failed.html')

@app.route('/home')
def home_page():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('home.html')
@app.route('/request', methods=['GET', 'POST'])
def cab_request():
    if request.method == 'POST':
        name = session.get('user_name')
        email = session.get('user_email')
        phone_number = request.form.get('mobile')
        destination = request.form.get('destination')
        date = request.form.get('date')
        time = request.form.get('time')
        datetime_combined = datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M')

        # Retrieve creator_email from session
        creator_email = email
        
        trip_id = str(uuid4())

        # Check if the user is the creator of the trip
        if email != creator_email:
            # Create a new trip
            new_request = CabRequest()
            new_request.name = name
            new_request.email = email
            new_request.phone_number = phone_number
            new_request.destination = destination
            new_request.time = datetime_combined
            new_request.creator_email = creator_email
            db.session.add(new_request)
            db.session.commit()
            return redirect(url_for('filter_requests', date=date, time_slot=time))
        
        # Check if the user already has an existing trip
        existing_trip = CabRequest.query.filter_by(email=email).first()

        if existing_trip:
            # If the user has an existing trip, allow them to delete it and create a new one
            if request.form.get('delete_trip'):
                db.session.delete(existing_trip)
                db.session.commit()
            else:
                # Redirect to options page to handle the existing trip
                return render_template('options.html', existing_trip=existing_trip)

        # Create a new trip
        new_request = CabRequest()
        new_request.name = name
        new_request.email = email
        new_request.phone_number = phone_number
        new_request.destination = destination
        new_request.time = datetime_combined
        new_request.creator_email = creator_email
        db.session.add(new_request)
        db.session.commit()
        return redirect(url_for('filter_requests', date=date, time_slot=time))

    return render_template('request.html')

@app.route('/list_requests')
def list_requests():
    user_email = session.get('user_email')
    # Assuming requests is a list of trip objects
    requests = CabRequest.query.filter(CabRequest.creator_email!=user_email).all()
    # You would also fetch the join requests made by the user
    user_join_requests = JoinRequest.query.filter_by(requester_email=user_email).all()
    # Create a set of trip IDs that the user has already requested to join
    requested_trip_ids = {req.cab_request_id for req in user_join_requests}

    return render_template('requests.html', requests=requests, requested_trip_ids=requested_trip_ids)

@app.route('/available')
def available_requests():
    requests = CabRequest.query.filter_by(verified=True).all()
    return render_template('available.html', requests=requests)

@app.route('/filter', methods=['GET', 'POST'])
def filter_requests():
    if request.method == 'POST':
        selected_date = request.form.get('date')
        selected_time_slot = request.form.get('time_slot')
        
        # Parse selected date and time slot
        start_time = datetime.strptime(f"{selected_date} {selected_time_slot}", '%Y-%m-%d %H:%M')
        end_time = start_time + timedelta(minutes=30)  # Calculate end time for the time slot

        # Filter requests by the specified time slot
        filtered_requests = CabRequest.query.filter(
            CabRequest.time >= start_time,
            CabRequest.time < end_time,
            CabRequest.verified == True
        ).all()

        # Check if there are existing trips for the selected time slot
        existing_trips = filtered_requests

        # Render a version of the requests template specific to the selected time slot
        return render_template('requests.html', requests=existing_trips, selected_date=selected_date, selected_time_slot=selected_time_slot)

    # Handle GET request if needed
    return redirect(url_for('home_page'))  # Redirect to home page or handle differently as needed

@app.route('/logout')
def logout():

    # Clear the session
    session.clear()
    return redirect(url_for('home_page'))

def get_creator_email(trip_id):
    trip = CabRequest.query.filter_by(id=trip_id).first()
    if trip:
        return trip.creator_email
    else:
        return None  # Or handle the case when the trip ID is not found
    
@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    user_email = session['user_email']

    # Trips the user has created
    created_trips = CabRequest.query.filter_by(creator_email=user_email).all()

    # Join requests the user has made to other trips
    sent_requests = JoinRequest.query.filter_by(requester_email=user_email).all()

    # Debugging to see what trips are being fetched
    for trip in created_trips:
        print(trip.id, trip.destination)  # Example of logging trip details

    # Join requests received for the user's trips
    received_requests = []
    for trip in created_trips:
        for join_request in trip.join_requests:
           if not join_request.accepted:  # Only include not yet accepted requests
                received_requests.append(join_request)
    # Ensure 'created_trips' is also passed to the template here
    return render_template('dashboard.html', created_trips=created_trips, sent_requests=sent_requests, received_requests=received_requests)

@app.route('/join_trip/<int:cab_request_id>', methods=['POST'])
def join_trip(cab_request_id):
    if 'user_email' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    user_email = session['user_email']
    existing_request = JoinRequest.query.filter_by(cab_request_id=cab_request_id, requester_email=user_email).first()
    
    if not existing_request:
        join_request = JoinRequest()
        join_request.cab_request_id = cab_request_id
        join_request.requester_email = user_email
        db.session.add(join_request)
        db.session.commit()
    
    return redirect(url_for('list_requests'))  # Redirect back to the requests list


@app.route('/handle_join_request/<int:join_request_id>/<action>', methods=['POST'])
def handle_join_request(join_request_id, action):
    if 'logged_in' not in session or not session['logged_in']:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('login'))

    join_request = JoinRequest.query.get(join_request_id)
    if not join_request:
        flash('Join request not found.', 'error')
        return redirect(url_for('dashboard'))
     
    if action == 'decline' and join_request.accepted:
        flash('This request has already been accepted and cannot be declined.', 'error')
        return redirect(url_for('dashboard'))

    if action == 'accept':
        # Mark the join request as accepted
        join_request.accepted = True
        flash('Request accepted. User added to the trip.', 'success')
        db.session.commit()
    elif action == 'decline':
        db.session.delete(join_request)
        flash('Request declined.', 'success')
        db.session.commit()

    return redirect(url_for('dashboard'))