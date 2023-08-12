from django.core.exceptions import ValidationError


def validate_me(value):
    if value.lower() == 'me':
        raise ValidationError('me - не допустимое имя')
