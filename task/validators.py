from django.utils import timezone
from django.core.exceptions import ValidationError


def datetime_checker(value):
    if value < timezone.now():
        raise ValidationError("Kichik vaqt bilan todo obyekt yarata olmaysiz.")
    return value
