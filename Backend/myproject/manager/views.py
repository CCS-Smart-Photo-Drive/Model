from flask import Flask, redirect, url_for, Blueprint, request, jsonify
from myproject import db 
from myproject.manager.models import Manager
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
