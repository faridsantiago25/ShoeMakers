from marshmallow import ValidationError

def validate_str(val):
    if not isinstance(val, str):
        raise ValidationError('Value must be a string.')
    if len(val) < 1:
        raise ValidationError('Value must not be empty.')

def validate_int(val):
    if not isinstance(val, int):
        raise ValidationError('Value must be an integer.')
    if val < 1:
        raise ValidationError('Value must be greater than 0.')
    
def validate_float(val):
    if not isinstance(val, float):
        raise ValidationError('Value must be a float.')
    if val < 1:
        raise ValidationError('Value must be greater than 0.')
