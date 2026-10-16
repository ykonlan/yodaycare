from django.core.exceptions import ValidationError

def validator_for_name(name):
    if(any(char.isdigit() for char in name)):
        raise ValidationError("Name cannot contain digits")