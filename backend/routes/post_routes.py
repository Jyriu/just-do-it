from flask import Blueprint, request, jsonify
from extensions import db, bcrypt
from models import User, Post
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

post_bp = Blueprint('post_bp', __name__)

@post_bp.route('/create_post', methods=['POST'])
@jwt_required()
def create_post():
    # get data send by user
    data = request.get_json()

    # get user from token
    user_id = get_jwt_identity()

    # add post to db
    post = Post(title=data['title'], content=data['content'], user_id=user_id)
    db.session.add(post)
    db.session.commit()

    return jsonify({'message': 'Post successfully created'}), 201