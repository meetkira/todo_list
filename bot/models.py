from django.db import models

from core.models import User


# Create your models here.
class TgUser(models.Model):
    class Meta:
        verbose_name = "Пользователь бота"
        verbose_name_plural = "Пользователи бота"

    telegram_chat_id = models.IntegerField(verbose_name="ID телеграмма чата")
    telegram_user_id = models.IntegerField(verbose_name="ID телеграмма пользователя")
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.PROTECT, null=True, blank=True)
