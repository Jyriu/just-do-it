from flask import jsonify

def error_response(message: str, status_code: int):
    """
    Renvoie une réponse d'erreur formatée.
    
    Args:
        message (str): Le message d'erreur
        status_code (int): Le code de statut HTTP
    
    Returns:
        Response: La réponse JSON avec le message d'erreur
    """
    # S'assurer que le message est une chaîne
    message = str(message)
    return jsonify({
        'error': message,
        'status': 'error'
    }), status_code
