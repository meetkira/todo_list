from typing import Any, List, Tuple

from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


def get_choices(constants_class: Any) -> List[Tuple[str, str]]:
    return [
        (value, value)
        for key, value in vars(constants_class).items()
        if not key.startswith('__')
    ]


class UserStatus:
    USER = "user"
    ADMIN = "admin"


# Create your models here.
class User(AbstractUser):
    phone = PhoneNumberField(null=True, blank=True, unique=True)
    user_status = models.CharField(max_length=5, default=UserStatus.USER, choices=get_choices(UserStatus))
