from flask import Flask, redirect, url_for, Blueprint, request, jsonify
from myproject import db 
from myproject.manager.models import Manager, Events
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime

manager_bp = Blueprint('manager_bp' ,__name__)


@manager_bp.route('/sign-up/', methods=['POST'])
def sign_up():
    data = request.json
    email = data.get('email')
    password_h = data.get('password')

    if not email or not password_h:
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400


    existing_manager = Manager.query.filter_by(email=email).first()
    if existing_manager:
        return jsonify({'success': False, 'error': 'manager with this email already exists'}), 400

    new_manager = Manager(email = email , password = password_h)
    db.session.add(new_manager)
    db.session.commit()

    # Generate JWT Token
    access_token = create_access_token(identity=email)

    return jsonify({"success": True, "message": "Manager created successfully!", "access_token": access_token}), 201



@manager_bp.route('/login' , methods=['POST'])
def login():
    data = request.json

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    manager = Manager.query.filter_by(email=email).first()

    if manager is None or not manager.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401

    access_token = create_access_token(identity=email)
    return jsonify({'success': True, 'access_token': access_token}), 200


@manager_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({'message': 'Successfully logged out, but the token is invalidated on client side.'}), 200


@manager_bp.route('/create-event', methods=['POST'])
@jwt_required()
def create_event():
    data = request.json
    event_name = data.get('event_name')
    description = data.get('description')
    date_str = data.get('date') # YYYY-MM-DD
    organised_by = data.get('organised_by')

    if not event_name or not description or not date_str:
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    new_event = Events(event_name=event_name, description=description, date=date, organised_by=organised_by)
    db.session.add(new_event)
    db.session.commit()

    return jsonify({"success": True, "message": "Event created successfully!"}), 201


@manager_bp.route('/events', methods=['GET'])
@jwt_required()
def get_events():
    events = Events.query.all()
    events_list = []
    for event in events:
        events_list.append({
            'event_name': event.event_name,
            'description': event.description,
            'date': event.date.strftime('%Y-%m-%d'),
            'organised_by': event.organised_by
        })
    return jsonify(events_list), 200


@manager_bp.route('/event-details', methods=['GET', 'POST'])
@jwt_required()
def get_event_details():
    if request.method == 'GET':
        event_name = request.args.get('event_name')
    else:  # POST
        data = request.json
        event_name = data.get('event_name')

    print(f"Received event_name: {event_name}")  # Debug statement

    if not event_name:
        return jsonify({'success': False, 'error': 'Event name is required'}), 400

    event = Events.query.filter_by(event_name=event_name).first()

    if not event:
        return jsonify({'success': False, 'error': 'Event not found'}), 404

    return jsonify({
        'success': True,
        'event': {
            'event_name': event.event_name,
            'description': event.description,
            'date': event.date,
            'organised_by': event.organised_by
        }
    }), 200




