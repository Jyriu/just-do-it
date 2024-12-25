from extensions import bcrypt
import re

def validate_password(password: str) -> tuple[bool, str]:
    """
    Valide un mot de passe selon les critères suivants :
    - Au moins 8 caractères
    - Au moins une lettre majuscule
    - Au moins une lettre minuscule
    - Au moins un chiffre
    """
    if len(password) < 8:
        return False, "Le mot de passe doit contenir au moins 8 caractères"
    
    if not re.search(r"[A-Z]", password):
        return False, "Le mot de passe doit contenir au moins une majuscule"
    
    if not re.search(r"[a-z]", password):
        return False, "Le mot de passe doit contenir au moins une minuscule"
    
    if not re.search(r"\d", password):
        return False, "Le mot de passe doit contenir au moins un chiffre"
    
    return True, "Mot de passe valide"

def hash_password(password: str) -> str:
    """Hash un mot de passe avec bcrypt."""
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(hashed_password: str, password: str) -> bool:
    """Vérifie si le mot de passe correspond au hash."""
    return bcrypt.check_password_hash(hashed_password, password)