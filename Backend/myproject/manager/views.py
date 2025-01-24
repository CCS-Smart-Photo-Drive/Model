from flask import Flask, redirect, url_for, Blueprint, request, jsonify
from myproject import db 
from myproject.manager.models import Manager, Events
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

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
    title = data.get('title')
    description = data.get('description')
    date = data.get('date')

    if not title or not description or not date:
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400

    new_event = Events(title=title, description=description, date=date)
    db.session.add(new_event)
    db.session.commit()

    return jsonify({"success": True, "message": "Event created successfully!"}), 201


@manager_bp.route('/events', methods=['GET'])
@jwt_required()
def get_events():
    events = Events.query.all()
    return jsonify([event.__dict__ for event in events]), 200


@manager_bp.route('/event-details', methods=['GET'])
@jwt_required()
def get_event_details():
    title = request.args.get('title')

    if not title:
        return jsonify({'success': False, 'error': 'Title is required'}), 400

    event = Events.query.filter_by(title=title).first()

    if not event:
        return jsonify({'success': False, 'error': 'Event not found'}), 404

    return jsonify({
        'success': True,
        'event': {
            'title': event.title,
            'description': event.description,
            'date': event.date,
            'organised_by': event.organised_by
        }
    }), 200




