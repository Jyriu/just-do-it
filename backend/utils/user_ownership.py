from flask import jsonify

def check_user_ownership(item, user_id):
    """Vérifie que l'utilisateur est bien propriétaire de l'objet (post ou réponse)."""
    if item.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    return None
