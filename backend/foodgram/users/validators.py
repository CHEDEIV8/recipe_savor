from django.core.exceptions import ValidationError


def validate_me(value):
    if value == 'me':
        raise ValidationError('Имя не должно быть me')
