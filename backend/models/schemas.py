from marshmallow import Schema, fields, validate, validates, ValidationError
import re

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(
        required=True, 
        validate=validate.Length(min=3, max=80)
    )
    email = fields.Email(required=True)
    password = fields.Str(
        required=True, 
        load_only=True,
        validate=validate.Length(min=8)
    )
    
    @validates('password')
    def validate_password(self, value):
        if not re.search(r'[A-Z]', value):
            raise ValidationError('Le mot de passe doit contenir au moins une majuscule')
        if not re.search(r'[a-z]', value):
            raise ValidationError('Le mot de passe doit contenir au moins une minuscule')
        if not re.search(r'\d', value):
            raise ValidationError('Le mot de passe doit contenir au moins un chiffre')

class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)