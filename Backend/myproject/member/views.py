from flask import Flask, redirect, url_for, Blueprint, request, jsonify
from myproject import db 
from myproject.member.models import Member
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

member_bp = Blueprint('member_bp' ,__name__)


@member_bp.route('/sign-up/', methods=['POST'])
def sign_up():
    data = request.json
    email = data.get('email')
    password_h = data.get('password')

    if not email or not password_h:
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400


    existing_member = Member.query.filter_by(email=email).first()
    if existing_member:
        return jsonify({'success': False, 'error': 'Member with this email already exists'}), 400

    new_member = Member(email = email , password = password_h)
    db.session.add(new_member)
    db.session.commit()

    # Generate JWT Token
    access_token = create_access_token(identity=email)

    return jsonify({"success": True, "message": "Member created successfully!", "access_token": access_token}), 201



@member_bp.route('/login' , methods=['POST'])
def login():
    data = request.json

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    member = Member.query.filter_by(email=email).first()

    if member is None or not member.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401

    access_token = create_access_token(identity=email)
    return jsonify({'success': True, 'access_token': access_token}), 200


@member_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({'message': 'Successfully logged out, but the token is invalidated on client side.'}), 200
